from flask import Flask, render_template, redirect, url_for, request, json, session, flash, jsonify
import datetime
import pymysql
import mysql.connector
from mysql.connector import Error
from db import databaseCMS
import json
import requests
import xlsxwriter

app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'
app.secret_key = 'ms3'






# @app.route('/testQuery/<kode_laporan>', methods=['POST','GET'])
# def testQuery(kode_laporan):
#     getQ = requests.get('http://127.0.0.1:5002/getQuery/'+kode_laporan)
#     qResp = json.dumps(getQ.json())
#     loadQ = json.loads(qResp)

    
#     queryList = []
#     for row in loadQ:
        
#         quer = row['query']
#         queryList.append(quer)


#     i = 1
#     for i in range(len(queryList)):
        
#         print('query',i,': ',queryList[i])
        
        
      
        

#     return qResp


@app.route('/previewLaporan/<kode_laporan>', methods=['POST','GET'])
def previewLaporan(kode_laporan):
    # MENDAPATKAN LIST PIC / PENERIMA SESUAI DENGAN LAPORAN
    getPIC = requests.get('http://127.0.0.1:5002/listPIC/'+kode_laporan)
    PICResp = json.dumps(getPIC.json())
    loadPIC = json.loads(PICResp)
    for i in loadPIC:
        namaPIC = i['PIC']

    getPen = requests.get('http://127.0.0.1:5002/listPenerima/'+kode_laporan)
    PenResp = json.dumps(getPen.json())
    loadPen = json.loads(PenResp)
    for i in loadPen:
        namaPenerima = i['Penerima']


    PIC = []
    Penerima = []

    PIC.append(namaPIC)
    Penerima.append(namaPenerima)
    #=========================================================

    # MENDAPATKAN JUMLAH HEADER (1 / 2)
    getHead = requests.get('http://127.0.0.1:5002/getJumlahHeader/'+kode_laporan)
    headResp = json.dumps(getHead.json())
    loadJmlHeader = json.loads(headResp)
    #=========================================================
    for i in loadJmlHeader:
        jmlHead = i['jumlahHeader']
        print('Jumlah Header: ',jmlHead)



    if jmlHead == '1':

        count_header = 0

        db = databaseCMS.db_template()
        cursor = db.cursor(buffered = True)







        # GET AND EXECUTE QUERY
        getQ = requests.get('http://127.0.0.1:5002/getQuery/'+kode_laporan)
        qResp = json.dumps(getQ.json())
        loadQ = json.loads(qResp)

        listQuery = []
        for i in loadQ:
            reportId = i['reportId']
            quer = i['query']
            qno = i['query_no']

            listQuery.append(quer)
        print('list Query: ',listQuery)
        lengthOfQuery = len(listQuery)

        for i in range (lengthOfQuery):
            sql2 = listQuery[i]
            cursor.execute(sql2)
            
            
        result = cursor.fetchall() 

        #HASIL DARI EXECUTE QUERY
        toExcel = []
        for i in result:
            toExcel.append(i)

        print(toExcel)   



        workbook = xlsxwriter.Workbook('%s.xls'% (kode_laporan))
        worksheet = workbook.add_worksheet()

        ##############style###############
        font_size = workbook.add_format({'font_size':8})
        format_header = workbook.add_format({'font_size':8,'top':1,'bottom':1,'bold':True})
        category_style = workbook.add_format({'font_size':8,'align':'right'})
        merge_format = workbook.add_format({
            'bold':2,
            'align' : 'center',
            'valign' : 'vcenter',
            'font_size':10})
        bold = workbook.add_format({'bold':True,'font_size':8})
        ##################################


        #=========================================================

        getDetH = requests.get('http://127.0.0.1:5002/getDetailH/'+kode_laporan)
        detHResp = json.dumps(getDetH.json())
        loadDetailH = json.loads(detHResp)

        countHeader = []
        for i in loadDetailH:
            namaKolom = i['namaKolom']
            lokasiKolom = i['lokasi']
            formatKolom = i['formatKolom']
            lebar = i['lebarKolom']
        

        countHeader.append(namaKolom)
        countHeader2 = len(countHeader)

        data = []
        data = toExcel



        row = 0
        kol = 0

        kolom = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        row2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]

        listKolom = []
        for i in loadDetailH:
            kolom = i['namaKolom']
            listKolom.append(kolom)
        print('list Kolom: ',listKolom)
        listKolom2 = len(listKolom)

        kolomList = (kolom[0:countHeader2])
        rowList = (row2[0:countHeader2])
        j = 1

        #ini untuk menulis header
        for i in (countHeader): 
            worksheet.write(row + 7,kol + j,i,format_header)
            j = j + 1
            count_header = count_header + 1

        #end menulis header
        ##########################
        lengthOfData = [x[0] for x in data]
        lengthOfData2 = len(lengthOfData)
        num = 1
        for i in range(lengthOfData2+1): #untuk menulis penomoran 1 s/d banyak data
            if (i == 0):
                worksheet.write(row + 7,kol,'No',format_header)
                row = row + 1
            else:
                worksheet.write(row + 7,kol,num,font_size)
                row = row + 1
                num = num + 1

        m = 1
        row2 = 0

        for i in range(lengthOfData2): #untuk menulis data
            worksheet.write_row(row2+8,kol+m,data[i],font_size)
            row2 = row2 + 1





        ###########################################
        #Mengatur bagian atas dari laporan
        
        listMaxCol = ['B1','C1','D1','E1','F1','G1','H1','I1','J1','K1','L1','N1','O1','P1']
        maxCol = (listMaxCol[countHeader2])

        detReport = requests.get('http://127.0.0.1:5002/getDetailReport/'+kode_laporan)
        detRResp = json.dumps(detReport.json())
        loadDetailReport = json.loads(detRResp)

        nOrg = requests.get('http://127.0.0.1:5001/getNamaOrg/'+loadDetailReport[5])
        orgResp = json.dumps(nOrg.json())
        loadNamaOrg = json.loads(orgResp)
        for i in loadNamaOrg:
            namaOrg = i['org_name']


        print(loadDetailReport)
        
        
        
        listColWidth =['B','C','D','E','F','G','H','I','J','K','L','N','O','P']
        colWidth = (listColWidth[0:countHeader2])
        
        worksheet.merge_range('A1:%s'%(maxCol),'%s'%(namaOrg), merge_format) 
        worksheet.write('A2','%s' % (loadDetailReport[1]),bold ) #nama report
        worksheet.write('A3','Report Code : %s' % (loadDetailReport[0]),font_size) #kode report
        worksheet.write('A4','PIC : %s' % (', '.join(PIC)),font_size)
        worksheet.write('A5','Penerima : %s' % (', '.join(Penerima)),font_size)
        worksheet.write('A6','Filter : %s' % (loadDetailReport[2]), bold ) #filter
        worksheet.write('A7','Period : %s' % (loadDetailReport[3]),font_size) #periode

        #penulisan printed date
        
        # curr.execute("select left(getdate(),19)")
        # printed_date_result = [x[0] for x in curr.fetchall()]
        # worksheet.write(2,2,'Printed Date : %s' % (printed_date_result[0]),font_size)

        # curr.execute(sql3)
        # width = [x[4] for x in curr.fetchall()]
        
        # for i in range(countHeader2):
        #     worksheet.set_column('%s:%s'%(colWidth[i],colWidth[i]), int(width[i]))

        
        ###########################################








        workbook.close()






        PIC = []
        Penerima = []


        

        return loadQ
    

    
        
    










