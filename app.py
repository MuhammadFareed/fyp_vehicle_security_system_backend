from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import yaml
from flask_cors import CORS
from models import User

app = Flask(__name__)
CORS(app)   


#Database
db = yaml.load(open('db.yaml', 'r'))
app.config['MYSQL_HOST'] = db["mysql_host"]
app.config['MYSQL_USER'] = db["mysql_user"]
app.config['MYSQL_PASSWORD'] = db["mysql_password"]
app.config['MYSQL_DB'] = db["mysql_db"]


mysqlcon = MySQL(app)

@app.route('/login/', methods=["POST"])
def login():    
    data= User().login()
    return data
    
def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        binaryData = file.read()
        
    return filename`


@app.route('/new_vehicle/', methods=["POST"])
def new_vehicle():
    # data= User().new_vehicle()
    # return data
    if request.method == 'POST':
        userDetails = request.form
        user_id = userDetails['user_id']
        user_name = userDetails['user_name']
        vehicle_image = request.files['vehicle_image']
        message = userDetails['message']
        if vehicle_image.filename != '':
            vehicle_image.save(vehicle_image.filename)
            formattedImage = convertToBinaryData(vehicle_image.filename)
            print(formattedImage)
        cur = mysqlcon.connection.cursor()
        cur.execute(
            "INSERT INTO input_vehicle(user_id, user_name, vehicle_image, message) VALUES(%s, %s, %s, %s)",
            (user_id, user_name, formattedImage, message))
        mysqlcon.connection.commit()
        cur.close()
        return {'success': 'success'}, 200
    else:
        return 'Error while adding new vehicle!', 404

if __name__ == "__main__" :
    app.run(debug=True)