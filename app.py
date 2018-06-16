from flask import Flask, render_template, request, session, url_for, flash, redirect
import sqlite3
import os

from utils.api import *
from utils.db_builder import *
from utils.forum import *

app = Flask(__name__)

# ------------------ Login------------------------------
app.secret_key = "messes up if we have this for real"
BAD_USER = -1
BAD_PASS = -2
GOOD = 1
user = ""

@app.route('/')
def root():
    tableCreation()
    if session.has_key('user') and user != "":
        return redirect( url_for('home') )
    # If not logged in yet:
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
    userType = request.form['userType']

    if userType == 'Parent':
        userType = 0
    elif userType == 'Student':
        userType = 1
    else:
        userType = 2

    if checkUsername(user):
        flash('Username unavailable. Please try another username.')
        return redirect(url_for('root'))
    else:
        addUser(user,password,name, 0, userType)
        session['user'] = user
        return redirect( url_for('home'))

# ------------------- Logout ---------------------------------
@app.route('/logout', methods = ['POST','GET'])
def logout():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))

    print "Session LogOut================"
    print session
    print "=============================="

    session.pop('user')
    flash('You have been logged out successfully')
    return redirect(url_for('root'))

# ------------------- Calendar ---------------------------------
@app.route('/calendar')
def calendar():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))
    return render_template("calendar.html")

#============================================================================
@app.route('/home', methods = ['POST','GET'])
def home():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))

    ID = getUserID(session['user'])
    #INFO ================================
    print 'username', getUserName(ID)

    print  'config',getConfig(ID)

    name = getName(ID)
    print 'name', name
    

    print 'usertype',getUserType(ID)

    #=====================================
    return render_template('home.html', name=name)

@app.route('/events', methods = ['POST','GET'])
def events():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))
    event = table_builder(get_events()).decode('utf-8')
    return render_template('events.html', event = event)

# 0 = View All Category
# 1 = View All Topic in Category
# 2 = View All Post in Topic
@app.route('/forum', methods = ['POST','GET'])
def forum(location=0):
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))
    
    cat = categoryTableBuilder(getAllCat())

    if location == 0:
        return render_template('forum.html', cat = cat)
    else:
        return render_template('forum.html', cat = cat)

@app.route('/forumconfig', methods = ['POST','GET'])
def forumconfig():
    if len(request.args) == 1:
        
    return 'testing'

if __name__=='__main__':
	app.run(debug=True)
