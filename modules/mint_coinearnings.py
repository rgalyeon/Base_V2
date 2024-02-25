from loguru import logger
from config import COINEARNINGS_ABI, COINEARNINGS_CONTRACT
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class CoinEarnings(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="base")

        self.contract = self.get_contract(COINEARNINGS_CONTRACT, COINEARNINGS_ABI)

    @retry
    @check_gas
    async def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint coinearnings")

        currency = self.w3.to_checksum_address('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE')
        price_per_token = 0
        allowlist_proof = {'proof': [], 'quantityLimitPerWallet': 2, 'pricePerToken': 0, 'currency': currency}
        quantity = 1
        token_id = 0

        n_nfts = await self.contract.functions.balanceOf(self.address, 0).call()
        if n_nfts < 1:
            tx_data = await self.get_tx_data()

            transaction = await self.contract.functions.claim(
                self.address,
                token_id,
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
