# BRIDGE FOR STELLAR AND EVM COMPATIBLE BLOCKCHAIN


A Bridge between Stellar and Evm compatiable blockchain, like ethereum, binance smart chain etc, This src has been tested on binance(Stellar - Bianace). The brideg uses Stellar as the base blockchain. This Use the approach where users can only withdraw and deposit fiat directly from the asset issuer app/website,  A general overview of the approach used;

To Make this contract work we have an event listner that watch for transaction on smart contract on binance smart chain

## KEY TERMS 

* **Asset Issuer**: The Account that issuer the Token/coin on stellar blockchain
* **Distributor Account** This is the account that hold all the user fund on stellar
* **IssuerID** : Any valid 14 length Hex (This Length  an be modify)
* **User Memo** : Any valid 26 length Hex (This Length  an be modify)
* **Erc20 burn Address** : 0x + IssuerID + User Memo 

# From Stellar To Binance Smart Chain

<!-- User has been verified to have the amount they intend to transfer -->

1. User call An enpoint with the following payload
        amount: The exact amount to be transfer via cross chain,
        address: Bep20 address to send token to,
        memo: User Unique memo, this is used to update user balance on the issuer db



2. Asset Issuer append two operation in a single transction and send to stellar;
        a. First operation will be a burn payment operation that send the specified amount to the issuer address;
        b. second operation will be a manage data operation that append the erc20 address as both the data name and the data value (Memo don't accept this length)

3. Once the above operation is Successful, we Parse data from the stellar xdr  call the solidity contract mint function using web3.py, this will mint the amount specified and send it to the address specified in the request payload.


4. Send A clear data transaction back to stellar, this is a single operation that append a manage data operation to a transaction, the operation will have no data value, this delete the data added to the distributor account

5. Endpoint return both transaction hash for stellar and binance chain transaction (update user balance) 

# From Bianace Smart Chain To Stellar

1. A user show intent to deposit via the asset issuer app/web.
2. A burn address with no-private key address is sent back as the deposit address (A deposit address for the burn/cross chain on Binance contain both the IssuerID and User Memo)

3. User transfer funds to this account

4. The Event listner parse the response, if it contain the issuerID we call stellar mint function passing memo to the transaction and send the amount to the distributor account.

5. Update User details on the issuer db:




This git repo contain the test code i ran to test the concept out and it works just fine. This is a truffle projects with web3.py and flask

To use this repo you need to 
* `install node js`
* `install truffle` 
* `pip install -r requirements.txt`

You also need to Create a couple of files for keeping your secret keys,
* Inside Sol_src you need to Create a **.secrets** file this will contain secrets key for bianace smart chain.

* Inside Stellar_Src You need to create a dirctory **pKeys** with three files **.asset_key**, **.distributor_key**, **.secrets**. The asset issuer key, distributor key and secret key for binance smart chain.


* Once Done, need to cd to the Sol_src directory and run ``truffle compile`` if eventhing is setup correctly you should have a build folder in you sol_src directory, then `truffle migrate --reset --network testnet` to deploy a new contract to the blockchain with the Token name **TELLER** and Token symbol as **TLR**

* Runing your main.py will create a new token with **TLR** as the token name, create trustline for Your distributor account and send a payment operation of 100 with memo *Trustline*. Uncomment the last three line of code in your Stellar_src/Stellar/SteelarBridge.py to avoid this action everytime the app reloads or every time you run main.py

* Once This is done You just need to run the main.py and etherEvent.py in two seperate terminal.



#### NOTE THIS CODE IS MAINLY FOR TESTING, PLEASE DONT USE FOR PRODUCTION WITHOUT PROPER AUDITING OG THE CODE, TOKEN ISSUE ON BINANCE SMART CHAIN ARE NOT TAKING OUT THE TOTAL SUPPLY, THEY ARE ONLY SEND TO AN ADDRESS UNACCESSIBLE TO ANYONE.








