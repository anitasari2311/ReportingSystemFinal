from flask import Flask, render_template, redirect, url_for, request, session, flash, json, jsonify
from base64 import b64encode
import auth
# from microservice1 import RequestLaporan
# from templatelaporan import TemplateLaporan
import pymysql
import mysql.connector
from mysql.connector import Error
import requests
import datetime
# import os
# import urllib.request
#from PIL import Image

app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'
app.secret_key = 'frontEnd'
url1 = "http://127.0.0.1:5001/"





##########################                  LOGIN                          ############################


@app.route('/login', methods=['POST','GET'])
def login():
    
    if request.method == 'POST':
        
        auth.auth_login()
        return auth.auth_login()

    return render_template('ms1login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/changePass')
def changePass():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        a = session['user_id']
        return render_template('ms1changePass.html')

@app.route('/sendDataPassword', methods=['GET', 'POST'])
def sendDataPassword():
    if request.method == 'POST':
        uId = session['user_id']
        passwordLama = request.form['oldPass']
        passwordBaru = request.form['newPass']
        konfirmasiPassword = request.form['confPass']

        request_data = {
            'uId' : uId,
            'passLama' : passwordLama,
            'passBaru' : passwordBaru,
            'konfPass' : konfirmasiPassword
        }

        dataRequest = json.dumps(request_data)

        if session.get('position') == 'User':
            requests.post('http://127.0.0.1:5001/updateDataPassword/'+dataRequest)
            return redirect(url_for('user'))
        elif session.get('position') == 'Admin' :
            requests.post('http://127.0.0.1:5001/updateDataPassword/'+dataRequest)
            return redirect(url_for('admin'))
        else:
            requests.post('http://127.0.0.1:5001/updateDataPassword/'+dataRequest)
            return redirect(url_for('spv'))


#=========================================================================================
#=========================================================================================
#=========================[           USER             ]==================================
#=========================================================================================
#=========================================================================================


@app.route('/user', methods=['POST','GET'])
def user():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        now = datetime.datetime.now()

        day = now.strftime("%A")
        date = now.strftime("%H:%M:%S")

        return render_template('ms1home1.html', day=day, date=date)

#================[List request user]=================
@app.route('/list', methods = ['POST','GET'])
def list():
    if session.get('user_id') is None:
        return render_template('ms1Login.html')
    else:
        a = session['user_id']

        listReq = requests.get(''.join(['http://127.0.0.1:5001/listRequestUser/'+a]))
        listResp = json.dumps(listReq.json())
        loadListReq = json.loads(listResp)

        return render_template('ms1listReq.html', listReqUser = loadListReq)

#==============[List request yang telah selesai ]===========
@app.route('/listFinished', methods = ['POST','GET'])
def listFinished():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        uId = session['user_id']

        listFinished = requests.get(''.join(['http://127.0.0.1:5001/listFinished/'+uId]))
        finishedResp = json.dumps(listFinished.json())
        loadFinished = json.loads(finishedResp)

        return render_template('ms1listFinished.html', listKelar = loadFinished)

#============[Read Report] CODINGAN BARU========================
@app.route('/readReport', methods=['POST','GET'])
def readReport():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        uId = session['user_id']

        eml = requests.get('http://127.0.0.1:5001/getEmail/'+uId)
        emlResp = json.dumps(eml.json())
        loadEmail = json.loads(emlResp)
        for i in loadEmail:
            emailUser = i[0]

        print('Read Report: ',emailUser)

        listRep = requests.get('http://127.0.0.1:5002/viewReport/'+emailUser)
        listResp = json.dumps(listRep.json())
        loadListReport = json.loads(listResp)

        print(loadListReport)
        return render_template('ms4viewReport.html', readReport = loadListReport)

#================[Saat user memberi rating]=================
@app.route('/sendRating', methods=['POST','GET'])
def sendRating():
    if request.method == 'POST':

        data = {
        'request_id' : request.form['finishRat'],
        'rating' : request.form['fRating'],
        'keterangan' : request.form['inputKeterangan'] 
        }

        dataRating = json.dumps(data)

        requests.post('http://127.0.0.1:5001/finishRating/'+dataRating)


        return redirect(url_for('listFinished'))

#================[Menampilkan layar Request Laporan]=================
@app.route('/newRequest', methods = ['GET','POST'])
def newRequest():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:

        org = requests.get(url1+'namaOrganisasi')
        orgResp=json.dumps(org.json())
        loadOrg = json.loads(orgResp)

        cat = requests.get('http://127.0.0.1:5001/namaDept')
        catResp = json.dumps(cat.json())
        loadCat = json.loads(catResp)

        PIC = requests.get('http://127.0.0.1:5001/namaPIC')
        picResp = json.dumps(PIC.json())
        loadPIC = json.loads(picResp)

        Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
        penResp = json.dumps(Pen.json())
        loadPen = json.loads(penResp)


        return render_template('ms1requestLaporan.html', listOrg = loadOrg, 
                                listDept = loadCat, listPIC = loadPIC, listPen = loadPen)

