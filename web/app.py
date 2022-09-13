from flask import Flask
#from web.model.mongodb import *
from flask import request, render_template, make_response, jsonify, session, redirect, url_for

#from datetime import datetime

import config

#conn = connect_conn(config.db_server, config.db_port)
#col_stock = connect_col(config.db_server, config.db_port, config.dic_dbname['stockdb'], config.dic_colname['stockcol'])
#col_user = connect_col(config.db_server, config.db_port, config.dic_dbname['userdb'], config.dic_colname['usercol'])

app = Flask(__name__)

class Services:
    pass

def create_app(test_config = None):
    app.debug = False
    
    return app

@app.route('/')
def main():
    return render_template('main.html')