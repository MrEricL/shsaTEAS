import sqlite3
import csv       
import hashlib
import uuid
import os
import datetime


DIR = os.path.dirname(__file__) or '.'
DIR += '/../data/data.db'

def tableCreation():

    if not os.path.isfile(DIR):
        db = sqlite3.connect(DIR) #open if f exists, otherwise create
        c = db.cursor()         #facilitates db ops

        users_table = 'CREATE TABLE users (username TEXT PRIMARY KEY, password BLOB, userID INTEGER, name TEXT, config INTEGER, userType INTEGER);'
        c.execute(users_table)

        progress_table = 'CREATE TABLE progress (userID INTEGER, progressInt INTEGER);'
        c.execute(progress_table)

        categories_table = 'CREATE TABLE categories (catID INTEGER, catName TEXT, catDesc TEXT);'
        c.execute(categories_table)

        topics_table = 'CREATE TABLE topics (userID INTEGER, catID INTEGER, topicID INTEGER, topic_date DATETIME, title TEXT);'
        c.execute(topics_table)

        posts_table = 'CREATE TABLE posts (userID INTEGER, catID INTEGER, topicID INTEGER, postID INTEGER, postDate DATETIME, body TEXT);'
        c.execute(posts_table)


        db.commit()
        db.close()

        addCategories()

#===========================================================================================================================================

#LOGIN STUFF

def hash_password(password):
    key = uuid.uuid4().hex
    return hashlib.sha256(key.encode() + password.encode()).hexdigest()+':' + key

def check_password(hashed_password, user_password):
    password, key = hashed_password.split(':')
    return password == hashlib.sha256(key.encode()+user_password.encode()).hexdigest()

#add a user
def addUser(new_username, new_password, new_name, new_config, new_userType):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    #global userID_counter
    #new_userID = userID_counter
    #userID_counter += 1

    userCount = c.execute('SELECT COUNT(*) FROM users;')

    new_userID = 0
    for x in userCount:
        new_userID = x[0]
    #new_userID += 1
    hash_pass = hash_password(new_password)
    #print ('The string to store in the db is: ' + hash_pass)
    c.execute('INSERT INTO users VALUES (?,?,?,?,?,?)',[new_username, hash_pass, new_userID, new_name, new_config, new_userType])
    db.commit()
    db.close() 

    addProgress(new_userID)

#=====================================================================================================================================
def authenticate(user, passw):
     info = getPass(user)
     if info == None:
         return -1
     elif check_password(info, passw):
          return 1
     else:
          return -2
     

def register(user, passw, name, userType):
     addUser(user, passw, name, 0, userType)


#==================================================================================================================================

#ACCESSORS/GETTING

def checkUsername(userN):
    db = sqlite3.connect(DIR)
    c = db.cursor()
    users = c.execute('SELECT username FROM users;')
    result = False
    for x in users:
        if (x[0] == userN):
            result = True
    db.close()
    return result

def getPass(username):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = "SELECT username, password FROM users"
    info = c.execute(command)

    retVal = None
    for entry in info:
        if str(entry[0]) == username:
            retVal = str(entry[1])
    db.close()
    return retVal

def getUserID(username):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = 'SELECT userID FROM users WHERE username ="' + username + '";'
    info = c.execute(command)
    retVal = info.fetchall()[0][0]

    db.close()
    return retVal

def getUserName(ID):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = 'SELECT userID FROM users WHERE userID ="' + str(ID) + '";'
    info = c.execute(command)

    retVal = None
    for user in info:
        #print user
        retVal = user[0]
    db.close()
    return retVal

def addProgress(ID):
    db = sqlite3.connect(DIR)
    c = db.cursor()        

    c.execute('INSERT INTO progress VALUES (?,?)',[ID, 0])
    db.commit()
    db.close()     

def getConfig(ID):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = 'SELECT config FROM users WHERE userID ="' + str(ID) + '";'
    info = c.execute(command)

    retVal = None
    for user in info:
        #print user
        retVal = user[0]
    db.close()
    return retVal

def getName(ID):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = 'SELECT name FROM users WHERE userID ="' + str(ID) + '";'
    info = c.execute(command)

    retVal = None
    for user in info:
        #print user
        retVal = user[0]
    db.close()
    return retVal    

def getUserType(ID):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = 'SELECT userType FROM users WHERE userID ="' + str(ID) + '";'
    info = c.execute(command)

    retVal = None
    for user in info:
        #print user
        retVal = user[0]
    db.close()
    return retVal

def getProgress(ID):
    db = sqlite3.connect(DIR) #open if f exists, otherwise create
    c = db.cursor()         #facilitates db ops
    command = 'SELECT progress FROM progressInt WHERE userID ="' + str(ID) + '";'
    info = c.execute(command)

    retVal = None
    for user in info:
        #print user
        retVal = user[0]
    db.close()
    return retVal

#==================================================================================================================================

def setConfig(ID):
    db = sqlite3.connect(DIR)
    c = db.cursor()
    command = 'UPDATE users SET config = 1 WHERE userID = '+str(ID)+';'
    c.execute(command)
    db.commit()
    db.close()

