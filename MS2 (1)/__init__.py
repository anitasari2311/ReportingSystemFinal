from flask import Flask, render_template, redirect, url_for, request, json, session
from microservice2 import Template, Schedule
import pymysql
import mysql.connector
from mysql.connector import Error
import datetime

app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'
app.secret_key = 'session1'




@app.route('/cekTemplate')
def cekTemplate():


	return render_template('cekReport.html')



@app.route('/addTemplate')
def addTemplate():
	ms2T = Template()

	return render_template('addNewTemplate.html', listServer = ms2T.listNamaServer(), 
		listOrg = ms2T.listNamaOrganisasi(), listKategori = ms2T.listKategori(),
		listKodeReport = ms2T.listKodeReport())
	

@app.route('/prosesAddNewTemplate', methods =['POST','GET'])
def addNewTemplate():
	if request.method == 'POST':
		ms2T = Template()

		kode_laporan 		= request.form['kodeLaporan2']
		nomor_laporan		= request.form['noLap']

		server_id 			= request.form['server']
		report_judul 		= request.form['namaLaporan']
		report_deskripsi 	= request.form['filter']
		report_header 		= request.form['jmlHeader']
		report_footer 		= request.form['jmlFooter'] 
		report_jmlTampilan 	= request.form['jmlTampilan']
		report_periode 		= request.form['periode']
		report_createDate	= datetime.datetime.now()
		report_userUpdate 	= 'testUser'
		report_lastUpdate 	= datetime.datetime.now()
		report_aktifYN 		= 'Y'
		org_id 				= request.form['organisasi'] 
		ktgri_id 			= request.form['kategori']
		report_printAllYN 	= request.form['printAll']
		report_createdUser  = 'testUser'
		report_scheduleYN	= 'N'
		report_tujuan		= request.form['tujuan']


		kodeLapFix			= kode_laporan +'-'+ktgri_id+nomor_laporan
		
		ms2T.addNewTemplate(kodeLapFix, server_id, report_judul, report_deskripsi,
						report_header, report_footer,
						report_periode, report_createDate, report_userUpdate, 
		                report_lastUpdate, report_aktifYN, org_id, ktgri_id,
		                report_printAllYN, report_createdUser, report_scheduleYN,
		                report_jmlTampilan, report_tujuan)

		
		#return redirect(url_for('formatTemplate'))
		return render_template('formatTemplate.html', detailTemplate = ms2T.addDetailTemplate(kodeLapFix),
		kode_laporan=kodeLapFix)

		


#Edit format template yang sudah dibuat
@app.route('/formatTemplate', methods=['POST','GET'])
def formatTemplate():
	ms2T = Template()	
	if request.method == 'POST':

		ms2T = Template()
		
		kode_laporan 		= request.form['kodeLaporan']

		
		return render_template('formatTemplate.html', detailTemplate = ms2T.addDetailTemplate(kode_laporan),
			kode_laporan=kode_laporan, detailFormatTemplate = ms2T.detailFormatTemplate(kode_laporan))
	# return redirect(url_for('addTemplate'))
	return render_template('perubahan.html', listKodeReport = ms2T.listKodeReport())

