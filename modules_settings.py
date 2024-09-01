import asyncio

from modules import *
from utils.progress_checker import Scan


async def bridge_base(wallet_info):
    """
    Deposit from official bridge
    ______________________________________________________
    all_amount - bridge from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 100
    max_percent = 100

    check_balance_on_dest = False
    check_amount = 0.005
    save_funds = [0.00045, 0.0007]
    min_required_amount = 0

    base_inst = Base(wallet_info)
    await base_inst.native_bridge_deposit(
        min_amount, max_amount, decimal, all_amount, min_percent, max_percent,
        save_funds, check_balance_on_dest, check_amount, min_required_amount
    )


async def withdraw_okx(wallet_info):
    """
    Withdraw ETH from OKX
    ______________________________________________________
    min_amount - min amount (ETH)
    max_amount - max_amount (ETH)
    chains - ['zksync', 'arbitrum', 'linea', 'base', 'optimism']
    terminate - if True - terminate program if money is not withdrawn
    skip_enabled - If True, the skip_threshold check will be applied; otherwise, it will be ignored
    skip_threshold - If skip_enabled is True and the wallet balance is greater than or equal to this threshold,
                     skip the withdrawal
    """
    token = 'ETH'
    chains = ['arbitrum', 'zksync', 'linea', 'base', 'optimism']

    min_amount = 0.0070
    max_amount = 0.0072

    terminate = False

    skip_enabled = False
    skip_threshold = 0.00327

    wait_unlimited_time = False
    sleep_between_attempts = [10, 20]  # min, max

    okx_exchange = Okx(wallet_info, chains)
    await okx_exchange.okx_withdraw(
        min_amount, max_amount, token, terminate, skip_enabled, skip_threshold,
        wait_unlimited_time, sleep_between_attempts
    )


async def transfer_to_okx(wallet_info):
    from_chains = ["optimism", "arbitrum", "base"]

    min_amount = 0.0012
    max_amount = 0.0012
    decimal = 4

    all_amount = True

    min_percent = 100
    max_percent = 100

    save_funds = [0.0001, 0.00012]
    min_required_amount = 0.002

    bridge_from_all_chains = True
    sleep_between_transfers = [120, 350]

    transfer_inst = Transfer(wallet_info)
    await transfer_inst.transfer_eth(
        from_chains, min_amount, max_amount, decimal, all_amount, min_percent,
        max_percent, save_funds, False, 0, min_required_amount,
        bridge_from_all_chains=bridge_from_all_chains,
        sleep_between_transfers=sleep_between_transfers
    )


async def bridge_orbiter(wallet_info):
    """
    Bridge from orbiter
    ______________________________________________________
    from_chains – source chain - ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one or more
                  If more than one chain is specified, the software will check the balance in each network and
                  select the chain with the highest balance.
    to_chains – destination chain - ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one or more
                If more than one is specified, randomly selected

    min_amount - the minimum possible amount for sending
    max_amount - maximum possible amount to send
    decimal - to which digit to round the amount to be sent

    all_amount - if True, percentage values will be used for sending (min_percent, max_percent
                 instead of min_amount, max_amount).

    min_percent - the minimum possible percentage of the balance to be sent
    max_percent - the maximum possible percentage of the balance to send

    check_balance_on_dest - if True, it will check the balance in the destination network.
    check_amount - amount to check the balance in the destination network. if the balance is greater than this amount,
                   the bridge will not be executed.
    save_funds - what amount to leave in the outgoing network [min, max], chosen randomly from the range
    min_required_amount - the minimum required balance in the network to make the bridge.
                          if there is no network with the required balance, the bridge will not be made
    bridge_from_all_chains - if True, will be produced from all chains specified in the parameter from_chains
    sleep_between_transfers - only if bridge_from_all_chains=True. sleep between few transfers
    wait_unlimited_time - the software will wait indefinitely for funds on the wallet in the source chain
    sleep_between_attempts - minimum-maximum delay between balance checks (if wait_unlimited_time - True)
    """

    from_chains = ["arbitrum", "optimism", "base", "linea"]  # Chain with max balance will be selected
    to_chain = ["scroll"]  # Randomly selected

    min_amount = 0.005
    max_amount = 0.0051
    decimal = 6

    all_amount = True

    min_percent = 98
    max_percent = 100

    check_balance_on_dest = True
    check_amount = 0.005
    save_funds = [0.0011, 0.0013]
    min_required_amount = 0.005

    bridge_from_all_chains = False
    sleep_between_transfers = [120, 300]

    wait_unlimited_time = False
    sleep_between_attempts = [200, 300]  # min, max

    orbiter_inst = Orbiter(wallet_info, from_chains=from_chains)
    await orbiter_inst.transfer_eth(
        from_chains, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, save_funds,
        check_balance_on_dest, check_amount, min_required_amount, to_chain, bridge_from_all_chains,
        sleep_between_transfers=sleep_between_transfers, wait_unlimited_time=wait_unlimited_time,
        sleep_between_attempts=sleep_between_attempts
    )


async def bridge_relay(wallet_info):
    """
    Bridge from relay

    Supported chains - 'arbitrum', 'arbitrum_nova', 'base', 'optimism', 'zksync', 'ethereum', 'zora', 'mode', 'blast'
    ______________________________________________________
    Description: Look at bridge_orbiter description
    """

    from_chains = ["base"]  # Chain with max balance will be selected
    to_chain = ["ethereum"]  # Randomly selected

    min_amount = 0.005
    max_amount = 0.0051
    decimal = 6

    all_amount = True

    min_percent = 100
    max_percent = 100

    check_balance_on_dest = False
    check_amount = 0.005
    save_funds = [0.00005, 0.00003]
    min_required_amount = 0

    bridge_from_all_chains = False
    sleep_between_transfers = [120, 300]

    wait_unlimited_time = False
    sleep_between_attempts = [200, 300]  # min, max

    relay_inst = Relay(wallet_info, from_chains=from_chains)
    await relay_inst.transfer_eth(
        from_chains, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, save_funds,
        check_balance_on_dest, check_amount, min_required_amount, to_chain, bridge_from_all_chains,
        sleep_between_transfers=sleep_between_transfers, wait_unlimited_time=wait_unlimited_time,
        sleep_between_attempts=sleep_between_attempts
    )


async def wrap_eth(wallet_info):
    """
    Wrap ETH
    ______________________________________________________
    all_amount - wrap from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 5
    max_percent = 10

    base_inst = Base(wallet_info)
    await base_inst.wrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def unwrap_eth(wallet_info):
    """
    Unwrap ETH
    ______________________________________________________
    all_amount - unwrap from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 100
    max_percent = 100

    base_inst = Base(wallet_info)
    await base_inst.unwrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def swap_uniswap(wallet_info):
    """
    Make swap on Uniswap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDBC | Select one
    to_token – Choose DESTINATION token ETH, USDBC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDBC"
    to_token = "ETH"

    min_amount = 0.001
    max_amount = 0.002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    uniswap_inst = Uniswap(wallet_info)
    await uniswap_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_pancake(wallet_info):
    """
    Make swap on PancakeSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDBC | Select one
    to_token – Choose DESTINATION token ETH, USDBC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDBC"

    min_amount = 0.001
    max_amount = 0.002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    pancake_inst = Pancake(wallet_info)
    await pancake_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_woofi(wallet_info):
    """
    Make swap on WooFi
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDBC | Select one
    to_token – Choose DESTINATION token ETH, USDBC | Select one
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDBC"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    woofi_inst = WooFi(wallet_info)
    await woofi_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_baseswap(wallet_info):
    """
    Make swap on BaseSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDBC | Select one
    to_token – Choose DESTINATION token ETH, USDBC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDBC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    baseswap_inst = BaseSwap(wallet_info)
    await baseswap_inst.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                             max_percent)


async def swap_alienswap(wallet_info):
    """
    Make swap on AlienSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDBC | Select one
    to_token – Choose DESTINATION token ETH, USDBC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    alienswap_inst = AlienSwap(wallet_info)
    await alienswap_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_odos(wallet_info):
    """
    Make swap on Odos
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDBC | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDBC | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDBC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    odos_inst = Odos(wallet_info)
    await odos_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_inch(wallet_info):
    """
    Make swap on 1inch
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDBC | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDBC | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDBC"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    inch_dex_inst = Inch(wallet_info)
    await inch_dex_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_openocean(wallet_info):
    """
    Make swap on OpenOcean
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDBC | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDBC | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDBC"

    min_amount = 0.0001
    max_amount = 0.0001
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    openocean_inst = OpenOcean(wallet_info)
    await openocean_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_xyswap(wallet_info):
    """
    Make swap on XYSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDBC | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDBC | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDBC"

    min_amount = 0.0001
    max_amount = 0.0001
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    xyswap_inst = XYSwap(wallet_info)
    await xyswap_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_maverick(wallet_info):
    """
    Make swap on Maverick
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDBC | Select one
    to_token – Choose DESTINATION token ETH, USDBC | Select one
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDBC"

    min_amount = 0.0001
    max_amount = 0.0001
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    maverick_inst = Maverick(wallet_info)
    await maverick_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def bungee_refuel(wallet_info):
    """
    Make refuel on Bungee
    ______________________________________________________
    to_chain – Choose DESTINATION chain: BSC, OPTIMISM, GNOSIS, POLYGON, ZKSYNC, ARBITRUM, AVALANCHE, AURORA, ZK_EVM

    Disclaimer - The chain will be randomly selected
    ______________________________________________________
    random_amount – True - amount random from min to max | False - use min amount
    """

    chain_list = ["GNOSIS"]

    random_amount = False

    bungee_inst = Bungee(wallet_info)
    await bungee_inst.refuel(chain_list, random_amount)


async def stargate_bridge(wallet_info):
    """
    Stargate bridge ETH
    ______________________________________________________
    to_chain – Choose DESTINATION chain: arbitrum, optimism, linea

    Disclaimer - The chain will be randomly selected
    ______________________________________________________
    random_amount – True - amount random from min to max | False - use min amount
    """

    chain_list = ["arbitrum", "optimism"]

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    slippage = 1

    all_amount = True

    min_percent = 10
    max_percent = 10

    stargate_inst = Stargate(wallet_info)
    await stargate_inst.bridge(chain_list, min_amount, max_amount, decimal,
                               slippage, all_amount, min_percent, max_percent)


async def deposit_aave(wallet_info):
    """
    Make deposit on Aave
    ______________________________________________________
    make_withdraw - True, if need withdraw after deposit

    all_amount - deposit from min_percent to max_percent
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    sleep_from = 5
    sleep_to = 24

    make_withdraw = True

    all_amount = True

    min_percent = 5
    max_percent = 10

    aave_inst = Aave(wallet_info)
    await aave_inst.router(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


async def deposit_moonwell(wallet_info):
    """
    Make deposit on MoonWell
    ______________________________________________________
    make_withdraw - True, if need withdraw after deposit

    all_amount - deposit from min_percent to max_percent
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    sleep_from = 5
    sleep_to = 24

    make_withdraw = True

    all_amount = True

    min_percent = 5
    max_percent = 10

    moonwell_inst = MoonWell(wallet_info)
    await moonwell_inst.router(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


async def bridge_nft(wallet_info):
    """
    Make mint NFT and bridge NFT on L2Telegraph
    """

    sleep_from = 5
    sleep_to = 20

    l2telegraph_inst = L2Telegraph(wallet_info)
    await l2telegraph_inst.bridge(sleep_from, sleep_to)


async def mint_mintfun(wallet_info):
    """
    Mint NFT on Mint.Fun
    ______________________________________________________
    Disclaimer - The Mint function should be called "mint", to make sure of this,
                 look at the name in Rabby Wallet or in explorer
    """

    nft_contracts_data = {
        "0x69b69cc6e9f99c62a003fd9e143c126504d49dc2": 1,
        "0xea0b3e39ccd46d7F2B338D784De8519902f7E17E": 3,
    }

    mintfun_inst = MintFun(wallet_info)
    await mintfun_inst.mint(nft_contracts_data)


async def mint_zerius(wallet_info):
    """
    Mint + bridge Zerius NFT
    ______________________________________________________
    chains - list chains for random chain bridge: arbitrum, optimism, polygon, bsc, avalanche, zora
    Disclaimer - The Mint function should be called "mint", to make sure of this,
                 look at the name in Rabby Wallet or in explorer
    """

    chains = ["zora"]

    sleep_from = 200
    sleep_to = 700

    zerius_inst = Zerius(wallet_info)
    await zerius_inst.mint_and_bridge(chains, sleep_from, sleep_to)


async def mint_nft(wallet_info):
    """
    Mint NFT on NFTS2ME
    ______________________________________________________
    Specify contracts at data/nfts2me_contracts.json file or use nfts2me_search_contracts() module
    """

    contracts = [
        ('0x8E16744fF0Ef42DB38276ecc32D248237548297f', 'mint'),  # sakura blade #1
        ('0x0E7733747cFB856637c171b049d1bF0b4a5636cd', 'mint'),  # sakura blade #2
        ('0x3cCF622C09CADd841AD1F1d2D3Fdd99A016Ba0c3', 'mint'),  # sakura blade #3
        ('0x21e3E261b234931Fef4291df2F8a3FeB1869CfaA', 'mint'),  # sakura blade #4
        ('0x995bD197fb9B866Ab262A6243a463F441894d35f', 'mint'),  # sakura blade #5
        ('0xeF9eCF45F22e96486ECDf41F7E732234995b98DD', 'mint'),  # Back to ATH
        ('0x19915657BFD1291b017Fa8b1fdDbc7274F99A3c0', 'mint'),  # MandaCat
        ('0xdE69cdB6a0E0DeBEFaCb4998FDdc9Ff32CE1e76D', 'mint'),  # Paradise on earth
        ('0x4a5b47e3b69Dc91fC0C951333c815Ea0d774a440', 'mint'),  # Girl with Pearl
        ('0x28F0249d4a52A803cb585E1a369CAf6b774D96c7', 'mint'),  # Blue hair girl
        ('0x3Ef5c6C5230b7832cC39830BAAa0BE1092b11C63', 'mint'),  # Battle Rhino
        ('0xCbc5c4F0eC44C2Ee19D90f6C2968189ABE49309c', 'mint'),  # The World Ahead
        ('0xc38964D832873Fb47555B903b03fB9Fd9ECdc346', 'mint'),  # Koala
        ('0x6C40aF77cd9ebe10290A95B59E6EF1D81f88D449', 'mint'),  # Skeleton
        ('0x8c157a18Da183DA04841CFeffA8278D66a7d0aE9', 'mint'),  # Meo Meo
        ('0x2BEADfCc95C9730BcdBc69FE853370994BfA31dF', 'mint'),  # cube building
        ('0x850116229A3dE92014d63eF6716d8BaCE40c6cbe', 'mint'),  # fuckers
        ('0x2C98B101335695Ab2fC46e84dA9b1518bc4cA0EE', 'mint'),  # Two-tailed fox
        ('0x84CF15984b24E10AB2Ff121bDA714Be2bA90f986', 'mint'),  # kateVG3
        ('0x811835dfA6bF48a0F1C4fCFCF93ea89F9e881e4f', 'mint'),  # nancyTON
        ('0xfEfc993328D387b5ca34b082a0ba350B03e2bf6d', 'mint'),  # alvar
        ('0xEc302Cb786F28229bB5b1f8Fa5BBC1c8F570647B', 'mint'),  # anny0
        ('0xC087546B6C7c62d6bBe148c6015Ca71e17f0757a', 'mint'),  # danny1
        ('0xC2A25349aDd0c6368CC099be5d3cde0426fc66a0', 'mint'),  # kelly
        ('0x3C3987317A224EC871c81ebFDd042eFFaba69E00', 'mint'),  # Marty
    ]

    minter = Minter(wallet_info)
    await minter.mint_nft(contracts)


async def mint_zkstars(wallet_info):
    """
    Mint ZkStars NFT
    """

    contracts = [
        "0x4c78c7d2f423cf07c6dc2542ac000c4788f03657",
        "0x657130a14e93731dfecc772d210ae8333303986c",
        "0x004416bef2544df0f02f23788c6ada0775868560",
        "0x39b06911d22f4d3191827ed08ae35b84f68843e4",
        "0x8a6a9ef84cd819a54eee3cf7cfd351d21ab6b5fe",
        "0x8fb3225d0a85f2a49714acd36cdcd96a7b2b7fbc",
        "0x91ad9ed35b1e9ff6975aa94690fa438efb5a7160",
        "0x32d8eeb70eab5f5962190a2bb78a10a5a0958649",
        "0xab62313752f90c24405287ad8c3bcf4c25c26e57",
        "0x6f562b821b5cb93d4de2b0bd558cc8e46b632a08",
        "0xb63159a26664a89abce783437fc17786af8bb46d",
        "0x7e6b32d7eecddb6be496f232ab9316a5bf9f4e17",
        "0xcb03866371fb149f3992f8d623d5aaa4b831e2fd",
        "0x78c85441f53a07329e2380e49f1870199f70cee1",
        "0x54c49cb80a0679e3217f86d891859b4e477b56c3",
        "0xad6f16f5ff3461c83d639901bae1fb2a8a68aa31",
        "0x023a7c97679f2c121a31bacf37292dabf7ab97e9",
        "0x5dabff127cad8d075b5cea7f795dcbae1ddf471d",
        "0xd3c6386362dabab1a30acc2c377d9ac2cc8b7b16",
        "0xed0407d6b84b2c86418cac16a347930b222b505c"
    ]

    mint_min = 1
    mint_max = 1

    mint_all = False

    sleep_from = 5
    sleep_to = 10

    zkkstars = ZkStars(wallet_info)
    await zkkstars.mint(contracts, mint_min, mint_max, mint_all, sleep_from, sleep_to)


async def swap_tokens(wallet_info):
    """
    SwapTokens module: Automatically swap tokens to ETH
    ______________________________________________________
    use_dex - Choose any dex: uniswap, pancake, woofi, baseswap, alienswap, maverick, odos, inch, xyswap, openocean
    """

    use_dex = [
        "uniswap", "pancake", "woofi", "baseswap",
        "alienswap", "maverick", "odos", "inch",
        "xyswap", "openocean"
    ]

    use_tokens = ["USDBC"]

    sleep_from = 300
    sleep_to = 600

    slippage = 1

    min_percent = 100
    max_percent = 100

    swap_tokens_inst = SwapTokens(wallet_info)
    await swap_tokens_inst.swap(use_dex, use_tokens, sleep_from, sleep_to, slippage, min_percent, max_percent)


async def swap_multiswap(wallet_info):
    """
    Multi-Swap module: Automatically performs the specified number of swaps in one of the dexes.
    ______________________________________________________
    use_dex - Choose any dex: uniswap, pancake, woofi, baseswap, alienswap, maverick, odos, inch, xyswap, openocean
    quantity_swap - Quantity swaps
    ______________________________________________________
    random_swap_token - If True the swap path will be [ETH -> USDBC -> USDBC -> ETH] (random!)
    If False the swap path will be [ETH -> USDBC -> ETH -> USDBC]
    """

    use_dex = ["uniswap", "pancake", "woofi", "baseswap", "odos"]

    min_swap = 1
    max_swap = 2

    sleep_from = 3
    sleep_to = 7

    slippage = 1

    random_swap_token = True

    min_percent = 5
    max_percent = 10

    multi = Multiswap(wallet_info)
    await multi.swap(
        use_dex, sleep_from, sleep_to, min_swap, max_swap, slippage, random_swap_token, min_percent, max_percent
    )


async def unlooped_mint(wallet_info):

    contract = "0xde3e6A01663025301838b64685845DAA5cFcCBD8"  # Mercury

    unlooped_inst = Unlooped(wallet_info)
    await unlooped_inst.mint(contract)


async def sound_xyz_mint(wallet_info):
    """
    Mint free nft (platform commission 0.000777 eth) on sound.xyz
    ______________________________________________________
    referral - wallet address of referral
    contracts - address of nft (soundtrack) and track edition in format ('address', 0 or 1)
                1 - Limited Edition, 0 - Free Edition; check info on website
    """

    referral = ""

    contracts = [
        ('0xf57FdEf4cBf30F7d47F578d313a181141C91c1E9', 1),  # INTRO
        ('0x68733a0fc8dEa32535A249cbFccd6Ae0329ce998', 0),  # Back Online (ft. Pluko x Biicla x EVAN GIIA)
        ('0x6ff2f9c5a59Adc4618617590A9DC77e5c9e4c68e', 0),  # anywhere but here
    ]

    sound_xyz_inst = SoundXyz(wallet_info)
    await sound_xyz_inst.mint_sound(contracts, referral)


async def mint_onchain_summer2_nfts(wallet_info):
    """
    Mint nft from Onchain Summer2 Campaign

    comment line if you don't need some nft

    only_claim - if True, soft will try to claim without mint
    ______________________________________________________
    """

    sleep_from = 10
    sleep_to = 20

    random_mint = True

    nfts = [
        'Celebrating the Ethereum ETF',  # 0.0001 eth
        'ETFEREUM',  # 0.0001 eth
        'ETH BREAKING THROUGH',  # 0.0001 eth
        'Ethereum ETF',  # 0.0001 eth
        "ETH can't be stopped",  # 0.0001 eth
        # # 'Happy Birthday Toshi',  # 0.0001 eth
        'EURC & Base Launch',  # 0.0001 eth
        'Introducing: Coinbase Wallet web app',  # 0.0001 eth
        'Mister Miggles',
        'Team Liquid Onchain Summer Premiere Series',
        # # 'Nouns Forever (Song A Day #5700)',
        'the world after ETH ETF approval',
        # # 'Adventure Begins',  # 0.00042 eth
        'Nouns everywhere ⌐◨-◨',
        # # 'Happy 3rd Nouniversary',
        # # 'Happy Nouniversary',
        # # 'Celebrating the end of Nouns: Season 3',
        'Celebrating Nouns',  # claim doesn't work on website
        'Nounish Vibe',
        'Hand of Nouns',
        'Happy Nouniversary from based Nouns!',
        # # 'Base God and Miggs wif Nouns',
        # # 'nounify the rockies',
        # # 'Dawn of Daylight',
        'Coffee Days 2024',
        # # 'STIX Launch Tournament Pass',
        'strut 001',
        'Nouniversary (Blue)',
        # # 'Toshi Onchain Summer',
        'Base Canada',
        'Butterfly',
        'THINK BIG',
        'Toshi Chess',
        'Toshi Vibe',
        "Whatchu Lookin' At?",
        'Stand with Crypto folk rock',
        # 'Endaoment X SWC Shield',
        'Stand with Crypto',
        'Yellow Collective Shield Trait',
        'Crypto will bloom',
        'Stand with Crypto Pizza',

        'Duality in motion',
        'Crypto Vibe',
        'Toshi x SWC 3',
        'The Creative Shield',
        'En grade',
        'Mint the vision',
        'Stand With Crypto Shield Rune',
        'Shielding the wonder',
        'Earth Stands with Crypto',
        '⌐◨-◨ Stand With Crypto',
        'We stand, we build',
        'Live and Let Live!',

        'Juicy Pack',
        'Forbes WEB3 Inspire',
        'Let The Shield Shine',
        'All for One',
        "Let's Stand",
        'The Eternal Skywheel',
        'New Way',
        'Nouns and community',
        'Truworld Onchain Summer Pass'
    ]

    only_claim = False

    os_inst = OnchainSummer(wallet_info)
    await os_inst.mint_all_nft(sleep_from, sleep_to, random_mint, nfts, only_claim)


async def register_onchain_summer(wallet_info):

    ref_code = "3e2cc38a-5422-42d5-bd2d-85b5340662fb"

    os_inst = OnchainSummer(wallet_info)
    await os_inst.register_account(ref_code)


async def mint_base_domain(wallet_info):
    """
    Create Base domain with discount

    sleep_from/to - sleep before claim task on onchain summerыс
    """
    sleep_from = 10
    sleep_to = 20

    only_claim = False

    os_inst = OnchainSummer(wallet_info)
    await os_inst.register_domain(sleep_from, sleep_to, only_claim)


async def claim_all_badges(wallet_info):
    """
    Claim badges Onchain Summer 2 Campaign
    ______________________________________________________
    """

    sleep_from = 10
    sleep_to = 20

    random_mint = True

    os_inst = OnchainSummer(wallet_info)
    await os_inst.claim_all_badges(sleep_from, sleep_to, random_mint)


async def custom_routes(wallet_info):
    """
    BRIDGE:
        – bridge_base
        – bridge_orbiter
        – bungee_refuel
        – stargate_bridge
    WRAP:
        – wrap_eth
        – unwrap_eth
    DEX:
        – swap_uniswap
        – swap_pancake
        – swap_woofi
        – swap_baseswap
        – swap_alienswap
        – swap_maverick
        – swap_odos
        – swap_inch
        – swap_openocean
        – swap_xyswap
    LANDING:
        – deposit_aave
        – deposit_moonwell
        – withdraw_aave
        – withdraw_moonwell
    NFT/DOMAIN:
        – mint_zerius
        – mint_zkstars
        – mint_mintfun
        – mint_nft
    ANOTHER:
        – send_message
        – send_mail (Dmail)
        – bridge_nft
        – create_portfolio
        – swap_tokens
        – swap_multiswap
        – create_safe
        – mint_nft
    BASE NFTS:
        - mint_onchain_summer_is_back_nft
    ONCHAIN_SUMMER2:
        - claim_all_badges
        - mint_onchain_summer2_nfts
        - spin_the_wheel


    If random_module = True and withdraw_okx in use_modules, withdraw_okx will always be executed first and
                       transfer_to_okx will be executed last
    ______________________________________________________
    Disclaimer - You can add modules to [] to select random ones,
    example [module_1, module_2, [module_3, module_4], module 5]
    The script will start with module 1, 2, 5 and select a random one from module 3 and 4

    You can also specify None in [], and if None is selected by random, this module will be skipped

    You can also specify () to perform the desired action a certain number of times
    example (send_mail, 1, 10) run this module 1 to 10 times
    """

    use_modules = [
        mint_onchain_summer2_nfts,
        mint_base_domain
    ]

    sleep_from = 60
    sleep_to = 120

    random_module = True

    routes_ints = Routes(wallet_info)
    await routes_ints.start(use_modules, sleep_from, sleep_to, random_module)


async def automatic_routes(wallet_info):
    """
    Модуль автоматически генерирует пути по которому пройдет кошелек,
    меняя вероятности выбрать тот или иной модуль для каждого кошелька

    Parameters
    ----------
    transaction_count - количество транзакций (не обязательно все выполнятся, модули могут пропускаться)
    cheap_ratio - от 0 до 1, доля дешевых транзакций при построении маршрута
    cheap_modules - список модулей, которые будут использоваться в качестве дешевых
    expensive_modules - список модулей, которые будут использоваться в качестве дорогих
    -------

    """

    transaction_count = 25
    cheap_ratio = 1.0

    sleep_from = 30
    sleep_to = 60

    use_none = True
    cheap_modules = [send_mail, create_safe, mint_zkstars, mint_nft]
    expensive_modules = [swap_multiswap, deposit_aave, deposit_moonwell, create_portfolio, mint_zerius]

    routes_inst = Routes(wallet_info)
    await routes_inst.start_automatic(transaction_count, cheap_ratio,
                                      sleep_from, sleep_to,
                                      cheap_modules, expensive_modules,
                                      use_none)


async def nfts2me_search_contracts():
    """
    Module for searching nfts collections created in the nfts2me service.
    If you do not want to search for smart contracts for the mint_nfts2me module,
    you can run this module and it will add the addresses of contracts to the config by itself.
    ______________________________________________________
    mint_price - mint price of the searched contract
    min_total_supply - minimum supply of the collection
    search_limit - The maximum number of recent transactions to search through. Max: 10000
    """
    mint_price = 0
    min_total_supply = 1000
    search_limit = 9000

    await find_and_update_nfts2me_contracts(mint_price, min_total_supply, search_limit)


# -------------------------------------------------------  NO NEED TO CHANGE MODULES

async def vote_rubyscore(wallet_info):
    """
    Vote in Scroll at Rubyscore
    """

    rubyscore_inst = Rubyscore(wallet_info)
    await rubyscore_inst.vote()


async def send_mail(wallet_info):
    dmail_inst = Dmail(wallet_info)
    await dmail_inst.send_mail()


async def withdraw_aave(wallet_info):
    aave_inst = Aave(wallet_info)
    await aave_inst.withdraw()


async def withdraw_moonwell(wallet_info):
    moonwell_inst = MoonWell(wallet_info)
    await moonwell_inst.withdraw()


async def send_message(wallet_info):
    l2telegraph_inst = L2Telegraph(wallet_info)
    await l2telegraph_inst.send_message()


async def create_portfolio(wallet_info):
    rai_inst = Rai(wallet_info)
    await rai_inst.create()


async def create_safe(wallet_info):
    gnosis_safe = GnosisSafe(wallet_info)
    await gnosis_safe.create_safe()


async def mint_coinearnings(wallet_info):
    nft = CoinEarnings(wallet_info)
    await nft.mint()


async def mint_eip4844(wallet_info):
    nft_inst = EIP4844(wallet_info)
    await nft_inst.mint_eip_4844()


async def mint_onchain_summer_is_back_nft(wallet_info):
    onchain_summer_inst = OnchainSummer(wallet_info)
    await onchain_summer_inst.mint_onchain_summer_is_back()


async def mint_based_summer_nft(wallet_info):
    nft = BasedSummer(wallet_info)
    await nft.mint()


async def mint_base_era_nft(wallet_info):
    nft = BaseEra(wallet_info)
    await nft.mint()


async def spin_the_wheel(wallet_info):
    os_inst = OnchainSummer(wallet_info)
    await os_inst.spin_the_wheel()


def get_tx_count():
    asyncio.run(check_tx())


def start_encrypt():
    encrypt_privates(force=True)


def progress_check(wallets_data):

    replace = True

    Scan(wallets_data).get_wallet_progress(replace)


def onchain_summer_stats_check(wallets_data):

    Scan(wallets_data).get_onchain_summer_stats()
