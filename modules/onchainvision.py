from loguru import logger
from mimesis.random import random

from config import ONCHAIN_VISION_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class OnchainVision(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="base")

        self.contracts = ["0xdC9cAdd2D8Eb0219244d27fC48651f96Ce81Ec92",
                          "0x7178dE2f83376e38c61dFD575c2ecd7B12908d23",
                          "0xd25cc942852FfE5368ee61255896fC004702Db63"]

    @retry
    @check_gas
    async def mint(self):
        logger.info(f"[{self.account_id}][{self.address}] Mint Onchain Vision nfts")

        random.shuffle(self.contracts)

        for contract_address in self.contracts:
            contract = self.get_contract(contract_address, ONCHAIN_VISION_ABI)

            n_nfts = await contract.functions.balanceOf(self.address).call()
            if n_nfts < 1:
                tx_data = await self.get_tx_data()

                transaction = await contract.functions.mint(
                    self.address,
                    1
                ).build_transaction(tx_data)

                signed_txn = await self.sign(transaction)
                txn_hash = await self.send_raw_transaction(signed_txn)
                await self.wait_until_tx_finished(txn_hash.hex())
                await sleep(20, 60)
            else:
                logger.info(f"[{self.account_id}][{self.address}] Already minted. Skip mint")