#Menyimpan format Template
@app.route('/prosesFormatTemplate', methods = ['POST','GET'])
def prosesFormatTemplate():
	if request.method == 'POST':

		ms2T = Template()

		#Template
		judul = request.form['namaReport']
		periode = request.form['periode']
		printAll = request.form['printAll']
		jmlHeader = request.form['jmlHeader']
		jmlFooter = request.form['jmlFooter']
		# jmlKolom = request.form['jmlKolom']

		#Header
		kol = []
		lok = []
		forK = []
		lebK = []
		kode_laporan = request.form['kodLap']
		# kolom = request.form['kolom'] 
		# lokasi = request.form['lokasi']
		# formatKolom = request.form['formatKolom']
		# lebarKolom = request.form['lebar']

		#Footer
		kolF = []
		kolF1 = []
		kolF2 = []
		kolomFooter = request.form['kolomFooter']



		for kolom in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']:
			
			if (request.form[kolom] is not  None) and (request.form[kolom] is not ''):
				kol.append(request.form[kolom])

		for lokasi in ['lokasi1', 'lokasi2', 'lokasi3', 'lokasi4', 'lokasi5', 'lokasi6', 'lokasi7', 'lokasi8', 'lokasi9', 'lokasi10', 'lokasi11', 'lokasi12', 'lokasi13', 'lokasi14', 'lokasi15', 'lokasi16', 'lokasi17', 'lokasi18', 'lokasi19', 'lokasi20']:
			
			if (request.form[lokasi] is not  None) and (request.form[lokasi] is not ''):
				lok.append(request.form[lokasi])

		for formatKol in ['formatKolom1', 'formatKolom2', 'formatKolom3', 'formatKolom4', 'formatKolom5', 'formatKolom6', 'formatKolom7', 'formatKolom8', 'formatKolom9', 'formatKolom10', 'formatKolom11', 'formatKolom12', 'formatKolom13', 'formatKolom14', 'formatKolom15', 'formatKolom16', 'formatKolom17', 'formatKolom18', 'formatKolom19', 'formatKolom20']:
			
			if (request.form[formatKol] is not  None) and (request.form[formatKol] is not ''):
				forK.append(request.form[formatKol])

		for lebarKol in ['lebar1', 'lebar2', 'lebar3', 'lebar4', 'lebar5', 'lebar6', 'lebar7', 'lebar8', 'lebar9', 'lebar10', 'lebar11', 'lebar12', 'lebar13', 'lebar14', 'lebar15', 'lebar16', 'lebar17', 'lebar18', 'lebar19', 'lebar20']:
			
			if (request.form[lebarKol] is not  None) and (request.form[lebarKol] is not ''):
				lebK.append(request.form[lebarKol])



		for footer in ['kolFooter1', 'kolFooter2']:
			if (kolomFooter is not None) and (kolomFooter is not ''):
				kolF.append(kolomFooter)


		# for check1 in ['B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1', 'J1', 'K1', 'L1', 'M1', 'N1']: 




		ms2T.saveFormatTemplate(kode_laporan, kol, lok, forK, lebK)#, kol, judul, periode, printAll, jmlHeader, jmlFooter, jmlKolom)

		return redirect(url_for('menu'))
		# return render_template('menu.html', kode_laporan=kode_laporan)


      






#####	#	#	####	#####	#	#	
#	#	#	#	#		#	#	  #
#	#	#	#	####	####	  #
######	#####	####	#	#	  #





@app.route('/insertQuery')
def insertQuery():
	ms2T = Template()



	return render_template('insertQuery.html', clearQ = ms2T.insQuery())


@app.route('/prosesInsertQuery', methods=['POST'])
def prosesInsertQuery():
	ms2T = Template()
	quer = []
	kode_laporan = request.form['kodLap']
	if request.method == 'POST':
		for query in ['query1', 'query2', 'query3', 'query4', 'query5', 'query6', 'query7', 'query8', 'query9', 'query10', 'query11', 'query12', 'query13', 'query14']:
			
			if (request.form[query] is not  None) and (request.form[query] is not ''):
				quer.append(request.form[query])

		ms2T.addQuery(kode_laporan,quer)
		return redirect(url_for('menu'))


@app.route('/editQuery', methods = ['POST', 'GET'])
def editQuery():
	ms2T= Template()

	if request.method == 'POST':
		ms2T = Template()

		kode_laporan = request.form['kodLap']
		kode_laporan.upper()


		return render_template('insertQuery.html', editQ = ms2T.viewEditQuery(kode_laporan),
								kode_laporan=kode_laporan)


	return render_template('perubahan.html', listKodeReportQuery=ms2T.listKodeReportQuery())


