from flask import Flask, render_template, request, make_response, redirect
from load_session import load_session


def get_bills():
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