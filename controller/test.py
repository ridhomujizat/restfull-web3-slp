from flask import request
from flask_restful import Resource

class Contoh(Resource):
    def get(self):
        response = {"msg": "testing"}
        return response

    def post(self): 
        initial = {}
        nama = request.form["nama"]
        umur = request.form["umur"]
        initial["nama"] = nama
        initial["umur"] = umur
        response = initial
        return response
