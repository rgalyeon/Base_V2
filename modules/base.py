from loguru import logger
from typing import List

from utils.gas_checker import check_gas
from utils.helpers import retry
from .transfer import Transfer

from config import (
    BASE_BRIDGE_CONTRACT,
    BASE_BRIDGE_ABI,
    BASE_TOKENS,
    WETH_ABI
)


class Base(Transfer):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info)

    async def native_bridge_deposit(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int,
            save_funds: List[float],
            check_balance_on_dest: bool,
            check_amount: float,
            min_required_amount: float
    ):
        self.bridge_logic = self.deposit_logic

        await self.transfer_eth(from_chains=['ethereum'],
                                min_amount=min_amount, max_amount=max_amount,
                                decimal=decimal, all_amount=all_amount,
                                min_percent=min_percent, max_percent=max_percent,
                                save_funds=save_funds, check_balance_on_dest=check_balance_on_dest,
                                check_amount=check_amount,
                                min_required_amount=min_required_amount, destination_chain='base')

    async def deposit_logic(self, source_chain, destination_chain, amount_wei, amount, balance):
        logger.info(f"[{self.account_id}][{self.address}] Bridge to Base | {amount} ETH")

        contract = self.get_contract(BASE_BRIDGE_CONTRACT, BASE_BRIDGE_ABI)

        tx_data = await self.get_tx_data(amount_wei)

        transaction = await contract.functions.depositTransaction(
            self.address,
            amount_wei,
            100000,
            False,
            "0x01"
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def wrap_eth(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = await self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        weth_contract = self.get_contract(BASE_TOKENS["WETH"], WETH_ABI)

        logger.info(f"[{self.account_id}][{self.address}] Wrap {amount} ETH")

        tx_data = await self.get_tx_data(amount_wei)

        transaction = await weth_contract.functions.deposit().build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def unwrap_eth(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = await self.get_amount(
            "WETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        weth_contract = self.get_contract(BASE_TOKENS["WETH"], WETH_ABI)

        logger.info(f"[{self.account_id}][{self.address}] Unwrap {amount} ETH")

        tx_data = await self.get_tx_data()

        transaction = await weth_contract.functions.withdraw(amount_wei).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())
