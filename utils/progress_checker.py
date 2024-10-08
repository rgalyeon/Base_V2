import json
import random
import warnings
from loguru import logger

from config import BASESCAN_URL, BASE_API_KEYS, PROGRESS_PATH, ONCHAIN_SUMMER_SCORE_PATH
import requests
from typing import List, Dict
import pandas as pd
from tqdm import tqdm
import time
import os

warnings.filterwarnings('ignore')


class Scan:
    def __init__(self, wallets_data):
        self.wallets_data = wallets_data

    def url_maker(self, module, action, scan_url, **kwargs) -> str:

        api_keys = BASE_API_KEYS

        url = scan_url + f'?module={module}' \
                         f'&action={action}' \
                         f'&apikey={random.choice(api_keys)}'
        if kwargs:
            for key, value in kwargs.items():
                url += f'&{key}={value}'
        return url

    def get_wallet_transactions(self, address, scan_url, proxies=None):
        url = self.url_maker('account', 'txlist', scan_url, address=address)
        n_tries = 5
        while n_tries:
            try:
                if proxies:
                    try:
                        resp = requests.get(url, proxies=proxies, timeout=10)
                    except:
                        resp = requests.get(url)
                else:
                    resp = requests.get(url)
                res = resp.json()
                break
            except json.JSONDecodeError:
                n_tries -= 1
                time.sleep(1)
        return res

    def parse_transactions(self, transactions: List[Dict], wallet, df: pd.DataFrame):
        df.loc[wallet, :] = False

        for tx in transactions:
            if tx['to'] == '0xb5408b7126142C61f509046868B1273F96191b6d'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Celebrating the Ethereum ETF'] = True
            elif tx['to'] == '0xE8aD8b2c5Ec79d4735026f95Ba7C10DCB0D3732B'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'ETFEREUM'] = True
            elif tx['to'] == '0x96E82d88c07eCa6a29B2AD86623397B689380652'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'ETH BREAKING THROUGH'] = True
            elif tx['to'] == '0xC00F7096357f09d9f5FE335CFD15065326229F66'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Ethereum ETF'] = True
            elif tx['to'] == '0xb0FF351AD7b538452306d74fB7767EC019Fa10CF'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "ETH can't be stopped"] = True
            elif tx['to'] == '0xE65dFa5C8B531544b5Ae4960AE0345456D87A47D'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Happy Birthday Toshi'] = True
            elif tx['to'] == '0x615194d9695d0c02Fc30a897F8dA92E17403D61B'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'EURC & Base Launch'] = True
            elif tx['to'] == '0x6B033e8199ce2E924813568B716378aA440F4C67'.lower():
                df.loc[wallet, 'Introducing: Coinbase Wallet web app'] = True
            # elif tx['to'] == '0xcF74F48B71f2A8160aDa67D1720ce0F2778b5a28'.lower() and tx['methodId'] == '0x574fed17':
            #     df.loc[wallet, 'Nouns Forever (Song A Day #5700)'] = True
            elif tx['to'] == '0x955FdFdFd783C89Beb54c85f0a97F0904D85B86C'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'the world after ETH ETF approval'] = True
            elif tx['to'] == '0x63197bb4dE33DA81FdB311Ef6395237fB0F65C7D'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Nouns everywhere ⌐◨-◨'] = True
            # elif tx['to'] == '0xae954896B4d3B113C9FCe85f64387229291fb5a9'.lower() and tx['methodId'] == '0x574fed17':
            #     df.loc[wallet, 'Happy 3rd Nouniversary'] = True
            # elif tx['to'] == '0xE0fE6DD851187c62a79D00a211953Fe3B5Cec7FE'.lower() and tx['methodId'] == '0x574fed17':
            #     df.loc[wallet, 'Happy Nouniversary'] = True
            # elif tx['to'] == '0x7B28d9Efa325225666Aa6ddaC20c46420cd75871'.lower() and tx['methodId'] == '0x574fed17':
            #     df.loc[wallet, 'Celebrating the end of Nouns: Season 3'] = True
            elif tx['to'] == '0x5680eAD37A60604a12F821Bb9Da42858cbC346Fd'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Celebrating Nouns'] = True
            elif tx['to'] == '0xCcbb9DC3FeCAf7a9cAe716eF1C16C8ca2f19a3D1'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Nounish Vibe'] = True
            elif tx['to'] == '0x250d4678a1175113eC96e7DeB90584267026D443'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Hand of Nouns'] = True
            elif tx['to'] == '0x6414A4359848d2BF12B93483cd8A6ef6B03779ae'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Happy Nouniversary from based Nouns!'] = True
            # elif tx['to'] == '0x25F98e990B6C0dBa5A109B92542F16DCbbD017C8'.lower() and tx['methodId'] == '0x574fed17':
            #     df.loc[wallet, 'Base God and Miggs wif Nouns'] = True
            # elif tx['to'] == '0x306671092213C4d0da1a7bB5c31D5B4F9aB62246'.lower() and tx['methodId'] == '0x574fed17':
            #     df.loc[wallet, 'nounify the rockies'] = True
            elif tx['to'] == '0xf16755b43eE1a458161f0faE5a9124729f4f6B1B'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Coffee Days 2024'] = True
            elif tx['to'] == '0x1aeD60A97192157fDA7fb26267A439d523d09c5e'.lower() and 'Dc03a75F96f38615B3eB55F0F289d36E7A706660'.lower() in tx['input']:
                df.loc[wallet, 'Mister Miggles'] = True
            elif tx['to'] == '0x1aeD60A97192157fDA7fb26267A439d523d09c5e'.lower() and '1b9ac8580d2e81d7322f163362831448e7fcad1b'.lower() in tx['input']:
                df.loc[wallet, 'Team Liquid Onchain Summer Premiere Series'] = True
            elif tx['to'] == '0x1aeD60A97192157fDA7fb26267A439d523d09c5e'.lower() and '31B81650997e26Eb527CA6541B1433d1EF348d93'.lower() in tx['input']:
                df.loc[wallet, 'Dawn of Daylight'] = True
            elif tx['to'] == '0xa7891c87933BB99Db006b60D8Cb7cf68141B492f'.lower() and tx['methodId'] == '0x84bb1e42':
                df.loc[wallet, 'STIX Launch Tournament Pass'] = True
            elif tx['to'] == '0x9FF8Fd82c0ce09caE76e777f47d536579AF2Fe7C'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'strut 001'] = True
            elif tx['to'] == '0xC8f93Ce7A12960466a2e13E70dE5CA41B652e4E6'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Nouniversary (Blue)'] = True
            elif tx['to'] == '0x7B791EdF061Df65bAC7a9d47668F61F1a9A998C0'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Base Canada'] = True
            elif tx['to'] == '0x44d461Da8A451f05b6b75EdD5C4a2d2f3C14aaB4'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Toshi Onchain Summer'] = True
            elif tx['to'] == '0x3b4B32a5c9A01763A0945A8a4a4269052DC3DE2F'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Butterfly'] = True
            elif tx['to'] == '0x752d593b3B8aD1c5d827F5B9AA9b653eE7134ea0'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'THINK BIG'] = True
            elif tx['to'] == '0xd60f13cC3e4d5bC96e7bAE8AAb5F448f3eFF3F0C'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Toshi Chess'] = True
            elif tx['to'] == '0xbFa3fF9dcdB811037Bbec89f89E2751114ECD299'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Toshi Vibe'] = True
            elif tx['to'] == '0x5307c5ee9AeE0B944fA2E0Dba5D35D1D454E4bcE'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "Whatchu Lookin' At?"] = True
            elif tx['to'] == '0x2382456097cC12ce54052084e9357612497FD6be'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "Stand with Crypto folk rock"] = True
            elif tx['to'] == '0x4e4431BDdC2a896b1268ded02807b78c318C82e0'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "Endaoment X SWC Shield"] = True
            elif tx['to'] == '0x146B627a763DFaE78f6A409CEF5B8ad84dDD4150'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "Stand with Crypto"] = True
            elif tx['to'] == '0xea50e58B518435AD2CeCE84d1e099b2e0878B9cF'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "Yellow Collective Shield Trait"] = True
            elif tx['to'] == '0x651b0A2b9FB9C186fB6C9a9CEddf25B791Ad5753'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "Crypto will bloom"] = True
            elif tx['to'] == '0x4beAdC00E2A6b6C4fAc1a43FF340E5D71CBB9F77'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "Stand with Crypto Pizza"] = True
            elif tx['to'] == '0x5b45498D20d24D9c6Da165eDcd0eBcE0636176Ae'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "Duality in motion"] = True
            elif tx['to'] == '0x6a43B7e3ebFc915A8021dd05f07896bc092d1415'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "Crypto Vibe"] = True
            elif tx['to'] == '0x6a43B7e3ebFc915A8021dd05f07896bc092d1415'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "Toshi x SWC 3"] = True
            elif tx['to'] == '0x892Bc2468f20D40F4424eE6A504e354D9D7E1866'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "The Creative Shield"] = True
            elif tx['to'] == '0x1f006edBc0Bcc528A743ee7A53b5e3dD393A1Df6'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "En grade"] = True
            elif tx['to'] == '0x8605522B075aFeD48f9987E573E0AA8E572B8452'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Mint the vision'] = True
            elif tx['to'] == '0x13fCcd944B1D88d0670cae18A00abD272256DDeE'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Stand With Crypto Shield Rune'] = True
            elif tx['to'] == '0x6A3dA97Dc82c098038940Db5CB2Aa6B1541f2ebe'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Shielding the wonder'] = True
            elif tx['to'] == '0xd1E1da0b62761b0df8135aE4e925052C8f618458'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Earth Stands with Crypto'] = True
            elif tx['to'] == '0x03c6eF731453bfEc65a800F83f026ad011D8Abec'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, '⌐◨-◨ Stand With Crypto'] = True
            elif tx['to'] == '0xEb9A3540E6A3dc31d982A47925d5831E02a3Fe1e'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'We stand, we build'] = True
            elif tx['to'] == '0x279dFFD2b14a4A60e266bEfb0D2c10E695D58113'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Live and Let Live!'] = True

            elif tx['to'] == '0x6ba5Ba71810c1196f20123B57B66C9ed2A5dBd76'.lower():
                df.loc[wallet, 'Juicy Pack'] = True
            elif tx['to'] == '0x0821D16eCb68FA7C623f0cD7c83C8D5Bd80bd822'.lower():
                df.loc[wallet, 'Forbes WEB3 Inspire'] = True
            elif tx['to'] == '0x2a8e46E78BA9667c661326820801695dcf1c403E'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'Let The Shield Shine'] = True
            elif tx['to'] == '0x8e50c64310b55729F8EE67c471E052B1Cd7AF5b3'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, 'All for One'] = True
            elif tx['to'] == '0x95ff853A4C66a5068f1ED8Aaf7c6F4e3bDBEBAE1'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "Let's Stand"] = True
            elif tx['to'] == '0xD3d124B6A9497B3695918cEEB0e9c4D9ED6972fB'.lower() and tx['methodId'] == '0x574fed17':
                df.loc[wallet, "The Eternal Skywheel"] = True

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

    def get_wallet_progress(self, replace=False):
        if os.path.exists(PROGRESS_PATH) and not replace:
            logger.info(f'Load progress from {PROGRESS_PATH}')
            return
        logger.info('Check progress from blockchain data')

        cols = ['Celebrating the Ethereum ETF', 'ETFEREUM', 'ETH BREAKING THROUGH',
                'Ethereum ETF', "ETH can't be stopped", 'Happy Birthday Toshi', 'EURC & Base Launch',
                'Introducing: Coinbase Wallet web app', 'Mister Miggles', 'Team Liquid Onchain Summer Premiere Series',
                'the world after ETH ETF approval', 'Nouns everywhere ⌐◨-◨',
                'Celebrating Nouns', 'Nounish Vibe', 'Hand of Nouns', 'Happy Nouniversary from based Nouns!',
                'Coffee Days 2024', 'Dawn of Daylight', 'STIX Launch Tournament Pass',
                'strut 001', 'Nouniversary (Blue)', 'Toshi Onchain Summer', 'Base Canada', 'Butterfly', 'THINK BIG',
                'Toshi Chess', 'Toshi Vibe', "Whatchu Lookin' At?",
                'Stand with Crypto folk rock', 'Endaoment X SWC Shield', 'Stand with Crypto',
                'Yellow Collective Shield Trait', 'Crypto will bloom', 'Stand with Crypto Pizza', 'Duality in motion',
                'Crypto Vibe', 'Toshi x SWC 3', 'The Creative Shield', 'En grade', 'Mint the vision',
                'Stand With Crypto Shield Rune', 'Shielding the wonder', '⌐◨-◨ Stand With Crypto',
                'Earth Stands with Crypto', 'We stand, we build', 'Live and Let Live!',
                'Juicy Pack', 'Forbes WEB3 Inspire', 'Let The Shield Shine', 'All for One', "Let's Stand",
                'The Eternal Skywheel']

        df = pd.DataFrame(columns=cols)
        all_proxies = [wallet_info['proxy'] for wallet_info in self.wallets_data]
        for wallet_info in tqdm(self.wallets_data):
            address = wallet_info['address'].lower()
            transactions = self.get_transaction_list(wallet_info, all_proxies, BASESCAN_URL)
            try:
                if transactions['status'] == '1':
                    self.parse_transactions(transactions['result'][-100:], wallet_info['address'], df)
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

    def get_onchain_summer_stats(self):
        logger.info('Start checking Onchain Summer Stats')

        df = pd.DataFrame()

        for wallet_info in tqdm(self.wallets_data):
            address = wallet_info['address'].lower()
            url = f'https://basehunt.xyz/api/profile/state?userAddress={address}&gameId=2'
            try:
                proxies = {'http': f'http://{wallet_info["proxy"]}', 'https': f'http://{wallet_info["proxy"]}'}
                resp = requests.get(url, proxies=proxies, timeout=10)
            except:
                resp = requests.get(url)

            results = resp.json()
            if results['isOptedIn'] is True:
                df.loc[address, 'n_quests'] = results['numChallengesCompleted']
                df.loc[address, 'n_refs'] = results['referralData']['numReferrals']
                df.loc[address, 'level'] = results['levelData']['currentLevel']['level']
                df.loc[address, 'score'] = results['scoreData']['currentScore']
                for badge in results['badges']:
                    df.loc[address, f'{badge["name"]} badge'] = True

        df.fillna(False, inplace=True)

        df.to_excel(ONCHAIN_SUMMER_SCORE_PATH)
