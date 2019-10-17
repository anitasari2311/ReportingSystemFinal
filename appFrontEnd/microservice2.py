from flask import Flask, render_template, redirect, url_for, request, json, session, flash, jsonify
import datetime
import pymysql
import random
import mysql.connector
from mysql.connector import Error
from db import databaseCMS
import json



app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'
app.secret_key = 'ms2'
    

class Template:

    def __init__(self):
        self.KodeLaporan = ''
        self.namaLaporan = ''
        self.namaOrganisasi = ''
        self.namaKategori = ''
        self.namaServer = ''
        self.deskripsi = ''
        self.jumlahKolom = ''
        self.jumlahHeader = ''
        self.jumlahFooter = ''
        self.periode = ''
        self.printAll = ''

    @app.route('/getIdOrgKat/<kode_laporan>', methods = ['POST','GET'])
    def getIdOrgKat(kode_laporan):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()
            
            cursor.execute('SELECT report_id, org_id, ktgri_id FROM M_report WHERE report_id = "'+kode_laporan+'" ')
            orgKat = cursor.fetchall()

            

            getList = []
            for row in orgKat:
                x = {
                "report_id": row[0],
                "report_org": row[1],
                "report_kat": row[2]
                }
                getList.append(x)

            namaOrgKat = json.dumps(getList)
             
            
            return namaOrgKat
            
        
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
            #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    
    #Mengambil semua list Kode Report
    @app.route('/getKodeReportAll')
    def getKodeReportAll():
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('select UPPER(report_id) AS report_id from m_report')
            

            listKodeReportAll = cursor.fetchall()

            kodeReportList = []

            for x in listKodeReportAll:
                kodeDict = {
                'report_id' : x[0]
                }
                kodeReportList.append(kodeDict)

            kodeReportAll = json.dumps(kodeReportList)
                

            
            return kodeReportAll
        
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
            #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    # LIST KODE REPORT YANG SUDAH MEMILIKI QUERY
    @app.route('/getKodeEditQuery', methods=['POST','GET'])
    def getKodeEditQuery():
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('select distinct UPPER(report_id) AS report_id from m_query')
            #listKodeReport = cursor.execute('select report_id, server_nama from M_report  a left join M_server b ON b.server_id = a.server_id;')

            listKodeReportQuery = cursor.fetchall()

            kodeL = []

            for i in listKodeReportQuery:
                kodeDict = {
                'reportId' : i[0]
                }
                kodeL.append(kodeDict)

            kodeD = json.dumps(kodeL)
            
            return kodeD
        
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
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT a.report_id, org_id, report_judul, report_deskripsi\
                            FROM m_report a LEFT JOIN t_schedule b ON a.report_id = b.report_id WHERE sch_reportPIC\
                            LIKE "%'+email+'%" OR sch_penerima LIKE "%'+email+'%" ')

            listReport = cursor.fetchall()

            LR = []
            for row in listReport:
                listDict={
                'reportId' : row[0],
                'orgId' : row[1],
                'reportJudul' : row[2],
                'reportDeskripsi': row[3]
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


    @app.route('/getServer', methods=['POST','GET'])
    def getServer():
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            listServer = cursor.execute('SELECT server_id, server_nama from m_server where server_aktifYN ="Y" order by server_id')

            listServer = cursor.fetchall()

            serL = []

            for i in listServer:
                serDict = {
                'serverId' : i[0],
                'serverName' : i[1]
                }
                serL.append(serDict)

            serD = json.dumps(serL)

            return serD

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")
   

    


    #Template
    @app.route('/addNewTemplate/<dataTemplate>', methods=['POST','GET'])
    def addNewTemplate(dataTemplate):
        report_createDate   = datetime.datetime.now()
        report_lastUpdate   = datetime.datetime.now()
        dataLoad = json.loads(dataTemplate)

        for x in dataLoad:
            kode_laporan = dataLoad['kode_laporan']
            server_id = dataLoad['server_id']
            report_judul = dataLoad['report_judul']
            report_deskripsi = dataLoad['report_deskripsi']
            report_header = dataLoad['report_header']
            report_footer = dataLoad['report_footer']
            report_jmlTampilan = dataLoad['report_jmlTampilan']
            report_periode = dataLoad['report_periode']
            # report_createDate = dataLoad['report_createDate']
            report_userUpdate = dataLoad['report_userUpdate']
            # report_lastUpdate = dataLoad['report_lastUpdate']
            report_aktifYN = dataLoad['report_aktifYN']
            org_id = dataLoad['org_id']
            ktgri_id = dataLoad['ktgri_id']
            report_printAllYN = dataLoad['report_printAllYN']
            report_createdUser = dataLoad['report_createdUser']
            report_scheduleYN  = dataLoad['report_scheduleYN']
            report_tujuan = dataLoad['report_tujuan']

        
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('INSERT INTO m_report VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                        (kode_laporan, server_id, report_judul, report_deskripsi, report_header, 
                        report_footer, report_periode, report_createDate, report_userUpdate,
                        report_lastUpdate, report_aktifYN, org_id, ktgri_id, report_printAllYN,
                        report_createdUser, report_scheduleYN, report_jmlTampilan, report_tujuan))
            
            db.commit()
            print("Template berhasil dibuat")
            return 'OK'
            


        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    def addDetailTemplate(self, kode_laporan):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT report_id, report_periode, report_printAllYN, report_judul, report_header, report_footer, report_jumlahTampilan,  report_deskripsi FROM m_report WHERE report_id="'+kode_laporan+'" ')

            detailTemplate = cursor.fetchall()

            print(detailTemplate)
            return detailTemplate

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    @app.route('/formatTemplate/<kode_laporan>', methods=['POST','GET']) 
    def formatTemplate(kode_laporan):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute(' SELECT report_id, report_periode, report_printAllYN, report_judul, report_header, report_footer, report_jumlahTampilan FROM m_report WHERE report_id = "'+kode_laporan+'" ')

            detailFormatTemplate = cursor.fetchall()

            detList = []
            for row in detailFormatTemplate:
                detDict={
                'reportId' : row[0],
                'reportPeriode' : row[1],
                'reportPrintAll' : row[2],
                'reportJudul' : row[3],
                'reportHeader' : row[4],
                'reportFooter' : row[5],
                'reportJmlTampilan' : row[6],
                }
                detList.append(detDict)

            detTemplate = json.dumps(detList)

            return detTemplate

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    @app.route('/detailFormatTemplate/<kode_laporan>', methods=['POST','GET'])
    def detailFormatTemplate(kode_laporan):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute(' SELECT c.report_id, c.report_periode, c.report_printAllYN, c.report_judul, c.report_header, c.report_footer, c.report_jumlahTampilan, c.report_deskripsi, a.nama_kolom, a.lokasi, a.format_kolom, a.lebar_kolom, b.nama_kolom as namaFooter, b.lokasi as lokasiFooter FROM m_report c LEFT JOIN m_detailF b ON c.report_id = b.report_id LEFT JOIN m_detailH a ON  c.report_id = a.report_id WHERE a.report_id = "'+kode_laporan+'"  ')

            detailFormatTemplate = cursor.fetchall()

            detList = []
            for row in detailFormatTemplate:
                detDict={
                'reportId' : row[0],
                'reportPeriode' : row[1],
                'reportPrintAll' : row[2],
                'reportJudul' : row[3],
                'reportHeader' : row[4],
                'reportFooter' : row[5],
                'reportJmlTampilan' : row[6],
                'reportDeskripsi' : row[7],
                'namaKolomH' : row[8],
                'lokasiH' : row[9],
                'formatKolomH' : row[10],
                'lebarKolomH' : row[11],
                'namaKolomF' : row[12],
                'lokasiF' : row[13]
                }
                detList.append(detDict)

            detTemplate = json.dumps(detList)

          

            return detTemplate

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")






    @app.route('/detailKolom/<kode_laporan>', methods=['POST','GET'])
    def detailKolom(kode_laporan):

        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT nama_kolom, lokasi, format_kolom, lebar_kolom FROM m_detailH WHERE report_id = "'+kode_laporan+'" ')

            detailK = cursor.fetchall()

            for x in detailK:
                i = 0
                detDict = {
                'kolom"'+str(i)+'"' : x[0]
                }
                i += 1
            
            
            detK = json.dumps(detailK)

            json.loads(detK)
            a = detK[0]

            print(detDict)
            print(a)
            return detK

            # print(detailK[0][0])
            # print(detailK[1][0])
            
            



        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")




    @app.route('/saveFormatTemplate')
    def saveFormatTemplate(self, kode_laporan, kol, lok, forK, lebK):#, judul, periode, printAll, jmlHeader, jmlFooter, jmlKolom):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            # cursor.execute('UPDATE m_report SET report_judul = "'+judul+'", report_periode ="'+periode+'", report_printAllYN = "'+printAll+'", report_header = "'+jmlHeader+'", report_footer = "'+jmlFooter+'", report_jumlahTampilan = "'+jmlKolom+'" WHERE report_id = "'+kode_laporan+'" ')
            cursor.execute('DELETE FROM m_detailH WHERE report_id ="'+kode_laporan+'"  ')
            cursor.execute('DELETE FROM m_detailF WHERE report_id ="'+kode_laporan+'"  ')
            
            for i in range (len(kol)):
                
                try:
                    cursor.execute('INSERT INTO m_detailH VALUES (%s,%s,%s,%s,%s)',( kode_laporan, kol[i], lok[i], forK[i], lebK[i]))
                    connection.commit()
                except Exception as e:
                    print(e)


            # for i in range (len(kolF)):

            #     try:
            #         cursor.execute('INSERT INTO m_detailF VALUES (%s, %s, %s, %s)',(kode_laporan, kolF[i], 'XX', str(i+1) ) )
            #         connection.commit()
            #     except Exception as e:
            #         print(e)


        except Error as e :
            print("Error while connecting file MySQL", e)


        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")







    #Menampilkan list kode Laporan yang belum ada querynya
    @app.route('/getKodeNewQuery')
    def getKodeNewQuery():
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute(''' SELECT UPPER(a.report_id) AS report_id FROM m_report a
                            LEFT JOIN m_query b on a.report_id = b.report_id
                            WHERE a.report_id NOT IN (Select report_id from m_query) ''')

            nQuery = cursor.fetchall()

            qList = []

            for i in nQuery:
                qDict={
                'reportId' : i[0]
                }
                qList.append(qDict)

            qDump = json.dumps(qList)

            return qDump

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    # Untuk membuat query pada template baru
    @app.route('/addQuery/<kode_laporan>/<dataQuery>', methods=['POST','GET'])
    def addQuery(kode_laporan,dataQuery):

        quer = json.loads(dataQuery)

        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('DELETE FROM m_query WHERE report_id ="'+kode_laporan+'"  ')
            
            for i in range (len(quer)):
                
                try:
                    # print(quer[i]+' '+str(i+1)+' '+str(datetime.datetime.now())+' '+'Y'+' '+kode_laporan)
                    
                    cursor.execute('INSERT INTO m_query VALUES (%s,%s,%s,%s,%s)',( str(i+1), quer[i], datetime.datetime.now(), 'Y', kode_laporan))
                    db.commit()



                    
                except Exception as e:
                    print(e)
                

            # clearQ = str(nQuery).replace("('",'').replace("',)","").replace("[,",'').replace("]",'')
            # print(clearQ)

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")        



    # Untuk menampilkan query yang ada pada template yang dipilih
    @app.route('/viewEditQuery/<kode_laporan>')
    def viewEditQuery(kode_laporan):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT query_query from m_query WHERE report_id="'+kode_laporan+'" ')

            editQ = cursor.fetchall()

            editL = []

            if (len(editQ)!= 14):
                for i in range (len(editQ),14):
                    editQ.append("")

            # for i in editQ:
            #     editDict = {
            #     'quer' : i[0]
            #     }
            
            dumpE = json.dumps(editQ)

            print(len(editQ))
            print(editQ)
            return dumpE


    
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")
           


