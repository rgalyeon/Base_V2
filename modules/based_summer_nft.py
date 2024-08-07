from loguru import logger
from config import OPENSEA_ABI, ZERO_ADDRESS, EIP4844_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account


class BasedSummer(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="base")

        self.contract = self.get_contract("0x00005EA00Ac477B1030CE78506496e8C2dE24bf5", OPENSEA_ABI)

    @retry
    @check_gas
    async def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint based summer nft")

        nft_contact_address = "0x616a7241b5Ee65d9Be08dE24a1c9c55D268De093"
        fee_recipient = "0x0000a26b00c1F0DF003000390027140000fAa719"
        minter_if_not_payer = ZERO_ADDRESS
        quantity = 1

        nft_contract = self.get_contract(nft_contact_address, EIP4844_ABI)
        n_nfts = await nft_contract.functions.balanceOf(self.address).call()
        if n_nfts < 1:
            tx_data = await self.get_tx_data()

            transaction = await self.contract.functions.mintPublic(
                nft_contact_address,
                fee_recipient,
                minter_if_not_payer,
                quantity
            ).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.info(f"[{self.account_id}][{self.address}] Already minted. Skip module")
