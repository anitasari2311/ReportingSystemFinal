from flask import Flask, render_template, redirect, url_for, request, session, flash
from base64 import b64encode
import auth
from microservice1 import RequestLaporan
from templatelaporan import TemplateLaporan
import pymysql
import mysql.connector
from mysql.connector import Error
import datetime
#from PIL import Image

app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'
app.secret_key = 'session1'

##########################                  LOGIN                          ############################
@app.route('/atasan')
def atasan():
    return render_template('taskSPV.html')

@app.route('/authLogin', methods=['GET','POST'])
def authLogin():
    auth.auth_login()
    return auth.auth_login()

@app.route('/')
def start():
    return redirect(url_for('login'))

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
    return render_template('changePass.html')

# @app.route('/changePassProcess')
# def changePassProcess():
#     request = RequestLaporan()

#     if request.methods == 'POST':

#         user_password = request.form[]
#         new_password = request.form[]
#         confirm_password = request.form[]

#         request.changePass(user_password, new_password, confirm_password)
        



#########################                   USER                 ###############################


## Menampilkan menu utama user
@app.route('/user', methods=['GET','POST'])
def user():
    # if request.method =='POST':
    #     request_id = request.form['btnCancel']

        
        listRequestLaporanUser = RequestLaporan()
        return render_template('menu.html', listReqUser = listRequestLaporanUser.listRequestUser(session['user_id']),
                            listKelar = listRequestLaporanUser.listFinished(session['user_id']))

### Cancel Detail Task to menuTaskProgrammer
@app.route('/cancelTask')
def cancelTask():
    return redirect(url_for('task'))



## Jika programmer mengklik tombol Finish pada menu Task Programmer
@app.route('/finishRequest', methods = ['POST'])
def finishRequest():
    if request.method == 'POST':
        finishreq = RequestLaporan()
        request_id = request.form['finishReq']
        kodLap = request.form['kodLap']

        if session['position'] == 'Admin':
            return redirect(url_for("task"), finishreq.finishRequest(request_id),
                finishreq.inputKodeFinish(request_id, kodLap))
        elif session['position'] == 'Atasan':

            return redirect(url_for("spv"), finishreq.finishRequest(request_id)
                        , finishreq.inputKodeFinish(request_id, kodLap))

#USER MEMBERIKAN RATING TERHADAP LAPORAN YANG TELAH SELESAI DIKERJAKAN
@app.route('/finishRating', methods = ['POST','GET'])
def finishRating():
    if request.method == 'POST':
        finishR = RequestLaporan()
        rating = request.form['fRating']
        request_id = request.form['finishRat']
        keterangan = request.form['inputKeterangan']

        return redirect(url_for('user'), finishR.finishRating(request_id, rating, keterangan))



## Jika user mengklik tombol confirm
@app.route('/confirmRequest', methods = ['POST','GET'])
def confirmRequest():
    if request.method =='POST':
        confirm = RequestLaporan()
        request_id = request.form ['confirmReq']

        return redirect(url_for("user"), confirm.confirmRequest(request_id))


#Untuk Button Cancel di Menu User
@app.route('/cancel', methods = ['POST'])
def cancel():
    if request.method == 'POST':

        cancel = RequestLaporan()
        request_id = request.form['btnCancel']

        return redirect(url_for("user", listReqUser = cancel.listRequestUser(session['user_id']),cancel_request = cancel.cancelRequest(request_id)))

@app.route('/reject', methods = ['POST'])
def reject():
    if request.method == 'POST':

        reject = RequestLaporan()
        request_id = request.form['btnReject']


        reject.rejectRequest(request_id)
        
        return redirect(url_for("spv"))

#BUAT CALL REQUEST
@app.route('/formRequest', methods=['GET', 'POST'])
def formRequest():
    newRequest = RequestLaporan()
    return render_template("requestLaporan.html", listOrg = newRequest.namaOrganisasi(), listDept = newRequest.namaDept(), listPIC = newRequest.namaPIC(),
                            listPen = newRequest.namaPenerima())


#BUAT NEW REQUEST
@app.route('/newReq', methods = ['POST'])
def newReq():
     if request.method == 'POST':
            reqSch_hari = ''
            reqSch_bulan = ''
            reqSch_tanggal = ''
            reqSch_reportPIC = ''
            reqSch_penerima = ''
            dateNow = datetime.datetime.now()

            newRequest = RequestLaporan()
           
            title = request.form['inputTitle']
            purpose = request.form['inputPurpose']
            description = request.form['keteranganlaporan']
            Organization = request.form['Organization']
            Department = request.form['Department']
            Display = request.form['inputDisplay']
            Period = request.form['inputPeriode']
            deadline = request.form['deadline']
            

            if 'inputFile' not in request.files:
                print('empty')
            file = request.files['inputFile'].read()
        # if user does not select file, browser also
        # submit an empty part without filename
            

            # reqSch_hari = request.form.getlist('haritest')
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
            for checkPIC in newRequest.namaPIC():
                print(checkPIC[0])
                if request.form.get(checkPIC[0]) is not None:
                    if reqSch_reportPIC == '':
                        reqSch_reportPIC += checkPIC[2]
                    else:
                        reqSch_reportPIC += ", "+checkPIC[2]
            print (reqSch_reportPIC)

            for checkPen in newRequest.namaPenerima():
                print(checkPen[0])
                if request.form.get(checkPen[2]) is not None:
                    if reqSch_penerima == '':
                        reqSch_penerima += checkPen[2]
                    else:
                        reqSch_penerima += ", "+checkPen[2]
            print (reqSch_penerima)            
           

            newRequest.requestLaporanBaru( None, session['user_id'], Organization, Department, None, title, description,
                             purpose, Display, Period, deadline, file, None,
                             reqSch_hari, reqSch_bulan, reqSch_tanggal,
                             Organization,Department, None, reqSch_reportPIC, reqSch_penerima)

            
            return redirect(url_for('user'))



