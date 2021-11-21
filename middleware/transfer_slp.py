from datetime import datetime, timedelta
from eth_account.messages import encode_defunct
from web3 import Web3
import json
import requests

with open('slp_abi.json') as f:
    slp_abi = json.load(f)
infura_url = "https://mainnet.infura.io/v3/0d0eda78b12241ad919e2efb7e1e7c64"

web3 = Web3(Web3.HTTPProvider(infura_url))


def transfer_slp(address, private_key, to_address, amount):
    checksum_address = Web3.toChecksumAddress(to_address)
    slp_contract = web3.eth.contract(address=checksum_address, abi=slp_abi)
    nounce = web3.eth.getTransactionCount(Web3.toChecksumAddress(to_address))

    transfer_txn = slp_contract.functions.transfer(
        checksum_address, int(amount)).buildTransaction({
            'chainId': 2020,
            'gas': 100000,
            'gasPrice': web3.toWei('0', 'gwei'),
            'nonce': nounce,
        })

    signed_txn = web3.eth.account.sign_transaction(
        transfer_txn, private_key=bytearray.fromhex(private_key.replace("0x", "")))
    web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Returns transaction hash.
    return web3.toHex(web3.keccak(signed_txn.rawTransaction))
