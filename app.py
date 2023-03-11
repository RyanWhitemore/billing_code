from flask import Flask, render_template, request, session, redirect
from login import login as login_function
from dotenv import load_dotenv
from flask_session import Session
import os
from insert import insert
from get_bills import get_bills
from delete_item import delete_item
from download_item import download_item

load_dotenv()

secret_key = os.environ["SECRET_KEY"]


# instatiate flask app
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = secret_key
Session(app)


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

    if not session.get('user_id'):
        return redirect('/login')

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


@app.route('/logout')
def logout():
    session['user_id'] = None

    return redirect('/login')
    

if __name__ == "__main__":
    app.run(debug=True)