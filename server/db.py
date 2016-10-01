import sqlite3
import hashlib

class db(object):

	def __init__(self, db_path):
		if not os.path.isfile(db_path):
			raise FileNotFoundError
		self.db_path = db_path
		self.conn = None

	def connect(self):
		self.conn = sqlite3.connect(db_path)

	def close(self):
		self.conn.close()

	def check_credentials(self, email, password):
		hashed = hashlib.sha256(password)
		c = self.conn.cursor()
		c.execute('SELECT Count(*) FROM users WHERE email=? AND password=?', email, hashed.hexdigest())
		(number_of_rows, ) = c.fetchone()
		return number_of_rows == 1
		
