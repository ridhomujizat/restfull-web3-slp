from datetime import datetime, timedelta
from eth_account.messages import encode_defunct
from web3 import Web3
import json
import requests

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
}


with open('slp_abi.json') as f:
    slp_abi = json.load(f)

with open('axie_abi.json') as x:
    axie_abi = json.load(x)

AXIE_CONTRACT = "0x32950db2a7164ae833121501c797d79e7b79d74c"
AXS_CONTRACT = "0x97a9107c1793bc407d6f527b77e7fff4d812bece"
SLP_CONTRACT = "0xa8754b9fa15fc18bb59458815510e40a12cd2014"
WETH_CONTRACT = "0xc99a6a985ed2cac1ef41640596c5a5f9f4e19ef5"
RONIN_PROVIDER_FREE = "https://proxy.roninchain.com/free-gas-rpc"
RONIN_PROVIDER = "https://api.roninchain.com/rpc"
SKY_MAVIS = "https://ronin-testnet.skymavis.com/rpc"
infura_url = "https://mainnet.infura.io/v3/0d0eda78b12241ad919e2efb7e1e7c64"

web3 = Web3(Web3.HTTPProvider(infura_url))
web3_2 = Web3(Web3.HTTPProvider(RONIN_PROVIDER_FREE))

slp_contract = web3.eth.contract(
    address=Web3.toChecksumAddress(SLP_CONTRACT), abi=slp_abi)
slp_contract_2 = web3_2.eth.contract(
    address=Web3.toChecksumAddress(SLP_CONTRACT), abi=slp_abi)


def get_claimed_slp(address):
    address_parse = Web3.toChecksumAddress(address)
    return int(slp_contract_2.functions.balanceOf(address_parse).call())


def get_unclaimed_slp(address):
    response = requests.get(
        f"https://game-api.skymavis.com/game-api/clients/{address}/items/1", headers=headers, data="")
    if (response.status_code != 200):
        print(response.text)
    assert(response.status_code == 200)
    result = response.json()

    total = int(result["total"])
    return total


def execute_slp_claim(address, private_key):
    access_token = get_jwt_access_token(address, private_key)
    # return access_token
    custom_headers = headers.copy()
    custom_headers["authorization"] = f"Bearer {access_token}"
    response = requests.post(
        f"https://game-api.skymavis.com/game-api/clients/{address}/items/1/claim", headers=custom_headers, json="")
    if (response.status_code != 200):
        print(response.text)
    assert(response.status_code == 200)

    address_parse = Web3.toChecksumAddress(address)
    signature = response.json()["blockchain_related"]["signature"]
    nonce = web3.eth.getTransactionCount(address_parse)

    claim_txn = slp_contract.functions.checkpoint(
        address_parse,
        signature['amount'],
        signature['timestamp'],
        signature['signature'].replace("0x", "")
    ).buildTransaction({'gas': 100000, 'gasPrice': 0, 'nonce': nonce})

    signed_txn = web3.eth.account.sign_transaction(
        claim_txn,
        private_key=bytearray.fromhex(private_key.replace("0x", ""))
    )

    web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Returns transaction hash.
    return web3.toHex(web3.keccak(signed_txn.rawTransaction))


def transfer_slp(address, private_key, amount):
    address_parse = Web3.toChecksumAddress(address)
    nonce = web3.eth.getTransactionCount(address_parse)

    transfer_txn = slp_contract.functions.transfer(
        address_parse,
        int(amount)).buildTransaction({
            'chainId': 2020,
            'gas': 100000,
            'gasPrice': web3.toWei('0', 'gwei'),
            'nonce': nonce,
        })

    signed_txn = web3.eth.account.sign_transaction(
        transfer_txn,
        private_key=bytearray.fromhex(private_key.replace("0x", "")))

    web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    # Returns transaction hash.
    return web3.toHex(web3.keccak(signed_txn.rawTransaction))

# =========== Generet Token ============


def sign_message(message, private_key):
    message_encoded = encode_defunct(text=message)
    message_signed = Web3().eth.account.sign_message(
        message_encoded, private_key=private_key)

    return message_signed['signature'].hex()


def get_jwt_access_token(address, private_key):
    random_message = create_random_message()
    random_message_signed = sign_message(random_message, private_key)

    payload = {
        "operationName": "CreateAccessTokenWithSignature",
        "variables": {
            "input": {
                "mainnet": "ronin",
                "owner": address,
                "message": random_message,
                "signature": random_message_signed
            }
        },
        "query": "mutation CreateAccessTokenWithSignature($input: SignatureInput!) {    createAccessTokenWithSignature(input: $input) {      newAccount      result      accessToken      __typename    }  }  "
    }

    # return payload
    response = requests.post(
        "https://axieinfinity.com/graphql-server-v2/graphql", headers=headers, json=payload)

    if (response.status_code != 200):
        print(response.text)
        return False
    assert(response.status_code == 200)
    return response.json()['data']['createAccessTokenWithSignature']['accessToken']


def create_random_message():
    payload = {
        "operationName": "CreateRandomMessage",
        "variables": {},
        "query": "mutation CreateRandomMessage {    createRandomMessage  }  "
    }

    response = requests.post(
        "https://axieinfinity.com/graphql-server-v2/graphql", headers=headers, json=payload)
    if (response.status_code != 200):
        print(response.text)
    assert(response.status_code == 200)
    return response.json()["data"]["createRandomMessage"]