#================[Mengirim data request ke MS1/addNewRequest]================= 
@app.route('/sendDataRequest', methods=['POST','GET'])
def sendDataRequest():
    PIC = requests.get('http://127.0.0.1:5001/namaPIC')
    picResp = json.dumps(PIC.json())
    loadPIC = json.loads(picResp)

    Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
    penResp = json.dumps(Pen.json())
    loadPen = json.loads(penResp)

    if request.method == 'POST':
        reqSch_hari = ''
        reqSch_bulan = ''
        reqSch_tanggal = ''
        reqSch_reportPIC = ''
        reqSch_penerima = ''

        title = request.form['inputTitle']
        purpose = request.form['inputPurpose']
        description = request.form['keteranganlaporan']
        Organization = request.form['Organization']
        Department = request.form['Department']
        Display = request.form['inputDisplay']
        Period = request.form['inputPeriode']
        deadline = request.form['deadline']
        file = ''

        for checkHari in ['mon','tue','wed','thu','fri','sat','sun']:
            if request.form.get(checkHari) is not None:
                if reqSch_hari == '':
                    reqSch_hari += request.form.get(checkHari)
                else:
                    reqSch_hari +=  ", "+request.form.get(checkHari)
        print(reqSch_hari)

        for checkBulan in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            if request.form.get(checkBulan) is not None:
                if reqSch_bulan == '':
                    reqSch_bulan += request.form.get(checkBulan)
                else:
                    reqSch_bulan +=  ", "+request.form.get(checkBulan)
        print (reqSch_bulan) 

        for checkTgl in ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29', 't30', 't31']:
            if request.form.get(checkTgl) is not None:
                if reqSch_tanggal == '':
                    reqSch_tanggal += request.form.get(checkTgl)
                else:
                    reqSch_tanggal +=  ", "+request.form.get(checkTgl)
        print (reqSch_tanggal)

        
        ####
        for checkPIC in loadPIC:
            
            if request.form.get(checkPIC['Id']) is not None:
                if reqSch_reportPIC == '':
                    reqSch_reportPIC += checkPIC['Email']
                else:
                    reqSch_reportPIC += ", "+checkPIC['Email']
        print (reqSch_reportPIC)

        for checkPen in loadPen:
            
            if request.form.get(checkPen['Email']) is not None:
                if reqSch_penerima == '':
                    reqSch_penerima += checkPen['Email']
                else:
                    reqSch_penerima += ", "+checkPen['Email']
        print (reqSch_penerima)


        
        

        request_data = {
        'ProgId' : None,
        'UserId' : session['user_id'],
        'OrgId' : Organization,
        'KtgriId' : Department,
        'kodLap' : None,
        'Judul' : title,
        'Deskripsi' : description,
        'Tujuan' : purpose,
        'Tampilan' : Display,
        'Periode' : Period,
        'Deadline' : deadline,
        'File' : None,
        'PIC' : None,
        'Hari' : reqSch_hari,
        'Bulan' : reqSch_bulan,
        'Tanggal' : reqSch_tanggal,
        'schOrg' : Organization,
        'schKtgri' : Department,
        'schLastUpdate' : None,
        'schPIC' : reqSch_reportPIC,
        'schPenerima' : reqSch_penerima
        }

        dataRequest = json.dumps(request_data)

        requests.post('http://127.0.0.1:5001/addNewRequest/'+dataRequest)

        return redirect(url_for('list'))

#==[Ketika user membatalkan request. Mengirim ReqID yang dicancel ke MS1/cancR]========
@app.route('/cancelRequest', methods=['POST','GET'])
def cancelRequest():

    if request.method == 'POST':

        rId  = request.form['btnCancel']

        data={
        'request_id' : rId
        }

        dataFix = json.dumps(data)


        requests.post('http://127.0.0.1:5001/cancR/'+dataFix)




        return redirect(url_for('list'))

#================[Menampilkan kode laporan yang ingin di edit]=================
#================[Menampilkan form edit laporan]=================
@app.route('/editReport', methods=['POST','GET'])
def editReport():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        uId = session['user_id']
        listReportId = requests.get('http://127.0.0.1:5001/getReportIdEdit/'+uId)
        listReportIdResp = json.dumps(listReportId.json())
        loadListRep = json.loads(listReportIdResp)
        
        if request.method == 'POST':
            kode_laporan = request.form['kodeLaporan']

            sendKodeLaporan = requests.get(''.join(['http://127.0.0.1:5001/getCurrentDisplay/'+kode_laporan]))
            KodeLaporanResp = json.dumps(sendKodeLaporan.json())
            loadLap = json.loads(KodeLaporanResp)

            PIC = requests.get('http://127.0.0.1:5001/namaPIC')
            picResp = json.dumps(PIC.json())
            loadPICe = json.loads(picResp)

            Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
            penResp = json.dumps(Pen.json())
            loadPene = json.loads(penResp)



            return render_template("ms1Edit2.html", listcurrentdisplay = loadLap, 
                                    listPIC = loadPICe, listPen = loadPene, kode_laporan=kode_laporan)

        return render_template('ms1Edit2.html', listKodeReport = loadListRep)