#EDIT REQUEST
@app.route('/editReport',methods=['GET', 'POST'])
def edit():
    
    template = TemplateLaporan()

    if request.method == 'POST':
        newRequest = RequestLaporan()

        kode_laporan = request.form['kodeLaporan']
        cur = template.getCurrentDisplay(kode_laporan)

        return render_template("Edit2.html",listcurrentdisplay = cur, listPIC = newRequest.namaPIC()
            ,listPen = newRequest.namaPenerima(), kode_laporan=kode_laporan)

    return render_template("Edit2.html", listKodeReport = template.getReportID())

    
# @app.route('/formEdit', methods=['POST','GET'])
# def formEdit():
#         newRequest = TemplateLaporan()
#         newRequest2 = RequestLaporan()


#         session['kodeLaporan'] = request.form['kodeLaporan']
#         print("kode laporan" + session['kodeLaporan'])

        
#         cur = newRequest.getCurrentDisplay(session['kodeLaporan'])
        
#         print("Kode Laporan Edit: ",session['kodeLaporan'])
#         return render_template("EditKolom.html",listcurrentdisplay = cur, listPIC = newRequest2.namaPIC())

#BUAT EDIT REQUEST
@app.route('/newEdit', methods = ['POST'])
def newEdit():
    if request.method == 'POST':
            reqSch_hari = ''
            reqSch_bulan = ''
            reqSch_tanggal = ''
            reqSch_reportPIC = ''
            reqSch_penerima = ''
            newRequest = RequestLaporan()

            kode_laporan = request.form['labelKodLap']

            filterBaru = request.form['inputFilterBaru']
            newDisplay = request.form['inputNewDisplay']
            deadline = request.form['deadline']
            if 'inputFile' not in request.files:
                print('empty')
            file = request.files['inputFile'].read()

            # reqSch_hari = request.form.getlist('haritest')
            # print(reqSch_hari)

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

            for checkPIC in newRequest.namaPIC():
                print(checkPIC[0])
                if request.form.get(checkPIC[0]) is not None:
                    if reqSch_reportPIC == '':
                        reqSch_reportPIC += checkPIC[2]
                    else:
                        reqSch_reportPIC += ", "+checkPIC[2]
            print (reqSch_reportPIC)

            for checkPen in newRequest.namaPenerima():
                print(checkPen[0])
                if request.form.get(checkPen[2]) is not None:
                    if reqSch_penerima == '':
                        reqSch_penerima += checkPen[2]
                    else:
                        reqSch_penerima += ", "+checkPen[2]
            print (reqSch_penerima)  

            #flash('Request berhasil dibuat!')   

            newRequest.requestEditLap( None, session['user_id'], kode_laporan , kode_laporan, filterBaru,
                             newDisplay, deadline, file,
                                None, reqSch_hari, reqSch_bulan, reqSch_tanggal)
            

            
            return redirect(url_for('user'))



# @app.route('/revisi', methods = ['GET', 'POST'])
# def revisi():
#     revisi = TemplateLaporan()
#     revisi_id = request.form['btnRevisi']
#     cur = revisi.getRevisiDisplay(revisi_id)
#     return render_template("EditRevisi.html",listrevisidisplay = cur)









#######################                  PROGRAMMER             #################################




@app.route('/task')

def task():
    availTask = RequestLaporan()
    return render_template('task2.html', listAvailTask = availTask.availableTask(), listTask = availTask.listTask()
                           ,listKodeLap = availTask.listKodeLaporan(),
                           historyTask = availTask.historyTask())

@app.route('/detailReq', methods=['GET', 'POST'])
def detailReq():
    if request.method == 'POST':
        detTask = RequestLaporan()
        request_id = request.form['buttonDetail']
        cur = detTask.getDetailTask(request_id)
        

        # obj = detTask.showImage(request_id)
        # print(obj)
        # f = open('test.txt','wb')
        # f.write(obj)
        # f.close()
        # image = b64encode(obj).decode("utf-8")

        return render_template('detailTask.html', detail_task = cur)


###########################################PROSES



@app.route('/listAvailTask', methods=['GET','POST'])
def listAvailTask():
    microservice2.listTask()
    return microservice2.listTask()



@app.route('/accRequest', methods = ['POST','GET'])
def confirm1():
    if request.method == 'POST':

        confirm = RequestLaporan()
        request_id = request.form['btnConfirmReq']


        if session['position'] == 'Admin':


            return redirect(url_for("task",  confirmReq = confirm.accRequest(request_id)))
        else:
            return redirect(url_for("spv", confirmReq = confirm.accRequest(request_id)))



#############################               ATASAN              ###########################

@app.route('/spv')
def spv():
    availTask = RequestLaporan()

    return render_template("taskSPV.html", listAvailTaskSPV = availTask.availableTaskSPV(),
                            onProgTask = availTask.onProgressTask(),
                            listTask = availTask.listTask())

@app.route('/prioritasReq', methods = ['POST'])
def prioritasReg():
    
    if request.method == 'POST':
        availTask = RequestLaporan()
        request_id = request.form['btnYes']

        return redirect(url_for("spv", update_prioritas = availTask.prioritas(request_id)))

@app.route('/undoPrioritas', methods= ['POST'])
def undoPrioritas():

    if request.method == 'POST':
        availTask = RequestLaporan()
        request_id = request.form['btnUndo']

        return redirect(url_for("spv", undo_prioritas = availTask.undoPrioritas(request_id)))


if __name__ == "__main__":
    app.run(debug=True)
