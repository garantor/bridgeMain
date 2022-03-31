# from variables import stellar_server, asset_issuer, general_network_passphrase
# from Ether.EtherBridge import EtherMain
# from stellar_sdk.transaction_envelope import TransactionEnvelope



# def stellar_events():
#     server = stellar_server
#     account_id = asset_issuer
#     last_cursor = "now"
#     for tx in server.transactions().for_account(account_id).cursor(last_cursor).stream():
#         if tx['successful'] == True:
#             stellar_tx_obj= TransactionEnvelope.from_xdr(tx['envelope_xdr'],  general_network_passphrase)
#             try:
#                 dest = stellar_tx_obj.transaction.operations[0].destination
#                 if dest == asset_issuer:
#                     print("Minting Token on Binance/Ethereum................")
#                     xdr = tx['envelope_xdr']
#                     adc = EtherMain()
#                     adc.processMint(xdr)
#             except Exception as e:
#                 print(e)
#                 print("Skipped")
#                 pass
            






# if __name__ == "__main__":
#     stellar_events()
