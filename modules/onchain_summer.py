from loguru import logger
from config import ONCHAIN_SUMMER_ABI, ONCHAIN_SUMMER_CONTRACT
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class OnchainSummer(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="base")

    @retry
    @check_gas
    async def mint_onchain_summer_is_back(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint Onchain Summer Is Back nft")

        contract = self.get_contract(ONCHAIN_SUMMER_CONTRACT, ONCHAIN_SUMMER_ABI)

        currency = self.w3.to_checksum_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE')
        price_per_token = 200000000000000
        allowlist_proof = {'quantityLimitPerWallet': 2 ** 256 - 1,
                           'pricePerToken': price_per_token,
                           'currency': currency}
        quantity = 1

        n_nfts = await contract.functions.balanceOf(self.address, 0).call()
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
