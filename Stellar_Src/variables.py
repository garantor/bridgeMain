
from sys import path
from stellar_sdk.network import Network
from stellar_sdk.server import Server, Keypair
import os, json
from pathlib import Path

from web3.main import Web3, HTTPProvider

# =========================================================================
                # Stellar Related
            # --------------------
stellar_server = Server(horizon_url="https://horizon-testnet.stellar.org")
general_network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
horizon_base_url = "https://horizon-testnet.stellar.org/"

dir_link = "/Users/afolabi/bridge"
asset_issuer_private_key = Path(os.path.join(dir_link, "Stellar_Src/pKeys/.asset_key")).read_text()

asset_issuer = Keypair.from_secret(asset_issuer_private_key).public_key
asset_code = "TLR"
# ===========================
distributor_secretKey = Path(os.path.join(dir_link, "Stellar_Src/pKeys/.distributor_key")).read_text()
distributor_PubKey = Keypair.from_secret(distributor_secretKey).public_key

# ==========================================================================


            # Web3 Related


# other_test_acct = "0x6F05560Cf14ddD9569bd5636c0006A9133977516"
main_address = "0xA1f7fAcb1e41Af5042463a952356A0ba3512AB9B" 


main_address_privateKey = Path("pKeys/.secrets").read_text() #Ethereum secret keys file
PATH_TRUFFLE_WK = '/Users/afolabi/bridge/Sol_src'
truffleFile = json.load(open(PATH_TRUFFLE_WK + '/build/contracts/StellarToken.json'))

# contract_address = "0x378d6Df9452ce3d81b66368E28Ce5089bD251175"
contract_address = truffleFile['networks']['97']['address']
contract_abi = truffleFile['abi'] # Contract Abi
contract_bytes = truffleFile['bytecode'] #Contract Addres, This change based on the netwrok

web3_instance = Web3(HTTPProvider("https://data-seed-prebsc-1-s1.binance.org:8545")) # Link to node to connect ot blockchain, this is binance smart chain testnet address
# contract_instance = web3_instance.eth.contract(abi=contract_abi, address=contract_address) # Contract Instance
contract_instance = web3_instance.eth.contract(abi=contract_abi, bytecode=contract_bytes, address=contract_address) # Contract Instance

test_url = "http://127.0.0.1:5000/"

