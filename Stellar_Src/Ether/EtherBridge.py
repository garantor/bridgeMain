
import json
from stellar_sdk.transaction_envelope import TransactionEnvelope
# from .Stellar.StellarBridge import StellarContract
from Stellar.StellarBridge import StellarContract
from variables import (general_network_passphrase, contract_instance, contract_address,
                            web3_instance, main_address, main_address_privateKey,
                            distributor_PubKey)
# 1. Events are send here from the stella events to process mint on ethereum 
# a. Recieve transaction_xdr
# b. decode, check if add is valid and call the mint function of ether


import threading

class EtherMain:
    
    def __init__(self) -> None:
        self.nounce = web3_instance.eth.get_transaction_count(main_address)


    def processMint(self, stellar_xdr):
        print("Processmint")
        """
        After a burn event is emitted on stellar, 
        the events handler forward the transaction xdr to this method.

        stellar_xdr: envelop_xdr from stellar transaction
        """
        stellar_tx_obj= TransactionEnvelope.from_xdr(stellar_xdr, general_network_passphrase)
    

        erc_20_addres = stellar_tx_obj.transaction.operations[1].data_value
        amount = stellar_tx_obj.transaction.operations[0].amount
        self.memo_data_name = stellar_tx_obj.transaction.operations[1].data_name

        self.mintMain(erc_20_addres, amt=amount)
       
            

    
    def mintMain(self, stellar_xdr):
        print("Mint called")
        print()
        """
        There can be changes here to make sure only the asset issue acct can mint token
        stellar_xdr: transaction envelop xdr
        """
        stellar_tx_obj= TransactionEnvelope.from_xdr(stellar_xdr, general_network_passphrase)
        erc_20_addres = stellar_tx_obj.transaction.operations[1].data_value
        amount = stellar_tx_obj.transaction.operations[0].amount
        self.memo_data_name = stellar_tx_obj.transaction.operations[1].data_name
        amt2 = web3_instance.toWei(amount, "ether")
        addr = erc_20_addres.decode("utf-8")
      
        
        transaction = contract_instance.functions.mint(
            addr,
            int(amt2)
        ).buildTransaction({
            'chainId':97,
            'gas':700000,
            'gasPrice': web3_instance.eth.gas_price,
            "nonce": web3_instance.eth.get_transaction_count(main_address),

        })
        signed_tx = web3_instance.eth.account.sign_transaction(transaction, main_address_privateKey)
        submit_tx = web3_instance.eth.send_raw_transaction(signed_tx.rawTransaction)
        hash = web3_instance.toHex(submit_tx)
        
        wait_tx_complete = web3_instance.eth.wait_for_transaction_receipt(hash)
        print("Mint Done.........................")

        adc = threading.Thread(target=StellarContract.clear_user_data, args=(self.memo_data_name,))
        adc.start()

        return hash

    @staticmethod
    def burnMain(amt, signature):
        acc = web3_instance.eth.account.privateKeyToAccount(signature)
        """
        This is the method that removes token from the user acct 
        and from the total supply of the token:

        amt: Amount to be burn
        signature: sender private key
        
        """
        print("Burning Token on Ethere##########################")
        amt2 = web3_instance.toWei(amt, "ether")
        
        transaction = contract_instance.functions.burn(
            int(amt2)
        ).buildTransaction({
            'chainId':97,
            'gas':700000,
            'gasPrice': web3_instance.eth.gas_price,
            "nonce":web3_instance.eth.get_transaction_count(acc.address),

        })
        signed_tx = web3_instance.eth.account.sign_transaction(transaction, signature)
        submit_tx = web3_instance.eth.send_raw_transaction(signed_tx.rawTransaction)
        hash = web3_instance.toHex(submit_tx)
        
        wait_tx_complete = web3_instance.eth.wait_for_transaction_receipt(hash)
        # transferEvent = contract_instance.events.Transfer().processReceipt(wait_tx_complete)

        return wait_tx_complete


    @staticmethod
    def handle_event(hash):
        wait_tx_complete = web3_instance.eth.wait_for_transaction_receipt(hash)
        eventResp = contract_instance.events.Transfer().processReceipt(wait_tx_complete)
        adc = web3_instance.toJSON(eventResp)
        transferEvent  = json.loads(adc)
        
        _contract_add = transferEvent[0]['address']
        
        
        burner_add = transferEvent[0]['args']['to'] #just to be sure the token is been burn on ethereum
        value = transferEvent[0]['args']['value']
        burn_value = web3_instance.fromWei(value, 'ether')
        _from_add = transferEvent[0]['args']['from']

        if burner_add == "0x0000000000000000000000000000000000000000" and _contract_add == contract_address :
            print("Minting Tokens on Stellar.......................")
            adc = StellarContract()
            adc.Mint(distributor_PubKey, burn_value, from_add=_from_add)
        else:
            pass