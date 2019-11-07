from flask import Flask, render_template, redirect, url_for, request, session, flash, json, jsonify, send_file
from base64 import b64encode
import auth
import pymysql
import mysql.connector
from mysql.connector import Error
import requests
import datetime
from db import databaseCMS


app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'
app.secret_key = 'ms4'

# @app.route('/Main_ReadReport/<uId>', methods=['POST'])
# def Main_ReadReport(uid):

@app.route('/getNamaFile/<kode_laporan>', methods=['GET'])
def getNamaFile(kode_laporan):
	try:
		db = databaseCMS.db_readReport()
		cursor = db.cursor()

		cursor.execute('SELECT namaFile from readreport WHERE report_id = "'+kode_laporan+'"')

		result = cursor.fetchone()

		return json.dumps(result)

	except Error as e :
		            print("Error while connecting file MySQL", e)
	finally:
	        #Closing DB Connection.
	            if(db.is_connected()):
	                cursor.close()
	                db.close()
	            print("MySQL connection is closed")

@app.route('/downloadReport/<kode_laporan>',methods=['POST','GET'])
def downloadReport(kode_laporan):

	
	namaF = requests.get('http://127.0.0.1:5004/getNamaFile/'+kode_laporan)
	namaResp = json.dumps(namaF.json())
	namaFi = json.loads(namaResp)
	namaFile = str(namaFi).replace("['","").replace("']","")


	print(namaFile)

	directory = 'C:/appReportingSystem/Schedule/'	
	try:

		return send_file(namaFile+'.xls', attachment_filename=namaFile+'.xls')

	except Exception  as e:
		print('FAILED TO SEND FILE')
		return str(e)


# @app.route('/downloadReport/<kode_laporan>',methods=['POST','GET'])
# def downloadReport(kode_laporan):
# 	directory = 'C:/appReportingSystem/Schedule/'
	
# 	try:
# 		return send_file(directory+kode_laporan+'.xls', attachment_filename=kode_laporan+'.xls')

# 	except Exception  as e:
# 		return str(e)

	
@app.route('/updateReport/<dataMS4>', methods=['POST','GET'])
def updateReport(dataMS4):
	if request.method == 'POST':
		loadData = json.loads(dataMS4)
		for row in loadData:
			kode_laporan = row['kode_laporan']
			org_id = row['org_id']
			namaFile = row['namaFile']
			PIC = row['PIC']
			Pen = row['Penerima']
			report_judul = row['reportJudul']



		lastProc = datetime.datetime.now()
		try:
			db = databaseCMS.db_readReport()
			cursor = db.cursor()
			cursor.execute("INSERT INTO readreport (report_id, report_judul, org_id, namaFile,\
	                             report_lastProcess, read_PIC, read_Penerima)\
	                             VALUES(%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE\
	                             report_judul='"+report_judul+"', org_id='"+org_id+"',\
	                             namaFile='"+namaFile+"', report_lastProcess='"+str(lastProc)+"',\
	                             read_PIC = '"+str(PIC)+"', read_Penerima='"+str(Pen)+"' ",(kode_laporan, report_judul,\
	                                org_id, namaFile, str(lastProc), str(PIC), str(Pen)))
			db.commit()
		except Error as e :
		            print("Error while connecting file MySQL", e)
		finally:
		        #Closing DB Connection.
		            if(db.is_connected()):
		                cursor.close()
		                db.close()
		            print("MySQL connection is closed")



@app.route('/viewReport/<email>', methods=['POST','GET'])
def viewReport(email):
	try:
		db = databaseCMS.db_readReport()
		cursor = db.cursor()

		cursor.execute('SELECT report_id, org_id, report_judul,namaFile, report_lastProcess\
		                FROM readreport WHERE read_PIC\
		                LIKE "%'+email+'%" OR read_penerima LIKE "%'+email+'%" ')

		listReport = cursor.fetchall()

		LR = []


		for row in listReport:
			a = requests.get('http://127.0.0.1:5001/getNamaOrg/'+str(row[1]))
			b = json.dumps(a.json())
			c = json.loads(b)
			for x in c:
				orgName = x['org_name']


			listDict={
			'reportId' : row[0],
			'orgName' : orgName,
			'orgId' : row[1],
			'reportJudul' : row[2],
			'namaFile' : row[3],
			'reportLastProc': row[4]
			}
			LR.append(listDict)

		result = json.dumps(LR)

		return result

	except Error as e :
		print("Error while connecting file MySQL", e)
	finally:
	#Closing DB Connection.
		if(db.is_connected()):
		        cursor.close()
		        db.close()
		print("MySQL connection is closed")


if __name__ == "__main__":
    app.run(debug=True, port='5004')