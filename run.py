import sys
import subprocess
import random
from datetime import datetime, timedelta

from web import app

try:   
    from flask import Flask
    from flask import request, render_template, make_response, jsonify, session, redirect, url_for

    from pymongo import MongoClient
    import yfinance as yf
except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

app = app.create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)