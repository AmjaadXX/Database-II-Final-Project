from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pymongo
from pandas import DataFrame
import pandas as pd



app = Flask(__name__)
app.secret_key = 'your secret key'


##############setting up mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'assignmentdb' 
mysql = MySQL(app)

##############setting up mongodb connection
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["restraunts_database"]
mycol = mydb["restraunts_database"]



@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            data = list(mycol.find())
            df = DataFrame(data)
            data = list(mycol.find())
            a = DataFrame(columns=['Name' ,'Cuisine','Street','Borough','Grade' ]) #,'Cuisine','street','borough','grade'
            for i in data:
                a=a.append({'Name':i['name'],'Cuisine':i['cuisine'],'Street':i['address']['street'] ,'Borough':i['borough'] ,'Grade':i['grades'][0]['grade']} ,ignore_index = True)
            msg = a
            siz = len(msg)
            return render_template('SearchPage.html',column_names=msg.columns.values, row_data=list(msg.values.tolist()), zip=zip ,size=siz )
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'gender' in request.form :
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not username or not password or not gender:
            msg = 'Some error in the values!'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)', (username, password, gender, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Some error in the values!'
    return render_template('register.html', msg = msg)


@app.route("/SearchPage" , methods =['GET', 'POST'])
def SearchPage():
    searchtag = request.form['categories']
    searchvalue = request.form['searchvalue']
    data = list(mycol.find({searchtag:searchvalue}))
    a = DataFrame(columns=['Name' ,'Cuisine','Street','Borough','Grade' ]) #,'Cuisine','street','borough','grade'
    msg = a
    for i in data:
        a=a.append({'Name':i['name'],'Cuisine':i['cuisine'],'Street':i['address']['street'] ,'Borough':i['borough'] ,'Grade':i['grades'][0]['grade']} ,ignore_index = True)
        msg = a
    siz = len(msg)
    return render_template('SearchPage.html',column_names=msg.columns.values, row_data=list(msg.values.tolist()), zip=zip , size= siz )