#from cgi import test
from flask import Flask
from flask_cors import CORS # 외부 접속 가능하게 해줌

import web.config as config
import web.model as model


app = Flask(__name__)

# 여러 함수를 import 하는 용도의 빈 클래스
class Services:
    pass

def create_app(test_config = None):
    #print("url : ", config.url)
    
    app.debug = False

    #CORS(app) # app 객체의 외부 접속이 가능해짐

    # Set config
    #if test_config is None:
    #    app.config.from_pyfile('config.py')
    #else:
    #    app.config.update(test_config)

    #SetUp Persistence Layer - Model
    #database = model.mongodb.connect_conn()

    #SetUp Business Layer - Controller
    #services = Services

    #SetUp Presentation Layer - View
    
    return app


import random
from datetime import datetime, timedelta
from urllib.parse import uses_netloc

#import web.config as config
from web.model.mongodb import *
from flask import Flask
from flask import request, render_template, make_response, jsonify, session, redirect, url_for
import yfinance as yf


conn = connect_conn(config.db_server, config.db_port)
col_stock = connect_col(config.db_server, config.db_port, config.dic_dbname['stockdb'], config.dic_colname['stockcol'])
col_user = connect_col(config.db_server, config.db_port, config.dic_dbname['userdb'], config.dic_colname['usercol'])

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/mypage', methods=['GET'])
#@login_required
def index():
    tickers = ["TSLA", "META", "GOOGL"]
    list_data = {}
    for ticker in tickers:
        list_data[ticker] = [random.randrange(-10, 11) for i in range(12)]
    return render_template('mypage.html', tickers_len=len(tickers), tickers=tickers, list_data=list_data)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['pw']
        tickers = ["QQQ", "SPY"]

        if dbcheck(col_user, username) is True:
            user = {'id':username, 'pw_hash':password_hash(password), 'tickers':tickers}
            setup(col_user, config.dic_dbname['userdb'], config.dic_colname['usercol'], user)

        else:
            return '이미 있음'
    elif request.method == 'GET':
        pass
    return render_template('signup.html', url=config.url)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['pw']
        
        if dblogin(col_user, username, password):
            remove_user(col_user, username)
            print(username, '님이(가) 로그인 했습니다.')
            try:
                tickers = dict(list(get_tickers(col_user, username))[0])['_ticker']
                print(tickers)
            except:
                tickers = ["qqq", "googl", "meta"]
                print("tickers is empty")

            return render_template('mypage.html', url=config.url, tickers_len=len(tickers), tickers=tickers)
        else:
            print(username, '계정 로그인 시도 발생')
            return '<script>alert("로그인 실패");</script><br><a href="/">home</a>'

    elif request.method == 'GET':
        pass
    
    return render_template('signin.html', url=config.url)


@app.route('/signout')
#@login_required
def signout():
    remove_user(col_user, "hwan")
    #session.pop('username', None)
    return redirect(url_for('/mypage'))

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'POST':
        try:
            ticker = request.form.get("ticker")
            yf_Ticker = yf.Ticker(ticker)
            startdate = "2020-01-01"
            enddate = datetime.now()
            interval = "1Mo"
            kind = 'Close'
            ticker_data = yf_Ticker.history(start=startdate, end=enddate, interval=interval)[kind]
            ticker_index = (lambda origin: [str(tmp.strftime("%Y-%m-%d")) for tmp in list(origin.index)])(ticker_data)
            ticker_value = (lambda origin: [round(tmp, 2) for tmp in list(origin.values)])(ticker_data)
            aver_step = (max(ticker_value) - min(ticker_value)) / len(ticker_value)
        except:
            pass
        #   return render_template('error_500.html')
    elif request.method == 'GET':
        ticker = ""
        ticker_index = []
        ticker_value = []
        aver_step = 0
    return render_template('graph.html', url=config.url, ticker=ticker, ticker_index=ticker_index, ticker_value=ticker_value, aver_step=aver_step)


# js
@app.route("/function.js", methods=["GET"])
def js_file():
    return make_response(render_template("/function.js"))

@app.route("/my_style.css", methods=["GET"])
def css_file():
    return make_response(render_template("/my_style.css"))

# error handling
@app.errorhandler(500)
def error_handling_500(error):
    #ticker = str(request.query_string, 'utf-8').replace("ticker=", "")
    ticker = "ticker "
    return render_template('error_500.html', ticker=ticker)
    #return jsonify({"Error Code : 500"})

@app.errorhandler(400)
def error_handling_400(error):
    #return render_template('error_400.html')
    return jsonify({"Error Code : 400"})