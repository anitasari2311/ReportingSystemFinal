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




@app.route('/previewLaporan/<kode_laporan>', methods=['POST','GET'])
def previewLaporan(kode_laporan):
    


    # MENDAPATKAN DETAIL REPORT

    detReport = requests.get('http://127.0.0.1:5002/getDetailReport/'+kode_laporan)
    detRResp = json.dumps(detReport.json())
    loadDetailReport = json.loads(detRResp)
    

    # MENDAPATKAN JUMLAH HEADER (1 / 2)
    jmlHead = loadDetailReport[6]
    print('Jumlah Header: ',jmlHead)
    #=========================================================


    if jmlHead == '1':

        count_header = 0

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
        #==============================================================================

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
        lebar = []
        listKolom = []
        for i in loadDetailH:
            namaKolom = i['namaKolom']
            lokasiKolom = i['lokasi']
            formatKolom = i['formatKolom']
            leb = i['lebarKolom']
        
            listKolom.append(namaKolom)
            lebar.append(leb)
            countHeader.append(namaKolom)
        

        listKolom2 = len(listKolom)
        countHeader2 = len(countHeader)

        print('list Kolom: ',listKolom)
        print('list Lebar: ',lebar)

        
        data = []
        data = toExcel



        row = 0
        kol = 0

        kolom = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        row2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]


        kolomList = (kolom[0:countHeader2])
        rowList = (row2[0:countHeader2])
        j = 1

        #ini untuk menulis header

        #sebelumnya for i in countHeader
        for i in (listKolom): 
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

        

        nOrg = requests.get('http://127.0.0.1:5001/getNamaOrg/'+loadDetailReport[5])
        orgResp = json.dumps(nOrg.json())
        loadNamaOrg = json.loads(orgResp)
        for i in loadNamaOrg:
            namaOrg = i['org_name']


        print(loadDetailReport)
        
        
        
        listColWidth =['B','C','D','E','F','G','H','I','J','K','L','N','O','P']
        colWidth = (listColWidth[0:countHeader2])
        
        print(colWidth)
        print(countHeader)
        print(countHeader2)
        worksheet.merge_range('A1:%s'%(maxCol),'%s'%(namaOrg), merge_format) 
        worksheet.write('A2','%s' % (loadDetailReport[1]),bold ) #nama report
        worksheet.write('A3','Report Code : %s' % (loadDetailReport[0]),font_size) #kode report
        worksheet.write('A4','PIC : %s' % (', '.join(PIC)),font_size)
        worksheet.write('A5','Penerima : %s' % (', '.join(Penerima)),font_size)
        worksheet.write('A6','Filter : %s' % (loadDetailReport[2]), bold ) #filter
        worksheet.write('A7','Period : %s' % (loadDetailReport[3]),font_size) #periode
        
        #penulisan printed date

        worksheet.write(2,2,'Printed Date : %s' % (datetime.datetime.now().replace(microsecond=0)),font_size)

        #Untuk mengatur lebar Kolom
        for i in range(countHeader2):
            worksheet.set_column('%s:%s'%(colWidth[i],colWidth[i]), int(lebar[i]))

        
        ###########################################

        #======================[ FOOTER ]================================

        # getF = requests.get('http://127.0.0.1:5002/getDetailF/'+kode_laporan)
        # FResp = json.dumps(getF.json())
        # detailFooter = json.loads(FResp)

        # kolomFooter = []
        # lokasiFooter = []
        # urutanFooter = []
        # for row in detailFooter:
        #     kodeReportF = row['reportId']
        #     namaKolomF = row['namaKolom']
        #     lokasi = row['lokasi']
        #     urutan = row['urutan'] 

        #     kolomFooter.append(namaKolomF)
        #     lokasiFooter.append(lokasi)
        #     urutanFooter.append(urutan)

        # lokasiCurr = []
        # countOfFooter = len(lokasiFooter)


        # l = 0
        # for i in range(countOfFooter):
        #     if (lokasi[l] == 'B         '):
        #         lokasiCurr.append(1)
        #     elif(lokasi[l] == 'C         '):
        #         lokasiCurr.append(2)
        #     elif(lokasi[l] == 'D         '):
        #         lokasiCurr.append(3)
        #     elif(lokasi[l] == 'E         '):
        #         lokasiCurr.append(4)
        #     elif(lokasi[l] == 'F         '):
        #         lokasiCurr.append(5)
        #     elif(lokasi[l] == 'G         '):
        #         lokasiCurr.append(6)
        #     elif(lokasi[l] == 'H         '):
        #         lokasiCurr.append(7)
        #     elif(lokasi[l] == 'I         '):
        #         lokasiCurr.append(8)
        #     elif(lokasi[l] == 'J         '):
        #         lokasiCurr.append(9)
        #     elif(lokasi[l] == 'K         '):
        #         lokasiCurr.append(10)
        #     elif(lokasi[l] == 'L         '):
        #         lokasiCurr.append(11)
        #     elif(lokasi[l] == 'M         '):
        #         lokasiCurr.append(12)
        #     elif(lokasi[l] == 'N         '):
        #         lokasiCurr.append(13)
        #     elif(lokasi[l] == 'O         '):
        #         lokasiCurr.append(14)
        #     elif(lokasi[l] == 'P         '):
        #         lokasiCurr.append(15)
        #     l = l + 1

        # countFooter = loadDetailReport[4]
        # lokasiCurr2 = []
        # l = 0
        # print(kolomFooter)
        # for i in range(countOfFooter):
        #     if (lokasi[l] == 'B         '):
        #         lokasiCurr2.append('B')
        #     elif(lokasi[l] == 'C         '):
        #         lokasiCurr2.append('C')
        #     elif(lokasi[l] == 'D         '):
        #         lokasiCurr2.append('D')
        #     elif(lokasi[l] == 'E         '):
        #         lokasiCurr2.append('E')
        #     elif(lokasi[l] == 'F         '):
        #         lokasiCurr2.append('F')
        #     elif(lokasi[l] == 'G         '):
        #         lokasiCurr2.append('G')
        #     elif(lokasi[l] == 'H         '):
        #         lokasiCurr2.append('H')
        #     elif(lokasi[l] == 'I         '):
        #         lokasiCurr2.append('I')
        #     elif(lokasi[l] == 'J         '):
        #         lokasiCurr2.append('J')
        #     elif(lokasi[l] == 'K         '):
        #         lokasiCurr2.append('K')
        #     elif(lokasi[l] == 'L         '):
        #         lokasiCurr2.append('L')
        #     elif(lokasi[l] == 'M         '):
        #         lokasiCurr2.append('M')
        #     elif(lokasi[l] == 'N         '):
        #         lokasiCurr2.append('N')
        #     elif(lokasi[l] == 'O         '):
        #         lokasiCurr2.append('O')
        #     elif(lokasi[l] == 'P         '):
        #         lokasiCurr2.append('P')
        #     l = l + 1

        # totalRow = len(lengthOfData)
        # lokasiCurr2Len = len(lokasiCurr2)
        # print(lokasiCurr2[0])
        # print(lokasiCurr2Len)
        # if (countFooter == 1):
        #     for i in range(lokasiCurr2Len):
        #         worksheet.write(row2+8,i,'',format_header)
        #         worksheet.write(row2+8,1,'%s' % (kolomFooter[0]),format_header)
        #         worksheet.write(row2+8,lokasiCurr[i],'=SUM(%s8:%s%s)'% (lokasiCurr2[i],lokasiCurr2[i],totalRow+8),format_header)





        # Penulisan Process Time
        worksheet.write(row2+9,1,'Process Time : s/d %s' % (datetime.datetime.now().replace(microsecond=0)),font_size)

        #Penulisan Since
        worksheet.write(row2+10,1,'Since : %s' % (loadDetailReport[7]),font_size)

        #Penulisan Schedule
        getSch = requests.get('http://127.0.0.1:5002/getSchedule/'+kode_laporan)
        getSchResp = json.dumps(getSch.json())
        loadGetSch = json.loads(getSchResp)

        worksheet.write(row2+11,1,'Schedule : %s %s %s' % (loadGetSch[1],loadGetSch[0],loadGetSch[2]),font_size)

        #Penulisan Creator
        worksheet.write(row2+9,count_header - 1,'CREATOR : %s' % (loadDetailReport[8]),font_size)


        workbook.close()