#########	#######		#	#
#			#			#	#
#########	#			#####
		#	#			#	#
#########	#######		#	#

@app.route('/addSchedule')
def addSchedule():
	ms2T = Template()
	ms2S = Schedule()

	return render_template('addNewSchedule.html', listKodeReportS = ms2T.listKodeReportAddNewSchedule(),
		listPIC = ms2S.namaPIC(), listPen = ms2S.namaPenerima(), 
		)

@app.route('/prosesAddNewSchedule', methods=['POST','GET'])
def addNewSchedule():
	print( "===============/prosesAddNewSchedule===============")
	if request.method =='POST':
		ms2S = Schedule()

		kode_laporan = request.form['valKode']
		header = request.form['header']
		keterangan = request.form['keterangan']
		note = request.form['note']
		reportPIC = ''
		reportPenerima = ''
		grouping = request.form['grouping']
		jadwalBln = ''
		jadwalHari = ''
		jadwalTgl = ''
		queryId = ''
		org = ms2S.getOrgLaporan(kode_laporan)
		kategori = ms2S.getKategoriLaporan(kode_laporan)
		aktifYN = ''
		lastUpdate = ''

		for checkHari in ['senin','selasa','rabu','kamis','jumat','sabtu','minggu']:
			if request.form.get(checkHari) is not None:
				if jadwalHari == '':
					jadwalHari += request.form.get(checkHari)
				else:
					jadwalHari +=  ", "+request.form.get(checkHari)
		print("Hari ",jadwalHari)

		for checkBulan in ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']:
			if request.form.get(checkBulan) is not None:
				if jadwalBln == '':
					jadwalBln += request.form.get(checkBulan)
				else:
					jadwalBln +=  ", "+request.form.get(checkBulan)
		print ("Bulan ",jadwalBln) 

		for checkTgl in ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29', 't30', 't31']:
			if request.form.get(checkTgl) is not None:
				if jadwalTgl == '':
					jadwalTgl += request.form.get(checkTgl)
				else:
					jadwalTgl +=  ", "+request.form.get(checkTgl)
		print ("Tanggal ",jadwalTgl)


		for checkPIC in ms2S.namaPIC():
			#print(checkPIC[0])
			if request.form.get(checkPIC[0]) is not None:
				if reportPIC == '':
					reportPIC += checkPIC[2]
				else:
					reportPIC += ", "+checkPIC[2]
		print ("PIC ",reportPIC)

		for checkPen in ms2S.namaPenerima():
			#print(checkPen[2])
			if request.form.get(checkPen[2]) is not None:
			    if reportPenerima == '':
			        reportPenerima += checkPen[2]
			    else:
			        reportPenerima += ", "+checkPen[2]
		print ("Penerima ", reportPenerima)      
		
		ms2S.addSchedule( kode_laporan, header, keterangan, note, reportPIC, reportPenerima, 
			grouping, jadwalBln, jadwalHari, jadwalTgl, org, kategori)

		return redirect(url_for('menu'))


# Menu edit Schedule (Tampilan pilih kode Laporan)
@app.route('/editSchedule', methods=['POST', 'GET'])
def formEditSchedule():
	
	ms2T = Template()
	ms2S = Schedule()
	
	if request.method == 'POST':

		kode_laporan = request.form['valKode']

		ms2T = Template()
		ms2S = Schedule()
		ms2S.listMaker(kode_laporan)

		# print(kode_laporan)
		return render_template('editSchedule2.html', kode_laporan=kode_laporan,
							detailSchedule = ms2S.showDetailSchedule(kode_laporan),
							listPIC = ms2S.namaPIC(), listPen = ms2S.namaPenerima())
		##return render_template('editSchedule.html', detailSchedule = ms2S.showDetailSchedule(kode_laporan))
		#return redirect (url_for('editSchedule', kode_laporan=kode_laporan,
							# detailSchedule = ms2S.showDetailSchedule()))

	
	return render_template('editSchedule.html', listKodeLap = ms2T.listKodeReportEditSchedule())	

