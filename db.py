import os
import psycopg2
from dotenv import find_dotenv, load_dotenv



def init_pgconnection():
    db=os.environ.get('pg_dbname')
    host=os.environ.get('pg_host')
    user=os.environ.get('pg_user')
    password=os.environ.get('pg_password')
    conn = psycopg2.connect(database=db,host=host,user=user,password=password)
    return conn

