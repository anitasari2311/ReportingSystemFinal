from flask import Flask, render_template, redirect, url_for, request, json, session
import datetime
import pymysql
import random
import mysql.connector
from mysql.connector import Error
from db import databaseCMS
import json
    

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


    def listKodeOrgServ(self):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()
            
            listKodeOrgServ = cursor.execute('select report_id, server_nama, org_nama from M_report a LEFT JOIN cms_request.m_organisasi c ON a.Org_id = c.org_id  left join M_server b ON b.server_id = a.server_id')
            listKodeOrgServ = cursor.fetchall()

            

            for row in listKodeOrgServ:
                    repId = row[0]
                    servName = row[1]
                    orgName = row[2]

            x = {
            "kodeReport": row[0],
            "namaServ": row[1],
            "namaorg": row[2]
            }

            y = json.dumps(x)
             
            print(y) 
            return listKodeOrgServ
            
        
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
            #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")


    def listKodeReport(self):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            listKodeReport = cursor.execute('select report_id from m_report')
            #listKodeReport = cursor.execute('select report_id, server_nama from M_report  a left join M_server b ON b.server_id = a.server_id;')

            listKodeReport = cursor.fetchall()

            for row in listKodeReport:
                repId = row[0]
                

            
            return listKodeReport
        
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
            #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    # LIST KODE REPORT YANG SUDAH MEMILIKI QUERY
    def listKodeReportQuery(self):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('select distinct UPPER(report_id) AS report_id from m_query ORDER BY report_id ASC ')
            #listKodeReport = cursor.execute('select report_id, server_nama from M_report  a left join M_server b ON b.server_id = a.server_id;')

            listKodeReportQuery = cursor.fetchall()
            
            
            
            
            return listKodeReportQuery
        
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
            #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    def listKodeReportAddNewSchedule(self):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('select UPPER(report_id) AS report_id from m_report where report_scheduleYN = "N" ')
            #listKodeReport = cursor.execute('select report_id, server_nama from M_report  a left join M_server b ON b.server_id = a.server_id;')

            listKodeReportS = cursor.fetchall()

            for row in listKodeReportS:
                repId = row[0]
                

            
            return listKodeReportS
        
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
            #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    def listKodeReportEditSchedule(self):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('select UPPER(report_id) AS report_id from m_report where report_scheduleYN = "Y"  or report_scheduleYN = "D" ')
            #listKodeReport = cursor.execute('select report_id, server_nama from M_report  a left join M_server b ON b.server_id = a.server_id;')

            listKodeLap = cursor.fetchall()

            for row in listKodeLap:
                repId = row[0]
                

            
            return listKodeLap
        
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
            #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")


        #Mengambil nama organisasi spesifik
    def listNamaOrganisasi(self):
        self.list_org = ''
        # if request.method == 'POST':
    
        try: 
            db = databaseCMS.db_request()
            cursor = db.cursor()

            listOrg = cursor.execute('SELECT org_id, org_nama FROM cms_request.m_organisasi ORDER BY org_nama')
            #listOrg = cursor.execute('select org_id, org_nama from m_organisasi where org_aktifYN = "Y" order by org_id')            
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


        #Mengambil nama server spesifik
    def listNamaServer(self):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            listServer = cursor.execute('SELECT server_id, server_nama from m_server where server_aktifYN ="Y" order by server_id')

            listServer = cursor.fetchall()

            return listServer

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")



    #Mengambil list kategori
    def listKategori(self):
        try: 
            db = databaseCMS.db_request()
            cursor = db.cursor()

            listKategori = cursor.execute('SELECT ktgri_id, ktgri_nama from m_kategori order by ktgri_nama')

            listKategori = cursor.fetchall()

            return listKategori

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")


    #Template
    def addNewTemplate(self, kodeLapFix, server_id, report_judul, report_deskripsi,
                        report_header, report_footer,
                        report_periode, report_createDate, report_userUpdate, 
                        report_lastUpdate, report_aktifYN, org_id, ktgri_id,
                        report_printAllYN, report_createdUser, report_scheduleYN, 
                        report_jumlahTampilan, report_tujuan):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('INSERT INTO m_report VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                        (kodeLapFix, server_id, report_judul, report_deskripsi, report_header, 
                        report_footer,
                        report_periode, report_createDate, report_userUpdate, 
                        report_lastUpdate, report_aktifYN, org_id, ktgri_id,
                        report_printAllYN, report_createdUser, report_scheduleYN,
                        report_jumlahTampilan, report_tujuan))
            

            

            db.commit()

            print("Template berhasil dibuat")


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

    
    def detailFormatTemplate(self, kode_laporan):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute(' SELECT a.nama_kolom, a.lokasi, a.format_kolom, a.lebar_kolom, b.nama_kolom as namaFooter, b.lokasi as lokasiFooter FROM m_detailH a LEFT JOIN m_detailF b ON a.report_id = b.report_id WHERE a.report_id = "'+kode_laporan+'"  ')

            detailFormatTemplate = cursor.fetchall()

            print(detailFormatTemplate)
            return detailFormatTemplate

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")


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
                    db.commit()
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
    def insQuery(self):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute(''' SELECT UPPER(a.report_id) AS report_id FROM m_report a
                            LEFT JOIN m_query b on a.report_id = b.report_id
                            WHERE a.report_id NOT IN (Select report_id from m_query) 
                            ORDER BY report_id ''')

            nQuery = cursor.fetchall()

            # clearQ = str(nQuery).replace("('",'').replace("',)","").replace("[,",'').replace("]",'')
            # print(clearQ)
            return nQuery

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    # Untuk membuat query pada template baru
    def addQuery(self,kode_laporan,quer):
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
    def viewEditQuery(self, kode_laporan):
        try: 
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT query_query from m_query WHERE report_id="'+kode_laporan+'" ')

            editQ = cursor.fetchall()
            if (len(editQ) != 14):
                for i in range (len(editQ), 14):
                    editQ.append("")

            # editQ = str(hasil).replace("('",'')
            

            print (len(editQ))
            return editQ
    
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")


    ###############################################################################################

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

    def getOrgLaporan(self, kode_laporan):
        try:
            db = databaseCMS.db_request()
            cursor = db.cursor()

            cursor.execute('SELECT org_nama from m_organisasi a LEFT JOIN cms_template.m_report b ON b.org_id = a.org_id WHERE report_id ="'+kode_laporan+'"')

            org = cursor.fetchone()
            clear = str(org).replace("('",'').replace("',)","")
            return clear

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

    def getKategoriLaporan(self, kode_laporan):
        try:
            db = databaseCMS.db_request()
            cursor = db.cursor()

            cursor.execute('SELECT ktgri_nama from m_kategori a LEFT JOIN cms_template.m_report b ON b.ktgri_id = a.ktgri_id WHERE report_id ="'+kode_laporan+'"')

            kategori = cursor.fetchone()
            clear = str(kategori).replace("('",'').replace("',)","")
            return clear
            
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")

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

    def showDetailSchedule(self, kode_laporan):
        # kode_laporan = request.form['valKode']
        
        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('SELECT report_judul, report_deskripsi, sch_note, sch_reportPIC, sch_penerima, sch_groupBy, sch_bulan, sch_hari, sch_tanggal, sch_aktifYN from t_schedule a LEFT JOIN m_report b ON b.report_id = a.report_id WHERE b.report_id = "'+kode_laporan+'" ')


            detailSchedule = cursor.fetchone()

            print(detailSchedule)
            return detailSchedule

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
        #Closing DB Connection.
            if(db.is_connected()):
                    cursor.close()
                    db.close()
            print("MySQL connection is closed")



    #Untuk membuat schedule baru
    def addSchedule(self, kode_laporan, header, keterangan, note, reportPIC, reportPenerima, 
                    grouping, jadwalBln, jadwalHari, jadwalTgl,  org, kategori, sch_id = '',
                    aktifYN = 'Y', lastUpdate = datetime.datetime.now()):

        # self.kode_laporan   = kode_laporan
        # self.header         = header
        # self.keterangan     = keterangan
        # self.note           = note
        # self.reportPIC      = reportPIC
        # self.reportPenerima = reportPenerima
        # self.grouping       = grouping
        # self.jadwalBln      = jadwalBln
        # self.jadwalHari     = jadwalHari
        # self.jadwalTgl      = jadwalTgl
        # self.sch_id         = ''
        # self.org            = org
        # self.kategori       = kategori
        # self.aktifYN        = aktifYN
        # self.lastUpdate     = lastUpdate
        # self.queryId        = queryId
        

        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            

            cursor.execute('INSERT INTO t_schedule VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (kode_laporan, jadwalHari, jadwalBln, jadwalTgl, grouping,
                    reportPIC, org, kategori, lastUpdate, aktifYN, keterangan, note, reportPenerima))
            

            cursor.execute('UPDATE m_report SET report_scheduleYN = "Y", report_judul ="'+header+'", report_deskripsi="'+keterangan+'"  WHERE report_id = "'+kode_laporan+'" ')
            db.commit()

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

    def deactivateSchedule(self, kode_laporan):
        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()

            cursor.execute('UPDATE t_schedule SET sch_aktifYN = "N" WHERE report_id = "'+kode_laporan+'" ')

            db.commit()


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
    def editSchedule(self, kode_laporan, header, keterangan, note, jadwalBln, jadwalHari, jadwalTgl, reportPIC, reportPenerima, 
                    lastUpdate , aktifYN = 'Y'):

        try:
            db = databaseCMS.db_template()
            cursor = db.cursor()
        # header = request.getform['']
        # keterangan = request.getform['']
        # note = request.getform['']
        # penerima = request.getform['']
        # grouping = request.getform['']
        # orderby = request.getform['']
        # jadwal = request.getform['']

        # sql = 'INSERT INTO m_schedule VALUES %s, %s, %s, %s, %s, %s, %s'
        # val = kode_laporan, organisasi, server, kategori, header, keterangan, note, penerima, grouping, orderby, jadwal

            cursor.execute('UPDATE m_report SET report_judul = "'+header+'", report_deskripsi = "'+keterangan+'" ')
            db.commit()
            cursor.execute( 'UPDATE t_schedule SET sch_hari = "'+jadwalHari+'", sch_tanggal= "'+jadwalTgl+'", sch_bulan= "'+jadwalBln+'", sch_reportPIC= "'+reportPIC+'", sch_penerima= "'+reportPenerima+'", sch_note="'+note+'", sch_lastUpdate = "'+str(lastUpdate)+'" WHERE report_id = "'+kode_laporan+'"')
            db.commit()


        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(db.is_connected()):
                        cursor.close()
                        db.close()
                    print("MySQL connection is closed")

#     #
#     def runScheduleToday():

#         db = get_cms_schedule
#         cursor = db.cursor()

#         sql = '"SELECT kodeLap, organisasi, kategori, penerima from m_schedule WHERE jadwal = "'+ getdate()+''

#         run_today = cursor.execute(sql)


#     def successRunSchedule():

#         ERROR = NONE

#     def failRunSchedule():
#         ERROR

#============================================================================================#


