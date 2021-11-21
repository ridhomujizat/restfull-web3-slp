from datetime import datetime, timedelta
from eth_account.messages import encode_defunct
from web3 import Web3
import json, requests

# web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:5005/api'))


headers = {
  "Content-Type": "application/json",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36" }


# return token jwt

def sign_message(message, private_key):
    message_encoded = encode_defunct(text = message)
    message_signed =  Web3().eth.account.sign_message(message_encoded, private_key = private_key)

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
  response = requests.post("https://axieinfinity.com/graphql-server-v2/graphql", headers=headers, json=payload)

  if (response.status_code != 200):
    print(response.text)
  assert(response.status_code == 200)
  return response.json()['data']['createAccessTokenWithSignature']['accessToken']


def create_random_message():
  payload = {
        "operationName": "CreateRandomMessage",
        "variables": {},
        "query": "mutation CreateRandomMessage {    createRandomMessage  }  "
    }

  response = requests.post("https://axieinfinity.com/graphql-server-v2/graphql", headers=headers, json=payload)
  if (response.status_code != 200):
    print(response.text)
  assert(response.status_code == 200)
  return response.json()["data"]["createRandomMessage"]