#===[Mengirim data edit laporan sebagai request baru ke MS1/editRequest]=================
@app.route('/sendEditRequest', methods = ['POST','GET'])
def sendEditRequest():
    if request.method == 'POST':
        PIC = requests.get('http://127.0.0.1:5001/namaPIC')
        picResp = json.dumps(PIC.json())
        loadPICe = json.loads(picResp)

        Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
        penResp = json.dumps(Pen.json())
        loadPene = json.loads(penResp)

        kode_laporan = request.form['labelKodLap']

        getJudulTujuan = requests.get('http://127.0.0.1:5001/getDataReport/'+kode_laporan)
        result = json.dumps(getJudulTujuan.json())
        loadJudulTujuan = json.loads(result)

        for i in loadJudulTujuan:
            req_tujuan = i['reportTujuan']
            req_judul = i['reportJudul']
            org_id = i['reportOrg']
            ktgri_id = i['reportKtgri']




        reqSch_hari = ''
        reqSch_bulan = ''
        reqSch_tanggal = ''
        reqSch_reportPIC = ''
        reqSch_penerima = ''
        

        

        newFilter = request.form['inputFilterBaru']
        newDisplay = request.form['inputNewDisplay']
        deadline = request.form['deadline']
        Period = request.form['inputPeriode']
        if 'inputFile' not in request.files:
            print('empty')
        file = request.files['inputFile'].read()

        


        for checkHari in ['mon','tue','wed','thu','fri','sat','sun']:
            if request.form.get(checkHari) is not None:
                if reqSch_hari == '':
                    reqSch_hari += request.form.get(checkHari)
                else:
                    reqSch_hari +=  ", "+request.form.get(checkHari)
        print(reqSch_hari)

        for checkBulan in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            if request.form.get(checkBulan) is not None:
                if reqSch_bulan == '':
                    reqSch_bulan += request.form.get(checkBulan)
                else:
                    reqSch_bulan +=  ", "+request.form.get(checkBulan)
        print (reqSch_bulan) 

        for checkTgl in ['t1', 't2', 't3', 't4', 't5', 't6', 't7', 't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15', 't16', 't17', 't18', 't19', 't20', 't21', 't22', 't23', 't24', 't25', 't26', 't27', 't28', 't29', 't30', 't31']:
            if request.form.get(checkTgl) is not None:
                if reqSch_tanggal == '':
                    reqSch_tanggal += request.form.get(checkTgl)
                else:
                    reqSch_tanggal +=  ", "+request.form.get(checkTgl)
        print (reqSch_tanggal)

        
        ####
        for checkPIC in loadPICe:
            
            if request.form.get(checkPIC['Id']) is not None:
                if reqSch_reportPIC == '':
                    reqSch_reportPIC += checkPIC['Email']
                else:
                    reqSch_reportPIC += ", "+checkPIC['Email']
        print (reqSch_reportPIC)

        for checkPen in loadPene:
            
            if request.form.get(checkPen['Email']) is not None:
                if reqSch_penerima == '':
                    reqSch_penerima += checkPen['Email']
                else:
                    reqSch_penerima += ", "+checkPen['Email']
        print (reqSch_penerima)


        edit_data = {
        'ProgId' : None,
        'UserId' : session['user_id'],
        'OrgId' : org_id,
        'KtgriId' : ktgri_id,
        'kodLap' : kode_laporan,
        'Judul' : req_judul,
        'Deskripsi' : newFilter,
        'Tujuan' : req_tujuan,
        'Tampilan' : newDisplay,
        'Periode' : Period,
        'Deadline' : deadline,
        'File' : None,
        'PIC' : None,
        'Hari' : reqSch_hari,
        'Bulan' : reqSch_bulan,
        'Tanggal' : reqSch_tanggal,
        'schOrg' : org_id,
        'schKtgri' : ktgri_id,
        'schLastUpdate' : None,
        'schPIC' : reqSch_reportPIC,
        'schPenerima' : reqSch_penerima
        }

        dataEdit = json.dumps(edit_data)

        requests.post('http://127.0.0.1:5001/editRequest/'+dataEdit)




        return redirect(url_for('list'))



#=========================================================================================
#=========================================================================================
#=========================[         SUPERVISOR             ]==============================
#=========================================================================================
#=========================================================================================


@app.route('/availableTaskSPV')
def listRequestSPV():
    # sessionId = session['user_id']

    listAvailableTask = requests.get('http://127.0.0.1:5001/availableTask')
    avTask = json.dumps(listAvailableTask.json())
    loadAvailTask = json.loads(avTask)

    # listTask = requests.get('http://127.0.0.1:5001/listTask/'+sessionId)
    # Task = json.dumps(listTask.json())
    # loadTask = json.loads(Task)

    return render_template('ms1availableTaskSPV.html', listAvailTaskSPV = loadAvailTask)
                            # listTask = loadTask)



@app.route('/onProgressTask')
def onProgressTask():

    onProgTask = requests.get('http://127.0.0.1:5001/onProgressTask')
    onTask = json.dumps(onProgTask.json())
    loadOnProgTask = json.loads(onTask)

    return render_template('ms1onProgressTaskSPV.html', onProgTask = loadOnProgTask)

