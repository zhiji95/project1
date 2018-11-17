from app import login, app, engine
"""from config import Config
"""
def find_name_password(conn, data):
	sql_text = '''
		SELECT username, password
		FROM users
		WHERE username = '%s'
	''' % (data)
	cursor = conn.execute(sql_text)
	fetch = cursor.first()
	cursor.close()
	return fetch

