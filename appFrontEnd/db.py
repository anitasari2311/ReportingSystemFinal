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



	def db_server(serverId):

		#OCULUS
		if serverId == '1':
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

		#PHARMANETDB1
		elif serverId == '2':
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

		#XENIA
		elif serverId == '3':
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

		elif serverId == '4':
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

		elif serverId == '5':
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

		elif serverId == '6':
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

		elif serverId == '7':
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

		elif serverId == '8':
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

		elif serverId == '9':
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

		elif serverId == '10':
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

		elif serverId == '11':
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

		elif serverId == '12':
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

		elif serverId == '13':
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

		elif serverId == '14':
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

		elif serverId == '15':
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

		elif serverId == '16':
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

		elif serverId == '18':
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

		elif serverId == '19':
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

		elif serverId == '21':
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

		elif serverId == '22':
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

		elif serverId == '23':
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

		elif serverId == '24':
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

		elif serverId == '25':
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


		elif serverId == '26':
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

		elif serverId == '27':
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

		elif serverId == '28':
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

		elif serverId == '29':
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

		elif serverId == '30':
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









	# def db_template():

	# 	connection = mysql.connector.connect(
	# 	host='localhost',
	# 	database='cms_template',
	# 	user='root',
	# 	password='qwerty')
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