@app.route('/spv')
def spv():
    return render_template('ms2homeSPV.html')

@app.route('/rejectRequest', methods=['POST','GET'])
def rejectRequest():
    if request.method == 'POST':

        data = {
        'request_id' : request.form['btnYes'],
        
        'userName' : session['username']
        }

        dataReject = json.dumps(data)

        requests.post('http://127.0.0.1:5001/reject/'+dataReject)


        return redirect(url_for('listRequestSPV'))

# CODINGANBARU
@app.route('/prioritasRequest', methods = ['POST', 'GET'])
def prioritasReq():
    if request.method == 'POST':

        data = {
        'request_id' : request.form['btnYesP'],
        }

        dataPrioritas = json.dumps(data)

        requests.post('http://127.0.0.1:5001/prioritas/'+dataPrioritas)


        return redirect(url_for('listRequestSPV'))

# CODINGANBARU
@app.route('/undoPrioritasRequest', methods = ['POST', 'GET'])
def undoPrioritasRequest():
    if request.method == 'POST':

        data = {
        'request_id' : request.form['btnUndo'],
        }

        dataUndoPrioritas = json.dumps(data)

        requests.post('http://127.0.0.1:5001/undoPrioritas/'+dataUndoPrioritas)


        return redirect(url_for('listRequestSPV'))

#=========================================================================================
#=========================================================================================
#=========================[         PROGRAMMER             ]==============================
#=========================================================================================
#=========================================================================================

#============[Menampilkan homepage programmer]============
@app.route('/admin')
def admin():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:

        return render_template('ms2home.html')

#============[Menampilkan list task yang bisa dikerjakan] CODINGAN BARU============
@app.route('/availableTask')
def availableTask():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:

        sessionName = session['username']
        sessionId = session['user_id']

        listAvailableTask = requests.get('http://127.0.0.1:5001/availableTask')
        avTask = json.dumps(listAvailableTask.json())
        loadAvailTask = json.loads(avTask)


        listReportId = requests.get('http://127.0.0.1:5001/getReportId')
        listReportIdResp = json.dumps(listReportId.json())
        loadListRep = json.loads(listReportIdResp)

        detailNormal = requests.get('http://127.0.0.1:5001/countRequestNormal/'+sessionName)
        detNormal = json.dumps(detailNormal.json())
        loadDetailNormal = json.loads(detNormal)

        detailImportant = requests.get('http://127.0.0.1:5001/countRequestImportant/'+sessionName)
        detImportant = json.dumps(detailImportant.json())
        loadDetailImportant = json.loads(detImportant)


        return render_template('ms1availableTask.html', listAvailTask = loadAvailTask,
                                listKodeLap = loadListRep, normal = loadDetailNormal,
                                important = loadDetailImportant)

#============[Menampilkan list task yang harus dikerjakan]============
@app.route('/listTask')
def listTask():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        sessionName = session['username']
        sessionId = session['user_id']

        listReportId = requests.get('http://127.0.0.1:5001/getReportId')
        listReportIdResp = json.dumps(listReportId.json())
        loadListRep = json.loads(listReportIdResp)

        listTask = requests.get('http://127.0.0.1:5001/listTask/'+sessionId)
        Task = json.dumps(listTask.json())
        loadTask = json.loads(Task)

        return render_template('ms1listTask.html', listTask = loadTask, 
                                listKodeLap = loadListRep)

#============[Menampilkan list task yang sudah selesai dikerjakan]============
@app.route('/historyTask')
def historyTask():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        sessionName = session['username']
        sessionId = session['user_id']

        listReportId = requests.get('http://127.0.0.1:5001/getReportId')
        listReportIdResp = json.dumps(listReportId.json())
        loadListRep = json.loads(listReportIdResp)

        histTask = requests.get('http://127.0.0.1:5001/historyTask/'+sessionName)
        hist = json.dumps(histTask.json())
        loadHist = json.loads(hist)

        return render_template('ms1historyTask.html', historyTask = loadHist, 
                                listKodeLap = loadListRep)

#=====[Saat programmer mengklik request yang ada]===========
@app.route('/detailRequest', methods=['POST','GET'])
def detailRequest():

    request_id = request.form['buttonDetail']
    sessionName = session['username']

    detailTask = requests.get('http://127.0.0.1:5001/getDetailTask/'+request_id)
    detTask = json.dumps(detailTask.json())
    loadDetailTask = json.loads(detTask)
        
        # UNTUK MENGAMBIL VALUE DALAM JSON
    for x in loadDetailTask:
        aaa = x['requestId']
        bbb = x['requestTujuan']

    # cba = detTask["requestId"]
    # print(cba)
    return render_template('ms1detailTask.html', detail_task = loadDetailTask)

#============[Mengirim data accept request ke MS1/accRequest]============
@app.route('/acceptRequest', methods=['POST','GET'])
def acceptRequest():
    if request.method == 'POST':
        request_id = request.form['btnConfirmReq']
        uId = session['user_id']
        uName = session['username']


        detailAccept = {
        'request_id': request_id,
        'uId' : uId,
        'uName' : uName
        }

        detAcc = json.dumps(detailAccept)

        requests.post('http://127.0.0.1:5001/accRequest/'+detAcc)


        # return redirect(url_for("task"))
        if session['position'] == 'Admin':

            return redirect(url_for("listTask"))
        else:
            return redirect(url_for("listRequestSPV"))


