from flask import Flask, jsonify, request
import json

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return filename


class User:
    def login(self):
        req = request.get_json(force=True)
        username = req.get('username', None)
        password = req.get('password', None)
        data = {'username': username, 'password': password}
        return jsonify(data)

    # def new_vehicle(self):
    #     if request.method == 'POST':
    #         userDetails = request.form
    #         user_id = userDetails['user_id']
    #         user_name = userDetails['user_name']
    #         vehicle_image = request.files['vehicle_image']
    #         message = userDetails['message']

    #         formattedImage = convertToBinaryData(vehicle_image)
    #         cur = db.connection.cursor()
    #         cur.execute(
    #             "INSERT INTO input_vehicle(user_id, user_name, message) VALUES(%s, %s, %s)",
    #             (user_id, user_name, message))
    #         connection.commit()
    #         cur.close()
    #         print(formattedImage)
    #         return {'success': 'success'}, 200
    #     else:
    #         return 'Error while adding new vehicle!', 404

    def all_vehicles(self):
        req = request.get_json(force=True)
        cplc = req.get('cplc', None)
        vehicle_number = req.get('vehicle_number', None)
        data = {'cplc': cplc, 'vehicle_number': vehicle_number}
        return jsonify(data)