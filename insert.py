from load_session import load_session
from flask import Flask, render_template, request, make_response, redirect, session
from flask_session import Session
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.environ["SECRET_KEY"]



def insert():
        
        app = Flask(__name__)
        app.config["SESSION_PERMANENT"] = False
        app.config["SESSION_TYPE"] = "filesystem"
        app.config["SECRET_KEY"] = secret_key
        Session(app)

        user_id = request.cookies.get('user_id')

        if session.get('user_id') != user_id:
             return redirect('/login')

        connection = load_session()
        cursor = connection.cursor()

        insert_query = """
        INSERT INTO bills (
            customer_name,
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
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        # initialize variables for query from the user input
        customer_name = request.form['customer']
        windows = request.form['windows']
        entry_doors = request.form['entry_doors']
        french_doors = request.form['french_doors']
        sgd = request.form['sgd']
        sgd_extra_panel = request.form['sgd_extra']
        hours_labor = request.form['extra_labor']
        receipts = request.form['receipts']
        measure = request.form['measure']
        # Convert string response for measure to make it TINYINT compatable
        if measure.upper() == 'YES':
            measure = 1
        else:
            measure = 0
        
        # Set values tuple to pass to cursor.execute
        values = (customer_name,
                  windows, 
                  entry_doors, 
                  french_doors, 
                  sgd, 
                  sgd_extra_panel, 
                  hours_labor, 
                  receipts, 
                  measure, 
                  user_id)
        
        cursor.execute(insert_query, values)
        connection.commit()
        connection.close()

        return redirect('/bills')