#============[Mengirim data finish request ke MS1/finReq]============
@app.route('/finishRequest', methods=['POST','GET'])
def finishRequest():
    if request.method == 'POST':
        request_id = request.form['finishReq']
        kodeL = request.form['kodLap']

        a = {
        'request_id' : request_id,
        'kode_laporan' : kodeL
        }

        b = json.dumps(a)

        requests.post('http://127.0.0.1:5001/finReq/'+b)



        # return redirect(url_for('task'))
        if session['position'] == 'Admin':

            return redirect(url_for("listTask"))
        else:
            return redirect(url_for("listRequestSPV"))


#=========================================================================================
#=========================================================================================
#=========================[    PROGRAMMER MICROSERVICE2     ]=============================
#=========================================================================================
#=========================================================================================


#=========================================================================================
#=========================================================================================
#=================================[    SCHEDULE     ]=====================================
#=========================================================================================
#=========================================================================================

#============[Menampilkan menu add new Schedule]============
@app.route('/addNewSchedule', methods = ['POST','GET'])
def addNewSchedule():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:

        getKodeS = requests.get('http://127.0.0.1:5002/listKodeReportAddNewSchedule')
        kodeNewS = json.dumps(getKodeS.json())
        loadKodeNewSchedule = json.loads(kodeNewS)

        PIC = requests.get('http://127.0.0.1:5001/namaPIC')
        picResp = json.dumps(PIC.json())
        loadPIC = json.loads(picResp)

        Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
        penResp = json.dumps(Pen.json())
        loadPen = json.loads(penResp)
        
        return render_template('ms2addNewSchedule.html', listKodeReportS = loadKodeNewSchedule,
                                listPIC = loadPIC,listPen = loadPen)

#============[Mengirim data add new schedule ke MS2/addSchedule]============
@app.route('/sendAddNewSchedule', methods=['POST','GET'])
def sendAddNewSchedule():
    if request.method == 'POST':
        PIC = requests.get('http://127.0.0.1:5001/namaPIC')
        picResp = json.dumps(PIC.json())
        loadPICs = json.loads(picResp)

        Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
        penResp = json.dumps(Pen.json())
        loadPens = json.loads(penResp)



        kode_laporan = request.form['valKode']

        #Untuk mendapatkan ID Organisasi & Kategori untuk didapatkan namanya.
        detailLap = requests.get('http://127.0.0.1:5002/getIdOrgKat/'+kode_laporan)
        orgKat = json.dumps(detailLap.json())
        loadOrgKat = json.loads(orgKat)
        for i in loadOrgKat:
            idOrg = i['report_org']
            idKat = i['report_kat']

        #Mendapatkan nama Organisasi
        gOrg = requests.get('http://127.0.0.1:5001/getNamaOrg/'+idOrg)
        org2 = json.dumps(gOrg.json())
        namaOrg = json.loads(org2)
        for x in namaOrg:
            nmOrg = x['org_name']

        #Mendapatkan nama Kategori
        gKat = requests.get('http://127.0.0.1:5001/getNamaKat/'+idKat)
        kat2 = json.dumps(gKat.json())
        namaKat = json.loads(kat2)
        for y in namaKat:
            nmKat = y['kat_name']



        header = request.form['header']
        keterangan = request.form['keterangan']
        note = request.form['note']
        grouping = request.form['grouping']
        org = nmOrg
        kategori = nmKat
        
        reportPIC = ''
        reportPenerima = ''
        
        jadwalBln = ''
        jadwalHari = ''
        jadwalTgl = ''
        
        


        for checkHari in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']:
            if request.form.get(checkHari) is not None:
                if jadwalHari == '':
                    jadwalHari += request.form.get(checkHari)
                else:
                    jadwalHari +=  ", "+request.form.get(checkHari)
        print("Hari ",jadwalHari)

        for checkBulan in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
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

        for checkPIC in loadPICs:
            #print(checkPIC[0])
            if request.form.get(checkPIC['Id']) is not None:
                if reportPIC == '':
                    reportPIC += checkPIC['Email']
                else:
                    reportPIC += ", "+checkPIC['Email']
        print ("PIC ",reportPIC)

        for checkPen in loadPens:
            #print(checkPen[2])
            if request.form.get(checkPen['Email']) is not None:
                if reportPenerima == '':
                    reportPenerima += checkPen['Email']
                else:
                    reportPenerima += ", "+checkPen['Email']
        print ("Penerima ", reportPenerima)  

       

        addS_data = {
        'report_id' : kode_laporan,
        'sch_header' : header,
        'sch_keterangan' : keterangan,
        'sch_note' : note,
        'sch_reportPIC' : reportPIC,
        'sch_reportPen' : reportPenerima,
        'sch_grouping' : grouping,
        'sch_bulan' : jadwalBln,
        'sch_hari' : jadwalHari,
        'sch_tanggal' : jadwalTgl,
        'sch_org' : org,
        'sch_kategori' : kategori
        }


        data_schedule = json.dumps(addS_data)

        requests.post('http://127.0.0.1:5002/addSchedule/'+data_schedule)

        return redirect(url_for('admin'))

