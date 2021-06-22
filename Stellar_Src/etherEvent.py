
import json
import asyncio
from variables import contract_instance, web3_instance, distributor_PubKey

from Stellar.StellarBridge import StellarContract
# from attributedict.collections import AttributeDict
# from hexbytes import HexBytes





def handle_event(event):
    event_obj = event
    print(event_obj)
    burner_add = event_obj['args']['_to'] #just to be sure the token is been burn on ethereum
    value = event_obj['args']['_value']
    burn_value = web3_instance.fromWei(value, 'ether')

    burner_add = event_obj['args']['_to'].split('10000000000000')
    try:
        check_add = burner_add[1]
    except Exception as e:
        print(e)
        pass

    else:
        print("Minting Tokens on Stellar.......................")
        adc = StellarContract()
        adc.Mint(distributor_PubKey, burn_value, from_add=event_obj['args']['_from'], memo=check_add)
        
 
async def log_loop(event_filter, poll_interval):
    while True:
        for transfer in event_filter.get_new_entries():
            handle_event(transfer)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "transfer" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def ethereum_events():
    event_filter = contract_instance.events.Transfer.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()

def main():
    ethereum_events()


if __name__ == "__main__":
    main()