##################################################################################################################

    elif jmlHead == '2':

        count_header = 0

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
        #==============================================================================

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


        ########style###########
        font_size = workbook.add_format({'font_size':8})
        fontsize_1stheader = workbook.add_format({'font_size':8,'top':1,'bold':2})
        merge_format = workbook.add_format({
            'align' : 'center',
            'valign' : 'vcenter',
            'font_size':8,
            'top':1,
            'bold':2})
        fontsize_2ndheader = workbook.add_format({'font_size':8,'bottom':1,'bold':2})
        font_number = workbook.add_format({'font_size':8})
        merge_format2 = workbook.add_format({
            'bold':2,
            'align' : 'center',
            'valign' : 'vcenter',
            'font_size':10})
        bold = workbook.add_format({'bold':True,'font_size':8})
        category_style = workbook.add_format({'font_size':8,'align':'right'})
        border_top  = workbook.add_format({'top':1})
        border_btm  = workbook.add_format({'bottom':1})
        ########################


        getDetH = requests.get('http://127.0.0.1:5002/getDetailH/'+kode_laporan)
        detHResp = json.dumps(getDetH.json())
        loadDetailH = json.loads(detHResp)

        countHeader = []
        lebar = []
        listKolom = []
        for i in loadDetailH:
            namaKolom = i['namaKolom']
            lokasiKolom = i['lokasi']
            formatKolom = i['formatKolom']
            leb = i['lebarKolom']
        
            listKolom.append(namaKolom)
            lebar.append(leb)
            countHeader.append(namaKolom)
        

        listKolom2 = len(listKolom)
        countHeader2 = len(countHeader)

        print('list Kolom: ',listKolom)
        print('list Lebar: ',lebar)




        data = [] 
        data = toExcel

        row = 0
        col = 0

        coloumn = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        row2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]


        

        return loadQ
    

    
        
    