#============[Memilih kode laporan yang akan diubah schedulenya]============
#============[Menampilkan form edit schedule]============
@app.route('/editSchedule', methods=['POST','GET'])
def editSchedule():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        kodeReport = requests.get('http://127.0.0.1:5002/listKodeReportEditSchedule')
        kodeAll = json.dumps(kodeReport.json())
        loadKodeAll = json.loads(kodeAll)

        if request.method == 'POST':
            kode_laporan = request.form['valKode']

            PIC = requests.get('http://127.0.0.1:5001/namaPIC')
            picResp = json.dumps(PIC.json())
            loadPICs = json.loads(picResp)

            Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
            penResp = json.dumps(Pen.json())
            loadPens = json.loads(penResp)

            detSch = requests.get('http://127.0.0.1:5002/showDetailSchedule/'+kode_laporan)
            detDumps = json.dumps(detSch.json())
            loadDetSch = json.loads(detDumps)


            return render_template('ms2editSchedule2.html', detailSchedule = loadDetSch,
                kode_laporan=kode_laporan, listPIC = loadPICs, listPen = loadPens)

        return render_template('ms2editSchedule.html', listKodeLap = loadKodeAll)

#============[Mengirim data edit schedule ke MS2/editSched]============
@app.route('/sendEditSchedule', methods=['POST','GET'])
def sendEditSchedule():
    PIC = requests.get('http://127.0.0.1:5001/namaPIC')
    picResp = json.dumps(PIC.json())
    loadPICs = json.loads(picResp)

    Pen = requests.get('http://127.0.0.1:5001/namaPenerima')
    penResp = json.dumps(Pen.json())
    loadPens = json.loads(penResp)



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


        aktifYN = request.form['aktifYND']
        lastUpdate = datetime.datetime.now()

        for checkHari in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']:
            if request.form.get(checkHari) is not None:
                if jadwalHari == '':
                    jadwalHari += request.form.get(checkHari)
                else:
                    jadwalHari +=  ", "+request.form.get(checkHari)
        print("Hari ",jadwalHari)

        for checkBulan in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
            if request.form.get(checkBulan) is not None:
                if jadwalBln == '':
                    jadwalBln += request.form.get(checkBulan)
                else:
                    jadwalBln +=  ", "+request.form.get(checkBulan)
        print ("Bulan ",jadwalBln) 

        for checkTgl in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']:
            if request.form.get(checkTgl) is not None:
                if jadwalTgl == '':
                    jadwalTgl += request.form.get(checkTgl)
                else:
                    jadwalTgl +=  ", "+request.form.get(checkTgl)
        print ("Tanggal ",jadwalTgl)

        for checkPIC in loadPICs:
            #print(checkPIC[0])
            if request.form.get(checkPIC['Id']) is not None:
                if reportPIC == '':
                    reportPIC += checkPIC['Email']
                else:
                    reportPIC += ", "+checkPIC['Email']
        print ("PIC ",reportPIC)

        for checkPen in loadPens:
            #print(checkPen[2])
            if request.form.get(checkPen['Email']) is not None:
                if reportPenerima == '':
                    reportPenerima += checkPen['Email']
                else:
                    reportPenerima += ", "+checkPen['Email']
        print ("Penerima ", reportPenerima)


        

        dataEdit = {
        'reportId' : kode_laporan,
        'header' : header,
        'keterangan' : keterangan,
        'note' : note,
        'grouping' : grouping,
        'PIC' : reportPIC,
        'Penerima' : reportPenerima,
        'jadwalBln' : jadwalBln,
        'jadwalHari' : jadwalHari,
        'jadwalTgl' : jadwalTgl,
        'aktifYN' : aktifYN,
        'lastUpdate' : str(lastUpdate)
        }

        editData = json.dumps(dataEdit)

        requests.post('http://127.0.0.1:5002/editSched/'+editData)


        return redirect(url_for('admin'))



#=========================================================================================
#=========================================================================================
#=================================[    QUERY     ]========================================
#=========================================================================================
#=========================================================================================

#============[Menampilkan layar insert query]============
@app.route('/insertQuery', methods=['POST','GET'])
def addQuery():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        kQuery = requests.get('http://127.0.0.1:5002/getKodeNewQuery')
        kDump = json.dumps(kQuery.json())
        kLoad = json.loads(kDump)

        return render_template('ms2insertQuery.html', kodeNewQuery = kLoad)

#============[Mengirim data query ke MS2/addQuery]============
@app.route('/sendNewQuery', methods=['POST','GET'])
def sendNewQuery():
    quer = []
    kode_laporan = request.form['kodLap']
    kode_laporan.upper()

    if request.method == 'POST':
        for query in ['query1', 'query2', 'query3', 'query4', 'query5', 'query6', 'query7', 'query8', 'query9', 'query10', 'query11', 'query12', 'query13', 'query14']:
            
            if (request.form[query] is not  None) and (request.form[query] is not ''):
                quer.append(request.form[query])
                queryDump = json.dumps(quer)



        requests.post('http://127.0.0.1:5002/addQuery/'+kode_laporan+'/'+queryDump)


        return redirect(url_for('admin'))

