#from ast import Delete

from queue import Empty
from pymongo import MongoClient
import hashlib


def connect_conn(host, port):
    return MongoClient(host, port)

def connect_col(host, port, db_name, col_name):
    return MongoClient(host, port).get_database(db_name).get_collection(col_name)

def setup(conn, db_name, col_name, user):
    db = conn.get_database(db_name)
    
    try:
        col = db.create_collection(col_name)
    except:
        col = db.get_collection(col_name)

    col.insert_one({'_id':user['id'], '_pw':user['pw_hash'], '_tickers':user['tickers']})


def is_empty(col, query):
    if len(list(col.find(query))) == 0:
        return True
    else:
        return False
    
def dbcheck(col, id):
    return is_empty(col, {"_id":id})

def dblogin(col, id, pw):
    return is_empty(col, {"_id":id, "_pw":pw})

def get_tickers(col, id):
    return col.find({"_id":id}).limit(1)

def remove_user(col, id):
    col.delete_one({"_id":id})

def password_hash(pw):
    return hashlib.sha256(bytes('PLU/'+pw+'/TO', 'utf-8')).hexdigest()
