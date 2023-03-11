from load_session import load_session
from flask import redirect, session, Flask, request
from flask_session import Session
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.environ['SECRET_KEY']

def delete_item(id):

    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SECRET_KEY"] = secret_key
    Session(app)

    # Load database connection
    connection = load_session()
    cursor = connection.cursor()

    # Query to find bill to delete
    find_user_id = """
    SELECT user_id
    FROM bills
    WHERE bill_id = %s"""

    # Query to delete bill
    delete_bill_query = """
    DELETE FROM bills
    WHERE bill_id = %s"""

    # Turn bill id into tuple to pass to cursor.execute
    bill_id = (id,)

    # Execute  find_user_id query
    cursor.execute(find_user_id, bill_id)
    # Fetch results from query
    user_id = cursor.fetchall()

    if str(session.get('user_id')) != str(user_id[0][0]):
        print('user_id :', user_id[0][0], 'session_id :', session.get('user_id'))
        return redirect('/login')

    # Execute delete query
    cursor.execute(delete_bill_query, bill_id)
    connection.commit()
    connection.close()

    return redirect('/bills')