#============[Memilih kode laporan yang akan diubah querynya]============
#============[Menampilkan menu insert Query]============
@app.route('/editQuery', methods=['POST','GET'])
def editQuery():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        kEQuery = requests.get('http://127.0.0.1:5002/getKodeEditQuery')
        kEDump = json.dumps(kEQuery.json())
        kELoad = json.loads(kEDump)

        if request.method == 'POST':
            kode_laporan = request.form['kodLap']

            Query = requests.get('http://127.0.0.1:5002/viewEditQuery/'+kode_laporan)
            QDump = json.dumps(Query.json())
            QLoad = json.loads(QDump)


            return render_template('ms2insertQuery.html', editQ = QLoad, kode_laporan=kode_laporan)

        return render_template('ms2editQuery.html', listKodeReportQuery = kELoad)



#=========================================================================================
#=========================================================================================
#==================================[    TEMPLATE     ]====================================
#=========================================================================================
#=========================================================================================

#============[Menampilkan menu untuk membuat template baru]============
@app.route('/addTemplate', methods=['POST','GET'])
def addTemplate():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        org = requests.get('http://127.0.0.1:5001/namaOrganisasi')
        orgResp=json.dumps(org.json())
        loadOrg = json.loads(orgResp)

        cat = requests.get('http://127.0.0.1:5001/namaDept')
        catResp = json.dumps(cat.json())
        loadCat = json.loads(catResp)

        ser = requests.get('http://127.0.0.1:5002/getServer')
        serResp = json.dumps(ser.json())
        loadSer = json.loads(serResp)


        return render_template('ms2addNewTemplate.html', listKategori = loadCat, listOrg = loadOrg,
                                listServer = loadSer)

#============[Mengirim data template baru ke MS2/addNewTemplate]============
@app.route('/sendNewTemplate', methods=['POST','GET'])
def sendNewTemplate():

    if request.method == 'POST':
        userName = session['username']

        kode_laporan        = request.form['kodeLaporan2']+'-'+request.form['kategori']+request.form['noLap']
        server_id           = request.form['server']
        report_judul        = request.form['namaLaporan']
        report_deskripsi    = request.form['filter']
        report_header       = request.form['jmlHeader']
        report_footer       = request.form['jmlFooter']
        report_jmlTampilan  = request.form['jmlTampilan']
        report_periode      = request.form['periode']
        #report_createDate   = datetime.datetime.now(),
        report_userUpdate   = userName
        #report_lastUpdate   = datetime.datetime.now(),
        report_aktifYN      = 'Y'
        org_id              = request.form['organisasi']
        ktgri_id            = request.form['kategori']
        report_printAllYN   = request.form['printAll']
        report_createdUser  = userName
        report_scheduleYN   = 'N'
        report_tujuan       = request.form['tujuan']

        
        data= {
        'kode_laporan'        : str(kode_laporan),
        'server_id'           : str(server_id),
        'report_judul'        : str(report_judul),
        'report_deskripsi'    : str(report_deskripsi),
        'report_header'       : str(report_header),
        'report_footer'       : str(report_footer),
        'report_jmlTampilan'  : str(report_jmlTampilan),
        'report_periode'      : str(report_periode),
        #'report_createDate'   : report_createDate,
        'report_userUpdate'   : str(report_userUpdate),
        #'report_lastUpdate'   : report_lastUpdate,
        'report_aktifYN'      : str(report_aktifYN),
        'org_id'              : str(org_id),
        'ktgri_id'            : str(ktgri_id),
        'report_printAllYN'   : str(report_printAllYN),
        'report_createdUser'  : str(report_createdUser),
        'report_scheduleYN'   : str(report_scheduleYN),
        'report_tujuan'       : str(report_tujuan)
        }
        
        dataTemplate = json.dumps(data)

        requests.post('http://127.0.0.1:5002/addNewTemplate/'+dataTemplate)

        detTem = requests.get('http://127.0.0.1:5002/formatTemplate/'+kode_laporan)
        detDump = json.dumps(detTem.json())
        loadDetail = json.loads(detDump)
        
        # return redirect(url_for('admin'))

        return render_template('addTemplate.html', detailFormatTemplate = loadDetail)

#============[Memilih kode laporan]============
#============[Menampilkan form format template]============
@app.route('/formatTemplate', methods=['POST','GET'])
def formatTemplate():
    kodeReport = requests.get('http://127.0.0.1:5002/getKodeReportAll')
    kodeAll = json.dumps(kodeReport.json())
    loadKodeAll = json.loads(kodeAll)

    if request.method == 'POST':
        kode_laporan = request.form['kodLap']

        detTem = requests.get('http://127.0.0.1:5002/detailFormatTemplate/'+kode_laporan)
        detDump = json.dumps(detTem.json())
        loadDetail = json.loads(detDump)


        return render_template('testFormatTemplate.html', kode_laporan=kode_laporan
            ,detailTemplate = loadDetail)


    return render_template('ms2formatTemplate1.html', listKodeReport = loadKodeAll)
        

