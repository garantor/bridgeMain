# BRIDGE FOR STELLAR AND EVM COMPATIBLE BLOCKCHAIN


A Bridge between Stellar and EVM compatible blockchain, like Ethereum, Binance smart chain etc, This src has been tested on Binance(Stellar - Binance). The bridge uses Stellar as the base blockchain. This Use the approach where users can only withdraw and deposit fiat directly from the asset issuer app/website,  A general overview of the approach used;

To Make this contract work we have an event listener that watches for transactions on a smart contract on Binance smart chain

## KEY TERMS;

* **Asset Issuer**: The Account that issuer the Token/coin on Stellar blockchain
* **Distributor Account** This is the account that holds all the user funds on stellar
* **IssuerID** : Any valid 14 length Hex (This Length can be modified)
* **User Memo** : Any valid 26 length Hex (This Length can be modified)
* **Erc20 burn Address** : 0x + IssuerID + User Memo (This Will Have No private Key)

# From Stellar To Binance Smart Chain

<!-- User has been verified to have the amount they intend to transfer -->

1. User call An endpoint with the following payload;

        * Amount: The exact amount to be transferred via a cross-chain,
        * Address: Bep20 address to send a token to,
        * memo: User Unique memo, this is used to update user balance on the issuer DB



2. Asset Issuer append two operations in a single transaction and send to stellar;

        * The First operation will be a burn payment operation that sends the specified amount to the issuer address;
        * The Second operation will be a manage data operation that appends the erc20 address as both the data name and the data value (Memo don't accept this length), This is mainly to tell the issuer account the address that owes the token(Instruction are used when minting on Binance)

3. Once the above operation is Successful, we Parse data from the stellar xdr call the solidity contract mint function using web3.py, this will mint the amount specified and send it to the address specified in the manage data operation from stellar.


4. Send A clear data transaction back to stellar, this is a single operation that appends a manage data operation to a transaction, the operation will have no data value and the data name is the same as the erc20 address(This was added earlier), this will delete data added to the distributor account

5. Once Transaction is successful, Endpoint returns both transaction hash for stellar and Binance chain transaction (update user balance). Transaction is Done 

# From Bianace Smart Chain To Stellar

1. A user show intent to deposit via the asset issuer app/web.
2. A **burn address** with no-private key address is sent back as the deposit address (A deposit address for the burn/cross chain on Binance to stellar contain both 0x + IssuerID + User Memo)

3. User transfer funds to this account

4. The Event listener parse the response, if it contains the **IssuerID** we call Stellar mint function passing memo to the transaction and send the amount to the distributor account with the memo added to the transaction(This tell the distributor account who owns the transaction).

5. Update User details on the issuer DB:




This git repo contains the test code I ran to test the concept out and it works just fine. This is a truffle project with web3.py and flask

To use this repo you need to 
* `install node js`
* `install truffle` 
* `pip install -r requirements.txt`

You also need to create a couple of files for keeping your secret keys,
* Inside **Sol_src** you need to Create a **.secrets** file this will contain secrets key for the Binance smart chain(This is the Secret Key of address that Deploys the contract to Binance Smart Chain).

* Inside **Stellar_Src** You need to create a dirctory **pKeys** with three files **.asset_key**, **.distributor_key**, **.secrets**. The asset issuer key, distributor key and secret key for binance smart chain respectively.


* Once Done, need to cd to the Sol_src directory and run ``truffle compile`` if everything is set up correctly you should have a build folder in your sol_src directory, then `truffle migrate --reset --network testnet` to deploy a new contract to the blockchain with the Token name **TELLER** and Token symbol as **TLR** and **18** decimals.

* Running your main.py will create a new token with **TLR** as the token name, **Create trustline** for Your distributor account and send a **payment operation of 100 TLR** with memo as *Trustline*. Uncomment the last three lines of code in your Stellar_src/Stellar/SteelarBridge.py to avoid this action every time the app reloads or every time you run main.py

* Once This is done You just need to run the main.py and etherEvent.py in two separate terminals and You can test the code out. The code was Tested with PostMan and it works just fine.

*ENJOY*



#### NOTE THIS CODE IS MAINLY FOR TESTING and EDUCATIONAL PURPOSE, PLEASE DONT USE FOR PRODUCTION WITHOUT PROPER AUDITING, REFACTORING OF THE CODE, TOKEN ISSUE ON BINANCE SMART CHAIN ARE NOT TAKING OUT THE TOTAL SUPPLY, THEY ARE ONLY SEND TO AN ADDRESS UNACCESSIBLE TO ANYONE.

