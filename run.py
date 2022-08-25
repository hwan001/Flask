import sys
import subprocess

try:   
    import flask
    import pymongo
    import mariadb
    import yfinance
    import tensorflow
    import numpy

except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

from web import app
app = app.create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)