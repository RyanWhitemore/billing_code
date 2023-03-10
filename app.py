from bill_object import Bill, User
from flask import Flask, render_template, url_for, request, make_response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import mysql.connector as connector

import os

load_dotenv()

user = os.environ['USER']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{user}:{password}@localhost:3306/{db_name}".format(
    user = user, password = password, db_name = db_name)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

def load_session():
    connection = connector.connect(user=user,
                                  password=password,
                                  host='localhost',
                                  port=3306,
                                  database='billing_app_db',
                                  auth_plugin='mysql_native_password')
    return connection

@app.route('/login', methods=['POST', 'GET'])
def login():
    
    if request.method == "POST":
        
        session = load_session()
        cursor = session.cursor()
        
        if request.form['action'] == 'Register':
            username = request.form['username']
            password = bcrypt.generate_password_hash(request.form['password'])
            query_variables = (username, password)
            add_query = """
            INSERT INTO users (username, password)
            VALUES (%s, %s)"""

            cursor.execute("""
            SELECT * FROM users""")
            results = cursor.fetchall()
            for tuple in results:
                if request.form['username'] in tuple:
                    return "username already exists"
            cursor.execute(add_query, query_variables)
            session.commit()
            return 'registered'
        
        elif request.form['action'] == 'Login':
            username = (request.form['username'],)
            print('username value is :', username)
            password_hash = str(request.form['password'])
            query = """SELECT password, user_id
            FROM users
            WHERE username = %s"""

            cursor.execute(query, username)
            results = cursor.fetchall()
            password = results[0][0]
            user_id = str(results[0][1])
            print(user_id)
            if bcrypt.check_password_hash( str(password), password_hash):
                resp = make_response(render_template('index.html'))
                resp.set_cookie('user_id', user_id)
                return resp
            
            else:
                return 'invalid username or password'
    else:
        return render_template('login.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        session = load_session()
        cursor = session.cursor()

        insert_query = """
        INSERT INTO bills (
            num_windows,
            num_entry_doors,
            num_french_doors,
            num_sgd,
            num_sgd_extra_panels,
            hours_extra_labor,
            receipt_total,
            measure,
            user_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        response = request.form
        windows = request.form['windows']
        entry_doors = request.form['entry_doors']
        french_doors = request.form['french_doors']
        sgd = request.form['sgd']
        sgd_extra_panel = request.form['sgd_extra']
        hours_labor = request.form['extra_labor']
        receipts = request.form['receipts']
        measure = request.form['measure']
        if measure.upper() == 'YES':
            measure = 1
        else:
            measure = 0
        user_id = request.cookies.get('user_id')
        
        values = (windows, 
                  entry_doors, 
                  french_doors, 
                  sgd, 
                  sgd_extra_panel, 
                  hours_labor, 
                  receipts, 
                  measure, 
                  user_id)
        
        cursor.execute(insert_query, values)
        session.commit()

        return response
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    