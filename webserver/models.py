from app import login, engine
"""from config import Config
"""


class User(object):
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
		return self.uid

@staticmethod
def load_user(uid):
	return find_user_id(engine, uid)


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