# Untuk menampilkan detail Schedule
# @app.route('/prosesViewEditSchedule', methods =['POST','GET'])
# def start():
# 	print( "===============/prosesViewEditSchedule===============")
# 	ms2T = Template()
# 	ms2S = Schedule()
	
# 	if request.method == 'POST':
		
# 		kode_laporan = request.form['valKode']
		
# 		ms2T = Template()
# 		ms2S = Schedule()
# 		ms2S.listMaker(kode_laporan)

# 		#return redirect (url_for('formEditSchedule', kode_laporan=kode_laporan))
# 		# return redirect (url_for('editSculhede', kode_laporan=kode_laporan,
# 		# 					detailSchedule = ms2S.showDetailSchedule(kode_laporan)))
# 		return render_template('editSchedule2.html', kode_laporan=kode_laporan,
# 							detailSchedule = ms2S.showDetailSchedule(kode_laporan),
# 							listPIC = ms2S.namaPIC(), listPen = ms2S.namaPenerima())
	

# Menyimpan perubaha schedule
@app.route('/prosesSimpanEditSchedule', methods=['POST', 'GET'])
def prosesSimpanEditSchedule():
	print( "===============/prosesSimpanEditSchedule===============")
	ms2S = Schedule()


	if request.method == 'POST':
		kode_laporan = request.form['kodLap2']
		header = request.form['header']
		keterangan = request.form['keterangan']
		note = request.form['note']
		grouping = request.form['grouping']
		reportPIC = ''
		reportPenerima = ''
		jadwalBln = ''
		jadwalHari = ''
		jadwalTgl = ''
		aktifYN = ''
		lastUpdate  = datetime.datetime.now()


		for checkHari in ['senin','selasa','rabu','kamis','jumat','sabtu','minggu']:
			if request.form.get(checkHari) is not None:
				if jadwalHari == '':
					jadwalHari += request.form.get(checkHari)
				else:
					jadwalHari +=  ", "+request.form.get(checkHari)
		print("Hari ",jadwalHari)

		for checkBulan in ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']:
			if request.form.get(checkBulan) is not None:
				if jadwalBln == '':
					jadwalBln += request.form.get(checkBulan)
				else:
					jadwalBln +=  ", "+request.form.get(checkBulan)
		print ("Bulan ",jadwalBln) 

		for checkTgl in ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29', 't30', 't31']:
			if request.form.get(checkTgl) is not None:
				if jadwalTgl == '':
					jadwalTgl += request.form.get(checkTgl)
				else:
					jadwalTgl +=  ", "+request.form.get(checkTgl)
		print ("Tanggal ",jadwalTgl)

		for checkPIC in ms2S.namaPIC():
			#print(checkPIC[0])
			if request.form.get(checkPIC[0]) is not None:
				if reportPIC == '':
					reportPIC += checkPIC[2]
				else:
					reportPIC += ", "+checkPIC[2]
		print ("PIC ",reportPIC)

		for checkPen in ms2S.namaPenerima():
			#print(checkPen[2])
			if request.form.get(checkPen[2]) is not None:
			    if reportPenerima == '':
			        reportPenerima += checkPen[2]
			    else:
			        reportPenerima += ", "+checkPen[2]
		print ("Penerima ", reportPenerima)      

		ms2S.editSchedule(kode_laporan, header, keterangan, note, jadwalBln, jadwalHari, jadwalTgl, reportPIC, reportPenerima, 
                    lastUpdate, aktifYN)
		return redirect(url_for('menu'))



#############################################          MODIFY USER
@app.route('/changePass')
def modifyUser():
	return render_template('changePass.html')
	
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/menu')
def menu():
    return render_template('home.html')

@app.route('/editProfile')
def editProfile():
	return render_template('changePass.html')


if __name__ == "__main__":
    app.run(debug=True)