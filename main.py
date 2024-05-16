import asyncio
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import questionary
from questionary import Choice

from settings import (
    RANDOM_WALLET,
    SLEEP_TO,
    SLEEP_FROM,
    QUANTITY_THREADS,
    THREAD_SLEEP_FROM,
    THREAD_SLEEP_TO,
    SAVE_LOGS
)
from modules_settings import *
from utils.sleeping import sleep
from utils.password_handler import get_wallet_data
from utils.logs_handler import filter_out_utils
from itertools import count
import threading
from loguru import logger
from config import HEADER

transaction_lock = threading.Lock()


def get_module():
    counter = count(1)
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice(f"{next(counter)}) Encrypt wallets", encrypt_privates),
            Choice(f"{next(counter)}) Withdraw from OKX", withdraw_okx),
            Choice(f"{next(counter)}) Make bridge to Base", bridge_base),
            Choice(f"{next(counter)}) Make bridge on Orbiter", bridge_orbiter),
            Choice(f"{next(counter)}) Wrap ETH", wrap_eth),
            Choice(f"{next(counter)}) Unwrap ETH", unwrap_eth),
            Choice(f"{next(counter)}) Swap on Uniswap", swap_uniswap),
            Choice(f"{next(counter)}) Swap on Pancake", swap_pancake),
            Choice(f"{next(counter)}) Swap on WooFi", swap_woofi),
            Choice(f"{next(counter)}) Swap on BaseSwap", swap_baseswap),
            Choice(f"{next(counter)}) Swap on AlienSwap", swap_alienswap),
            Choice(f"{next(counter)}) Swap on Maverick", swap_maverick),
            Choice(f"{next(counter)}) Swap on Odos", swap_odos),
            Choice(f"{next(counter)}) Swap on 1inch", swap_inch),
            Choice(f"{next(counter)}) Swap on OpenOcean", swap_openocean),
            Choice(f"{next(counter)}) Swap on XYSwap", swap_xyswap),
            Choice(f"{next(counter)}) Bungee Refuel", bungee_refuel),
            Choice(f"{next(counter)}) Stargate bridge", stargate_bridge),
            Choice(f"{next(counter)}) Deposit Aave", deposit_aave),
            Choice(f"{next(counter)}) Withdraw Aave", withdraw_aave),
            Choice(f"{next(counter)}) Deposit MoonWell", deposit_moonwell),
            Choice(f"{next(counter)}) Withdraw MoonWell", withdraw_moonwell),
            Choice(f"{next(counter)}) Mint NFT on MintFun", mint_mintfun),
            Choice(f"{next(counter)}) Mint and Bridge Zerius NFT", mint_zerius),
            Choice(f"{next(counter)}) Mint ZkStars NFT", mint_zkstars),
            Choice(f"{next(counter)}) Dmail sending mail", send_mail),
            Choice(f"{next(counter)}) Send message L2Telegraph", send_message),
            Choice(f"{next(counter)}) Mint and bridge NFT L2Telegraph", bridge_nft),
            Choice(f"{next(counter)}) Create portfolio on Ray", create_portfolio),
            Choice(f"{next(counter)}) Create gnosis safe", create_safe),
            Choice(f"{next(counter)}) Search NFTS2ME contracts", nfts2me_search_contracts),
            Choice(f"{next(counter)}) Mint NFT on NFTS2ME", mint_nft),
            Choice(f"{next(counter)}) Swap tokens to ETH", swap_tokens),
            Choice(f"{next(counter)}) Use Multiswap", swap_multiswap),
            Choice(f"{next(counter)}) Mint COINearnings", mint_coinearnings),
            Choice(f"{next(counter)}) Mint unlooped", unlooped_mint),
            Choice(f"{next(counter)}) Mint EIP-4844 nft", mint_eip4844),
            Choice(f"{next(counter)}) Use custom routes", custom_routes),
            Choice(f"{next(counter)}) Use automatic routes", automatic_routes),
            Choice(f"{next(counter)}) Progress checker", progress_check),
            Choice(f"{next(counter)}) Check transaction count", "tx_checker"),
            Choice(f"{next(counter)}) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        sys.exit()
    return result


def get_wallets():
    wallets_data = get_wallet_data()
    return list(wallets_data.values())


async def run_module(module, wallet_data):
    try:
        await module(wallet_data)
    except Exception as e:
        logger.error(e)
        import traceback

        traceback.print_exc()

    await sleep(SLEEP_FROM, SLEEP_TO, message=f"Move to the next wallet or end of script")


def _async_run_module(module, wallet_data):
    asyncio.run(run_module(module, wallet_data))


def main(module):
    if module == encrypt_privates:
        return encrypt_privates(force=True)
    if module == nfts2me_search_contracts:
        return asyncio.run(nfts2me_search_contracts())

    wallets_data = get_wallets()

    if module == progress_check:
        return progress_check(wallets_data)

    if RANDOM_WALLET:
        random.shuffle(wallets_data)

    with ThreadPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
        for _, wallet_data in enumerate(wallets_data, start=1):
            executor.submit(
                _async_run_module,
                module,
                wallet_data
            )
            if _ != len(wallet_data):
                time.sleep(random.randint(THREAD_SLEEP_FROM, THREAD_SLEEP_TO))


if __name__ == '__main__':
    print(HEADER)
    print("Author – https://t.me/block_nine\n")

    if SAVE_LOGS:
        logger.add('logs.txt', filter=filter_out_utils)

    module = get_module()
    if module == "tx_checker":
        get_tx_count()
    else:
        main(module)

    print("ALL DONE!")
    print("Author – https://t.me/block_nine\n")
