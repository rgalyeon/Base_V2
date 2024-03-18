from loguru import logger
from config import EIP_4844_CONTRACT, NFTS2ME_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class EIP4844(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="base")

        self.contract = self.get_contract(EIP_4844_CONTRACT, NFTS2ME_ABI)

    @retry
    @check_gas
    async def mint_eip_4844(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint eip-4844 nft")
        balance = await self.contract.functions.balanceOf(self.address).call()
        if balance > 0:
            logger.warning(f"[{self.account_id}][{self.address}] EIP-4844. Skip module")
            return

        tx_data = await self.get_tx_data()
        transaction = await self.contract.functions.mint().build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        tnx_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(tnx_hash.hex())
