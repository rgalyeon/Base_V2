import random

import aiohttp
from loguru import logger
from config import ONCHAIN_SUMMER_ABI, ONCHAIN_SUMMER_CONTRACT
from utils.gas_checker import check_gas
from utils.helpers import retry, sleep
from .account import Account
from fake_useragent import UserAgent


class OnchainSummer(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="base")

        ua = UserAgent().getRandom

        self.headers = {
            'referer': 'https://wallet.coinbase.com/',
            'accept': '*/*',
            'accept-language': 'en-GB,en;q=0.6',
            'content-type': 'application/json',
            'origin': 'https://wallet.coinbase.com',
            'priority': 'u=1, i',
            'sec-ch-ua': "",
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            "Sec-Ch-Ua-Platform": ua["os"],
            "User-Agent": ua['useragent']
        }

        self.os_nfts2 = [
            ('Celebrating the Ethereum ETF', '0xb5408b7126142C61f509046868B1273F96191b6d', '5e383RWcRtGAwGUorkGiYC'),
            # ('Mr. Miggles | Song A Day', '0x1f52841279fA4dE8B606a70373E9c84e84Ce9204'),
            ('ETFEREUM', '0xE8aD8b2c5Ec79d4735026f95Ba7C10DCB0D3732B', 'ocsChallenge_eba9e6f0-b7b6-4d18-8b99-a64aea045117'),
            ('ETH BREAKING THROUGH', '0x96E82d88c07eCa6a29B2AD86623397B689380652', '78AUXYw8UCyFUPE2zy9yMZ'),
            # ('Mr. Miggles, Gary, And The ETH ETF', '0xC2a3BdB4cb165Ad52096550654552974E6748Be5'),
            # ('the world after ETH ETF approval', '0x955FdFdFd783C89Beb54c85f0a97F0904D85B86C'),
            ('Ethereum ETF', '0xC00F7096357f09d9f5FE335CFD15065326229F66', 'ocsChallenge_ee0cf23e-74a1-4bb3-badf-037a6bbf35e8'),
            ("ETH can't be stopped", '0xb0FF351AD7b538452306d74fB7767EC019Fa10CF', 'ocsChallenge_c1de2373-35ad-4f3c-ab18-4dfadf15754d'),
            # ('Onchain Summer Chibling', '0x13F294BF5e26843C33d0ae739eDb8d6B178740B0'),
            ('Happy Birthday Toshi', '0xE65dFa5C8B531544b5Ae4960AE0345456D87A47D', '1pjoNf5onjgsi7r9fWp3ob'),
            ('EURC & Base Launch', '0x615194d9695d0c02Fc30a897F8dA92E17403D61B', '1iZiHPbqaIGW5F08bCit6J'),
        ]

        self.badges = [
            ('StandWithCryptoBadge', '1'),
            ('CoinbaseOneBadge', '2'),
            ('BuildathonBadge', '3'),
            ('CollectorBadge', '4'),
            ('TraderBadge', '5'),
            ('SaverBadge', '6'),
            ('TX10Badge', '7'),
            ('TX50Badge', '8'),
            ('TX100Badge', '9'),
            ('TX1000Badge', '10')
        ]

    @retry
    @check_gas
    async def mint_onchain_summer_is_back(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint Onchain Summer Is Back nft")

        contract = self.get_contract(ONCHAIN_SUMMER_CONTRACT, ONCHAIN_SUMMER_ABI)

        currency = self.w3.to_checksum_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE')
        price_per_token = 200000000000000
        allowlist_proof = {'quantityLimitPerWallet': 2 ** 256 - 1,
                           'pricePerToken': price_per_token,
                           'currency': currency,
                           'proof': []}
        quantity = 1
        n_nfts = await contract.functions.balanceOf(self.address).call()
        if n_nfts < 1:
            tx_data = await self.get_tx_data(value=price_per_token)

            transaction = await contract.functions.claim(
                self.address,
                quantity,
                currency,
                price_per_token,
                allowlist_proof,
                "0x"
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already minted. Skip module")

    @retry
    @check_gas
    async def mint_nft(self, nft_name, nft_contract):

        logger.info(f"[{self.account_id}][{self.address}] Mint {nft_name} nft")

        mint_price = 0.0001
        contract = self.get_contract(nft_contract, ONCHAIN_SUMMER_ABI)
        n_nfts = await contract.functions.balanceOf(self.address).call()
        if n_nfts < 1:
            tx_data = await self.get_tx_data(value=self.w3.to_wei(mint_price, 'ether'))

            transaction = await contract.functions.mintWithComment(
                self.address,
                1,
                ""
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already minted")

    @retry
    async def claim_task(self, nft_name, challendge_id):

        url = 'https://basehunt.xyz/api/challenges/complete'

        params = {
            'gameId': 2,
            'userAddress': f"{self.address}",
            'challengeId': challendge_id
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, proxy=self.proxy, json=params) as response:
                response_data = await response.json()
                if response.status in (200, 201):
                    message = response_data['message']
                    if message in ('challenge-completed', 'challenge-claimed'):
                        logger.success(f"[{self.account_id}][{self.address}] Successfully claimed points {nft_name}")
                    else:
                        logger.error(f"[{self.account_id}][{self.address}] Error on claim {nft_name}")
                else:
                    logger.error(f"[{self.account_id}][{self.address}] Error on claim {nft_name}")

    @retry
    async def claim_badge(self, badge_id, badge_name):
        logger.info(f"[{self.account_id}][{self.address}] Start claim {badge_name} badge")

        data = {
            'gameId': 2,
            'userAddress': self.address,
            'badgeId': badge_id,
        }

        url = 'https://basehunt.xyz/api/badges/claim'

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, proxy=self.proxy, json=data) as response:
                response_data = await response.json()
                if response.status in (200, 201):
                    message = response_data['message']
                    if message == 'challenge-completed':
                        logger.success(f"[{self.account_id}][{self.address}] Successfully claimed {badge_name} badge")
                    else:
                        logger.error(f"[{self.account_id}][{self.address}] Error on claim {badge_name}")
                else:
                    logger.error(f"[{self.account_id}][{self.address}] Error on claim {badge_name}")

    async def claim_all_badges(self, sleep_from, sleep_to, random_badge):

        badges = self.badges.copy()

        if random_badge:
            random.shuffle(badges)

        for badge_name, badge_id in badges:
            await self.claim_badge(badge_id, badge_name)
            await sleep(sleep_from, sleep_to, 'Sleep before next badge claim')

    async def mint_all_nft(self, sleep_from, sleep_to, random_mint, nfts_for_mint):

        nfts = self.os_nfts2.copy()

        nfts = [nft for nft in nfts if nft[0] in set(nfts_for_mint)]

        if random_mint:
            random.shuffle(nfts)

        for nft_name, nft_contract, challenge_id in nfts:
            await self.mint_nft(nft_name, nft_contract)
            await self.claim_task(nft_name, challenge_id)
            await sleep(sleep_from, sleep_to, 'Sleep before next badge claim')
