from flask import Flask, render_template, redirect, url_for, request, session, flash, json, jsonify
from base64 import b64encode
import auth
# from microservice1 import RequestLaporan
# from templatelaporan import TemplateLaporan
import pymysql
import mysql.connector
from mysql.connector import Error
import requests
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

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/changePass')
def changePass():
    if session.get('user_id') is None:
        return render_template('login.html')
    else:
        a = session['user_id']
        return render_template('changePass.html')

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

    requests.post('http://127.0.0.1:5001/updateDataPassword/'+dataRequest)
    return redirect(url_for('user'))


#=========================================================================================
#=========================================================================================
#=========================[           USER             ]==================================
#=========================================================================================
#=========================================================================================


@app.route('/user', methods=['POST','GET'])
def user():

    if session.get('user_id') is None:
        return render_template('login.html')
    else:
        return render_template('home1.html')


@app.route('/list', methods = ['POST','GET'])
def list():

    if session.get('user_id') is None:
        return render_template('login.html')
    else:
        a = session['user_id']
        listReq = requests.get(''.join(['http://127.0.0.1:5001/listRequestUser/'+a]))
        listResp = json.dumps(listReq.json())
        loadListReq = json.loads(listResp)

        return render_template('listReq.html', listReqUser = loadListReq)


@app.route('/listFinished', methods = ['POST','GET'])
def listFinished():

    if session.get('user_id') is None:
        return render_template('login.html')
    else:
        a = session['user_id']
        listFinished = requests.get(''.join(['http://127.0.0.1:5001/listFinished/'+a]))
        finishedResp = json.dumps(listFinished.json())
        loadFinished = json.loads(finishedResp)

        return render_template('listFinished.html', listReqUser = loadFinished)


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


@app.route('/newRequest', methods = ['GET','POST'])
def newRequest():

    if session.get('user_id') is None:
        return render_template('login.html')
    else:
        org = requests.get(url1+'namaOrganisasi')
        orgResp = json.dumps(org.json())
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

        return render_template('requestLaporan.html', listOrg = loadOrg, listDept = loadCat, listPIC = loadPIC, listPen = loadPen)


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

        for checkBulan in ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agus', 'Sept', 'Okt', 'Nov', 'Des']:
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


@app.route('/cancelRequest', methods=['POST','GET'])
def cancelRequest():

    if request.method == 'POST':

        rId = request.form['btnCancel']

        data = {'request_id' : rId}

        dataFix = json.dumps(data)

        requests.post('http://127.0.0.1:5001/cancR/'+dataFix)

        return redirect(url_for('list'))
 

@app.route('/editReport', methods=['POST','GET'])
def editReport():

    if session.get('user_id') is None:
        return render_template('login.html')
    else:
        listReportId = requests.get('http://127.0.0.1:5001/getReportId')
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
 
            return render_template("Edit2.html", listcurrentdisplay = loadLap, listPIC = loadPICe, listPen = loadPene, kode_laporan=kode_laporan)

        return render_template('Edit2.html', listKodeReport = loadListRep)


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
 
        for checkHari in ['senin','selasa','rabu','kamis','jumat','sabtu','minggu']:
            if request.form.get(checkHari) is not None:
                if reqSch_hari == '':
                    reqSch_hari += request.form.get(checkHari)
                else:
                    reqSch_hari +=  ", "+request.form.get(checkHari)
        print(reqSch_hari)

        for checkBulan in ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agus', 'Sept', 'Okt', 'Nov', 'Des']:
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
#=========================[         PROGRAMMER             ]==============================
#=========================================================================================
#=========================================================================================


@app.route('/task')
def task():

    sessionName = session['username']
    sessionId = session['user_id']

    listAvailableTask = requests.get('http://127.0.0.1:5001/availableTask')
    avTask = json.dumps(listAvailableTask.json())
    loadAvailTask = json.loads(avTask)
 
    listTask = requests.get('http://127.0.0.1:5001/listTask/'+sessionId)
    Task = json.dumps(listTask.json())
    loadTask = json.loads(Task)

    histTask = requests.get('http://127.0.0.1:5001/historyTask/'+sessionId)
    hist = json.dumps(histTask.json())
    loadHist = json.loads(hist)

    listReportId = requests.get('http://127.0.0.1:5001/getReportId')
    listReportIdResp = json.dumps(listReportId.json())
    loadListRep = json.loads(listReportIdResp)
 
    return render_template('task2.html', listAvailTask = loadAvailTask, listTask = loadTask,
                            historyTask = loadHist, listKodeLap = loadListRep)


@app.route('/detailRequest', methods=['POST','GET'])
def detailRequest():

    request_id = request.form['buttonDetail']

    detailTask = requests.get('http://127.0.0.1:5001/getDetailTask/'+request_id)
    detTask = json.dumps(detailTask.json())
    loadDetailTask = json.loads(detTask)

    # UNTUK MENGAMBIL VALUE DALAM JSON
    for x in loadDetailTask:
        aaa = x['requestId']
        bbb = x['requestTujuan']

    print(aaa)
    print(bbb)

    # cba = detTask["requestId"]
    # print(cba)
    return render_template('detailTask.html', detail_task = loadDetailTask)


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

            return redirect(url_for("task"))
        else:
            return redirect(url_for("listRequestSPV"))


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
            return redirect(url_for("task"))
        else:
            return redirect(url_for("listRequestSPV"))


#=========================================================================================
#=========================================================================================
#=========================[         SUPERVISOR             ]==============================
#=========================================================================================
#=========================================================================================


@app.route('/listRequestSPV')
def listRequestSPV():

    sessionId = session['user_id']

    listAvailableTask = requests.get('http://127.0.0.1:5001/availableTask')
    avTask = json.dumps(listAvailableTask.json())
    loadAvailTask = json.loads(avTask)

    onProgTask = requests.get('http://127.0.0.1:5001/onProgressTask')
    onTask = json.dumps(onProgTask.json())
    loadOnProgTask = json.loads(onTask)

    listTask = requests.get('http://127.0.0.1:5001/listTask/'+sessionId)
    Task = json.dumps(listTask.json())
    loadTask = json.loads(Task)

    return render_template('taskSPV.html', listAvailTaskSPV = loadAvailTask,
                            onProgTask = loadOnProgTask, listTask = loadTask)

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

if __name__ == "__main__":
    app.run(debug=True)
