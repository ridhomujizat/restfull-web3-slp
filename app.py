from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from controller.get_token import *
from controller.slp_hendler import *
from controller.transfer_handler import *

app = Flask(__name__)

api = Api(app)

CORS(app)

api.add_resource(get_token, "/api", methods=["POST"])
api.add_resource(get_claimed, "/get-claimed", methods=["POST"])
api.add_resource(get_unclaimed, "/get-unclaimed", methods=["POST"])
api.add_resource(trasferslp, "/transfer-slp", methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)
