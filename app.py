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

db = MySQL(app)

@app.route('/login/', methods=["POST"])


def login():
    data= User().login()
    return data

@app.route('/new_vehicle/', methods=["POST"])
def new_vehicle():
    data= User().new_vehicle()
    return data

if __name__ == "__main__" :
    app.run(debug=True)