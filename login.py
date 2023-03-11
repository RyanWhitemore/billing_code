from flask import Flask, render_template, request, make_response, redirect, flash, session
from flask_bcrypt import Bcrypt
from load_session import load_session
from flask_session import Session
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.environ["SECRET_KEY"]


def login():
        
        app = Flask(__name__)
        app.config["SESSION_PERMANENT"] = False
        app.config["SESSION_TYPE"] = "filesystem"
        app.config["SECRET_KEY"] = secret_key
        Session(app)
        bcrypt = Bcrypt(app)
    # Make connection to database for post actions
        connection = load_session()
        cursor = connection.cursor()
        
        if request.form['action'] == 'Register':

            if not request.form['username'] or not request.form['password']:
                 return "Username or password feild must not be empty"


            username = request.form['username']
            # Hash password before storing in database
            password = bcrypt.generate_password_hash(request.form['password'])
            # define a tuple of the query variables to pass to cursor.exevute

            query_variables = (username, password)
            add_query = """
            INSERT INTO users (username, password)
            VALUES (%s, %s)"""

            # Fetch all usernames currently in the database
            cursor.execute("""
            SELECT * FROM users""")
            results = cursor.fetchall()

            # Check given username against existing
            for tuple in results:
                if request.form['username'] in tuple:
                    return "username already exists"
            # username doesnt already exist, add to database
            cursor.execute(add_query, query_variables)
            connection.commit()
            connection.close()
            return render_template('registered.html')
        
        elif request.form['action'] == 'Login':

            if not request.form['username'] or not request.form['password']:
                 return "username or password feild cannot be empty"
            # Get username and password from user input
            username = (request.form['username'],)
            password = str(request.form['password'])
 

            # query for information to populate /bills table
            table_query = """
            SELECT
            bill_id,
            num_windows,
            num_entry_doors,
            num_french_doors,
            num_sgd,
            num_sgd_extra_panels,
            hours_extra_labor,
            receipt_total,
            measure,
            customer_name
            FROM bills
            WHERE user_id = %s
            """

            # Fetch credentials from database to check against
            query = """SELECT password, user_id
            FROM users
            WHERE username = %s"""

            # execute credential query
            cursor.execute(query, username)
            results = cursor.fetchall()

            if results:
                 
                password_hash = results[0][0]
                user_id = str(results[0][1])

                # execute table population query
                cursor.execute(table_query, (user_id,))
                table_results = cursor.fetchall()
                connection.close()
            
                # Check if password matches password in database
                if bcrypt.check_password_hash(str(password_hash), password):
                
                    # Set response to index.html and set user_id cookie for future use
                    resp = make_response(render_template('bills.html', results=table_results))
                    resp.set_cookie('user_id', user_id)

                    session["user_id"] = user_id

                    return resp
                else:
                     connection.close()
                     return "invalid username or password"
            
            else:
                connection.close()
                return 'invalid username or password'
