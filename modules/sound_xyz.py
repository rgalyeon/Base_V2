from loguru import logger
from config import SOUND_XYZ_ABI, SOUND_XYZ_CONTRACT, SOUND_XYZ_NFT_ABI, ZERO_ADDRESS
from utils.gas_checker import check_gas
from utils.helpers import retry
from .account import Account
import random


class SoundXyz(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="base")

    @retry
    @check_gas
    async def mint_sound(self, contracts, ref=""):
        logger.info(f"[{self.account_id}][{self.address}] Mint nft on Sound.xyz")

        if ref:
            ref = self.w3.to_checksum_address(ref)
        else:
            ref = ZERO_ADDRESS
        sound_contract = self.get_contract(SOUND_XYZ_CONTRACT, SOUND_XYZ_ABI)

        nfts = contracts.copy()
        while len(nfts):
            contr, is_limited_edition = random.choice(contracts)
            nft_contract = self.get_contract(contr, SOUND_XYZ_NFT_ABI)
            balance = await nft_contract.functions.balanceOf(self.address).call()

            if balance == 0:
                edition = self.w3.to_checksum_address(contr)

                data = [edition, is_limited_edition, 0, self.address, 1, ZERO_ADDRESS,
                        4294967295, [], 0, 0, 0, 0, "0x", ref, [], 0]

                tx_data = await self.get_tx_data(value=self.w3.to_wei(0.000777, "ether"))

                transaction = await sound_contract.functions.mintTo(data).build_transaction(tx_data)
                signed_txn = await self.sign(transaction)
                txn_hash = await self.send_raw_transaction(signed_txn)
                await self.wait_until_tx_finished(txn_hash.hex())

                break
        else:
            logger.info(f"[{self.account_id}][{self.address}] All nfts minted. Skip module")


