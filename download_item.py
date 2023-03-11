from load_session import load_session
from bill_object import Bill
from flask import Response, redirect, session, Flask
from flask_session import Session
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.environ["SECRET_KEY"]

def download_item(id):

    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SECRET_KEY"] = secret_key
    Session(app)

    # load connection
    connection = load_session()
    cursor = connection.cursor()

    query_for_user_id = """
    SELECT user_id
    FROM bills
    WHERE bill_id = %s"""
    
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
    bill_id = (id,)

    cursor.execute(select_query, bill_id)
    bill_to_download = cursor.fetchall()
    bill_columns = cursor.column_names

    cursor.execute(query_for_user_id, bill_id)
    user_id = cursor.fetchone()

    if str(session.get('user_id')) != str(user_id[0]):
        print(user_id, session.get('user_id'))
        return redirect('/login')
   
    # instatiate bill calss
    bill = Bill()
    
    # populate bill attributes with info from database
    for i in range(len(bill_columns) - 1):
        bill.update_attribute(bill_columns[i], bill_to_download[0][i])

    # add customer name to bill
    bill.add_name(bill_to_download[0][8])
    
    # Generate bill pdf
    pdf = bill.generate_bill()

    connection.close()

    resp = Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attatchment;filename={}'.format(bill.file_name)})

    return resp