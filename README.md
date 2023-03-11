# Billing_code
---
A personnal project based around a bit of code I wrote for generating a pdf bill

## About this project
---
I wrote some code in python to help me write bills for my current job as a window and door installer
a while back and recently decided to take the billing code I had written and turn it into a web app
as a bit of practice. I taught myself the basics of flask while doing this project so this project 
was a great learning experience for me.

## Technologies in this project
---
Flask 
- A web framework used in this case to design a billing web app  
mysql connector python 
- An api used to make a connection to a database through python  
flask_bcrypt 
- A version of bcrypt designed for use with the flask framework to hash passwords and  
- check hashed passwords  
FPDF 
- A python module used to generate pdf reports  
bill_object 
- The python code that I wrote and based this project around, it generates a pdf file  
- based on the attributes assigned to the instance of the object  

## How the app works
---
The functionality of the web app is pretty straight forward, the landing page is meant to be the
login.html page, from there you may either register your login information or log in. Once logged
in it takes you to a page with all the bill information saved in the database under your user id.
From that page you can delete or download bills or use the link to add another bill which takes 
you to a page designed for adding bill information to the database under your user id.

## To test this code on your machine
---
If for some reason you are interested in testing the functionality of this code on your own machine
here are some things you must do
- Create a .env file with your database credentials as USER, PASSWORD, and DB_NAME
- Create a mysql database with the following tables and rows (An entity relationship diagram is provided in the program files)
    - user table
        -  user_id
        -  username
        -  password
    - bills table
        -  bill_id
        -  num_windows
        -  num_entry_doors
        -  num_french_doors
        -  num_sgd
        -  num_sgd_extra_panels
        -  hours_extra_labor
        -  receipt_total
        -  measure
        -  user_id
        -  customer_name  
With those two requirements satisfied the app should function as intended
