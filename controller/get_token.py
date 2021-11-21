from flask import request, jsonify, abort
from flask_restful import Resource
from middleware.token_hendler import *


class get_token(Resource):

    def post(self):
        try:
            address = request.form["address"]
            private_key = request.form["private_key"]
            token = get_jwt_access_token(address, private_key)
            response = jsonify({
                "statusCode": "200",
                "accessToken": token
            })
            return response
        except:
            response = jsonify({
                "statusCode": 500,
                "statusMessage": "Wrong token, please try again.",
            })
            response.status_code = 500
            return response
