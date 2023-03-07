from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()

user = os.environ['USER']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{user}:{password}@localhost/{db_name}".format(
    user = user, password = password, db_name = db_name)
db = SQLAlchemy(app)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        response = request.form
        windows = request.form['num_windows']
        entry_doors = request.form['num_doors']
        french_doors = request.form['num_french']
        sgd = request.form['num_sgd']
        sgd_extra_panel = request.form['num_extra_panel']
        hours_labor = request.form['hours_labor']
        receipts = request.form['receipts']
        measure = request.form['measure']
        return response
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    