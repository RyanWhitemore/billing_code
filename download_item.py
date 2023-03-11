from load_session import load_session
from bill_object import Bill
from flask import Response

def download_item(id):
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