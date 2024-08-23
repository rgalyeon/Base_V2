import json
import random

import aiohttp
import web3
from loguru import logger
from config import ONCHAIN_SUMMER_ABI, ONCHAIN_SUMMER_CONTRACT, INTRODUCING_ABI, COINEARNINGS_ABI, ZERO_ADDRESS
from utils.gas_checker import check_gas
from utils.helpers import retry, sleep
from .account import Account
from fake_useragent import UserAgent
from enum import Enum


class MintType(Enum):
    COMMENT = 1
    RESERVOIR = 2
    ADVENTURE = 3
    INTRODUCING = 4
    STIX = 5


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
            ('Celebrating the Ethereum ETF', '0xb5408b7126142C61f509046868B1273F96191b6d', '5e383RWcRtGAwGUorkGiYC', MintType.COMMENT),
            # ('Mr. Miggles | Song A Day', '0x1f52841279fA4dE8B606a70373E9c84e84Ce9204', MintType.COMMENT),
            ('ETFEREUM', '0xE8aD8b2c5Ec79d4735026f95Ba7C10DCB0D3732B', 'ocsChallenge_eba9e6f0-b7b6-4d18-8b99-a64aea045117', MintType.COMMENT),
            ('ETH BREAKING THROUGH', '0x96E82d88c07eCa6a29B2AD86623397B689380652', '78AUXYw8UCyFUPE2zy9yMZ', MintType.COMMENT),
            # ('Mr. Miggles, Gary, And The ETH ETF', '0xC2a3BdB4cb165Ad52096550654552974E6748Be5', MintType.COMMENT),
            # ('the world after ETH ETF approval', '0x955FdFdFd783C89Beb54c85f0a97F0904D85B86C', MintType.COMMENT),
            ('Ethereum ETF', '0xC00F7096357f09d9f5FE335CFD15065326229F66', 'ocsChallenge_ee0cf23e-74a1-4bb3-badf-037a6bbf35e8', MintType.COMMENT),
            ("ETH can't be stopped", '0xb0FF351AD7b538452306d74fB7767EC019Fa10CF', 'ocsChallenge_c1de2373-35ad-4f3c-ab18-4dfadf15754d', MintType.COMMENT),
            # ('Onchain Summer Chibling', '0x13F294BF5e26843C33d0ae739eDb8d6B178740B0', MintType.COMMENT),
            ('Happy Birthday Toshi', '0xE65dFa5C8B531544b5Ae4960AE0345456D87A47D', '1pjoNf5onjgsi7r9fWp3ob', MintType.COMMENT),
            ('EURC & Base Launch', '0x615194d9695d0c02Fc30a897F8dA92E17403D61B', '1iZiHPbqaIGW5F08bCit6J', MintType.COMMENT),
            ('Introducing: Coinbase Wallet web app', '0x6B033e8199ce2E924813568B716378aA440F4C67', '78zcHkWSABcPWMoacVI9Vs', MintType.INTRODUCING),
            ('Mister Miggles', '0xDc03a75F96f38615B3eB55F0F289d36E7A706660', 'ocsChallenge_d0778cee-ad0b-46b9-93d9-887b917b2a1f', MintType.RESERVOIR),
            ('Team Liquid Onchain Summer Premiere Series', '0x1b9ac8580d2e81d7322f163362831448e7fcad1b', '6VRBNN6qr2algysZeorek8', MintType.RESERVOIR),
            ('Dawn of Daylight', '0x31B81650997e26Eb527CA6541B1433d1EF348d93', 'ocsChallenge_18c8180f-2818-41b7-bc10-6dbd53d86260', MintType.RESERVOIR),
            ('Nouns Forever (Song A Day #5700)', '0xcF74F48B71f2A8160aDa67D1720ce0F2778b5a28', '3M9bT5pBKJE6jgolwMFsJU', MintType.COMMENT),
            ('the world after ETH ETF approval', '0x955FdFdFd783C89Beb54c85f0a97F0904D85B86C', 'ocsChallenge_65c17605-e085-4528-b4f1-76ce5f48da56', MintType.COMMENT),
            ('Adventure Begins', '0xbb613f51CF6414a8470Ba8Ec51097812d8761f4C', 'ocsChallenge_b6599260-7e14-4f69-9d64-5198edd05ab4', MintType.ADVENTURE),
            ('Nouns everywhere ⌐◨-◨', '0x63197bb4dE33DA81FdB311Ef6395237fB0F65C7D', 'ocsChallenge_d122a59b-6a04-4949-9cdb-b9262e843aa6', MintType.COMMENT),
            ('Happy 3rd Nouniversary', '0xae954896B4d3B113C9FCe85f64387229291fb5a9', '7ktuPuO5kUtvQmvzd4T5r3', MintType.COMMENT),
            ('Happy Nouniversary', '0xE0fE6DD851187c62a79D00a211953Fe3B5Cec7FE', '44wp1P8LSnwkPSz7Ft3q78', MintType.COMMENT),
            ('Celebrating the end of Nouns: Season 3', '0x7B28d9Efa325225666Aa6ddaC20c46420cd75871', 'ocsChallenge_15259510-7040-4f16-bdfa-f137846b546c', MintType.COMMENT),
            ('Celebrating Nouns', '0x5680eAD37A60604a12F821Bb9Da42858cbC346Fd', '6VA9MQosJnPcCwEeNkNVsW', MintType.COMMENT),
            ('Nounish Vibe', '0xCcbb9DC3FeCAf7a9cAe716eF1C16C8ca2f19a3D1', '2r8tpvuVPkYIuhAWSoMYY1', MintType.COMMENT),
            ('Hand of Nouns', '0x250d4678a1175113eC96e7DeB90584267026D443', '2qOcpUCs12XwgLUpoQQgYT', MintType.COMMENT),
            ('Happy Nouniversary from based Nouns!', '0x6414A4359848d2BF12B93483cd8A6ef6B03779ae', '71QheN8IVzfyoVtE8oeHNU', MintType.COMMENT),
            ('Base God and Miggs wif Nouns', '0x25F98e990B6C0dBa5A109B92542F16DCbbD017C8', '1eeRIVPiOVBJ3rlM5sGnpx', MintType.COMMENT),
            ('nounify the rockies', '0x306671092213C4d0da1a7bB5c31D5B4F9aB62246', '21pui4pvJ0h6YA8EAlvjqh', MintType.COMMENT),
            ('Coffee Days 2024', '0xf16755b43eE1a458161f0faE5a9124729f4f6B1B', 'ocsChallenge_9142cba1-ec12-4ee8-915e-7976536908cd', MintType.COMMENT),
            ('STIX Launch Tournament Pass', '0xa7891c87933BB99Db006b60D8Cb7cf68141B492f', 'ocsChallenge_bd5208b5-ff1e-4f5b-8522-c4d4ebb795b7', MintType.STIX),
            ('strut 001', '0x9FF8Fd82c0ce09caE76e777f47d536579AF2Fe7C', '5c3PqZ2EGVbzQ2CQXL1vWK', MintType.COMMENT),
            ('Nouniversary (Blue)', '0xC8f93Ce7A12960466a2e13E70dE5CA41B652e4E6', 'ocsChallenge_578c4c33-4506-4604-8359-ac0b43a3809c', MintType.COMMENT),
            ('Toshi Onchain Summer', '0x44d461Da8A451f05b6b75EdD5C4a2d2f3C14aaB4', '4g9y1NVvIxiOCSeGvPLmJS', MintType.COMMENT),
            ('Base Canada', '0x7B791EdF061Df65bAC7a9d47668F61F1a9A998C0', '1BWyKWI2UZHnOEw8E4hpS5', MintType.COMMENT),
            ('Butterfly', '0x3b4B32a5c9A01763A0945A8a4a4269052DC3DE2F', '6UuHdstl9MRFd4cgFf15kk', MintType.COMMENT),
            ('THINK BIG', '0x752d593b3B8aD1c5d827F5B9AA9b653eE7134ea0', '3EOQYszODyvZvbQMoKPoDO', MintType.COMMENT),
            ('Toshi Chess', '0xd60f13cC3e4d5bC96e7bAE8AAb5F448f3eFF3F0C', '1HMONONDaMukjieAOD3PHQ', MintType.COMMENT),
            ('Toshi Vibe', '0xbFa3fF9dcdB811037Bbec89f89E2751114ECD299', '3WE9nylUC2bMHz9c6hxFnL', MintType.COMMENT),
            ("Whatchu Lookin' At?", '0x5307c5ee9AeE0B944fA2E0Dba5D35D1D454E4bcE', '39XYCR1jsdPwnoFEpwCwhD', MintType.COMMENT),
            ('Stand with Crypto folk rock', '0x2382456097cC12ce54052084e9357612497FD6be', '5Hyw2HMBfOBFDvCBkvdVmX', MintType.COMMENT),
            ('Endaoment X SWC Shield', '0x4e4431BDdC2a896b1268ded02807b78c318C82e0', '359X8U2xzQmVIQRe7xSFk9', MintType.COMMENT),
            ('Stand with Crypto', '0x146B627a763DFaE78f6A409CEF5B8ad84dDD4150', '3ofLIMuInVt5sKkQOtLWp0', MintType.COMMENT)

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

        mint_price = 0.0006 if nft_contract == '0xf16755b43eE1a458161f0faE5a9124729f4f6B1B' else 0.0001
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
            return True
        return False

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
                        logger.error(f"[{self.account_id}][{self.address}] Error on claim {nft_name}: "
                                     f"{response_data['message']}")
                        raise ValueError('Error on claim')
                else:
                    logger.error(f"[{self.account_id}][{self.address}] Bad response on claim {nft_name}: "
                                 f"{response.status}")
                    raise ValueError('Error on claim')

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
                        raise ValueError('Error on claim')
                else:
                    logger.error(f"[{self.account_id}][{self.address}] Error on claim {badge_name}")
                    raise ValueError('Error on claim')

    async def claim_all_badges(self, sleep_from, sleep_to, random_badge):

        badges = self.badges.copy()

        if random_badge:
            badges = badges[:-4]
            random.shuffle(badges)
            badges += self.badges[-4:]

        for badge_name, badge_id in badges:
            if badge_name == 'BuildathonBadge':
                await self.mint_buildathon_badge()
            await self.claim_badge(badge_id, badge_name)
            await sleep(sleep_from, sleep_to, 'Sleep before next badge claim')

    @retry
    @check_gas
    async def mint_introducing_coinbase_wallet_nft(self, nft_name, nft_contract):
        logger.info(f"[{self.account_id}][{self.address}] Mint {nft_name} nft")

        contract = self.get_contract(nft_contract, INTRODUCING_ABI)
        n_nfts = await contract.functions.balanceOf(self.address).call()

        mint_price = 0.0001
        currency = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

        if n_nfts < 1:
            tx_data = await self.get_tx_data(value=self.w3.to_wei(mint_price, 'ether'))

            transaction = await contract.functions.claim(
                self.address,
                1,
                currency,
                100000000000000,
                {'proof': [],
                 'quantityLimitPerWallet': 2 ** 256 - 1,
                 'pricePerToken': 100000000000000,
                 'currency': currency
                 },
                "0x"
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already minted")
            return True
        return False

    @retry
    @check_gas
    async def mint_reservoir_nfts(self, nft_name, nft_contract):
        logger.info(f"[{self.account_id}][{self.address}] Mint {nft_name} nft")

        if nft_contract == '0xDc03a75F96f38615B3eB55F0F289d36E7A706660':
            contract = self.get_contract(nft_contract, COINEARNINGS_ABI)
            n_nfts = await contract.functions.balanceOf(self.address, 0).call()
        else:
            contract = self.get_contract(nft_contract, ONCHAIN_SUMMER_ABI)
            n_nfts = await contract.functions.balanceOf(self.address).call()

        if n_nfts < 1:
            if nft_name == 'Dawn of Daylight':
                data = f"0x760f2a0b000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000849ef788b40af342e2883c3112dd636f03a4203e000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000005af3107a40000000000000000000000000000000000000000000000000000000000000000464b510391f000000000000000000000000{self.address[2:].lower()}000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000003e4e8d51ef50000000000000000000000000000000000000000000000000000000000000060000000000000000000000000{self.address[2:].lower()}00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000002000000000000000000000000031b81650997e26eb527ca6541b1433d1ef348d9300000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002c000000000000000000000000031b81650997e26eb527ca6541b1433d1ef348d930000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000032000000000000000000000000000000000000000000000000000000000000001a484bb1e42000000000000000000000000{self.address[2:].lower()}0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000180000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000055c88bb05602da94fce8feadc1cbebf5b72c245300000000000000000000000000000000000000000000000000005af3107a4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001d4da48b00000000"
                value = 100000000000000
            elif nft_name == 'Mister Miggles':
                data = f"0x760f2a0b000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000849ef788b40af342e2883c3112dd636f03a4203e00000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000b5e620f480000000000000000000000000000000000000000000000000000000000000000484b510391f000000000000000000000000{self.address[2:].lower()}00000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000404e8d51ef50000000000000000000000000000000000000000000000000000000000000060000000000000000000000000{self.address[2:].lower()}000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000dc03a75f96f38615b3eb55f0f289d36e7a70666000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000005af3107a400000000000000000000000000000000000000000000000000000000000000002e0000000000000000000000000dc03a75f96f38615b3eb55f0f289d36e7a7066600000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000034000000000000000000000000000000000000000000000000000000000000001c457bc3d78000000000000000000000000{self.address[2:].lower()}00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000000000000000000000000000000005af3107a400000000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000000000000001a00000000000000000000000000000000000000000000000000000000000000080ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000000000000000000000000000000000000000000000005af3107a4000000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000055c88bb05602da94fce8feadc1cbebf5b72c245300000000000000000000000000000000000000000000000000005af3107a4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001d4da48b00000000"
                value = 200000000000000
            elif nft_name == 'Team Liquid Onchain Summer Premiere Series':
                data = f"0x760f2a0b000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000849ef788b40af342e2883c3112dd636f03a4203e000000000000000000000000000000000000000000000000000000000000006000000000000000000000000000000000000000000000000000005af3107a40000000000000000000000000000000000000000000000000000000000000000464b510391f000000000000000000000000{self.address[2:].lower()}000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000003e4e8d51ef50000000000000000000000000000000000000000000000000000000000000060000000000000000000000000{self.address[2:].lower()}0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000001b9ac8580d2e81d7322f163362831448e7fcad1b00000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002c00000000000000000000000001b9ac8580d2e81d7322f163362831448e7fcad1b0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000032000000000000000000000000000000000000000000000000000000000000001a484bb1e42000000000000000000000000{self.address[2:].lower()}0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000c00000000000000000000000000000000000000000000000000000000000000180000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000055c88bb05602da94fce8feadc1cbebf5b72c245300000000000000000000000000000000000000000000000000005af3107a4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001d4da48b00000000"
                value = 100000000000000
            tx_data = await self.get_tx_data(value)
            tx_data['data'] = data
            tx_data['to'] = '0x1aeD60A97192157fDA7fb26267A439d523d09c5e'

            signed_txn = await self.sign(tx_data)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already minted")
            return True
        return False

    async def mint_adventure(self, nft_name, nft_contract):
        logger.info(f"[{self.account_id}][{self.address}] Mint {nft_name} nft")

        contract = self.get_contract(nft_contract, ONCHAIN_SUMMER_ABI)
        n_nfts = await contract.functions.balanceOf(self.address).call()

        mint_price = 0.00042

        if n_nfts < 1:
            tx_data = await self.get_tx_data(value=self.w3.to_wei(mint_price, 'ether'))

            transaction = await contract.functions.mintWithComment(
                0,
                1,
                []
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already minted")
            return True
        return False

    @retry
    @check_gas
    async def mint_stix(self, nft_name, nft_contract):
        logger.info(f"[{self.account_id}][{self.address}] Mint {nft_name} nft")

        contract = self.get_contract(nft_contract, ONCHAIN_SUMMER_ABI)
        n_nfts = await contract.functions.balanceOf(self.address).call()

        currency = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

        if n_nfts < 1:
            tx_data = await self.get_tx_data()

            transaction = await contract.functions.claim(
                self.address,
                1,
                currency,
                0,
                {'proof': [self.w3.to_bytes(hexstr=f'0x{"0" * 64}')],
                 'quantityLimitPerWallet': 1,
                 'pricePerToken': 0,
                 'currency': currency
                 },
                "0x"
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already minted")
            return True
        return False

    async def mint_all_nft(self, sleep_from, sleep_to, random_mint, nfts_for_mint):

        nfts = self.os_nfts2.copy()

        nfts = [nft for nft in nfts if nft[0] in set(nfts_for_mint)]

        if random_mint:
            random.shuffle(nfts)

        is_minted = False

        for nft_name, nft_contract, challenge_id, mint_type in nfts:
            if mint_type == MintType.COMMENT:
                is_minted = await self.mint_nft(nft_name, nft_contract)
            elif mint_type == MintType.RESERVOIR:
                is_minted = await self.mint_reservoir_nfts(nft_name, nft_contract)
            elif mint_type == MintType.ADVENTURE:
                is_minted = await self.mint_adventure(nft_name, nft_contract)
            elif mint_type == MintType.INTRODUCING:
                is_minted = await self.mint_introducing_coinbase_wallet_nft(nft_name, nft_contract)
            elif mint_type == MintType.STIX:
                is_minted = await self.mint_stix(nft_name, nft_contract)
            await self.claim_task(nft_name, challenge_id)
            if not is_minted:
                await sleep(sleep_from, sleep_to, 'Sleep before next mint')

    async def check_available_spin(self):
        data = {
            'userAddress': self.address,
            'gameId': '2',
        }

        url = 'https://basehunt.xyz/api/spin-the-wheel'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, proxy=self.proxy, params=data) as response:
                if response.status in (200, 201):
                    response_data = await response.json()
                else:
                    logger.error(f"[{self.account_id}][{self.address}] Bad response {await response.text()}")
                    raise ValueError('Bad response')

        is_available = response_data['spinData']['hasAvailableSpin']
        return is_available

    @retry
    async def spin_the_wheel(self):
        logger.info(f"[{self.account_id}][{self.address}] Start spin the wheel")

        is_available = await self.check_available_spin()
        if is_available:
            data = {
                'gameId': '2',
                'userAddress': self.address
            }

            url = 'https://basehunt.xyz/api/spin-the-wheel/execute'

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=self.headers, proxy=self.proxy, json=data) as response:
                    if response.status in (200, 201):
                        response_data = await response.json()
                        type_ = response_data['spinData']['lastSpinResult']['type']
                        points = response_data['spinData']['lastSpinResult']['points']
                        logger.success(f"[{self.account_id}][{self.address}] Successfully earned {points} {type_}")
                    else:
                        logger.error(
                            f"[{self.account_id}][{self.address}] Bad response: {await response.text()}")
                        raise aiohttp.ContentTypeError
        else:
            logger.info(f"[{self.account_id}][{self.address}] Wheel is not available")

    @retry
    @check_gas
    async def mint_buildathon_badge(self):
        logger.info(f"[{self.account_id}][{self.address}] Start mint Buildathon Badge")

        nft_contract = self.get_contract("0x0c45CA58cfA181b038E06dd65EAbBD1a68d3CcF3", ONCHAIN_SUMMER_ABI)
        n_nft = await nft_contract.functions.balanceOf(self.address).call()

        if n_nft < 1:
            data = f"0x760f2a0b000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000020000000000000000000000000849ef788b40af342e2883c3112dd636f03a4203e00000000000000000000000000000000000000000000000000000000000000600000000000000000000000000000000000000000000000000000b5e620f480000000000000000000000000000000000000000000000000000000000000000464b510391f000000000000000000000000{self.address[2:].lower()}000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000000000000000000000000000000000000003e4e8d51ef50000000000000000000000000000000000000000000000000000000000000060000000000000000000000000{self.address[2:].lower()}0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000200000000000000000000000000c45ca58cfa181b038e06dd65eabbd1a68d3ccf300000000000000000000000000000000000000000000000000000000000000e000000000000000000000000000000000000000000000000000005af3107a400000000000000000000000000000000000000000000000000000000000000002c00000000000000000000000000c45ca58cfa181b038e06dd65eabbd1a68d3ccf30000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000032000000000000000000000000000000000000000000000000000000000000001a484bb1e42000000000000000000000000{self.address[2:].lower()}0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000000000000000000000000000000005af3107a400000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000001800000000000000000000000000000000000000000000000000000000000000080ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000000000000000000000000000000000000000000000005af3107a4000000000000000000000000000eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000055c88bb05602da94fce8feadc1cbebf5b72c245300000000000000000000000000000000000000000000000000005af3107a4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001d4da48b00000000"
            tx_data = await self.get_tx_data(self.w3.to_wei(0.0002, 'ether'))
            tx_data['data'] = data
            tx_data['to'] = '0x1aeD60A97192157fDA7fb26267A439d523d09c5e'

            signed_txn = await self.sign(tx_data)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already minted")
