import sqlite3
import csv       
import hashlib
import uuid
import os


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


        db.commit()
        db.close()

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
