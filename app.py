from flask import Flask, render_template, request, session, url_for, flash, redirect
import sqlite3
import os
from datetime import date

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
#@app.route('/calendar')
#def calendar():
#    try:
#        ID = getUserID(session['user'])
#    except:
#        return redirect( url_for('root'))
#
#
#    eventl = get_name_events(get_events())
#
#
#    return render_template("calendar.html", a = eventl[4], b =  eventl[1], c = eventl[2], d= eventl[3])
#
#============================================================================
@app.route('/home', methods = ['POST','GET'])
def home():

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    monthname = now.strftime("%B")
    day = now.day

    prettydate = "{} {}, {}".format(monthname, day, year)

    a = date(year,month,day)
    b = date(2018,10,22)

    #print 'days left-----------'
    #print (b-a).days
    left = (b-a).days / 365.0
    left *= 100
    #print '--------------------'

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
    if getConfig(ID) != 1:
        return render_template('config.html')

    else:
        return render_template('home.html', name=name, left = left, prettydate = prettydate)


@app.route('/config', methods = ['POST','GET'])
def config():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))

    setConfig(ID)

    return redirect( url_for('home'))



@app.route('/events', methods = ['POST','GET'])
def events():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))

    events = table_builder(get_events()).decode('utf-8')

    print "==================================="
    print events
    print "==================================="

    return render_template('events.html', events = events)


@app.route('/calendar', methods = ['POST','GET'])
def calendar():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))
    
    events = getData()
    e = get_name_events()


    return render_template('calendar.html', events =events, a = e[1], b = e[2], c = e[3], d = e[4] )

@app.route('/calenderdb', methods = ['POST','GET'])
def calenderdb():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))



    print request.args

# 0 = View All Category
# 1 = View All Topic in Category
# 2 = View All Post in Topic
@app.route('/forum', methods = ['POST','GET'])
def forum():
    try:
        ID = getUserID(session['user'])
    except:
        return redirect( url_for('root'))

    rawCategories = getAllCat()


    #Browsing category
    if len(request.args) == 0:
        cat = categoryTableBuilder(rawCategories)
        return render_template('forum.html', cat = cat)

    #Browsing topic in category
    elif len(request.args) == 1:

        '''
        print "TESTING TOPICS=============="
        print getAllTopicInCat(int(request.args['category']))
        print "============================"
        '''


        topic = getAllTopicInCat(request.args['category'])
        topictable = topicTableBuilder(topic, request.args['category'])

        categoryname = rawCategories[int(request.args['category'])]['name']


        if topic == []:
            return render_template('topic.html', topic = None, name = categoryname, catint = int(request.args['category']))

        else:
            return render_template('topic.html', topic = True, name = categoryname, catint = int(request.args['category']), topictable = topictable)
        
    elif len(request.args) == 2:

        title = getTopicTitle(request.args['category'], request.args['topic'])
        rawpost = getAllPostInTopic(request.args['category'], request.args['topic'])
        postID = rawpost[0]['postID']

        posts = postTableBuilder(rawpost)

        print "********************************"
        print posts
        #print postID
        print "********************************"

        return render_template('post.html', title = title , catint = int(request.args['category']), topicint = request.args['topic'], postint = postID, posts = posts)

    else:
        cat = categoryTableBuilder(rawCategories)
        return render_template('forum.html', cat = cat)


#   NOTE TO WHOEVER IS READING: This is super repetitive and useless but
#   it's too much work to delete. :(

@app.route('/forumconfig', methods = ['POST','GET'])
def forumconfig():
    if len(request.args) == 1:
        print "Forum Configuration ======================"
        print request.args['category']
        print "=========================================="
        return redirect( url_for('forum', category = request.args['category']))

    elif len(request.args) == 2:

        print request.args['topic']

        return redirect( url_for('forum', category = request.args['category'], topic = request.args['topic']))

    else:
        
        return 'testing'

@app.route('/addtopic', methods = ['POST','GET'])
def addtopic():
    ID = getUserID(session['user'])
    title = request.form['title']
    body = request.form['body']
    cat = request.form['category']

    addTopic(ID, cat, title, body)

    return redirect( url_for('forum', category = cat))

@app.route('/addpost', methods = ['POST','GET'])
def addpost():
    ID = getUserID(session['user'])
    body = request.form['body']
    cat = request.form['category']
    top = request.form['topic']
    post = request.form['post']

    #addTopic(ID, cat, title, body)
    addToPost (ID, cat, top, post, body)

    return redirect( url_for('forum', category = cat, topic = top))

if __name__=='__main__':
	app.run(debug=True)
