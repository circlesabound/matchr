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
    email = 'j@j.com'
    cursor = conn.execute('''SELECT id, bracePlacement, spaceOrTab, indentAmount, varConvention, commentStyle, maxLineLength 
        FROM users WHERE email = ?;''', (email,))
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
        braceDifference = abs(bracePlacement - row[1])
        spaceOrTabDifference = abs(spaceOrTab - row[2])
        indentAmountDifference = min(indentAmount - row[3], 40)
        varConventionDifference = abs(varConvention - row[4])
        commentStyleDifference = abs(commentStyle - row[5])
        maxLineLengthDifference = min(maxLineLength - row[6], 100)

        if (braceDifference == 0):
            braceDifference += 1

        if (spaceOrTabDifference == 0):
            spaceOrTabDifference += 1

        if (indentAmountDifference == 0):
            indentAmountDifference += 1

        if (varConventionDifference == 0):
            varConventionDifference += 1

        if (commentStyleDifference == 0):
            commentStyleDifference += 1

        if (maxLineLengthDifference == 0):
            maxLineLengthDifference += 1

        score += 1/(braceDifference) * 30
        score += 1/(spaceOrTabDifference) * 30
        score += 1/(indentAmountDifference) * 15
        score += 1/(varConventionDifference) * 15
        score += 1/(commentStyleDifference) * 5
        score += 1/(maxLineLengthDifference) * 5
        score = int(round(score))
        print(score)
        #insert calculated score, id of latest user in earlier query which is 'first' user, row[0] which is id of 'second' user
        conn.execute('''INSERT INTO relationship (relationshipScore, idFirst, idSecond) values (?, ?, ?);''',
                     (score, id, row[0]))    

def generateFirstUsers (conn):
    conn.execute('''INSERT INTO users (fName, lName, gender, age, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('James', 'Smith', 'm', 25, 'dfs', 'hi', 'a@a.com', 'asd', -20, 20, 4, 1, 1, 45);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, age, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Jane', 'Jones', 'f', 20, 'dfs', 'asd', 'b@b.com', 'bsd', -10, 10, 4, 1, 1, 45);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, age, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Janet', 'Jacob', 'f', 32, 'qwe', 'asd', 'c@c.com', 'bsd', 0, 0, 3, 1, 1, 45);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, age, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Kathy', 'Kim', 'f', 19, 'rty', 'jkd', 'd@d.com', 'bsd', 10, 10, 2, 1, 1, 45);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, age, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Lisa', 'Jones', 'f', 28, 'testing', 'lmd', 'e@e.com', 'bsd', 20, -20, 4, 0, 1, 45);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, age, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Philip', 'Skat', 'm', 23, 'checking', 'nads', 'f@f.com', 'bsd', 5, -10, 4, 1, 0, 45);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, age, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Karen', 'Rea', 'f', 25, 'dfs', 'work', 'g@g.com', 'bsd', -5, -5, 0, 1, 0, 55);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, age, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Pam', 'Manthrey', 'f', 22, 'slate', 'dfsa', 'h@h.com', 'bsd', 10, 1, 4, 0, 0, 30);''')
    conn.execute('''INSERT INTO users (fName, lName, gender, age, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES ('Trisha', 'Kam', 'f', 20, 'dka', 'enm', 'i@i.com', 'bsd', 15, 0, 3, 0, 1, 25);''')

def generateNewUser (conn):
    # plain text password is "asdf"
    conn.execute('''INSERT INTO users (fName, lName, gender, age, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
        varConvention, commentStyle, maxLineLength) VALUES ('Sarah', 'Adam', 'f', 35, 'csad', 'i love code', 'j@j.com',
        'f0e4c2f76c58916ec258f246851bea091d14d4247a2fc3e18694461b1816e13b',
        0, 0, 3, 1, 1, 15);''')
    conn.commit()


if os.path.isfile('matchr.db'):
    print("removing old db")
    os.remove('matchr.db')

conn = sqlite3.connect('matchr.db')

conn.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, fName TEXT, lName TEXT, gender TEXT, age INT, 
    image BLOB, description TEXT, email TEXT, password TEXT, bracePlacement INT, spaceOrTab INT, 
    indentAmount INT, varConvention INT, commentStyle INT, maxLineLength INT);''')

conn.execute('''CREATE TABLE relationship (id INTEGER PRIMARY KEY, relationshipScore INT, idFirst INT, 
    idSecond INT, statusFirst INT, statusSecond INT);''')

currentSession = (None,)
"""
conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
    varConvention, commentStyle, maxLineLength) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', (fName, lName, gender, image, description, 
    email, password, bracePlacement, spaceOrTab, indentAmount, varConvention, commentStyle, maxLineLength))
"""

print("db created")

# generateFirstUsers(conn)

# generateNewUser(conn)

# generateRelationships(conn)

# cursor = conn.execute('''SELECT idSecond FROM relationship WHERE statusFirst = NULL AND idFirst = ? ORDER BY relationshipScore DESC;''', currentSession)
# print(cursor.fetchall())
# cursor = conn.execute('''SELECT idFirst FROM relationship WHERE statusSecond = NULL AND idSecond = ? ORDER BY relationshipScore DESC;''', currentSession)
# print(cursor.fetchall())
# cursor = conn.execute("SELECT Count(*) FROM users")
# print(cursor.fetchall())

conn.close()
