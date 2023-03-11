from load_session import load_session
from flask import Flask, render_template, request, make_response, redirect



def insert():
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