# @app.route('/generateToExcel/<kode_laporan>', methods=['POST','GET'])
# def generateToExcel(kode_laporan):

# 	#Mendapatkan query dari laporan yang dipilih
# 	Query = requests.get('http://127.0.0.1:5002/viewEditQuery/'+kode_laporan)
#     QDump = json.dumps(Query.json())
#     QLoad = json.loads(QDump)

#     formatTemplate = requests.get('http://127.0.0.1:5002/detailFormatTemplate/'+kode_laporan)
#     fDump = json.dumps(formatTemplate.json())
#     fLoad = json.loads(fDump)

#     for x in fLoad:
#     	letakKolom = fLoad['lokasiH']

#     print(letakKolom)


# 	workbook = xlsxwriter.Workbook('test.xlsx')
#     worksheet1 = workbook.add_worksheet('My 1')
#     bold = workbook.add_format({'bold': True})


#     worksheet1.write('B6','User Id', bold)
#     worksheet1.write('C6','Nama', bold)
#     worksheet1.write('D6','Password', bold)

#     try:
#     	db = database.CMS.db_template()
#     	cursor = connection.cursor()

#         sql = "SELECT * FROM m_user"


#         try:
#           cursor.execute(sql)
#           results = cursor.fetchall()
          
#           x = 0
#           i = 7;
#           for row in results:
#             worksheet1.write('B' + str(i), row[0])
#             worksheet1.write('C' + str(i), row[1])
#             worksheet1.write('D' + str(i), row[2])
#             i += 1
#             x += 1
              
#         except:
#            print("Error: unable to fetch data")

#         bold = workbook.add_format({'bold': True})

#         #add new worksheet
#         worksheet2 = workbook.add_worksheet('My 2')

#         worksheet2.write('A1','Col 1')
#         worksheet2.write('B1','Col 2')
#         worksheet2.write('C1','Col 3')

#         worksheet2.write('A2','Data 1')
#         worksheet2.write('B2','Data 2', bold)
#         worksheet2.write('C2','Data 3')

#         connection.close()

#         workbook.close()


#     except Error as e :
#             print("Error while connecting file MySQL", e)
#     finally:
#     #Closing DB Connection.
#         if(connection.is_connected()):
#                 cursor.close()
#                 connection.close()
#         print("MySQL connection is closed")



if __name__ == "__main__":
    app.run(debug=True, port='5003')