import sqlite3

conn = sqlite3.connect('matchr.db')

conn.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, fName TEXT, lName TEXT, gender TEXT, 
	image TEXT, description TEXT, email TEXT, password TEXT, bracePlacement INT, spaceOrTab INT, 
	indentAmount INT, varConvention INT, commentStyle INT, maxLineLength INT);''')

conn.execute('''CREATE TABLE relationship (relationshipScore INT, idFirst INT, 
	idSecond INT, statusFirst INT, statusSecond INT);''')

currentSession = null
conn.execute('''SELECT idSecond FROM relationship WHERE statusFirst = NULL AND idFirst = ? ORDER BY relationshipScore;''', currentSession)
conn.execute('''SELECT idFirst FROM relationship WHERE statusSecond = NULL AND idSecond = ? ORDER BY relationshipScore;''', currentSession)

conn.execute('''INSERT INTO users (fName, lName, gender, image, description, email, password, bracePlacement, spaceOrTab, indentAmount, 
	varConvention, commentStyle, maxLineLength) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', (fName, lName, gender, image, description, 
	email, password, bracePlacement, spaceOrTab, indentAmount, varConvention, commentStyle, maxLineLength)



print("opened db")

conn.close()

def functionName (arg1)
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
		int score = 0;
		if (row[1] == bracePlacement) {
			score += 5;
		}
		if (row[2] == spaceOrTab) {
			score += 5;
		}
		if (row[3] == indentAmount) {
			score += 3;
		}
		if (row[4] == varConvention) {
			score += 3;
		}
		if (row[5] == commentStyle) {
			score += 1;
		}
		if (row[6] == maxLineLength) {
			score += 1;
		}
	conn.execute('''INSERT INTO relationship (relationshipScore, idFirst, idSecond, statusFirst, statusSecond) values (?, ?, ?, ?, ?)''')
	