import datetime
import pymysql
import random
import mysql.connector
#from requestlaporan import RequestLaporan
from mysql.connector import Error
from db import databaseCMS
  
class TemplateLaporan:
    def __init__(self):
        self.kode_laporan = ''

#BUAT GET DATA REPORT_ID

    @app.route('/getReportId', methods=['POST','GET'])
    def getReportID():
        try: 

            db = databaseCMS.db_template()
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_template',
            user='root',
            password='mis301')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()
     
            cursor.execute('select report_id from m_report')
            
            listKodeReport = cursor.fetchall()
            
            return listKodeReport

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")     

#BUAT NAMPILIN KOLOM BERDASARKAN REPORT_ID YANG DIPILIH        
    def viewReportID(self, kodeLaporan):
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_template',
            user='root',
            password='mis301')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()
        
            cursor.execute(''.join(['SELECT report_tampilan FROM m_report WHERE report_id = "'+kodeLaporan+'"']))

            connection.commit()

            record = cursor.fetchone()
            print ("Your connected...",record)

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")
    
        
    def getDataReport(self, report_id):
        self.judul = ''
        self.tujuan = ''

        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_template',
            user='root',
            password='mis301')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()
     
            cursor.execute(''.join(['select report_id ,report_judul, report_tujuan from m_report where report_id = "'+report_id+'"']))
            
            record = cursor.fetchone()
            # 
            return record

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")

    def getCurrentDisplay(self, report_id):
        self.current_display=''
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_template',
            user='root',
            password='mis301')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()
     
            cursor.execute(''.join(['select nama_kolom from m_detailH where report_id = "'+report_id+'"']))
            
            record = cursor.fetchall()
            clear = str(record).replace("('",'').replace("',)",'').replace('[','').replace(']','')
            return clear

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")

    def getRevisiDisplay(self, request_id):
        self.revisi_display=''
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_request',
            user='root',
            password='mis301')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()
     
            #cursor.execute(''.join(['select req_id, req_tampilan from t_request where req_id = "'+request_id+'"']))
            cursor.execute('select req_id, req_tampilan from t_request where req_id = "'+request_id+'"')
            record = cursor.fetchall()
            #clear = str(record).replace("('",'').replace("',)",'')
            return record

        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")

    def updateStatusCancel(self, request_id):
        self.cancel=''
        try: 
            connection = mysql.connector.connect(
            host='localhost',
            database='cms_request',
            user='root',
            password='mis301')
            if connection.is_connected():
                db_Info= connection.get_server_info()
            print("Connected to MySQL database...",db_Info)

            cursor = connection.cursor()

            cursor.execute('update t_request set req_status = "Cancelled" where req_id = "'+request_id+'"')

            connection.commit()
            record = cursor.fetchone()
            return record
            print ("Record Updated successfully ")
        except Error as e :
            print("Error while connecting file MySQL", e)
        finally:
                #Closing DB Connection.
                    if(connection.is_connected()):
                        cursor.close()
                        connection.close()
                    print("MySQL connection is closed")


                    
#TemplateLaporan().viewReportID('DGM-0001')
#TemplateLaporan().updateStatusCancel('DGM-0001')