#=========================================================================================
#=========================================================================================
#==================================[    PREVIEW      ]====================================
#=========================================================================================
#=========================================================================================

@app.route('/runSchedule', methods=['POST','GET'])
def runSchedule():
    getKodeToday = requests.get('http://127.0.0.1:5002/getKodeReportRunToday')
    kodeTodayResp = json.dumps(getKodeToday.json())
    loadKodeToday = json.loads(kodeTodayResp)

    getStatus = requests.get('http://127.0.0.1:5003/getStatusRunSchedule')
    statusResp = json.dumps(getStatus.json())
    loadStatus = json.loads(statusResp)

    return render_template('ms3runSchedule.html', kodeToday = loadKodeToday,
        statusSchedule = loadStatus)


#============[Menampilkan seluruh list report yang ada]============
@app.route('/listReport', methods=['POST','GET'])
def listReport():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:

        detR = requests.get('http://127.0.0.1:5002/getListReport')
        detResp = json.dumps(detR.json())
        loadListReport = json.loads(detResp)

        return render_template('ms2listReport.html', listReport = loadListReport)


#============[Memilih kode laporan yang akan dipreview]============
#============[Mengirim kode laporan ke MS3/previewLaporan]============
# @app.route('/preview', methods=['POST','GET'])
# def preview():
#     if session.get('user_id') is None:
#         return render_template('ms1login.html')
#     else:

#         kEQuery = requests.get('http://127.0.0.1:5002/getKodeEditQuery')
#         kEDump = json.dumps(kEQuery.json())
#         kELoad = json.loads(kEDump)


#         if request.method == 'POST':
#             kode_laporan = request.form['kodLap']

#             requests.post('http://127.0.0.1:5003/testPreviewLaporan/'+kode_laporan)


#             return redirect(url_for('admin'))

#         return render_template('ms2preview.html', kodeReportAdaQuery = kELoad)

@app.route('/preview', methods=['POST','GET'])
def preview():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:

        kEQuery = requests.get('http://127.0.0.1:5002/getKodeEditQuery')
        kEDump = json.dumps(kEQuery.json())
        kELoad = json.loads(kEDump)


        if request.method == 'POST':
            
            kode_laporan = request.form['kodLap']
            
            # VALIDASI ERROR / TIDAK
            a = requests.get('http://127.0.0.1:5003/testPreviewLaporan/'+kode_laporan)
            if a:
                b = json.dumps(a.json())
                c = json.loads(b)
                
                return str(c)
            else:
                return redirect(url_for('admin'))

            return requests.get('http://127.0.0.1:5003/testPreviewLaporan/'+kode_laporan)
                    
        return render_template('ms2preview.html', kodeReportAdaQuery = kELoad)

@app.route('/downloadReport', methods=['POST','GET'])
def downloadReport():
    if request.method == 'POST':
        kode_laporan = request.form['kodLap']

        tgl = datetime.datetime.now().strftime('%d')
        bln = datetime.datetime.now().strftime('%b')

        resp = requests.get('http://127.0.0.1:5004/downloadReport/'+kode_laporan)
        
        directory = 'C:/'+tgl+bln

        if not os.path.exists(directory):
            os.makedirs(directory)

        output = open(directory+'/'+kode_laporan+'.xls', 'wb')
        output.write(resp.content)
        output.close()

        return 'Downloaded'


@app.route('/testURL/<kode_laporan>', methods=['POST','GET'])
def testURL(kode_laporan):
    tgl = datetime.datetime.now().strftime('%d')
    bln = datetime.datetime.now().strftime('%b')

    directory = 'C:/'+tgl+bln

    resp = requests.get('http://127.0.0.1:5004/downloadReport/'+kode_laporan)
    print(resp)

    if not os.path.exists(directory):
        os.makedirs(directory)

    output = open(directory+'/test.xls','wb')
    output.write(resp.content)
    output.close()

@app.route('/readReport2',methods=['POST','GET'])
def readReport2():
    kode_laporan = request.form['kodLap2']
    resp = requests.get('http://127.0.0.1:5004/downloadReport/'+kode_laporan)

    os.startfile(resp)


@app.route('/testLayar')
def testLayar():

    kodeReport = requests.get('http://127.0.0.1:5002/getKodeReportAll')
    kodeAll = json.dumps(kodeReport.json())
    loadKodeAll = json.loads(kodeAll)

    if request.method == 'POST':
        kode_laporan = request.form['kodLap']

        detTem = requests.get('http://127.0.0.1:5002/detailFormatTemplate/'+kode_laporan)
        detDump = json.dumps(detTem.json())
        loadDetail = json.loads(detDump)


        return render_template('testFormatTemplate.html', kode_laporan=kode_laporan
            ,detailTemplate = loadDetail, detailFormatTemplate = loadDetail)


    return render_template('ms2formatTemplate1.html', listKodeReport = loadKodeAll)



if __name__ == "__main__":
    app.run(debug=True)