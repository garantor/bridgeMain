
from os import wait
import time
import json
import sys

import unittest
from unittest.case import TestCase
import requests

from variables import  (contract_address, contract_instance, stellar_server, distributor_PubKey,
                                asset_issuer, asset_code, web3_instance, test_url, main_address)
import requests

class ContractGTest(unittest.TestCase):
    amount = 100
    memo = "9383764836737"
    test_key = "5bc123b019d30975ab544555f2696db5d668dc1e86930cc64d08b84ee0614ee5" #DO NOT DO THIS

    # def setUp(self) -> None:
    #     print("worked")
    #     return super().setUp()

    def test_001_check_connection(self):
        connection = web3_instance.isConnected()
        self.assertEqual(connection, True)
        print("check_connection Passed")

    def test_002_transfer(self):
        """
        method to call transfer/mint from the stellar contract, 
        this will mint new token and send to distributor acct or transfer token btw two acct
        """
        data = {
            "amt":self.amount,
            "addr": asset_issuer,
            "type":"transfer",
            "memo": str(self.memo)
        }
        url = test_url + "deposit"
        resp = requests.post(url=url, data=data)
        hash = resp.text.split('"')
   

        chk_trx = stellar_server.payments().for_transaction(hash[1]).call()
        chk_trx_obj = chk_trx["_embedded"]["records"][0]
    

        self.assertTrue(resp.status_code == 200)
        self.assertEqual(chk_trx_obj['transaction_successful'], True)
        self.assertTrue(chk_trx_obj["asset_code"] == asset_code)
        self.assertTrue(chk_trx_obj["asset_issuer"] == asset_issuer)
        self.assertEqual(float(chk_trx_obj['amount']), float(self.amount))
        self.assertEqual(chk_trx_obj['from'], asset_issuer)
        self.assertEqual(chk_trx_obj['to'], asset_issuer)
        print("Transfer Passed")


    def test_003_stellar_cross(self):
        """
        test methodd to burn amt of token on stellar and mint amount on ethereum and also send the amount 
        to the specify address(address from the payload)

        """
        url = test_url + "fromStellarToEther"
        addr = "0xbCD18E8a0bD51c8F4c6E3b5b258D7e43fB4359CC"
        data = {
            "amt": self.amount,
            "eth_add": addr,
            "memo": "User Unique Memo"
        }
        resp = requests.post(url=url, data=data)
        hash = resp.text.split('"')


        wait_tx_complete = web3_instance.eth.wait_for_transaction_receipt(hash[1])
        eventResp = contract_instance.events.Transfer().processReceipt(wait_tx_complete)
        adc =web3_instance.toJSON(eventResp)
        transferEvent  = json.loads(adc)
  
        self.assertTrue(transferEvent[0]['args']['_from'] == "0x0000000000000000000000000000000000000000")
        self.assertTrue(transferEvent[0]['args']['_to'] == addr)
        self.assertTrue(transferEvent[0]['args']['_value'] == web3_instance.toWei(self.amount, "ether"))
        # self.assertTrue(transferEvent[0]['transactionHash'] == hash[1])
        print("stellar_cross passed")


    def test_004_etherCross(self):
        """
        Test method to burn token on ethereum and issue the same amt on 
        stellar sending it to the distributor acct with the memo as a unique identify
        """
        acct = web3_instance.eth.account.from_key(self.test_key)
        amtMain = web3_instance.toWei(self.amount, "ether")
       
        eth_add = "0x10000000000000AfCd3a25B558562dA165cd1607"
        addr = web3_instance.toChecksumAddress(eth_add)
        transaction = contract_instance.functions.transfer(
            addr,
            amtMain,
        ).buildTransaction({
            'chainId':97,
            'gas':700000,
            'gasPrice': web3_instance.eth.gas_price,
            "nonce": web3_instance.eth.get_transaction_count(acct.address),

        })
        signed_tx = web3_instance.eth.account.sign_transaction(transaction, self.test_key)
        submit_tx = web3_instance.eth.send_raw_transaction(signed_tx.rawTransaction)
        hash = web3_instance.toHex(submit_tx)
        
        wait_tx_complete = web3_instance.eth.wait_for_transaction_receipt(hash)
        eventResp = contract_instance.events.Transfer().processReceipt(wait_tx_complete)

        adc =web3_instance.toJSON(eventResp)
        transferEvent  = json.loads(adc)
        print(transferEvent[0]['args'])
        self.assertTrue(transferEvent[0]['args']['_from'] == acct.address)
        self.assertTrue(transferEvent[0]['args']['_to'] == eth_add)
        self.assertTrue(transferEvent[0]['args']['_value'] ==  web3_instance.toWei(self.amount, "ether"))
        print("EtherCross Passed")
        


if __name__ =="__main__":
    unittest.main()

# wait_tx_complete = web3_instance.eth.wait_for_transaction_receipt("0xcfab3e8157b6eba0f746232bd84a614bee6d52eec24991ef96cd1ba0a19c4985")
# eventResp = contract_instance.events.Transfer().processReceipt(wait_tx_complete)
# # wait_tx_complete = web3_instance.eth.wait_for_transaction_receipt(hash[1])
# adc =web3_instance.toJSON(eventResp)

# transferEvent  = json.loads(adc)
# print(transferEvent)
# print(transferEvent['from'])
# print(transferEvent['to'])
# print(transferEvent['transactionHash'])