@app.route('/testPreviewLaporan/<kode_laporan>', methods=['POST','GET'])
def testPreviewLaporan(kode_laporan):
    


    # MENDAPATKAN DETAIL REPORT
    detReport = requests.get('http://127.0.0.1:5002/getDetailReport/'+kode_laporan)
    detRResp = json.dumps(detReport.json())
    loadDetailReport = json.loads(detRResp)
    

    # MENDAPATKAN JUMLAH HEADER (1 / 2)
    jmlHead = loadDetailReport[6]
    print('Jumlah Header: ',jmlHead)
    #=========================================================


    if jmlHead == '1':

        count_header = 0

        PIC = []
        Penerima = []

        # MENDAPATKAN LIST PIC / PENERIMA SESUAI DENGAN LAPORAN
        getPIC = requests.get('http://127.0.0.1:5002/listPIC/'+kode_laporan)
        PICResp = json.dumps(getPIC.json())
        loadPIC = json.loads(PICResp)
        for i in loadPIC:
            namaPIC = i['PIC']
            PIC.append(namaPIC)

        getPen = requests.get('http://127.0.0.1:5002/listPenerima/'+kode_laporan)
        PenResp = json.dumps(getPen.json())
        loadPen = json.loads(PenResp)
        for i in loadPen:
            namaPenerima = i['Penerima']
            Penerima.append(namaPenerima)


        # PIC = []
        # Penerima = []

        # PIC.append(namaPIC)
        # Penerima.append(namaPenerima)
        #==============================================================================

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
        lebar = []
        listKolom = []
        lokasiHeader = []
        for i in loadDetailH:
            namaKolom = i['namaKolom']
            lokasiKolom = i['lokasi']
            formatKolom = i['formatKolom']
            leb = i['lebarKolom']
        
            listKolom.append(namaKolom)
            lebar.append(leb)
            lokasiHeader.append(lokasiKolom)
            countHeader.append(namaKolom)
        

        listKolom2 = len(listKolom)
        countHeader2 = len(countHeader)

        print('list Kolom: ',listKolom)
        print('list Lebar: ',lebar)

        
        data = []
        data = toExcel



        row = 0
        kol = 0

        kolom = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        row2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]


        kolomList = (kolom[0:countHeader2])
        rowList = (row2[0:countHeader2])
        j = 1

        #ini untuk menulis header

        #sebelumnya for i in countHeader

        lok = 0
        for i in (listKolom): 
            worksheet.write(lokasiHeader[lok],i,format_header)
            lok = lok + 1
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

        

        nOrg = requests.get('http://127.0.0.1:5001/getNamaOrg/'+loadDetailReport[5])
        orgResp = json.dumps(nOrg.json())
        loadNamaOrg = json.loads(orgResp)
        for i in loadNamaOrg:
            namaOrg = i['org_name']


        print(loadDetailReport)
        
        
        
        listColWidth =['B','C','D','E','F','G','H','I','J','K','L','N','O','P']
        colWidth = (listColWidth[0:countHeader2])
        
        print(colWidth)
        print(countHeader)
        print(countHeader2)
        worksheet.merge_range('A1:%s'%(maxCol),'%s'%(namaOrg), merge_format) 
        worksheet.write('A2','%s' % (loadDetailReport[1]),bold ) #nama report
        worksheet.write('A3','Report Code : %s' % (loadDetailReport[0]),font_size) #kode report
        worksheet.write('A4','PIC : %s' % (', '.join(PIC)),font_size)
        worksheet.write('A5','Penerima : %s' % (', '.join(Penerima)),font_size)
        worksheet.write('A6','Filter : %s' % (loadDetailReport[2]), bold ) #filter
        worksheet.write('A7','Period : %s' % (loadDetailReport[3]),font_size) #periode
        
        #penulisan printed date

        worksheet.write(2,2,'Printed Date : %s' % (datetime.datetime.now().replace(microsecond=0)),font_size)

        #Untuk mengatur lebar Kolom
        for i in range(countHeader2):
            worksheet.set_column('%s:%s'%(colWidth[i],colWidth[i]), int(lebar[i]))

        
        ###########################################

        #======================[ FOOTER ]================================

        # getF = requests.get('http://127.0.0.1:5002/getDetailF/'+kode_laporan)
        # FResp = json.dumps(getF.json())
        # detailFooter = json.loads(FResp)

        # kolomFooter = []
        # lokasiFooter = []
        # urutanFooter = []
        # for row in detailFooter:
        #     kodeReportF = row['reportId']
        #     namaKolomF = row['namaKolom']
        #     lokasi = row['lokasi']
        #     urutan = row['urutan'] 

        #     kolomFooter.append(namaKolomF)
        #     lokasiFooter.append(lokasi)
        #     urutanFooter.append(urutan)

        # lokasiCurr = []
        # countOfFooter = len(lokasiFooter)


        # l = 0
        # for i in range(countOfFooter):
        #     if (lokasi[l] == 'B         '):
        #         lokasiCurr.append(1)
        #     elif(lokasi[l] == 'C         '):
        #         lokasiCurr.append(2)
        #     elif(lokasi[l] == 'D         '):
        #         lokasiCurr.append(3)
        #     elif(lokasi[l] == 'E         '):
        #         lokasiCurr.append(4)
        #     elif(lokasi[l] == 'F         '):
        #         lokasiCurr.append(5)
        #     elif(lokasi[l] == 'G         '):
        #         lokasiCurr.append(6)
        #     elif(lokasi[l] == 'H         '):
        #         lokasiCurr.append(7)
        #     elif(lokasi[l] == 'I         '):
        #         lokasiCurr.append(8)
        #     elif(lokasi[l] == 'J         '):
        #         lokasiCurr.append(9)
        #     elif(lokasi[l] == 'K         '):
        #         lokasiCurr.append(10)
        #     elif(lokasi[l] == 'L         '):
        #         lokasiCurr.append(11)
        #     elif(lokasi[l] == 'M         '):
        #         lokasiCurr.append(12)
        #     elif(lokasi[l] == 'N         '):
        #         lokasiCurr.append(13)
        #     elif(lokasi[l] == 'O         '):
        #         lokasiCurr.append(14)
        #     elif(lokasi[l] == 'P         '):
        #         lokasiCurr.append(15)
        #     l = l + 1

        # countFooter = loadDetailReport[4]
        # lokasiCurr2 = []
        # l = 0
        # print(kolomFooter)
        # for i in range(countOfFooter):
        #     if (lokasi[l] == 'B         '):
        #         lokasiCurr2.append('B')
        #     elif(lokasi[l] == 'C         '):
        #         lokasiCurr2.append('C')
        #     elif(lokasi[l] == 'D         '):
        #         lokasiCurr2.append('D')
        #     elif(lokasi[l] == 'E         '):
        #         lokasiCurr2.append('E')
        #     elif(lokasi[l] == 'F         '):
        #         lokasiCurr2.append('F')
        #     elif(lokasi[l] == 'G         '):
        #         lokasiCurr2.append('G')
        #     elif(lokasi[l] == 'H         '):
        #         lokasiCurr2.append('H')
        #     elif(lokasi[l] == 'I         '):
        #         lokasiCurr2.append('I')
        #     elif(lokasi[l] == 'J         '):
        #         lokasiCurr2.append('J')
        #     elif(lokasi[l] == 'K         '):
        #         lokasiCurr2.append('K')
        #     elif(lokasi[l] == 'L         '):
        #         lokasiCurr2.append('L')
        #     elif(lokasi[l] == 'M         '):
        #         lokasiCurr2.append('M')
        #     elif(lokasi[l] == 'N         '):
        #         lokasiCurr2.append('N')
        #     elif(lokasi[l] == 'O         '):
        #         lokasiCurr2.append('O')
        #     elif(lokasi[l] == 'P         '):
        #         lokasiCurr2.append('P')
        #     l = l + 1

        # totalRow = len(lengthOfData)
        # lokasiCurr2Len = len(lokasiCurr2)
        # print(lokasiCurr2[0])
        # print(lokasiCurr2Len)
        # if (countFooter == 1):
        #     for i in range(lokasiCurr2Len):
        #         worksheet.write(row2+8,i,'',format_header)
        #         worksheet.write(row2+8,1,'%s' % (kolomFooter[0]),format_header)
        #         worksheet.write(row2+8,lokasiCurr[i],'=SUM(%s8:%s%s)'% (lokasiCurr2[i],lokasiCurr2[i],totalRow+8),format_header)





        # Penulisan Process Time
        worksheet.write(row2+9,1,'Process Time : s/d %s' % (datetime.datetime.now().replace(microsecond=0)),font_size)

        #Penulisan Since
        worksheet.write(row2+10,1,'Since : %s' % (loadDetailReport[7]),font_size)

        #Penulisan Schedule
        # getSch = requests.get('http://127.0.0.1:5002/getSchedule/'+kode_laporan)
        # getSchResp = json.dumps(getSch.json())
        # loadGetSch = json.loads(getSchResp)

        # if loadGetSch:
        #     worksheet.write(row2+11,1,'Schedule : %s %s %s' % (loadGetSch[1],loadGetSch[0],loadGetSch[2]),font_size)
        # else: 
        #     worksheet.write(row2+11,1,'Schedule : -')
        #Penulisan Creator
        worksheet.write(row2+9,count_header - 1,'CREATOR : %s' % (loadDetailReport[8]),font_size)


        workbook.close()

































    elif jmlHead == '2':

        count_header = 0


        PIC = []
        Penerima = []
        # MENDAPATKAN LIST PIC / PENERIMA SESUAI DENGAN LAPORAN
        getPIC = requests.get('http://127.0.0.1:5002/listPIC/'+kode_laporan)
        PICResp = json.dumps(getPIC.json())
        loadPIC = json.loads(PICResp)
        for i in loadPIC:
            namaPIC = i['PIC']
            PIC.append(namaPIC)

        getPen = requests.get('http://127.0.0.1:5002/listPenerima/'+kode_laporan)
        PenResp = json.dumps(getPen.json())
        loadPen = json.loads(PenResp)
        for i in loadPen:
            namaPenerima = i['Penerima']
            Penerima.append(namaPenerima)


        

        
        
        #==============================================================================

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
        format_headerMid = workbook.add_format({'font_size':8,'top':1,'bold':True,'align' : 'center','valign' : 'center'})
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
        loadDetailH1 = json.loads(detHResp)

        getDetH2 = requests.get('http://127.0.0.1:5002/getDetailH2/'+kode_laporan)
        detHResp2 = json.dumps(getDetH2.json())
        loadDetailH2 = json.loads(detHResp2)


        ########## HEADER 1 #############

        countHeader = []
        lebar = []
        listKolom = []
        lokasiH1 = []
        
        for i in loadDetailH1:
            namaKolom = i['namaKolom']
            lokasiKolom = i['lokasi']
            formatKolom = i['formatKolom']
            leb = i['lebarKolom']
        
        
            listKolom.append(namaKolom)
            lebar.append(leb)
            lokasiH1.append(lokasiKolom)
            
            countHeader.append(namaKolom)
        
        listKolom2 = len(listKolom)
        countHeader2 = len(countHeader)

        
        mCell = i['formatMerge'].replace('-',':').split(', ')
        

        

        print('merge Cell: ',mCell)
        print('list Kolom1: ',listKolom)
        print('list Lebar1: ',lebar)


        ##########  HEADER 2 ############



        listKolomHeader2 = []
        lebarH2 = []
        lokasiH2 = []
        for i in loadDetailH2:
            namaKolomH2 = i['namaKolom']
            lokasi2 = i['lokasi']
            formatKolomH2 = i['formatKolom']
            lebH2 = i['lebarKolom']

            listKolomHeader2.append(namaKolomH2)
            lebarH2.append(lebH2)
            lokasiH2.append(lokasi2)

        countHeaderH2 = len(listKolomHeader2)
        print('list Kolom2: ',listKolomHeader2)
        print('list Lebar2: ',lebarH2)
        print('lokasi2: ', lokasiH2)

        
        data = []
        data = toExcel



        row = 0
        kol = 0

        kolom = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        row2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]


        kolomList = (kolom[0:countHeader2])
        rowList = (row2[0:countHeader2])
        j = 1



        # MERGE CELL
        for i in range(len(mCell)):
            worksheet.merge_range('%s'%(mCell[i]),'%s'%(''), format_headerMid)

        #ini untuk menulis header
        lok = 0
        #HEADER 1
        for i in (listKolom): 
            worksheet.write(lokasiH1[lok],i,format_headerMid)
            lok = lok + 1
            count_header = count_header + 1

        #HEADER 2
        lok2 = 0
        for x in (listKolomHeader2):
            worksheet.write(lokasiH2[lok2], x,format_header)
            lok2 = lok2 + 1
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
                worksheet.write(row + 8,kol,num,font_size)
                row = row + 1
                num = num + 1

        m = 1
        row2 = 0

        for i in range(lengthOfData2): #untuk menulis data
            worksheet.write_row(row2+9,kol+m,data[i],font_size)
            row2 = row2 + 1





        ###########################################
        #Mengatur bagian atas dari laporan
        
        listMaxCol = ['B1','C1','D1','E1','F1','G1','H1','I1','J1','K1','L1','N1','O1','P1']
        maxCol = (listMaxCol[countHeader2])

        

        nOrg = requests.get('http://127.0.0.1:5001/getNamaOrg/'+loadDetailReport[5])
        orgResp = json.dumps(nOrg.json())
        loadNamaOrg = json.loads(orgResp)
        for i in loadNamaOrg:
            namaOrg = i['org_name']


        print(loadDetailReport)
        
        
        
        listColWidth =['B','C','D','E','F','G','H','I','J','K','L','N','O','P']
        colWidth = (listColWidth[0:countHeader2])
        
        print(colWidth)
        print(countHeader)
        print(countHeader2)
        worksheet.merge_range('A1:%s'%(maxCol),'%s'%(namaOrg), merge_format) 
        worksheet.write('A2','%s' % (loadDetailReport[1]),bold ) #nama report
        worksheet.write('A3','Report Code : %s' % (loadDetailReport[0]),font_size) #kode report
        worksheet.write('A4','PIC : %s' % (', '.join(PIC)),font_size)
        worksheet.write('A5','Penerima : %s' % (', '.join(Penerima)),font_size)
        worksheet.write('A6','Filter : %s' % (loadDetailReport[2]), bold ) #filter
        worksheet.write('A7','Period : %s' % (loadDetailReport[3]),font_size) #periode
        
        #======================[ FOOTER ]================================

        getF = requests.get('http://127.0.0.1:5002/getDetailF/'+kode_laporan)
        FResp = json.dumps(getF.json())
        detailFooter = json.loads(FResp)

        kolomFooter = []
        lokasiFooter = []
        urutanFooter = []
        for row in detailFooter:
            kodeReportF = row['reportId']
            namaKolomF = row['namaKolom']
            lokasi = row['lokasi']
            urutan = row['urutan'] 

            kolomFooter.append(namaKolomF)
            lokasiFooter.append(lokasi)
            urutanFooter.append(urutan)

        lokasiCurr = []
        countOfFooter = len(lokasiFooter)
        print('kolomFooter: ',kolomFooter)
        print('lokasiFooter: ',lokasiFooter)
        print('urutanFooter: ',urutanFooter)

        l = 0
        for i in range(countOfFooter):
            if (lokasi[l] == 'B         '):
                lokasiCurr.append(1)
            elif(lokasi[l] == 'C         '):
                lokasiCurr.append(2)
            elif(lokasi[l] == 'D         '):
                lokasiCurr.append(3)
            elif(lokasi[l] == 'E         '):
                lokasiCurr.append(4)
            elif(lokasi[l] == 'F         '):
                lokasiCurr.append(5)
            elif(lokasi[l] == 'G         '):
                lokasiCurr.append(6)
            elif(lokasi[l] == 'H         '):
                lokasiCurr.append(7)
            elif(lokasi[l] == 'I         '):
                lokasiCurr.append(8)
            elif(lokasi[l] == 'J         '):
                lokasiCurr.append(9)
            elif(lokasi[l] == 'K         '):
                lokasiCurr.append(10)
            elif(lokasi[l] == 'L         '):
                lokasiCurr.append(11)
            elif(lokasi[l] == 'M         '):
                lokasiCurr.append(12)
            elif(lokasi[l] == 'N         '):
                lokasiCurr.append(13)
            elif(lokasi[l] == 'O         '):
                lokasiCurr.append(14)
            elif(lokasi[l] == 'P         '):
                lokasiCurr.append(15)
            l = l + 1
                        
        #curr.execute(sql4)
        countFooter = loadDetailReport[4]
        print(countOfFooter)
        #lenCountFooter = len(countFooter)
        lokasiCurr2 = []
        l = 0
        for i in range(countOfFooter):
            if (lokasi[l] == 'B         '):
                lokasiCurr2.append('B')
            elif(lokasi[l] == 'C         '):
                lokasiCurr2.append('C')
            elif(lokasi[l] == 'D         '):
                lokasiCurr2.append('D')
            elif(lokasi[l] == 'E         '):
                lokasiCurr2.append('E')
            elif(lokasi[l] == 'F         '):
                lokasiCurr2.append('F')
            elif(lokasi[l] == 'G         '):
                lokasiCurr2.append('G')
            elif(lokasi[l] == 'H         '):
                lokasiCurr2.append('H')
            elif(lokasi[l] == 'I         '):
                lokasiCurr2.append('I')
            elif(lokasi[l] == 'J         '):
                lokasiCurr2.append('J')
            elif(lokasi[l] == 'K         '):
                lokasiCurr2.append('K')
            elif(lokasi[l] == 'L         '):
                lokasiCurr2.append('L')
            elif(lokasi[l] == 'M         '):
                lokasiCurr2.append('M')
            elif(lokasi[l] == 'N         '):
                lokasiCurr2.append('N')
            elif(lokasi[l] == 'O         '):
                lokasiCurr2.append('O')
            elif(lokasi[l] == 'P         '):
                lokasiCurr2.append('P')
            l = l + 1

        footer_format2 = workbook.add_format({'font_size':8,'bottom':1})
        totalRow = len(lengthOfData)

        lokasiCurr2Len = len(lokasiCurr2)

        if countFooter == 1:
            for i in range(lokasiCurr2Len):
                worksheet.write(row2+9,1,'%s' % (kolomFooter[0]),font_size)
                worksheet.write(row2+9,lokasiCurr[0],'=SUM(%s8:%s%s)'% (lokasiCurr2[i],lokasiCurr2[i],totalRow+8),footer_format2)





















        #penulisan printed date

        worksheet.write(2,2,'Printed Date : %s' % (datetime.datetime.now().replace(microsecond=0)),font_size)

        #Untuk mengatur lebar Kolom
        for i in range(countHeader2):
            worksheet.set_column('%s:%s'%(colWidth[i],colWidth[i]), int(lebar[i]))



        # Penulisan Process Time
        worksheet.write(row2+11,1,'Process Time : s/d %s' % (datetime.datetime.now().replace(microsecond=0)),font_size)

        #Penulisan Since
        worksheet.write(row2+12,1,'Since : %s' % (loadDetailReport[7]),font_size)

        #Penulisan Schedule
        getSch = requests.get('http://127.0.0.1:5002/getSchedule/'+kode_laporan)
        getSchResp = json.dumps(getSch.json())
        loadGetSch = json.loads(getSchResp)

        if loadGetSch:

            worksheet.write(row2+13,1,'Schedule : %s %s %s' % (loadGetSch[1],loadGetSch[0],loadGetSch[2]),font_size)
        else:
            worksheet.write(row2+13,1,'Schedule : -', font_size)
        #Penulisan Creator
        worksheet.write(row2+11,count_header - 1,'CREATOR : %s' % (loadDetailReport[8]),font_size)


        workbook.close()


if __name__ == "__main__":
    app.run(debug=True, port='5003')