def setProgress(ID, progress):
    db = sqlite3.connect(DIR)
    c = db.cursor()
    command = 'UPDATE progress SET progressInt = {} WHERE userID ={};'
    c.execute(command.format(ID, progress))
    db.commit()
    db.close()

#Forum Stuff========================================================================================================================
#(catID INTEGER, catName TEXT, catDesc TEXT);
def addCategories():
    db = sqlite3.connect(DIR)
    c = db.cursor()
    c.execute('INSERT INTO categories VALUES (?,?,?)',[0, 'General Help', 'Post anything that you have help with.'])
    c.execute('INSERT INTO categories VALUES (?,?,?)',[1, 'English Language Arts Help', 'Post anything to do with the ELA section.'])
    c.execute('INSERT INTO categories VALUES (?,?,?)',[2, 'Mathematics Section Help', 'Post anything to do with the math section.'])
    c.execute('INSERT INTO categories VALUES (?,?,?)',[3, 'School Talk', 'Post here to talk about specialized high schools.'])
    c.execute('INSERT INTO categories VALUES (?,?,?)',[4, 'Miscellaneous', 'Post here about anything else.'])

    db.commit()
    db.close() 


'''
topics_table = 'CREATE TABLE topics (userID INTEGER, catID INTEGER, topicID INTEGER, topic_date DATETIME, title TEXT);'
c.execute(topics_table)

posts_table = 'CREATE TABLE posts (userID INTEGER, catID INTEGER, topicID INTEGER, postID INTEGER, title TEXT, body TEXT, postDate DATETIME);'
c.execute(posts_table)

'''

def addTopic(ID, catID, title, body):

    db = sqlite3.connect(DIR)
    c = db.cursor()


    date = (datetime.datetime.now()).strftime('%Y-%m-%d')
    topicID = c.execute('SELECT max(topicID) FROM topics WHERE userID = {}'.format(ID)).fetchone()[0]

    if topicID == None:
        topicID = 0
    else:
        topicID = int(topicID) + 1


    c.execute('INSERT INTO topics VALUES (?,?,?,?,?)',[ID, catID, topicID, date, title])


    db.commit()
    db.close() 

    addPost(ID, catID, topicID, body)

'''
topics_table = 'CREATE TABLE topics (userID INTEGER, catID INTEGER, topicID INTEGER, topic_date DATETIME, title TEXT);'
c.execute(topics_table)

posts_table = 'CREATE TABLE posts (userID INTEGER, catID INTEGER, topicID INTEGER, postID INTEGER, postDate DATETIME, body TEXT);'
c.execute(posts_table)
'''

def addPost(ID, catID, topicID, body):

    db = sqlite3.connect(DIR)
    c = db.cursor()

    date = (datetime.datetime.now()).strftime('%Y-%m-%d')
    postID = c.execute('SELECT max(postID) FROM posts WHERE topicID = {}'.format(topicID)).fetchone()[0]

    if postID == None:
        postID = 0
    else:
        postID = int(postID) + 1


    c.execute('INSERT INTO posts VALUES (?,?,?,?,?,?)',[ID, catID, topicID, postID, date, body])

    db.commit()
    db.close() 


def addToPost (ID, catID, topicID, postID, body):

    db = sqlite3.connect(DIR)
    c = db.cursor()

    date = (datetime.datetime.now()).strftime('%Y-%m-%d')

    postID = c.execute('SELECT max(postID) FROM posts WHERE topicID = {} AND postID = {}'.format(topicID, postID)).fetchone()[0]

    postID = int(postID) + 1

    c.execute('INSERT INTO posts VALUES (?,?,?,?,?,?)',[ID, catID, topicID, postID, date, body])

    db.commit()
    db.close() 



def getAllTopicInCat(catID):
    db = sqlite3.connect(DIR)
    c = db.cursor()
    allTopic = c.execute('SELECT * FROM topics WHERE catID = {};'.format(catID)).fetchall()
    db.close()

    ret = []
    for each in allTopic:
        d = {}
        d['title'] = each[4]
        d['topicID'] = each[2]
        d['userID'] = each[0]
        ret.append(d)

    print ret


def getAllPostInTopic(catID, topicID):
    db = sqlite3.connect(DIR)
    c = db.cursor()
    allPost = c.execute('SELECT * FROM posts WHERE catID = {} AND topicID = {};'.format(catID, topicID)).fetchall()
    db.close()

    ret = []
    for each in allPost:
        d = {}
        d['body'] = each[5]
        d['userID'] = each[0]
        ret.append(d)

    return ret




if __name__ == '__main__':  
    tableCreation()

    #getAllPostInTopic(0, 0)

    #getAllTopicInCat(0)
    #addTopic(0, 0, 'Test Title', 'Body')

    #addToPost(0, 0, 0, 0, 'More stuff')

    '''
    addPost(ID, catID, topicID, body)
    addPost(ID, catID, topicID, body)

    addTopic(ID, catID, title, body)
    addPost(ID, catID, topicID, body)
    addPost(ID, catID, topicID, body)
    addPost(ID, catID, topicID, body)
    '''

    pass


