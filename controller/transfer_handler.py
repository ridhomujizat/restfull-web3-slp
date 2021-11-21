from flask import request, jsonify, abort
from flask_restful import Resource
from middleware.transfer_slp import *


class trasferslp(Resource):
    def post(self):
        address = request.form["address"]
        private_key = request.form["private_key"]
        to_address = request.form["to_address"]
        amount = request.form["amount"]
        hex_transfer = transfer_slp(address, private_key, to_address, amount)
        return hex_transfer
        # try:
        #     address = request.form["address"]
        #     total_claimed = get_claimed_slp(address)
        #     response = jsonify({
        #         "statusCode": "200",
        #         "total_claimed": total_claimed
        #     })
        #     return response
        # except:
        #     response = jsonify({
        #         "statusCode": 500,
        #         "statusMessage": "Invalide address, please try again.",
        #     })
        #     response.status_code = 500
        #     return response
