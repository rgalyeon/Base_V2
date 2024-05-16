import random

from loguru import logger

from config import ETHERSCAN_API_KEYS, PROGRESS_PATH
import requests
from typing import List, Dict
import pandas as pd
from tqdm import tqdm
import time
import os


class Scan:
    def __init__(self, wallets_data):
        self.wallets_data = wallets_data
        self.etherscan_url = 'https://api.etherscan.io/api'

    def url_maker(self, module, action, scan_url, **kwargs) -> str:

        api_keys = ETHERSCAN_API_KEYS

        url = scan_url + f'?module={module}' \
                         f'&action={action}' \
                         f'&apikey={random.choice(api_keys)}'
        if kwargs:
            for key, value in kwargs.items():
                url += f'&{key}={value}'
        return url

    def get_wallet_transactions(self, address, scan_url, proxies=None):
        url = self.url_maker('account', 'txlist', scan_url, address=address)
        if proxies:
            try:
                resp = requests.get(url, proxies=proxies, timeout=10)
            except:
                resp = requests.get(url)
        else:
            resp = requests.get(url)
        res = resp.json()
        return res

    def parse_transactions(self, transactions: List[Dict], wallet, df: pd.DataFrame, scan_url):
        df.loc[wallet, :] = False

        bridge_volume = 0
        if scan_url == self.etherscan_url:
            for tx in transactions:
                if tx['to'] == '0x49048044d57e1c92a77f79988d21fa8faf74e97e' and tx['methodId'] == '0xe9e05c42':
                    bridge_volume += int(tx['value'])
        df.loc[wallet, 'native_bridge_deposit'] = bridge_volume / 10 ** 18

    def wait_transactions(self, address, all_proxies, scan_url):
        n_attemps = 10
        while n_attemps:
            proxy = random.choice(all_proxies)
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            transactions = self.get_wallet_transactions(address.lower(), scan_url, proxies)
            if transactions['status'] == 1:
                return transactions
            n_attemps -= 1
            time.sleep(5)

    def get_wallet_progress(self, replace=False, check_eth=True):
        if os.path.exists(PROGRESS_PATH) and not replace:
            logger.info(f'Load progress from {PROGRESS_PATH}')
            return
        logger.info('Check progress from blockchain data')

        cols = ['native_bridge_deposit']

        scanners = [self.etherscan_url]
        if check_eth:
            pass
            # scanners.append(self.etherscan_url)

        df = pd.DataFrame(columns=cols)
        all_proxies = [wallet_info['proxy'] for wallet_info in self.wallets_data]
        for wallet_info in tqdm(self.wallets_data):
            address = wallet_info['address'].lower()
            for scan_url in scanners:
                transactions = self.get_transaction_list(wallet_info, all_proxies, scan_url)
                try:
                    if transactions['status'] == '1':
                        self.parse_transactions(transactions['result'][:100], wallet_info['address'], df, scan_url)
                    else:
                        print(transactions)
                except Exception as e:
                    logger.warning(f'Can not parse {address} wallet. Error: {e}')
        df.fillna(False).to_excel(PROGRESS_PATH)

    def get_transaction_list(self, wallet_info, all_proxies, scan_url):
        address = wallet_info['address'].lower()
        proxies = {'http': f'http://{wallet_info["proxy"]}', 'https': f'http://{wallet_info["proxy"]}'}
        try:
            transactions = self.get_wallet_transactions(address, scan_url, proxies)
            if transactions['status'] != '1':
                transactions = self.wait_transactions(address, all_proxies, scan_url)
        except:
            transactions = self.wait_transactions(address, all_proxies, scan_url)

        return transactions
