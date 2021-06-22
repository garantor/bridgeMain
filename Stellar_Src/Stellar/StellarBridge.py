from stellar_sdk import account
from stellar_sdk import server
from stellar_sdk import keypair
from stellar_sdk.asset import Asset
from stellar_sdk.keypair import Keypair
from stellar_sdk.memo import Memo
# from stellar_sdk.keypair import Keypair
from stellar_sdk.transaction_builder import TransactionBuilder
from stellar_sdk.transaction_envelope import TransactionEnvelope, Transaction
import threading
from variables import (distributor_secretKey, asset_issuer_private_key, horizon_base_url, 
                        stellar_server, asset_issuer, distributor_PubKey, asset_code, general_network_passphrase)
# from Bridges.variables import *





# print(Create_Asset(asset_issuer, "TEST"))


class StellarContract:
    def __init__(self) -> None:
        self.horizon_base_url = horizon_base_url
        self.stellar_server = stellar_server
        self.asset_issuer = asset_issuer
        self.asset_code = asset_code
        


    @classmethod
    def trust_asset(cls, signing_key):
        '''
        :param - signing_key is the person that want to add trustline key
        :param - asses_code eg USD
        :param - assest issuer public address of the issuer
        '''
        

        source_keypair = Keypair.from_secret(signing_key)
        source_public_key = source_keypair.public_key

        source_account = stellar_server.load_account(source_public_key)
        transaction = (
            TransactionBuilder(
                source_account=source_account,
                network_passphrase=general_network_passphrase,
                base_fee=100,
            ).append_change_trust_op(asset_code, asset_issuer).build())

        transaction.sign(source_keypair)
        response = stellar_server.submit_transaction(transaction)

        return response


    def Mint(self, addr, amt, from_add, memo="MintErc"):
        print("Mint Called")
        # There Shoule be some sort of restriction to the mint function to 
        # restrict it to just the asset issuer
        
        """
        Called when user make deposit from ethereum to the dummy address 
        and a transfer event is emitted, this medthod doesnt check for trustline or
        if acct has been created and token can only be mintted to our distributor acct.

        addr: Stellar Compatiable address
        amt: amount emitted from the erc20 contract event
        memo: user memo if Available 
        asset_code: code of the asset to mint
        asset_issuer: Issuer of the asset to mint
        """
        fees = self.stellar_server.fetch_base_fee()
        src_acct = self.stellar_server.load_account(asset_issuer)
        transaction_obj = TransactionBuilder(
            source_account=src_acct,
            network_passphrase=general_network_passphrase,
            base_fee=fees
            ).append_payment_op(
                addr, str(amt), self.asset_code, self.asset_issuer
            ).add_text_memo(str(memo)
            ).build()

        transaction_obj.sign(asset_issuer_private_key)
        submit_tx = self.stellar_server.submit_transaction(transaction_obj)
        print("Mint done............")
   
        return submit_tx
        


    def Burn(self, eth_addr, amt, acctPkey=distributor_secretKey, memo="XLMBurn"):
        """
        This is called when users want to deposit to an eth addrees, token are send back to the 
        asset issuer address, this process takes it out of the total supply

        eth_addr: the eth address, this does nothing here
        amt: the exact amt that will be credited to the user eth address
        memo: other text to attach to burn, this is not added to the erc deposit
        acctPkey: the sender private key(Not a good approach)
        """
        print("Burning Token on Stellar ##########################")
        distributor = Keypair.from_secret(acctPkey)
        fees = self.stellar_server.fetch_base_fee()
        src_acct = self.stellar_server.load_account(distributor.public_key)
        transaction_obj = TransactionBuilder(
            source_account=src_acct,
            network_passphrase=general_network_passphrase,
            base_fee=fees
            ).append_payment_op(
                self.asset_issuer, str(amt), self.asset_code, self.asset_issuer
            ).append_manage_data_op(data_name=eth_addr, data_value=eth_addr
            ).add_text_memo(memo
            ).build()

        transaction_obj.sign(distributor.secret)

        submit_tx = self.stellar_server.submit_transaction(transaction_obj)
        

        return submit_tx

    def transfer(self,sender_Pkey=asset_issuer_private_key, reciever_addr=distributor_PubKey, amt=1, memo=''):
        """
        Transfer will be an operation btw two stellar account, 
        account A transfer to account B all on stellar. The default 
        parameter send from the asset issuer to the distribution acct, this can be alter by changing the default 
        parameters
        """
        sender = Keypair.from_secret(sender_Pkey)
        fees = self.stellar_server.fetch_base_fee()
        src_acct = self.stellar_server.load_account(sender.public_key)
        transaction_obj = TransactionBuilder(
            source_account=src_acct,
            network_passphrase=general_network_passphrase,
            base_fee=fees
            ).append_payment_op(
                reciever_addr, str(amt), self.asset_code, self.asset_issuer
            ).add_text_memo(str(memo)
            ).build()

        transaction_obj.sign(sender.secret)
        submit_tx = self.stellar_server.submit_transaction(transaction_obj)
        

        return submit_tx

    @staticmethod
    def clear_user_data(data):
        d_data = None
        try:
            d_data = data.decode("utf-8")
        except AttributeError:
            d_data = data


        """
        We need to clear the deposit erc20 address from the distributor's acct
        This only works because we control the distributor acct
        """
        sender = Keypair.from_secret(distributor_secretKey)
        fees = stellar_server.fetch_base_fee()
        src_acct = stellar_server.load_account(sender.public_key)
        transaction_obj = TransactionBuilder(
            source_account=src_acct,
            network_passphrase=general_network_passphrase,
            base_fee=fees
            ).append_manage_data_op(data_name=d_data, data_value=None
            ).build()

        transaction_obj.sign(sender.secret)
        submit_tx = stellar_server.submit_transaction(transaction_obj)
        

        return submit_tx
    @staticmethod
    def Create_Asset(asset_issuer, asset_code):
        asset = Asset(asset_code, asset_issuer)
        print(asset.code)
        print(asset.issuer)
        return asset.code, asset.issuer
        





# print(StellarContract.Create_Asset(asset_issuer=asset_issuer, asset_code=asset_code))
# print(StellarContract.trust_asset(distributor_secretKey))
# print(StellarContract().Mint(distributor_PubKey, 100, None, memo="Trustline"))




# ad = StellarContract().transfer(memo="Fee745c1EBe0095987F9Df8d5f2e7deCfb2f9A77")

# print(ad)

# import secrets
# from eth_account import Account



# add = secrets.token_hex(20)

# add3 = "0x"+add
# bewAdd = web3_instance.toChecksumAddress(add3)
