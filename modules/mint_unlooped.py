from loguru import logger
from config import UNLOOPED_ABI, UNLOOPED_CONTRACT, ERC721_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
from time import time


class Unlooped(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="base")

        self.contract = self.get_contract(UNLOOPED_CONTRACT, UNLOOPED_ABI)

    @retry
    @check_gas
    async def mint(self, contract):
        logger.info(f"[{self.account_id}][{self.address}] Mint NFT on unlooped")

        nft_address = self.w3.to_checksum_address(contract)
        start_date = await self.contract.functions.startDate(nft_address).call()
        end_date = await self.contract.functions.endDate(nft_address).call()

        if start_date < int(time()) < end_date:
            nft_contract = self.get_contract(nft_address, ERC721_ABI)
            balance = await nft_contract.functions.balanceOf(self.address).call()
            if balance < 1:
                tx_data = await self.get_tx_data()
                transaction = await self.contract.functions.mint(nft_address, 1).build_transaction(tx_data)

                signed_txn = await self.sign(transaction)
                txn_hash = await self.send_raw_transaction(signed_txn)
                await self.wait_until_tx_finished(txn_hash.hex())
            else:
                logger.info(f"[{self.account_id}][{self.address}] Already minted. Skip module")
        else:
            logger.warning(f"[{self.account_id}][{self.address}] Mint on unlooped ended")
