from distutils.debug import DEBUG
import sys
import subprocess
from unittest import result

try:
    from flask_jwt_extended import *


except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    from flask_jwt_extended import *


#from web.model.mongodb import *
#from datetime import datetime

from flask import Flask
from flask import request, render_template, make_response, jsonify, session, redirect, url_for

from web import config

#conn = connect_conn(config.db_server, config.db_port)
#col_stock = connect_col(config.db_server, config.db_port, config.dic_dbname['stockdb'], config.dic_colname['stockcol'])
#col_user = connect_col(config.db_server, config.db_port, config.dic_dbname['userdb'], config.dic_colname['usercol'])

app = Flask(__name__)
app.config.update(DEBUG=True, JWT_SECRET_KEY = config.secret_key)

jwt = JWTManager(app)

class Services:
    pass

def create_app(test_config = None):
    app.debug = False
    
    return app


@app.route('/')
def main():
    return render_template('main.html')


@app.route("/login", methods=['POST'])
def login():
    input_data = request.get_json()
    user_name = input_data['id']
    user_pw = input_data['pw']

    if (user_name == config.admin_id) and (user_pw == config.admin_pw):
        return jsonify(
            result = "success",
            access_token = create_access_token(
                identity = user_name, 
                expires_delta= False)
        )
    else:
        return jsonify(
            result = "Invalid Params"
        )