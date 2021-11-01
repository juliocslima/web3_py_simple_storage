import json
from solcx import compile_standard, install_solc
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    # print(simple_storage_file)

install_solc("0.6.0")

# Solidity source code
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# for connecting to Rinkeby
w3 = Web3(Web3.HTTPProvider(os.getenv("ENDPOINT_RINKEBY_INFURA")))
chain_id = 4
address = "0x59B331CCCC3d65eCD1187F9309F95bE7aC14A5A6"
private_key = os.getenv("PRIVATE_KEY_RINKEBY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction
nonce = w3.eth.getTransactionCount(address)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
# Submit the transaction that deploys the contract
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": address, "nonce": nonce}
)

# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying contract!")

# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Working with the contract, you always need
# Contract ABI
# Contract Address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call --> Simulate making a call and getting a return value
# Transact --> Actually make a state change

# Initial value of favorite number
print("Interact with the contract functions ...")
print(simple_storage.functions.retrieve().call())
print(simple_storage.functions.store(15).call())

print("Updating contract ...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": address, "nonce": nonce + 1}
)

signed_store_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

send_store_transaction = w3.eth.send_raw_transaction(
    signed_store_transaction.rawTransaction
)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_transaction)
print("Updated!")
print(tx_receipt)
