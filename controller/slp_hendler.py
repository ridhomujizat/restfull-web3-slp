from flask import request, jsonify, abort
from flask_restful import Resource
from middleware.slp_hendler import *


class get_claimed(Resource):
    def post(self):
        # try:
        address = request.form["address"]
        total_claimed = get_claimed_slp(address)
        response = jsonify({
            "statusCode": "200",
            "total_claimed": total_claimed
        })
        return response
        # except:
        #     response = jsonify({
        #         "statusCode": 500,
        #         "statusMessage": "Invalide address, please try again.",
        #     })
        #     response.status_code = 500
        #     return response


class get_unclaimed(Resource):
    def post(self):
        address = request.form["address"]
        total_unclaimed = get_unclaimed_slp(address)
        response = jsonify({
            "statusCode": "200",
            "total_unclaimed": total_unclaimed
        })
        return response
