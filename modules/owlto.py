from loguru import logger
from config import OWLTO_CHECKIN_CONTRACT, OWLTO_CHECKIN_ABI, RPC
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
import time


class Owlto(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info, chain="base")

        self.contract = self.get_contract(OWLTO_CHECKIN_CONTRACT, OWLTO_CHECKIN_ABI)

    @retry
    @check_gas
    async def check_in(self):
        logger.info(f"[{self.account_id}][{self.address}] Start Owlto Check-in")

        date = time.strftime("%Y%m%d")

        tx_data = await self.get_tx_data()
        transaction = await self.contract.functions.checkIn(int(date)).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)
        txn_hash = await self.send_raw_transaction(signed_txn)
        await self.wait_until_tx_finished(txn_hash.hex())