from flask import Flask
from flask import request, render_template, make_response, jsonify, session, redirect, url_for, Response
from flask_restx import Api, Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager

#from web.model.mongodb import *
from datetime import datetime, timedelta
from web import config

#conn = connect_conn(config.db_server, config.db_port)
#col_stock = connect_col(config.db_server, config.db_port, config.dic_dbname['stockdb'], config.dic_colname['stockcol'])
#col_user = connect_col(config.db_server, config.db_port, config.dic_dbname['userdb'], config.dic_colname['usercol'])

app = Flask(__name__)
app.config.update(DEBUG=True, JWT_SECRET_KEY = config.secret_key)
app.config['JWT_SECRET_KEY'] = config.flaskJwt_secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1) # default : 15분
#app.config['JWT_REFRESH_TOKEN_EXPIRES'] = config.flaskJwt_refresh # default : 30일

jwt = JWTManager(app)
#api = Api(app)
api = Api(
    app,
    version='0.1',
    title="Hwan's API Server",
    description="Hwan's Todo API Server!",
    terms_url="/",
    contact="Hwan001.tistory.com",
    license="MIT"
)


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
        
        
@app.route("/my_jwt_test", methods=['GET'])
@jwt_required()
def my_jwt_test():
    current_user = get_jwt_identity() 
    
    return jsonify(logged_in_as=current_user), 200


# API 등록
@api.route('/api/<string:name>') 
class Api_class(Resource):
    def get(self, name): 
        return {"message": f"Hello! {name}"}



Todo = Namespace('Todo')

@Todo.route('')
class TodoPost(Resource):
    def post(self):
        count = 1
        todos = {}
        
        idx = count
        count += 1
        todos[idx] = request.json.get('data')
        
        return { 
            'todo_id': idx,
            'data':todos[idx]        
        }
