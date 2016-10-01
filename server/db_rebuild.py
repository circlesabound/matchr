#!/usr/bin/python3

import sqlite3
import os.path
import os

#function call order
#1) generateFirstUsers()
#2) generateNewUser()
#3) generateRelationships()

#generates relationships with all existing users
def generateRelationships (conn):
    #assuming this is called right after latest user created - get latest user
    cursor = conn.execute('''SELECT id, bracePlacement, spaceOrTab, indentAmount, varConvention, commentStyle, maxLineLength 
        FROM users WHERE email = ?;''', email)
    for row in cursor:
        id = row[0]
        bracePlacement = row[1]
        spaceOrTab = row[2]
        indentAmount = row[3]
        varConvention = row[4]
        commentStyle = row[5]
        maxLineLength = row[6]  
    cursor = conn.execute('''SELECT id, bracePlacement, spaceOrTab, indentAmount, varConvention, commentStyle, maxLineLength FROM users;''')
    for row in cursor:
        score = 0
        if row[1] == bracePlacement:
            score += 5
        if row[2] == spaceOrTab:
            score += 5
        if row[3] == indentAmount:
            score += 3
        if row[4] == varConvention:
            score += 3
        if row[5] == commentStyle:
            score += 1
        if row[6] == maxLineLength:
            score += 1
        #insert calculated score, id of latest user in earlier query which is 'first' user, row[0] which is id of 'second' user
        conn.execute('''INSERT INTO relationship (relationshipScore, idFirst, idSecond) values (?, ?, ?, ?, ?);''', (score, id, row[0]))    

def generateFirstUsers (conn):
    conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('James', 'Smith', 'm', 'dfs', 'hi', 'a@a.com', 'asd', -50, 4, 4, 1, 1, 45);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Jane', 'Jones', 'f', 'dfs', 'asd', 'b@b.com', 'bsd', -100, 0, 4, 1, 1, 45);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Janet', 'Jacob', 'f', 'qwe', 'asd', 'c@c.com', 'bsd', 0, 0, 3, 1, 1, 45);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Kathy', 'Kim', 'f', 'rty', 'jkd', 'd@d.com', 'bsd', -30, 1, 2, 1, 1, 45);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Lisa', 'Jones', 'f', 'testing', 'lmd', 'e@e.com', 'bsd', -70, 0, 4, 0, 1, 45);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Philip', 'Skat', 'm', 'checking', 'nads', 'f@f.com', 'bsd', 40, 0, 4, 1, 0, 45);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Karen', 'Rea', 'f', 'dfs', 'work', 'g@g.com', 'bsd', 55, 0, 4, 1, 0, 55);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Pam', 'Manthrey', 'f', 'slate', 'dfsa', 'h@h.com', 'bsd', 70, 1, 4, 0, 0, 30);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Trisha', 'Kam', 'f', 'dka', 'enm', 'i@i.com', 'bsd', 80, 0, 3, 0, 1, 25);''')

def generateNewUser (conn):
    # plain text password is "asdf"
    conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
        varConvention, commentStyle, maxLineLength) VALUES ('Sarah', 'Adam', 'f', 'csad', 'i love code', 'j@j.com',
        'f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b',
        0, 0, 3, 1, 1, 15);''')
    conn.commit()

def test1():
    import db

    database = db.db('matchr.db')
    database.connect()
    ud = {}
    ud["first_name"] = "John"
    ud["last_name"] = "Howard"
    ud["gender"] = 'm'
    ud["image"] = None
    ud["description"] = "I used to be PM"
    ud["email"] = "j.howard@gov.au"
    ud["password"] = "maddj"
    ud["brace_placement"] = -50
    ud["space_or_tab"] = -50
    ud["indent_amount"] = 4
    ud["var_convention"] = -50
    ud["comment_style"] = -50
    ud["max_line_length"] = 120
    try:
        database.add_new_user(ud)
        print("welcome john howard")
    except ValueError:
        print("John howard already registed")
    finally:
        print(database.get_user_details(database.get_id_from_email(ud["email"])))


if os.path.isfile('matchr.db'):
    print("removing old db")
    os.remove('matchr.db')

conn = sqlite3.connect('matchr.db')

conn.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, fName TEXT, lName TEXT, gender TEXT, 
    image BLOB, description TEXT, email TEXT, password TEXT, bracePlacement INT, spaceOrTab INT, 
    indentAmount INT, varConvention INT, commentStyle INT, maxLineLength INT);''')

conn.execute('''CREATE TABLE relationship (relationshipScore INT, idFirst INT, 
    idSecond INT, statusFirst INT, statusSecond INT);''')

currentSession = (None,)
conn.execute('''SELECT idSecond FROM relationship WHERE statusFirst = NULL AND idFirst = ? ORDER BY relationshipScore DESC;''', currentSession)
conn.execute('''SELECT idFirst FROM relationship WHERE statusSecond = NULL AND idSecond = ? ORDER BY relationshipScore DESC;''', currentSession)

"""
conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', (fName, lName, gender, image, description, 
    email, password, bracePlacement, spaceOrTab, indentAmount, varConvention, commentStyle, maxLineLength))
"""

print("db created")

generateNewUser(conn)

cursor = conn.execute("SELECT Count(*) FROM users")
print(cursor.fetchall())

conn.close()

test1()