#=========================================================================================
#=========================================================================================
#===================================[    SCHEDULING     ]================================
#=========================================================================================
#=========================================================================================

class Schedule:
    def __init__(self):
        self.kode_laporan = ''
        self.organisasi = ''
        self.server = ''
        self.kategori = ''
        self.header = ''
        self.keterangan = ''
        self.note = ''
        self.reportPenerima = ''
        self.reportPIC = ''
        self.grouping = ''
        self.jadwalBln = ''
        self.jadwalHari = ''
        self.jadwalTgl = ''
        self.orderby = ''
        self.aktifYN = ''
    
    
    

    def listMaker(self , kode_laporan):
        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            
            cursor.execute('SELECT sch_tanggal from t_schedule WHERE report_id = "'+kode_laporan+'" ')
            sch_tanggal = cursor.fetchall()
            cursor.execute('SELECT sch_hari from t_schedule WHERE report_id = "'+kode_laporan+'" ')
            sch_hari = cursor.fetchall()
            cursor.execute('SELECT sch_bulan from t_schedule WHERE report_id = "'+kode_laporan+'" ')
            sch_bulan = cursor.fetchall()


            print(sch_tanggal)
            print(sch_hari)
            print(sch_bulan)
            return sch_tanggal

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    


    #Hanya menampilkan kode report dimana scheduleYN = "Y" dan "D"
    @app.route('/listKodeReportEditSchedule', methods = ['POST','GET'])
    def listKodeReportEditSchedule():
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            listKodeEditSchedule = cursor.execute(' select distinct report_id from t_schedule where sch_aktifYN IN ("D", "Y") ')
            listKodeEditSchedule = cursor.fetchall()

            listKodeEdit = []

            for x in listKodeEditSchedule:
                listDict = {
                'reportId' : x[0]
                }
                listKodeEdit.append(listDict)

            kodeReportEdit = json.dumps(listKodeEdit)

            
            return kodeReportEdit
        
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
            #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    #Hanya menampilkan kode report dimana scheduleYN = N
    @app.route('/listKodeReportAddNewSchedule', methods = ['POST','GET'])
    def listKodeReportAddNewSchedule():
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            listKodeReport = cursor.execute('select report_id from m_report where report_scheduleYN = "N" ')
            listKodeReport = cursor.fetchall()

            listKode = []

            for x in listKodeReport:
                listDict = {
                'reportId' : x[0]
                }
                listKode.append(listDict)

            kodeReport = json.dumps(listKode)

            
            return kodeReport
        
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
            #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")


    #Untuk membuat schedule baru
    @app.route('/addSchedule/<dataSchedule>', methods=['POST','GET'])
    def addSchedule(dataSchedule):
        if request.method == 'POST':

            queryId = ''
            sch_id = ''
            aktifYN = 'Y'
            lastUpdate = datetime.datetime.now() 


            loadDataSchedule = json.loads(dataSchedule)
            for x in loadDataSchedule:
                kode_laporan = loadDataSchedule['report_id']
                jadwalHari = loadDataSchedule['sch_hari']
                jadwalBln = loadDataSchedule['sch_bulan']
                jadwalTgl = loadDataSchedule['sch_tanggal']
                grouping = loadDataSchedule['sch_grouping']
                reportPIC = loadDataSchedule['sch_reportPIC']
                org = loadDataSchedule['sch_org']
                kategori = loadDataSchedule['sch_kategori']
                header = loadDataSchedule['sch_header']
        
                
                keterangan = loadDataSchedule['sch_keterangan']
                note = loadDataSchedule['sch_note']
                reportPenerima = loadDataSchedule['sch_reportPen']
        
            

            try:
                db = databaseCMS.db_template()
                cursor = db.cursor()

                cursor.execute('DELETE FROM t_schedule WHERE report_id = "'+kode_laporan+'" ')
                

                cursor.execute('INSERT INTO t_schedule VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (kode_laporan, jadwalHari, jadwalBln, jadwalTgl, grouping,
                        reportPIC, org, kategori, lastUpdate, aktifYN, keterangan, note, reportPenerima))
                db.commit()

                cursor.execute('UPDATE m_report SET report_scheduleYN = "Y", report_judul ="'+header+'", report_deskripsi="'+keterangan+'"  WHERE report_id = "'+kode_laporan+'" ')
                db.commit()


                return 'Success'

            except Error as e :
                print("Error while connecting file MySQL", e)
            finally:
                    #Closing DB Connection.
                        if(db.is_connected()):
                            cursor.close()
                            db.close()
                        print("MySQL connection is closed")


    @app.route('/showDetailSchedule/<kode_laporan>', methods =['POST','GET'])                        
    def showDetailSchedule(kode_laporan):
        # kode_laporan = request.form['valKode']
        
        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT report_judul, report_deskripsi, sch_note, sch_reportPIC, sch_penerima, sch_groupBy, sch_bulan, sch_hari, sch_tanggal, sch_aktifYN from t_schedule a LEFT JOIN m_report b ON b.report_id = a.report_id WHERE b.report_id = "'+kode_laporan+'" ')

            detailSch = cursor.fetchall()

            detList = []

            
            for x in detailSch:
                detDict={
                'report_judul' : x[0],
                'report_deskripsi' : x[1],
                'sch_note' : x[2],
                'sch_PIC' : x[3],
                'sch_Pen' : x[4],
                'sch_groupBy' : x[5],
                'sch_bulan' : x[6],
                'sch_hari' : x[7],
                'sch_tanggal' : x[8],
                'sch_aktifYN' : x[9]
                }
                detList.append(detDict)

            detailSchedule = json.dumps(detList)


            
            return detailSchedule

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")


