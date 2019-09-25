import mysql.connector
from mysql.connector import Error

class databaseCMS:


	def db_request():
		
		connection = mysql.connector.connect(
		host='localhost',
		database='cms_request',
		user='root',
		password='qwerty')
		if connection.is_connected():
		    db_Info= connection.get_server_info()
		print("=======================================")
		print("Connected to MySQL database...",db_Info)
		print("=======================================")


		return connection


	def db_template():

		connection = mysql.connector.connect(
		host='localhost',
		database='cms_template',
		user='root',
		password='qwerty')
		if connection.is_connected():
		    db_Info= connection.get_server_info()
		print("=======================================")
		print("Connected to MySQL database...",db_Info)
		print("=======================================")


		return connection












	# def db_template():

	# 	connection = mysql.connector.connect(
	# 	host='localhost',
	# 	database='cms_template',
	# 	user='root',
	# 	password='mis301')
	# 	if connection.is_connected():
	# 		dbInfo = connection.get_server_info()
	# 	print("=======================================")
	# 	print("Connected to MySQL database...",db_Info)
	# 	print("=======================================")

	# 	return connection









# def close_db(e=None):
#     """If this request connected to the database, close the
#     connection.
#     """
#     db = g.pop("db", None)
#
#     if db is not None:
#         db.close()
