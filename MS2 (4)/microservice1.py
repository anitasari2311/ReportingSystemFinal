from flask import Flask, render_template, redirect, url_for, request, json, session, flash
import datetime
import pymysql
import random
import mysql.connector
from auth import auth_login
from mysql.connector import Error
from db import databaseCMS
from templatelaporan import TemplateLaporan
#from PIL import Image
import json

class RequestLaporan:
   
    def __init__(self):
        self.req_id = ''
        self.org_id = ''
        self.ktgri_id = ''
        self.req_kodeLaporan = ''
        self.req_judul = ''
        self.req_deskripsi = ''
        self.req_tujuan = ''
        self.req_tampilan = ''
        self.req_periode = ''
        self.req_deadline = ''
        self.req_file = ''
        self.req_PIC = ''
        self.req_penerima = ''
        self.sch_id = ''
        self.report_id = ''
        self.query_id = ''
        self.reqSch_hari = ''
        self.reqSch_bulan = ''
        self.reqSch_tanggal = ''
        self.reqSch_groupBy = ''
        self.reqSch_reportPIC = ''
        self.reqSch_orgNama = ''
        self.reqSch_ktgriNama = ''
        self.reqSch_lastUpdate = ''
        self.reqSch_aktifYN = ''
        self.reqSch_reportPenerima = ''
    

    #BUAT GENERATE REQUESTID SECARA OTOMATIS
    def get_numberID(self):
        try: 
            db = databaseCMS.db_request()
            

            cursor = db.cursor()
     
            cursor.execute('select count(req_id) from t_request where month(req_date) = month(now())')
            
            record = cursor.fetchone()
            clear = str(record).replace('(','').replace(',)','')
            return int(clear)

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")
        
    def generateRequestID(self):
        now  = datetime.datetime.now()
        requestID = 'REQ_'+str(now.strftime('%Y%m'))+str(self.get_numberID()).zfill(5)
        return requestID
    
    
    #BUAT MENDAPATKAN LIST ORGANISASI DARI MYSQL
    def namaOrganisasi(self):
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
        
            listOrg = cursor.execute('select org_id, org_nama from m_organisasi where org_aktifYN = "Y" order by org_id')
            listOrg = cursor.fetchall()
            
            return listOrg

        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")
                    
    #BUAT MENDAPATKAN LIST KATEGORI DARI MYSQL
    def namaDept(self):
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
     
            cursor.execute('select ktgri_id, ktgri_nama from m_kategori where ktgri_aktifYN = "Y" Order by ktgri_id')
            
            listDept = cursor.fetchall()
   
            return listDept
            

        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    #BUAT MENAMPILKAN LIST PIC DARI MYSQL
    def namaPIC(self):
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
     
            cursor.execute(''.join(['select user_id, user_name, user_email from m_user where user_flag = "User" ']))
            
            listPIC = cursor.fetchall()

             
            return listPIC
            

        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    #BUAT MENAMPILKAN LIST PENERIMA DARI MYSQL
    def namaPenerima(self):
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
     
            cursor.execute(''.join(['select user_id, user_name, user_email from m_user where user_flag = "User" ']))
            
            listPen = cursor.fetchall()

             
            return listPen
            

        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")
                    
    #BUAT MENAMPILKAN LIST REQUEST PADA MENU
    def listRequestUser(self, username):
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute  (''.join(['SELECT req_id ,IFNULL(req_judul,""), IFNULL(req_date,""),IFNULL(req_deadline,""), IFNULL(req_status,""), IFNULL(req_PIC,""), IFNULL(req_kodelaporan, "") from t_request WHERE (req_status IN ("On Process" , "Waiting") OR req_status LIKE "%Rejected%") AND user_id="'+session['user_id']+'" ORDER BY req_id desc']))
            listReqUser = cursor.fetchall()
            print(listReqUser)
            return listReqUser
        
        except Error as e :
                print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                if(db.is_connected()):
                    cursor.close()
                    db.close()
                print("MySQL connection is closed")
        

    #BUAT MENAMPILKAN REQUEST YANG UDAH KELAR
    def listFinished(self, username):
        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()
            listFinished = cursor.execute(''.join(['SELECT req_kodeLaporan, req_judul, req_date, req_PIC, req_endDate, b.req_id, rating FROM t_request a LEFT JOIN m_rating b ON a.req_id = b.req_id WHERE req_status = "Finished" and user_id="'+session['user_id']+'" ORDER BY req_date desc']))
            listFinished = cursor.fetchall()
            return listFinished

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")

    #BUAT INSERT REQUEST DAN SCHEDULE BARU                
    def requestLaporanBaru(self, prog_id, user_id, org_id, ktgri_id, req_kodeLaporan, req_judul, req_deskripsi,
                           req_tujuan, req_tampilan, req_periode, req_deadline, req_file, req_PIC,
                           reqSch_hari, reqSch_bulan, reqSch_tanggal, 
                           reqSch_orgNama,reqSch_ktgriNama, reqSch_lastUpdate, reqSch_reportPIC, reqSch_penerima,
                           reqSch_aktifYN = 'Y', reqSch_groupBy = 'Dr. Andre Lembong', 
                           req_dateAccept = None, req_endDate=None, 
                           req_status='Waiting', req_prioritas='1'
                          ):
        self.req_id = self.generateRequestID()
        self.prog_id = prog_id
        self.user_id  = user_id
        self.org_id = self.namaOrganisasi()
        self.ktgri_id = ktgri_id
        self.req_kodeLaporan = req_kodeLaporan
        self.req_judul = req_judul
        self.req_deskripsi = req_deskripsi
        self.req_tujuan = req_tujuan 
        self.req_tampilan = req_tampilan
        self.req_periode = req_periode                                          
        self.req_deadline = req_deadline
        self.req_file = req_file
        self.req_date  = datetime.datetime.now()
        self.req_dateAccept = req_dateAccept
        self.req_endDate = req_endDate
        self.req_status = req_status
        self.req_PIC = req_PIC
        self.req_prioritas = req_prioritas

        
        self.reqSch_hari = reqSch_hari
        self.reqSch_bulan = reqSch_bulan
        self.reqSch_tanggal = reqSch_tanggal
        self.reqSch_groupBy = reqSch_groupBy
        self.reqSch_orgNama = self.namaOrganisasi()
        self.reqSch_ktgriNama = reqSch_ktgriNama
        self.reqSch_lastUpdate = datetime.datetime.now()
        self.reqSch_aktifYN = reqSch_aktifYN

        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute('INSERT INTO t_request VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (self.req_id, prog_id, user_id, org_id, ktgri_id, req_kodeLaporan, req_judul, req_deskripsi,
                           req_tujuan, req_tampilan, req_periode,req_deadline,req_file, self.req_date,
                            req_dateAccept, req_endDate, self.req_status, req_PIC,
                            req_prioritas))
            db.commit()

            print("Successed")

            cursor.execute('INSERT INTO t_reqSchedule VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (self.req_id, reqSch_hari, reqSch_bulan, reqSch_tanggal, reqSch_groupBy, reqSch_reportPIC, reqSch_orgNama, reqSch_ktgriNama, self.reqSch_lastUpdate, reqSch_aktifYN, reqSch_penerima))
            db.commit()

            record = cursor.fetchone()
            print ("Your connected...",record)

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")
             
    #BUAT NAMPILIN GAMBAR DI DETAIL TASK
    # def showImage(self, request_id):
    #     try: 
    #         connection = mysql.connector.connect(
    #         host='localhost',
    #         database='cms_request',
    #         user='root',
    #         password='qwerty')
    #         if connection.is_connected():
    #             db_Info= connection.get_server_info()
    #         print("Connected to MySQL database...",db_Info)

    #         cursor = connection.cursor()
    #         cursor.execute('SELECT req_file from t_request where req_id = "'+request_id+'"')
    #         connection.commit()

    #         record = cursor.fetchone()[0]
    #         return record
    #         print ("Your connected...",record)

    #     except Error as e :
    #         print("Error while connecting file MySQL", e)
    #         flash('Error,', e)
    #     finally:
    #             #Closing DB Connection.
    #                 if(connection.is_connected()):
    #                     cursor.close()
    #                     connection.close()
    #                 print("MySQL connection is closed")

    #BUAT INSERT EDIT REPORT
    def requestEditLap(self, prog_id, user_id,req_report, req_kodeLaporan, req_deskripsi,
                           req_tampilan, req_deadline, req_file, req_PIC,
                           reqSch_hari, reqSch_bulan, reqSch_tanggal,
                            reqSch_groupBy = 'Dr. Andre Lembong', reqSch_reportPIC = None,
                           reqSch_ktgriNama = None, reqSch_orgNama = None, reqSch_aktifYN = 'Y',
                           req_dateAccept = None, req_endDate=None, req_status='Waiting', req_prioritas='1',
                           reqSch_penerima=None):
        self.req_id = self.generateRequestID()
        self.prog_id = prog_id
        self.user_id  = user_id
        self.org_id = ''
        self.ktgri_id = ''
        self.req_kodeLaporan = req_kodeLaporan
        self.req_deskripsi = req_deskripsi
        self.req_tampilan = req_tampilan
        self.req_periode = ''                                         
        self.req_deadline = req_deadline
        self.req_file = req_file
        self.req_date  = datetime.datetime.now()
        self.req_dateAccept = req_dateAccept
        self.req_endDate = req_endDate
        self.req_status = req_status
        self.req_PIC = req_PIC
        self.req_prioritas = req_prioritas
        self.last_report = TemplateLaporan().getDataReport(req_report)
        self.req_judul = self.last_report[1]
        self.req_tujuan = self.last_report[2]

        self.reqSch_hari = reqSch_hari
        self.reqSch_bulan = reqSch_bulan
        self.reqSch_tanggal = reqSch_tanggal
        self.reqSch_groupBy = reqSch_groupBy
        self.reqSch_lastUpdate = datetime.datetime.now()

       
        
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute('INSERT INTO t_request VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (self.req_id, prog_id, user_id, self.org_id, self.ktgri_id, req_kodeLaporan, self.req_judul, req_deskripsi,
                           self.req_tujuan, req_tampilan, self.req_periode, req_deadline, req_file, self.req_date,
                            req_dateAccept, req_endDate, self.req_status, req_PIC, req_prioritas))
            db.commit()

            record = cursor.fetchone()

            cursor.execute('INSERT INTO t_reqSchedule VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (self.req_id, reqSch_hari, reqSch_bulan, reqSch_tanggal, reqSch_groupBy, reqSch_reportPIC, reqSch_orgNama, reqSch_ktgriNama, self.reqSch_lastUpdate, reqSch_aktifYN,
                            reqSch_penerima))
            db.commit()

            record = cursor.fetchone()
            print ("Your connected...",record)

        except Error as e :
            print("Error while connecting file MySQL", e)
            flash('Error,', e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")


    #BUAT UPDATE STATUS CANCEL PADA REQUEST
    def cancelRequest(self, request_id):
        self.cancel_request=''
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute(''.join(['UPDATE t_request SET req_status = "Cancel"  WHERE req_id = "'+request_id+'"']))            
            
            db.commit()
           
            cancel_request = cursor.fetchone()
           
            return cancel_request
        except Error as e : 
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")
    
    #PROSES REJECT REQUEST
    def rejectRequest(self, request_id):
        try:
            db = databaseCMS.db_request()
            cursor = db.cursor()
            cursor.execute('UPDATE t_request SET req_status = "Rejected by '+session['username']+'" WHERE req_id = "'+request_id+'" ')

            db.commit()
            
        except Error as e : 
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")
    ##################################################################################################
    #BUAT LIST AVAILABLE TASK
    def availableTask(self):
        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            listAvailTask = cursor.execute('''SELECT req_id, req_judul, user_name, ktgri_nama,
                                        req_date, req_deadline, req_prioritas
                                        FROM t_request a
                                        LEFT JOIN m_user b
                                            ON  a.user_id = b.user_id
                                        LEFT JOIN m_kategori c
                                            ON  a.ktgri_id = c.ktgri_id
                                        WHERE req_status LIKE 'Waiting%' ORDER BY req_deadline asc''')
            listAvailTask = cursor.fetchall()


            for row in listAvailTask:
                requestId = row[0]
                requestJudul = row[1]
                requestNama = row[2]
                requestKategori = row[3]
                requestTanggal = row[4]
                requestDeadline = row[5]
                requstPrioritas = row[6]

            return listAvailTask
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")

    #BUAT LIST TASK PROGRAMMER
    def listTask(self):
        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            #listTask = cursor.execute(''.join(['SELECT req_id, req_judul, user_name, ktgri_nama, req_date, req_deadline, req_prioritas FROM t_request a LEFT JOIN m_user b ON  a.user_id = b.user_id LEFT JOIN m_kategori c ON  a.ktgri_id = c.ktgri_id WHERE req_PIC = "'+session['username']+'" ORDER BY req_id']))
            listTask = cursor.execute('SELECT req_id, req_judul, user_name, ktgri_nama, req_date, req_deadline, req_prioritas, req_status, prog_id FROM t_request a LEFT JOIN m_user b ON  a.user_id = b.user_id LEFT JOIN m_kategori c ON  a.ktgri_id = c.ktgri_id WHERE req_status = "On Process" and req_PIC = "'+session['username']+'" ORDER BY req_id desc')
            listTask = cursor.fetchall()
            
            return listTask

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")
   
    #BUAT TAMPILIN TASK YANG UDAH PERNAH DIKERJAIN
    def historyTask(self):
        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            
            cursor.execute('SELECT req_id, req_judul, user_name, ktgri_nama, req_date, req_endDate, req_kodelaporan FROM t_request a LEFT JOIN m_user b ON  a.user_id = b.user_id LEFT JOIN m_kategori c ON  a.ktgri_id = c.ktgri_id WHERE req_status = "Finished" and req_PIC = "'+session['username']+'" ORDER BY req_id desc')
            historyTask = cursor.fetchall()
            
            return historyTask

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")

    #BUAT TAMPILIN DETAIL TASK SAAT TEKAN TOMBOL SELECT
    def getDetailTask(self, request_id):
        self.detail_task=''
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute(''.join(['SELECT a.req_id, req_judul, req_deskripsi, org_nama, ktgri_nama, req_tampilan, req_periode, req_deadline, req_file, reqSch_tanggal, reqSch_bulan, reqSch_hari, req_kodeLaporan, req_tujuan  FROM t_request a LEFT JOIN m_organisasi b ON a.org_id = b.org_id LEFT JOIN m_kategori c ON a.ktgri_id = c.ktgri_id LEFT JOIN t_reqSchedule d ON a.req_id = d.req_id  WHERE a.req_id = "'+request_id+'"']))            
           
            detail_task = cursor.fetchone()
            
            print(detail_task)
            return detail_task

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    #BUAT TAMPILIN KODE REPORT DI PAGE EDIT REPORT
    def getReportIDEdit(self, username):
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_request',
            user='root',
            password='qwerty')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()
     
            cursor.execute('select req_kodelaporan from t_request where user_id = "'+session['user_id']+'" ')
            
            listKodeReportEdit = cursor.fetchall()
            
            return listKodeReportEdit

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")     

    #BUAT ACCEPT REQUEST
    def accRequest(self, request_id):
        self.confirm=''
        self.accReq = datetime.datetime.now()
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()

            cursor.execute('update t_request set req_dateAccept = "'+str(self.accReq)+'",req_status = "On Process", req_PIC = "'+session['username']+'", prog_id = "'+session['user_id']+'" where req_id = "'+request_id+'"')

            db.commit()
            confirmReq = cursor.fetchall()


            return confirmReq

            print ("Record Updated successfully ")
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")


    #BUAT UPDATE STATUS REQUEST JADI CONFIRMED
    def confirmRequest(self, request_id):
        self.confirm_request =''
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute(''.join(['UPDATE t_request SET req_status = "Confirmed"  WHERE req_id = "'+request_id+'"']))            
            
            db.commit()
            
            confirm_request = cursor.fetchone()
         
            return confirm_request
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

        

    #BUAT PROGRAMMER TELAH SELESAI MENGERJAKAN REQUEST DAN 
    #MENGINPUT KODE LAPORAN UNTUK REQUEST TERSEBUT 
    def listKodeLaporan(self):
        try:
            db = databaseCMS.db_template()

            cursor = db.cursor()
            cursor.execute('SELECT report_id from m_report')

            listKodeLap = cursor.fetchall()

            return listKodeLap
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed") 


    #KASIH RATING KE REQUEST YANG UDAH SELESAI
    def finishRating(self, request_id, rating, keterangan):
        try:
            db = databaseCMS.db_request()
            cursor = db.cursor()
            cursor.execute(' UPDATE m_rating SET rating = "'+rating+'" , keterangan ="'+keterangan+'" WHERE req_id = "'+request_id+'"    ')

            db.commit()

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed") 


    #BUAT TOMBOL FINISH CONNECT TO DB TO GET STATUS FINISHED
    def finishRequest(self, request_id):
        self.finish_request =''
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute(''.join(['UPDATE t_request SET req_status = "Finished"  WHERE req_id = "'+request_id+'"']))            
        
            db.commit()
            
            cursor.execute('INSERT INTO m_rating VALUES (%s,%s,%s)',(request_id,'0',''))

            db.commit()
            # finish_request = cursor.fetchone()
         
            # return finish_request
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")    

    #BUAT TOMBOL FINISH UNTUK INPUT KODE REPORT DI TASK PROGRAMMER
    def inputKodeFinish(self, request_id, kodLap):
        self.endDate = datetime.datetime.now()
        
        try: 
            db = databaseCMS.db_request()

            cursor = db.cursor()
            cursor.execute(''.join(['UPDATE t_request SET req_endDate = "'+str(self.endDate)+'", req_kodeLaporan = "'+kodLap+'"  WHERE req_id = "'+request_id+'"']))            
            
            db.commit()

            # kode_finish = cursor.fetchone()

            # return kode_finish
            
            print(request_id, kodLap)
         
            
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    #BUAT TAMPILIN AVAILABLE TASK DI LAYAR SPV
    def availableTaskSPV(self):
        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            listAvailTaskSPV = cursor.execute('''SELECT user_name, user_posisi, req_id, req_judul, ktgri_nama, org_nama, req_date, 
                                            req_deadline, req_prioritas
                                            FROM    m_user a
                                            LEFT JOIN   t_request b
                                            ON  a.user_id = b.user_id
                                            LEFT JOIN m_kategori c
                                            ON  b.ktgri_id = c.ktgri_id
                                            LEFT JOIN   m_organisasi d
                                            ON  b.org_id = d.org_id
                                            WHERE req_status LIKE 'Waiting%' ORDER BY req_deadline asc ''')
            listAvailTaskSPV = cursor.fetchall()

            for taskSPV in listAvailTaskSPV:
                uName = taskSPV[0]
                posisi = taskSPV[1]
                reqId = taskSPV[2]
                reqJud = taskSPV[3]
                ktgri = taskSPV[4]
                org = taskSPV[5]
                rDate = taskSPV[6]            
                rDead = taskSPV[7]
                rPrio = taskSPV[8]
                

                return listAvailTaskSPV
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")

    #BUAT TAMPILIN TASK YANG LAGI DIKERJAIN, DI LAYAR SPV
    def onProgressTask(self):
        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            cursor.execute('''SELECT user_name, req_id, req_judul, ktgri_nama, org_nama, req_date, 
                            req_dateAccept, req_PIC, req_deadline
                            FROM m_user a
                            LEFT JOIN t_request b
                            ON a.user_id = b.user_id
                            LEFT JOIN m_kategori c
                            ON b.ktgri_id = c.ktgri_id
                            LEFT JOIN m_organisasi d
                            ON b.org_id = d.org_id
                            WHERE req_status = "On Process" ''')

            onProgTask = cursor.fetchall()

            for onProg in onProgTask:
                onNama = onProg[0]
                onId = onProg[1]
                onJud = onProg[2]
                onKat = onProg[3]
                onOrg = onProg[4]
                onDate = onProg[5]
                onDateA = onProg[6]
                onPIC = onProg[7]
                onDead = onProg[8]
                return onProgTask

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")

    #BUAT UPDATE REQUEST JADI PRIORITAS
    def prioritas(self, request_id):
        self.update_prioritas=''
        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            cursor.execute('UPDATE t_request SET req_prioritas = "0" WHERE req_id= "'+request_id+'" ')
            db.commit()

            update_prioritas = cursor.fetchone()

            return update_prioritas

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")

    #BUAT NGEMBALIIN REQUEST JADI "NORMAL" / UNIMPORTANT
    def undoPrioritas(self, request_id):
        self.undo_prioritas = ''

        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            cursor.execute('UPDATE t_request SET req_prioritas = "1" WHERE req_id= "'+request_id+'" ')
            db.commit()

            undo_prioritas = cursor.fetchone()

            return undo_prioritas

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")

    #BUAT GANTI PASSWORD
    def changePass(self, old_password, new_password, confirm_password):

        try:
            db = databaseCMS.db_request()

            cursor = db.cursor()

            cursor.execute(' UPDATE m_user SET user_password = "'+confirm_password+'" WHERE user_id = "'+session['user_id']+'" and user_password = "'+old_password+'" ')
            db.commit()

            undo_prioritas = cursor.fetchone()

            return undo_prioritas

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
            if(db.is_connected()):
                cursor.close()
                db.close()
            print("MySQL connection is closed")