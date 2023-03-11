from flask import Flask, render_template, request
import mysql.connector as connector
from login import login as login_function
from insert import insert
from get_bills import get_bills
from delete_item import delete_item
from download_item import download_item


# instatiate and configure flask app
app = Flask(__name__)



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
        return login_function()
        
    else:
        return render_template('login.html')

# Route for adding billing info to database
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return insert()
    else:
        return render_template('index.html')
    

@app.route('/bills', methods=['POST', 'GET'])
def bills():

    return get_bills()


# Route for deleting bills
@app.route('/delete/<int:id>')
def delete(id):

    return delete_item(id)


# App route to download bill pdf
@app.route('/download/<int:id>')
def download(id):
    
   return download_item(id)

if __name__ == "__main__":
    app.run(debug=True)
    