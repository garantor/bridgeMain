import unittest, secrets
from eth_utils import address
from flask import Flask, abort
from flask import json
from flask.helpers import make_response
from flask.json import jsonify
from flask_restful import Api, Resource, reqparse
from Ether.EtherBridge import EtherMain

from variables import web3_instance, general_network_passphrase, asset_issuer
from Stellar.StellarBridge import StellarContract
from stellar_sdk.transaction_envelope import TransactionEnvelope


app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()


class StellarEndpoint(Resource):
    # This will call the stellar burn function, 
    # this will emit an event which will send instruction on how to mint on ethereum
    def post(self):
        parser.add_argument("amt", required=True, help="Amount to withdraw")
        parser.add_argument("eth_add", required=True, help="Ethereum address to credit on ethereum")
        parser.add_argument("memo", required=True, help="user memo")
        
        args = parser.parse_args()
        amt = args['amt']
        eth_addr = args['eth_add']
        memo = args['memo']
        hash = None
        resp = None
        add_check = web3_instance.isAddress(eth_addr)
        if add_check == True:
            try:
                resp = StellarContract().Burn(eth_addr=eth_addr, amt=amt, memo=memo)
            except:
                abort(500, "internal server error")
            else:
                if resp['successful'] == True:
                    stellar_tx_obj= TransactionEnvelope.from_xdr(resp['envelope_xdr'],  general_network_passphrase)
                    try:
                        dest = stellar_tx_obj.transaction.operations[0].destination
                        if dest == asset_issuer:
                            print("Minting Token on Binance/Ethereum. main.py  ...............")
                            xdr = resp['envelope_xdr']
                            adc = EtherMain()
                            hash = adc.mintMain(xdr)
                    except Exception as e:
                        print(e)
                        pass
                    else:
                        return jsonify({
                                "Ethereum_hash": hash,
                                "Stellar_hash": resp['hash']
                            })

        else:
            abort(400, "Invalid Erc20 Address")

class StellarDeposit(Resource):
    #Endpoint to be called during deposit, this can useful when users deposit has 
    # been validated and successful, users bal will be updated using the memo and the amount will be minted or transfer as the case maybe
    # There Shoukd be some sort of check here to make sure only the right/authorized person can call the mint function
    # Like checking for valid transaction from an on_ramp api/endpoint, using stellar sep10, using JWT and so on
    def post(self):
        parser.add_argument("amt", required=True, help="Amount to transfer/mint")
        parser.add_argument("addr", required=True, help="Stellar Address to recieve token")
        parser.add_argument("type", required=True, help="transfer type, mint or transfer")
        parser.add_argument("memo", required=True, help="Transaction Memo")
        args = parser.parse_args()
        addr = args['addr']
        type = args['type']
        amt = args['amt']
        tx_memo = args['memo']
        if type == "transfer":
            resp = StellarContract().transfer(reciever_addr=addr, amt=amt, memo=tx_memo)
            return resp['hash']
    def get(self):
        add = secrets.token_hex(13)
        add3 = "0x"+"10000000000000"+add
        bewAdd = web3_instance.toChecksumAddress(add3)
        addr = web3_instance.isAddress(bewAdd)

        if addr == True:
            return jsonify({
                "address": bewAdd,
                "message": "send deposit to the above address"
            })
        else:
            return "Try again"


# api.add_resource(EtherEnpoints, "/etherCross")
api.add_resource(StellarEndpoint, "/fromStellarToEther")
api.add_resource(StellarDeposit, "/deposit")



if __name__ == "__main__":
    app.run(debug=True)