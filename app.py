from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import yaml
from flask_cors import CORS
from models import User
from flask_ngrok import run_with_ngrok
from datetime import datetime
import json
import MySQLdb.cursors
import ast
# import re

app = Flask(__name__)
CORS(app)   
# run_with_ngrok(app)


#Database
db = yaml.load(open('db.yaml', 'r'))
app.config['MYSQL_HOST'] = db["mysql_host"]
app.config['MYSQL_USER'] = db["mysql_user"]
app.config['MYSQL_PASSWORD'] = db["mysql_password"]
app.config['MYSQL_DB'] = db["mysql_db"]

mysqlcon = MySQL(app)
    
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return filename

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/signup/', methods =['POST'])
def signup():
    userDetails = request.form
    if request.method == 'POST' and 'user_name' in userDetails and 'password' in userDetails and 'email' in userDetails and 'role' in userDetails :
        user_name = userDetails['user_name']
        password = userDetails['password']
        email = userDetails['email']
        role = userDetails['role']
        cur = mysqlcon.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM accounts WHERE user_name = %s OR email = %s', (user_name, email,))
        account = cur.fetchone()
        if account:
            return {'error': 'Account already exists!', 'status': '404'},200
        else:
            cur.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (user_name, password, email, role ))
            mysqlcon.connection.commit()
            return {'success': 'Account created successfully!', 'status': '201'},201
    else:
        return {'error': 'Signup error!', 'status': 404 }, 404

@app.route('/login/', methods=["POST"])
def login():    
    a= request.data
    userDetails = ast.literal_eval(a.decode('utf-8'))
    user_name = userDetails['user_name']    
    password = userDetails['password']
    cur = mysqlcon.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cur.execute('SELECT * FROM accounts WHERE user_name = %s AND password = %s', (user_name, password,))
        account = cur.fetchone()
        user_deails = {
            "email": account['email'],
            "id": account['id'],
            "user_name": account['user_name']
        }
        print(user_deails)
        if account:
            return jsonify({'success': 'Logged in successfully!', 'status': '200', 'user': user_deails})
        else:
            return jsonify({'error': 'Login failed!', 'status': '404'})
    except:
        return jsonify({'error': 'Login failed!', 'status': '404'})

@app.route('/new_vehicle/', methods=["POST"])
def new_vehicle():
    if request.method == 'POST':
        userDetails = request.form
        user_id = userDetails['user_id']
        user_name = userDetails['user_name']
        vehicle_image = request.files['vehicle_image']
        message = userDetails['message']
        if vehicle_image.filename != '':
            vehicle_image.save(vehicle_image.filename)
            formattedImage = convertToBinaryData(vehicle_image.filename)
        cur = mysqlcon.connection.cursor()
        cur.execute(
            "INSERT INTO input_vehicle(user_id, user_name, vehicle_image, message) VALUES(%s, %s, %s, %s)",
            (user_id, user_name, formattedImage, message))
        mysqlcon.connection.commit()
        cur.close()
        
        current_time_and_time = datetime.now()
        vehicle_data = {
            'vehicle_number' : 'KBY-0022',
            'time_and_time': current_time_and_time,
            'status': 'bsdk',
            'red_alert': 'true',
            'sent_by': 'bsdk',
            'last_shown': 'bsdk',
            'last_appearence': 'bsdk',
            'others_info': 'bsdk'
        }   
        return vehicle_data, 200
    else:
        return 'Error while adding new vehicle!', 404

@app.route('/get_all_vehicles/', methods=["GET"])
def get_all_vehicles():
    if request.method == 'GET':
        cur = mysqlcon.connection.cursor()
        cur.execute('SELECT * FROM input_vehicle')
        rows = cur.fetchall()
        cur.close()
        # return all_vehicles, 200
        return jsonify({'success': 'success', 'status': 200}), 200    
    else: 
        return {'error': 'failed to fetch data', 'status': 404}, 404



if __name__ == "__main__" :
    app.run(debug=True)