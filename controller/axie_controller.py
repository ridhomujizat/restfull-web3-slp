from flask import request, jsonify, abort
from flask_restful import Resource
from middleware.axie import *


class get_claimed(Resource):
    def post(self):
        address = request.form["address"]
        total_claimed = get_claimed_slp(address)
        response = jsonify({
            "statusCode": "200",
            "total_claimed": total_claimed
        })
        return response


class get_unclaimed(Resource):
    def post(self):
        address = request.form["address"]
        print(address)
        total_unclaimed = get_unclaimed_slp(address)
        print(total_unclaimed)
        response = jsonify({
            "statusCode": "200",
            "data": [
                {
                    "currecy": "SLP",
                    "amount":  total_unclaimed,
                    "status": "unclaimed"
                }
            ]
        })
        return response


class claim_slp(Resource):
    def post(self):
        address = request.form["address"]
        private_key = request.form["private_key"]
        respon = execute_slp_claim(address, private_key)
        # if(token):

        return respon

class trasferslp(Resource):
    def post(self):
        address = request.form["address"]
        private_key = request.form["private_key"]
        amount = request.form["amount"]
        respon = transfer_slp(address, private_key, amount)
        return respon