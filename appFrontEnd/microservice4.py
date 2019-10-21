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


@app.route('/downloadReport/<kode_laporan>',methods=['POST','GET'])
def downloadReport(kode_laporan):

	
	try:
		return send_file(kode_laporan+'.xls', attachment_filename=kode_laporan+'.xls')

	except Exception  as e:
		return str(e)




	
@app.route('/updateReport/<kode_laporan>/<namaFile>/')
def updateReport():
	lastProc = datetime.datetime.now()
	try:
		db = databaseCMS.db_readReport()
		cursor = db.cursor()
		cursor.execute("INSERT INTO readreport (report_id, report_judul, org_id, namaFile,\
                             report_lastProcess, read_PIC)\
                             VALUES(%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE\
                             report_judul='"+report_judul"', org_id='"+org_id+"',\
                             namaFile='"+namaFile+"', report_lastProcess='"+lastProc+"' ",(kode_laporan, judul_laporan,\
                                org_id, namaFile, lastProc, PIC))

# def ListenNewSchedul;


if __name__ == "__main__":
    app.run(debug=True, port='5004')