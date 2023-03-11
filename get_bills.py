from flask import Flask, render_template, request, make_response, redirect, session
from load_session import load_session
from dotenv import load_dotenv
from flask_session import Session
import os

load_dotenv()
secret_key = os.environ["SECRET_KEY"]


def get_bills():

# instantiate session for user verification
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SECRET_KEY"] = secret_key
    Session(app)


# load database connection
    connection = load_session()
    cursor = connection.cursor()
    user_id = (request.cookies.get('user_id'),)

    if session.get('user_id') != user_id[0]:
        return redirect('/login')
          
    # Query to select necessary information based on user_id
    query = """
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
    WHERE user_id = %s"""

    cursor.execute(query, user_id)
    
    results = cursor.fetchall()

    connection.close()

    return render_template('bills.html', results=results)