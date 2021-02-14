from flask import Flask, jsonify, request
import json

class User :
    def login(self):
        req = request.get_json(force=True)
        username = req.get('username', None)
        password = req.get('password', None)
        data = {
            'username': username,
            'password': password
        }
        return jsonify(data)
    
    def new_vehicle(self):
        # req = request.get_json(force=True)
        cplc = request.form['cplc']
        vehicle_number = request.form['vehicle_number']
        data = {
            'cplc': cplc,
            'vehicle_number': vehicle_number
        }
        return jsonify(data)

    def all_vehicles(self):
        req = request.get_json(force=True)
        cplc = req.get('cplc', None)
        vehicle_number = req.get('vehicle_number', None)
        data = {
            'cplc': cplc,
            'vehicle_number': vehicle_number
        }
        return jsonify(data)