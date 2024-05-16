import random
from typing import List

from loguru import logger
from config import BASE_TOKENS
from modules import *
from utils.sleeping import sleep


class SwapTokens(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="base")

        self.swap_modules = {
            "uniswap": Uniswap,
            "pancake": Pancake,
            "woofi": WooFi,
            "baseswap": BaseSwap,
            "alienswap": AlienSwap,
            "maverick": Maverick,
            "odos": Odos,
            "inch": Inch,
            "xyswap": XYSwap,
            "openocean": OpenOcean,
        }
        self.wallet_info = wallet_info

    def get_swap_module(self, use_dex: list):
        swap_module = random.choice(use_dex)
        return self.swap_modules[swap_module]

    async def swap(
            self,
            use_dex: List,
            tokens: List,
            sleep_from: int,
            sleep_to: int,
            slippage: int,
            min_percent: int,
            max_percent: int,
    ):
        random.shuffle(tokens)

        logger.info(f"[{self.account_id}][{self.address}] Start swap tokens")

        for _, token in enumerate(tokens, start=1):
            if token == "ETH":
                continue

            balance = await self.get_balance(BASE_TOKENS[token])

            if balance["balance_wei"] > 0:
                swap_module = self.get_swap_module(use_dex)(self.wallet_info)
                await swap_module.swap(
                    token,
                    "ETH",
                    balance["balance"],
                    balance["balance"],
                    balance["decimal"],
                    slippage,
                    True,
                    min_percent,
                    max_percent
                )

            if _ != len(tokens):
                await sleep(sleep_from, sleep_to, message=f"[{self.account_id}][{self.address}] Sleep before next swap")
