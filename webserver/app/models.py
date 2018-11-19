from config import Config
from app import login, engine



class Customer(object):
	def __init__(self, fetch):
			self.username = fetch.username
			self.uid = fetch.uid
			self.password = fetch.password
			self.gender = fetch.gender
			self.birth_date = fetch.birth_date
			self.phone_number = fetch.phone_number
			self.address = fetch.address

	def is_active(self):
		return True

	def is_authenticated(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.username


@login.user_loader
def load_user(username):
	return find_user(engine, username)

@staticmethod
def insert(engine, table, uid, phone_number, address, gender, birth_date, password, username):
	assert type(table) == str
	sql_text = """
	INSERT INTO '%s'
	VALUES ('%s', '%s','%s','%s','%s','%s','%s')
	""" % (table, uid, phone_number, address, gender, birth_date, password, username)
	try:
		engine.excute(sql_text)
	except:
		print("Invalid insertion")

def find_user(engine, data):
	sql_text = '''
		SELECT *
		FROM users
		WHERE username = '%s'
	''' % (data)
	cursor = engine.execute(sql_text)
	fetch = cursor.first()
	cursor.close()
	return fetch


def find_user_id(engine, data):
	sql_text = '''
			SELECT *
			FROM users
			WHERE uid = '%s'
		''' % (data)
	cursor = engine.execute(sql_text)
	fetch = cursor.first()
	cursor.close()
	return fetch