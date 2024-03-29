![Base](https://github.com/rgalyeon/Base_V2/assets/28117274/6bde4f42-8df2-45f2-9cb7-1345666d6279)

# Base V2
Software for working with the Base chain. Supports multiple OKX accounts, multithreading, encrypts sensitive data, after encryption wallets can be started using only the wallet address (no need to re-enter data). This is updated version of the [SybilWave fork software](https://github.com/rgalyeon/base).

Main features: smart bridges, smart okx withdrawal for volumes, ETH collector from all networks on OKX, modules with cheap transaction's fee

## 🗂️ Description
With the help of the software you can make a withdrawal from the OKX exchange, bridge from/to Base, make swap, deposit/withdraw to/from lendings etc...

**Modules**
1. `encrypt_privates_and_proxy` - module is necessary for the first launch of the software. Reads data from the table `wallet_data.xlsx`, encrypts and deletes sensitive data from the table. For repeated runs it is enough to specify only the wallet address, because the rest of the data is stored in encrypted form. If you want to add new data (add wallets or change proxies), you will need to use this module again.
2. `withdraw_okx` - module for withdrawing tokens from the OKX. Supports checking the balance on the wallet to avoid withdrawing money in case it is already in the chain
3. `custom_routes` - module for customizing your own route
4. `automatic_routes` - module for automatic route building. You can customize the number of required transactions, you can add skipping some transactions. You can configure delays between transactions. You can control the probability of making cheap transactions and expensive ones.
5. Off bridge
6. Orbiter bridge
7. Transfer ETH from chains to OKX/addresses
8. Swap uniswap/pancake/woofi/baseswap/odos
9. Deposit/withdraw to/from aave/moonwell
10. Vote on Rubyscore
11. Create Gnosis Safe
12. Dmail
13. Mint/Bridge Zerius
14. Mint zkstars
15. Mint nfts2me
16. Search nfts2me contracts
17. Mint unlooped
18. Mint coineranings
19. Create Rai portfolio
20. Tx count checker (nonce)

## ⚙️ Installation
```bash
git clone https://github.com/rgalyeon/Base_V2.git
cd Base_V2
python -m venv venv
source venv/bin/activate (on MacOs) or .\venv\Scripts\activate (on Windows)
pip install -r requirements.txt
```

## 🚀 How to run software
### 1. First, you must fill in the appropriate columns in the `wallet_data.xslx` table:
- `name` - name/index of wallet (optional)
- `address` - wallet address
- `private` - private key 
- `proxy` - proxy, if used for wallet in the format `login:pass@ip:port` (optional)
- `okx_api` - api okx account in the format `api;secret;password` (you can customize okx api for each wallet) (optional)
- `okx_address` - address for transfer eth to OKX (optional)

### 2. Encrypt data
- Run script with `python main.py` command and choose `Encrypt private keys and proxies`
- Set up a password to access the data

#### 3. Customize the modules and get them up and running. 
- Set up general settings in `settings.py` (thread_count, retry_count, etc...)
- Set up modules settings in `module_settings.py`
- Add the wallet addresses you want to run to the `wallet_data.xlsx` file (only wallet addresses are needed after encryption)
- Run script with `python main.py` command and choose necessary module.

## 🔗 Contacts
- [Author](https://t.me/rgalyeon)
- Buy me a coffee: `rgalyeon.eth`

