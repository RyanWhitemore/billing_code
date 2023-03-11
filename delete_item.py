from load_session import load_session
from flask import redirect

def delete_item(id):
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