import json

WALLET_DATA_PATH = 'wallet_data.xlsx'
SHEET_NAME = 'evm'
ENCRYPTED_DATA_PATH = 'encrypted_data.txt'
REALTIME_SETTINGS_PATH = 'realtime_settings.json'
PROGRESS_PATH = 'progress.xlsx'
ONCHAIN_SUMMER_SCORE_PATH = 'os_scores.xlsx'

with open('data/rpc.json') as file:
    RPC = json.load(file)

with open('data/abi/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open("data/abi/erc721_abi.json", "r") as file:
    ERC721_ABI = json.load(file)

with open('data/abi/base/bridge.json') as file:
    BASE_BRIDGE_ABI = json.load(file)

with open('data/abi/base/weth.json') as file:
    WETH_ABI = json.load(file)

with open("data/abi/uniswap/router.json", "r") as file:
    UNISWAP_ROUTER_ABI = json.load(file)

with open("data/abi/pancake/factory.json", "r") as file:
    UNISWAP_FACTORY_ABI = json.load(file)

with open("data/abi/uniswap/quoter.json", "r") as file:
    UNISWAP_QUOTER_ABI = json.load(file)

with open("data/abi/pancake/router.json", "r") as file:
    PANCAKE_ROUTER_ABI = json.load(file)

with open("data/abi/pancake/factory.json", "r") as file:
    PANCAKE_FACTORY_ABI = json.load(file)

with open("data/abi/pancake/quoter.json", "r") as file:
    PANCAKE_QUOTER_ABI = json.load(file)

with open("data/abi/woofi/router.json", "r") as file:
    WOOFI_ROUTER_ABI = json.load(file)

with open("data/abi/baseswap/router.json", "r") as file:
    BASESWAP_ROUTER_ABI = json.load(file)

with open("data/abi/alien/abi.json", "r") as file:
    ALIEN_ROUTER_ABI = json.load(file)

with open("data/abi/maverick/position.json", "r") as file:
    MAVERICK_POSITION_ABI = json.load(file)

with open("data/abi/maverick/router.json", "r") as file:
    MAVERICK_ROUTER_ABI = json.load(file)

with open("data/abi/bungee/abi.json", "r") as file:
    BUNGEE_ABI = json.load(file)

with open("data/abi/stargate/bridge.json", "r") as file:
    STARGATE_BRIDGE_ABI = json.load(file)

with open("data/abi/stargate/router.json", "r") as file:
    STARGATE_ROUTER_ABI = json.load(file)

with open("data/abi/aave/abi.json", "r") as file:
    AAVE_ABI = json.load(file)

with open("data/abi/moonwell/abi.json", "r") as file:
    MOONWELL_ABI = json.load(file)

with open("data/abi/l2telegraph/send_message.json", "r") as file:
    L2TELEGRAPH_MESSAGE_ABI = json.load(file)

with open("data/abi/l2telegraph/bridge_nft.json", "r") as file:
    L2TELEGRAPH_NFT_ABI = json.load(file)

with open("data/abi/mintfun/abi.json", "r") as file:
    MINTFUN_ABI = json.load(file)

with open("data/abi/rai/abi.json", "r") as file:
    RAI_ABI = json.load(file)

with open("data/abi/gnosis/abi.json", "r") as file:
    SAFE_ABI = json.load(file)

with open("data/abi/zerius/abi.json", "r") as file:
    ZERIUS_ABI = json.load(file)

with open("data/abi/nft2me/abi.json", "r") as file:
    NFTS2ME_ABI = json.load(file)

with open("data/abi/nft2me/abi_main.json", "r") as file:
    NFTS2ME_MAIN_ABI = json.load(file)

with open("data/abi/dmail/abi.json", "r") as file:
    DMAIL_ABI = json.load(file)

with open("data/abi/zkstars/abi.json", "r") as file:
    ZKSTARS_ABI = json.load(file)

with open("data/abi/coinearnings/abi.json", "r") as file:
    COINEARNINGS_ABI = json.load(file)

with open("data/abi/unlooped/abi.json", "r") as file:
    UNLOOPED_ABI = json.load(file)

with open("data/abi/rubyscore/abi.json") as file:
    RUBYSCORE_ABI = json.load(file)

with open("data/nfts2me_contracts.json", "r") as file:
    NFTS2ME_CONTRACTS = json.load(file)

with open('data/orbiter_maker.json', 'r') as file:
    ORBITER_MAKER = json.load(file)

with open('data/abi/eip4844_nft/abi.json', 'r') as file:
    EIP4844_ABI = json.load(file)

with open('data/abi/onchain_summer/abi.json', 'r') as file:
    ONCHAIN_SUMMER_ABI = json.load(file)

with open('data/abi/soundxyz/abi.json', 'r') as file:
    SOUND_XYZ_ABI = json.load(file)

with open('data/abi/soundxyz/nfts_abi.json', 'r') as file:
    SOUND_XYZ_NFT_ABI = json.load(file)

with open('data/abi/onchain_summer/opensea.json', 'r') as file:
    OPENSEA_ABI = json.load(file)

with open('data/abi/onchain_summer/introducing.json', 'r') as file:
    INTRODUCING_ABI = json.load(file)

with open('data/abi/onchain_summer/domain.json', 'r') as file:
    BASENAME_ABI = json.load(file)

with open('data/abi/onchain_summer/pass.json', 'r') as file:
    PASS_ABI = json.load(file)

with open('data/abi/onchainvision/abi.json', 'r') as file:
    ONCHAIN_VISION_ABI = json.load(file)

with open('data/abi/onchainvision/abi1.json', 'r') as file:
    ONCHAIN_VISION_ABI1 = json.load(file)

with open("data/abi/owlto/abi.json", "r") as file:
    OWLTO_CHECKIN_ABI = json.load(file)

NFTS2ME_CONTRACTS_PATH = 'data/nfts2me_contracts.json'

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

BASE_BRIDGE_CONTRACT = "0x49048044D57e1C92A77f79988d21Fa8fAF74E97e"

ORBITER_CONTRACT = ""

BASE_TOKENS = {
    "ETH": "0x4200000000000000000000000000000000000006",
    "WETH": "0x4200000000000000000000000000000000000006",
    "USDBC": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA",
    "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "DAI": "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",
}

UNISWAP_CONTRACTS = {
    "router": "0x2626664c2603336E57B271c5C0b26F421741e481",
    "factory": "0x33128a8fC17869897dcE68Ed026d694621f6FDfD",
    "quoter": "0x3d4e44Eb1374240CE5F1B871ab261CD16335B76a",
}

PANCAKE_CONTRACTS = {
    "router": "0x678Aa4bF4E210cf2166753e054d5b7c31cc7fa86",
    "factory": "0x0BFbCF9fa4f9C56B0F40a671Ad40E0805A091865",
    "quoter": "0xB048Bbc1Ee6b733FFfCFb9e9CeF7375518e25997"
}

WOOFI_CONTRACTS = {
    "router": "0x27425e9fb6a9a625e8484cfd9620851d1fa322e5"
}

BASESWAP_CONTRACTS = {
    "router": "0x327Df1E6de05895d2ab08513aaDD9313Fe505d86"
}

ALIEN_CONTRACTS = {
    "router": "0x8c1a3cf8f83074169fe5d7ad50b978e1cd6b37c7"
}

ODOS_CONTRACT = {
    "router": "0x19ceead7105607cd444f5ad10dd51356436095a1",
    "use_ref": False  # If you use True, you support me 0.1% of the transaction amount
}

INCH_CONTRACT = {
    "router": "0x1111111254eeb25477b68fb85ed929f73a960582",
    "use_ref": False  # If you use True, you support me 0.1% of the transaction amount
}

OPENOCEAN_CONTRACT = {
    "router": "0x6352a56caadc4f1e25cd6c75970fa768a3304e64",
    "use_ref": False  # If you use True, you support me 0.1% of the transaction amount
}

XYSWAP_CONTRACT = {
    "router": "0x6acd0ec9405ccb701c57a88849c4f1cd85a3f3ab",
    "use_ref": False  # If you use True, you support me 1% of the transaction amount
}

MAVERICK_CONTRACTS = {
    "router": "0x32AED3Bce901DA12ca8489788F3A99fCe1056e14",
    "pool": "0x06e6736ca9e922766279a22b75a600fe8b8473b6",
    "pool_information": "0x6E230D0e457Ea2398FB3A22FB7f9B7F68F06a14d",
}

BUNGEE_CONTRACT = "0xe8c5b8488feafb5df316be73ede3bdc26571a773"

STARGATE_CONTRACTS = {
    "router": "0xAF54BE5B6eEc24d6BFACf1cce4eaF680A8239398",
    "bridge": "0x50b6ebc2103bfec165949cc946d739d5650d7ae4"
}

AAVE_CONTRACT = "0x18cd499e3d7ed42feba981ac9236a278e4cdc2ee"

AAVE_WETH_CONTRACT = "0xD4a0e0b9149BCee3C920d2E00b5dE09138fd8bb7"

MOONWELL_CONTRACT = "0x70778cfcFC475c7eA0f24cC625Baf6EaE475D0c9"

MOONWELL_WETH_CONTRACT = "0x628ff693426583D9a7FB391E54366292F509D457"

MINTFUN_CONTRACT = "0xf39ac57beaf8f97b89db7a9203a4e47c17cf4391"

L2TELEGRAPH_MESSAGE_CONTRACT = "0x64e0f6164ac110b67df9a4848707ffbcb86c87a9"

L2TELEGRAPH_NFT_CONTRACT = "0x36a358b3ba1fb368e35b71ea40c7f4ab89bfd8e1"

RAI_CONTRACT = "0xbc097e42bf1e6531c32c5cee945e0c014fa21964"

SAFE_CONTRACT = "0xc22834581ebc8527d974f8a1c97e1bea4ef910bc"

ZERIUS_CONTRACT = "0x178608ffe2cca5d36f3fc6e69426c4d3a5a74a41"

DMAIL_CONTRACT = "0x47fbe95e981C0Df9737B6971B451fB15fdC989d9"

NFTS2ME_CREATOR_CONTRACT = '0x2269bCeB3f4e0AA53D2FC43B1B7C5C5D13B119a5'

COINEARNINGS_CONTRACT = "0x1d6b183bd47f914f9f1d3208edcf8befd7f84e63"

UNLOOPED_CONTRACT = "0x358268927d4f229629afeb59cd3a84f33e771690"

RUBYSCORE_CONTRACT = "0xe10add2ad591a7ac3ca46788a06290de017b9fb4"

EIP_4844_CONTRACT = "0x273cA93A52b817294830eD7572aA591Ccfa647fd"

ONCHAIN_SUMMER_CONTRACT = "0x768E7151500bB5120983d9619374F31DD71D8357"

SOUND_XYZ_CONTRACT = "0x000000000001a36777f9930aaeff623771b13e70"

OWLTO_CHECKIN_CONTRACT = "0x26637c9fDbD5Ecdd76a9E21Db7ea533e1B0713b6"


#################################################################
#                      BASESCAN API                             #
#################################################################

BASESCAN_URL = 'https://api.basescan.org/api'

BASE_API_KEYS = ['']

ETHERSCAN_API_KEYS = ['']  # api from https://etherscan.io/ ['api_key1', 'api_key2']

CHAINS_OKX = {
    'linea': 'Linea',
    'base': 'Base',
    'arbitrum': 'Arbitrum One',
    'optimism': 'Optimism',
    'zksync': 'zkSync Era'
}

ORBITER_CHAINS_INFO = {
    1: {'name': 'Arbitrum', 'chainId': 42161, 'id': 2},
    2: {'name': 'Arbitrum Nova', 'chainId': 42170, 'id': 16},
    3: {'name': 'Base', 'chainId': 8453, 'id': 21},
    4: {'name': 'Linea', 'chainId': 59144, 'id': 23},
    5: {'name': 'Manta', 'chainId': 169, 'id': 31},
    6: {'name': 'Polygon', 'chainId': 137, 'id': 6},
    7: {'name': 'Optimism', 'chainId': 10, 'id': 7},
    8: {'name': 'Scroll', 'chainId': 534352, 'id': 19},
    9: {'name': 'Starknet', 'chainId': 'SN_MAIN', 'id': 4},
    10: {'name': 'Polygon zkEVM', 'chainId': 1101, 'id': 17},
    11: {'name': 'zkSync Era', 'chainId': 324, 'id': 14},
    12: {'name': 'Zora', 'chainId': 7777777, 'id': 30},
    13: {'name': 'Ethereum', 'chainId': 1, 'id': 1},
    14: {'name': 'BNB Chain', 'chainId': 56, 'id': 15},
    26: {'name': 'Metis', 'chainId': 1088, 'id': 10},
    28: {'name': 'OpBNB', 'chainId': 204, 'id': 25},
    29: {'name': 'Mantle', 'chainId': 5000, 'id': 24},
    45: {'name': 'ZKFair', 'chainId': 42766, 'id': 38}
}

LAYERZERO_WRAPED_NETWORKS = {
    1: 1,
    2: 2,
    3: 27,
    4: 34,
    5: 14,
    6: 15,
    7: 3,
    8: 35,
    9: 19,
    10: 23,
    11: 21,
    12: 36,
    13: 13,
    14: 33,
    15: 37,
    16: 38,
    17: 20,
    18: 17,
    19: 25,
    20: 32,
    21: 31,
    22: 4,
    23: 44,
    24: 5,
    25: 29,
    26: 39,
    27: 26,
    28: 16,
    29: 30,
    30: 40,
    31: 7,
    32: 24,
    33: 6,
    34: 10,
    35: 8,
    36: 41,
    37: 18,
    38: 22,
    39: 42,
    40: 43,
    41: 12,
    42: 28,
    43: 11,
    44: 46
}

RHINO_CHAIN_INFO = {
    1: 'ARBITRUM',
    2: 'ARBITRUMNOVA',
    3: 'BASE',
    4: 'LINEA',
    5: 'MANTA',
    6: 'MATIC_POS',
    7: 'OPTIMISM',
    8: 'SCROLL',
    9: 'STARKNET',
    10: 'ZKEVM',
    11: 'ZKSYNC',
}


HEADER = """██████╗  █████╗ ███████╗███████╗    ██╗   ██╗██████╗ 
██╔══██╗██╔══██╗██╔════╝██╔════╝    ██║   ██║╚════██╗
██████╔╝███████║███████╗█████╗      ██║   ██║ █████╔╝
██╔══██╗██╔══██║╚════██║██╔══╝      ╚██╗ ██╔╝██╔═══╝ 
██████╔╝██║  ██║███████║███████╗     ╚████╔╝ ███████╗
╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝      ╚═══╝  ╚══════╝                                                 
"""
