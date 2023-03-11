from bill_object import Bill, User
from flask import Flask, render_template, url_for, request, make_response, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import mysql.connector as connector
from fileinput import filename
import os

# load and define environment variables
load_dotenv()
user = os.environ['USER']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']

# instatiate and configure flask app
app = Flask(__name__)
bcrypt = Bcrypt(app)


# Define a function to make a connection to the mysql database
def load_session():
    connection = connector.connect(user=user,
                                  password=password,
                                  host='localhost',
                                  port=3306,
                                  database='billing_app_db',
                                  auth_plugin='mysql_native_password')
    return connection


# Login route
@app.route('/login', methods=['POST', 'GET'])
def login():
    
    if request.method == "POST":
        
        # Make connection to database for post actions
        session = load_session()
        cursor = session.cursor()
        
        if request.form['action'] == 'Register':
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
            session.commit()
            session.close()
            return 'registered'
        
        elif request.form['action'] == 'Login':
            # Get username and password from user input
            username = (request.form['username'],)
            password_hash = str(request.form['password'])

            # Fetch credentials from database to check against
            query = """SELECT password, user_id
            FROM users
            WHERE username = %s"""

            cursor.execute(query, username)
            results = cursor.fetchall()
            session.close()
            
            password = results[0][0]
            user_id = str(results[0][1])
            
            # Check if password matches password in database
            if bcrypt.check_password_hash( str(password), password_hash):
                
                # Set response to index.html and set user_id cookie for future use
                resp = make_response(render_template('index.html'))
                resp.set_cookie('user_id', user_id)
                return resp
            
            else:
                session.close()
                return 'invalid username or password'
    else:
        return render_template('login.html')

# Route for adding billing info to database
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        session = load_session()
        cursor = session.cursor()

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
        response = request.form
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
        user_id = request.cookies.get('user_id')
        
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
        session.commit()
        session.close()

        return redirect('/bills')
    else:
        return render_template('index.html')
    
    make_response

@app.route('/bills', methods=['POST', 'GET'])
def bills():

    # load database connection
    session = load_session()
    cursor = session.cursor()
    user_id = (request.cookies.get('user_id'),)
          
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

    session.close()

    return render_template('bills.html', results=results)


# Route for deleting bills
@app.route('/delete/<int:id>')
def delete(id):

    # Load database connection
    session = load_session()
    cursor = session.cursor()

    # Query to find bill to delete
    find_bill_query = """
    SELECT bill_id
    FROM bills
    WHERE bill_id = %s"""

    # Query to delete bill
    delete_bill_query = """
    DELETE FROM bills
    WHERE bill_id = %s"""

    # Turn bill id into tuple to pass to cursor.execute
    bill_id = (id,)

    # Execute  find_bill_query
    cursor.execute(find_bill_query, bill_id)
    # Fetch results from query
    bill_to_delete = cursor.fetchall()

    # Execute delete query
    cursor.execute(delete_bill_query, bill_to_delete[0])
    session.commit()
    session.close()

    return redirect('/bills')


# App route to download bill pdf
@app.route('/download/<int:id>')
def download(id):
    
    # load session
    session = load_session()
    cursor = session.cursor()

    # query to select necesarry info for bill
    select_query = """
    SELECT 
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
    WHERE bill_id = %s
    """
    
    # make user_id tuple to pass to cursor.execute
    user_id = (id,)

    cursor.execute(select_query, user_id)
    bill_to_download = cursor.fetchall()
    bill_columns = cursor.column_names
   
    # instatiate bill calss
    bill = Bill()
    
    # populate bill attributes with info from database
    for i in range(len(bill_columns) - 1):
        bill.update_attribute(bill_columns[i], bill_to_download[0][i])

    # add customer name to bill
    bill.add_name(bill_to_download[0][8])
    
    # Generate bill pdf
    pdf = bill.generate_bill()


    resp = Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attatchment;filename={}'.format(bill.file_name)})

    return resp

if __name__ == "__main__":
    app.run(debug=True)
    