import mysql.connector as connector
from dotenv import load_dotenv
import os

load_dotenv()
user = os.environ['USER']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']

def load_session():
    connection = connector.connect(user=user,
                                  password=password,
                                  host='localhost',
                                  port=3306,
                                  database='billing_app_db',
                                  auth_plugin='mysql_native_password')
    return connection
