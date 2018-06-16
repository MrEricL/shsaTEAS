from flask import Flask, render_template, request, session, url_for, flash, redirect
import sqlite3
import os

from utils.db_builder import *


app = Flask(__name__)



# ------------------ Login Stuff ------------------------------
app.secret_key = "messes up if we have this for real"
BAD_USER = -1
BAD_PASS = -2
GOOD = 1
user = ""


@app.route('/')
def index():
	tableCreation()
	if session.has_key('user'):
		return redirect( url_for('home') )
	else:
		return render_template("login.html")

# ------------------- Login -----------------------------------
@app.route('/login', methods = ['POST','GET'])
def login():
    user = request.form['user']
    #print user
    passw = request.form['pass']
    #print passw

    result = authenticate(user, passw)
    #print result

    #if successful, redirect to home
    #otherwise redirect back to root with flashed message 
    if result == GOOD:
        session['user'] = user
        return redirect( url_for('home') )
    if result == BAD_USER:
        flash('Incorrect username. Please try again.')
        return redirect( url_for('root') )
    if result == BAD_PASS:
        flash('Incorrect password. Please try again.')
        return redirect( url_for('root') )
    return redirect( url_for('root') )

# ------------------- Register ---------------------------------
@app.route('/register', methods = ['POST', 'GET'])
def register():
    user = request.form['user']
    password = request.form['pass']
    name = request.form['name']

    if checkUsername(user):
        flash('Username unavailable. Please try another username.')
        return redirect(url_for('root'))
    else:
        addUser(user,password,name, 0)
        session['user'] = user
        return redirect( url_for('home'))

# ------------------- Logout ---------------------------------
@app.route('/logout', methods = ['POST','GET'])
def logout():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))
    session.pop('user')
    flash('You have been logged out successfully')
    return redirect(url_for('root'))

#============================================================================

@app.route('/home', methods = ['POST','GET'])
def home():
	return render_template('home.html')


if __name__=='__main__':
	app.run(debug=True)