#     #Untuk menampilkan List Edit Schedule
#     def viewEditSchedule(self, kode_laporan, organisasi, server, kategori):
#         db = get_cms_schedule()

#         cursor = db.cursor()

#         view_schedule = cursor.execute('SELECT header, keterangan, note, penerima, grouping, jadwal, aktifYN from m_schedule')

#         for row in view_schedule:
#             header = row[0]
#             keterangan = row[1]
#             note = row[2]
#             penerima = row[3]
#             grouping = row[4]
#             jadwal = row[5]
#             aktifYN = row[6]


#         return view_schedule


    #Menginput hasil edit schedule
    @app.route('/editSched/<data>', methods=['POST','GET'])
    def editSched(data):

        loadData = json.loads(data)
        for i in loadData:
            header = loadData['header']
            keterangan = loadData['keterangan']
            kode_laporan = loadData['reportId']
            jadwalHari = loadData['jadwalHari']
            jadwalTgl = loadData['jadwalTgl']
            jadwalBln = loadData['jadwalBln']
            reportPIC = loadData['PIC']
            reportPenerima = loadData['Penerima']
            note = loadData['note']
            lastUpdate = loadData['lastUpdate']
            grouping = loadData['grouping']
            aktifYN = loadData['aktifYN']
        print(kode_laporan)
        print(reportPIC)
        print(reportPenerima)
        print(jadwalHari)
        print(jadwalBln)
        print(jadwalTgl)
        print(aktifYN)

        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('UPDATE m_report SET report_judul = "'+header+'", report_deskripsi="'+keterangan+'" WHERE report_id ="'+kode_laporan+'" ')
            db.commit()

            cursor.execute( 'UPDATE t_schedule SET sch_hari = "'+jadwalHari+'", sch_tanggal= "'+jadwalTgl+'", sch_bulan= "'+jadwalBln+'", sch_reportPIC= "'+reportPIC+'", sch_penerima= "'+reportPenerima+'", sch_note="'+note+'", sch_lastUpdate = "'+lastUpdate+'", sch_groupBy = "'+grouping+'", sch_aktifYN = "'+aktifYN+'" WHERE report_id = "'+kode_laporan+'"')
            db.commit()

            print(kode_laporan)
            return 'Edit Schedule Success'

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    @app.route('/getDetailReport/<kode_laporan>', methods=['POST','GET'])
    def getDetailReport(kode_laporan):
        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT report_id, report_judul, report_deskripsi, report_periode, report_footer, org_id, report_header, LEFT(report_createdDate,11), report_userUpdate FROM m_report WHERE report_id = "'+kode_laporan+'" ')

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



    @app.route('/getDetailH/<kode_laporan>', methods = ['POST','GET'])
    def getDetailH(kode_laporan):
        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT * FROM m_detailH WHERE report_id = "'+kode_laporan+'" ')

            res = cursor.fetchall()

            detL = []

            for row in res:
                detDict = {
                'reportId' : row[0],
                'namaKolom' : row[1],
                'lokasi' : row[2],
                'formatKolom' : row[3],
                'lebarKolom' : row[4]
                }
                detL.append(detDict)
            detailH = json.dumps(detL)

            return detailH
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    @app.route('/getJumlahHeader/<kode_laporan>', methods = ['POST','GET'])
    def getJumlahHeader(kode_laporan):
        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT report_header FROM m_report WHERE report_id = "'+kode_laporan+'" ')

            result = cursor.fetchall()

            jList = []

            for row in result:
                jDict = {
                'jumlahHeader' : row[0]
                }
                jList.append(jDict)

            jumlahHeader = json.dumps(jList)

          

            return jumlahHeader

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")


    @app.route('/listPIC/<kode_laporan>', methods=['POST','GET'])
    def listPIC(kode_laporan):

        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT sch_reportPIC FROM t_schedule WHERE report_id = "'+kode_laporan+'" ')
            resultPIC = cursor.fetchall()

            picL = []
            for row in resultPIC:
                picDict = {
                'PIC' : row[0]
                }
                picL.append(picDict)

            resultPIC = json.dumps(picL)

            

            return resultPIC
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    @app.route('/listPenerima/<kode_laporan>', methods=['POST','GET'])
    def listPenerima(kode_laporan):

        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT sch_penerima FROM t_schedule WHERE report_id = "'+kode_laporan+'" ')
            resultPen = cursor.fetchall()

            penL = []
            for row in resultPen:
                penDict = {
                'Penerima' : row[0]
                }
                penL.append(penDict)

            resultPenerima = json.dumps(penL)


            return resultPenerima
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    @app.route('/getQuery/<kode_laporan>', methods=['POST','GET'])
    def getQuery(kode_laporan):
        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT report_id, query_query, query_no FROM m_query WHERE report_id= "'+kode_laporan+'" ')

            result = cursor.fetchall()

            qList = []

            for row in result:
                qDict = {
                'reportId' : row[0],
                'query' : row[1],
                'query_no' : row[2]
                }
                qList.append(qDict)

            resultQuery = json.dumps(qList)

            return resultQuery
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")







    @app.route('/testQ/<kode_laporan>', methods = ['POST','GET'])
    def testQ(kode_laporan):
        db = databaseCMS.db_template()
        curr = db.cursor(buffered = True)

        sql1 = 'SELECT report_id, query_query, query_no FROM m_query WHERE report_id= "'+kode_laporan+'" '
            
        curr.execute(sql1)

        query = [x[1] for x in curr.fetchall()] #dari hasil sql1, kita mau ambil kolom query nya saja, kenapa tidak SELECT query nya saja ?, karena nnti untuk mengambil
                                                #atribut nama_user dst.

        print(query)

        lengthOfQuery = len(query) #mau ambil berapa panjang/berapa baris isi dari atribut query, untuk keperluan looping

        for i in range (lengthOfQuery):
            sql2 = query[i].replace("~","'")
            curr.execute(sql2)
            
            
        result = curr.fetchall()
        print(result)
        print(sql2)

if __name__ == "__main__":
    app.run(debug=True, port='5002')