import tkinter as TK
import menuutama
from tkinter import messagebox
import pyodbc
import xlsxwriter
import decimal
#import connection as connection
#conn = connection.connection()
#curr = conn.cursor()

pic = []
def doPreview(root,cbKodeReport,username,cbOrganisasi,cbServer,login_name,password):

    del pic[:]
    conn = pyodbc.connect(r'Driver={SQL Server};Server=oculus;Database=CMS_2;UID=reporting_dept;PWD=r3porting')
    curr = conn.cursor()

    queryHeader = "SELECT jml_baris_header\
                  FROM [CMS_2].[dbo].[report]\
                  WHERE kode_report = '%s'\
                  AND aktif = 'Y'" % (cbKodeReport)
    currqueryHeader = conn.cursor()
    currqueryHeader.execute(queryHeader)
    currqueryHeader_result = [x[0] for x in currqueryHeader.fetchall()]
    #print(currqueryHeader_result)
##################################################################################################################################################
    if (currqueryHeader_result[0] == 1):

        count_header = 0
        
        #PIC
        queryEmailPIC = "SELECT [penerima] \
                        FROM [CMS_2].[dbo].[scheduling]\
                        WHERE kode_report = '%s'\
                        AND aktif = 'Y'" % (cbKodeReport)
        curr.execute(queryEmailPIC)
        queryEmailPIC_result = [x[0] for x in curr.fetchall()]

        split_queryEmailPIC = queryEmailPIC_result[0].split(', ')

        lensplit_queryEmailPIC = len(split_queryEmailPIC)

        for i in range(lensplit_queryEmailPIC):
            curr.execute("SELECT nama_pengguna\
                         FROM [CMS_2].[dbo].[pengguna]\
                         WHERE email = '%s'\
                         AND blokir = 'N'" % (split_queryEmailPIC[i]))
            Pic_result = [x[0] for x in curr.fetchall()]
            pic.append(Pic_result[0])

        print(pic)
        sql1 = "SELECT kode_report,query,no_urut,nama_user\
                FROM CMS_2.dbo.query query\
                LEFT JOIN CMS_2.dbo.organisasi organisasi\
                ON query.id_organisasi = organisasi.id_organisasi\
                AND organisasi.aktif = 'Y'\
                AND organisasi.nama_organisasi = '%s'\
                LEFT JOIN CMS_2.dbo.server server\
                ON query.id_server = server.id_server\
                AND server.aktif = 'Y'\
                AND server.nama_server = '%s'\
                WHERE kode_report = '%s'" % (cbOrganisasi,cbServer,cbKodeReport)
        
        curr.execute(sql1)

        query = [x[1] for x in curr.fetchall()] #dari hasil sql1, kita mau ambil kolom query nya saja, kenapa tidak SELECT query nya saja ?, karena nnti untuk mengambil
                                                #atribut nama_user dst.

        lengthOfQuery = len(query) #mau ambil berapa panjang/berapa baris isi dari atribut query, untuk keperluan looping

        for i in range (lengthOfQuery):
            sql2 = "%s" % (query[i].replace("~","'"))
            curr.execute(sql2)
            #conn.commit()
            
        result = curr.fetchall()
        toExcel = []

        for i in result:
            toExcel.append(i)
        
        workbook = xlsxwriter.Workbook('%s.xls'% (cbKodeReport))
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
        
        data = []
        data = toExcel

        row = 0
        col = 0

        coloumn = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        row2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        
        sql3 = "SELECT * \
                FROM CMS_2.dbo.detail_h\
                WHERE kode_report = '%s'" % (cbKodeReport)
        
        curr.execute(sql3)

        countHeader = [x[1] for x in curr.fetchall()]
        countHeader2 = len (countHeader)
        
        columnList = (coloumn[0:countHeader2])
        rowList = (row2[0:countHeader2])
        j = 1

        
        #ini untuk menulis header

        for i in (countHeader): 
            worksheet.write(row + 6,col + j,i,format_header)
            j = j + 1
            count_header = count_header + 1
            
        #end menulis header
        ##########################
        lengthOfData = [x[0] for x in data]
        lengthOfData2 = len(lengthOfData)
        num = 1
        for i in range(lengthOfData2+1): #untuk menulis penomoran 1 s/d banyak data
            if (i == 0):
                worksheet.write(row + 6,col,'No',format_header)
                row = row + 1
            else:
                worksheet.write(row + 6,col,num,font_size)
                row = row + 1
                num = num + 1

        m = 1
        row2 = 0

        for i in range(lengthOfData2): #untuk menulis data
            worksheet.write_row(row2+7,col+m,data[i],font_size)
            row2 = row2 + 1


        ###########################################
        #Mengatur bagian atas dari laporan
        
        listMaxCol = ['B1','C1','D1','E1','F1','G1','H1','I1','J1','K1','L1','N1','O1','P1']
        maxCol = (listMaxCol[countHeader2])

        sql4 = "SELECT kode_report,nama_report,filter,periode,jml_baris_footer \
                FROM CMS_2.dbo.report\
                WHERE kode_report = '%s'" % (cbKodeReport)
        curr.execute(sql4)
        report = curr.fetchone()
        
        listColWidth =['B','C','D','E','F','G','H','I','J','K','L','N','O','P']
        colWidth = (listColWidth[0:countHeader2])
        
        worksheet.merge_range('A1:%s'%(maxCol),'%s'%(cbOrganisasi), merge_format) 
        worksheet.write('A2','%s' % (report[1]),bold ) #nama report
        worksheet.write('A3','Report Code : %s' % (report[0]),font_size) #kode report
        worksheet.write('A4','PIC : %s' % (', '.join(pic)),font_size)
        worksheet.write('A5','Filter : %s' % (report[2]), bold ) #filter
        worksheet.write('A6','Period : %s' % (report[3]),font_size) #periode

        #penulisan printed date
        curr.execute("select left(getdate(),19)")
        printed_date_result = [x[0] for x in curr.fetchall()]
        worksheet.write(2,2,'Printed Date : %s' % (printed_date_result[0]),font_size)

        curr.execute(sql3)
        width = [x[4] for x in curr.fetchall()]
        
        for i in range(countHeader2):
            worksheet.set_column('%s:%s'%(colWidth[i],colWidth[i]), int(width[i]))

        
        ###########################################


        #################################
        #footer    
        curr1 = conn.cursor()
        curr2 = conn.cursor()
        curr3 = conn.cursor()
        curr4 = conn.cursor()
        
        sql5 = "SELECT kode_report,nama_kolom,lokasi,urutan \
                FROM   CMS_2.dbo.detail_f\
                WHERE  kode_report = '%s'" % (cbKodeReport)
        curr1.execute(sql5)
        kodeReport = [a[0] for a in curr1.fetchall()]
        
        curr2.execute(sql5)
        namaKolom = [b[1] for b in curr2.fetchall()]
        
        curr3.execute(sql5)
        lokasi = [c[2] for c in curr3.fetchall()]
        
        curr4.execute(sql5)
        urutan = [d[3] for d in curr4.fetchall()]
        
        lokasiCurr = []
        countOfFooter = len(lokasi)

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
        countFooter = report[4]
        #lenCountFooter = len(countFooter)
        lokasiCurr2 = []
        l = 0
        print(lokasi[0])
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

            
        totalRow = len(lengthOfData)
        lokasiCurr2Len = len(lokasiCurr2)
        print(lokasiCurr2[0])
        print(lokasiCurr2Len)
        if (countFooter == 1):
            for i in range(lokasiCurr2Len):
                worksheet.write(row2+7,i,'',format_header)
                worksheet.write(row2+7,1,'%s' % (namaKolom[0]),format_header)
                worksheet.write(row2+7,lokasiCurr[i],'=SUM(%s8:%s%s)'% (lokasiCurr2[i],lokasiCurr2[i],totalRow+7),format_header)

        #penulisan creator        
        curr.execute("select id_organisasi\
                     FROM [CMS_2].[dbo].[organisasi]\
                     WHERE nama_organisasi = '%s'\
                     AND aktif = 'Y'" %(cbOrganisasi))
        id_organisasi_result = [x[0] for x in curr.fetchall()]

        curr.execute("select id_server\
                     FROM [CMS_2].[dbo].server\
                     WHERE nama_server = '%s'\
                     AND aktif = 'Y'" %(cbServer))
        id_server_result = [x[0] for x in curr.fetchall()]
        
        curr.execute("SELECT [nama_user]\
                     FROM [CMS_2].[dbo].[query]\
                     WHERE kode_report = '%s'\
                     AND id_organisasi = '%s'\
                     AND id_server = '%s'"%(cbKodeReport,id_organisasi_result[0],id_server_result[0]))
        creator_result = [x[0] for x in curr.fetchall()]
        worksheet.write(row2+8,count_header - 2,'CREATOR : %s' % (creator_result[0]),font_size)

        #penulisan schedule
        curr.execute("SELECT jadwal_bulan,jadwal_tanggal,jadwal_hari\
                     FROM [CMS_2].[dbo].[scheduling]\
                     WHERE kode_report = '%s'\
                     AND id_organisasi = '%s'\
                     AND id_server = '%s'" % (cbKodeReport,id_organisasi_result[0],id_server_result[0]))
        jadwal_bulan_result = [x[0] for x in curr.fetchall()]

        curr.execute("SELECT jadwal_bulan,jadwal_tanggal,jadwal_hari\
                     FROM [CMS_2].[dbo].[scheduling]\
                     WHERE kode_report = '%s'\
                     AND id_organisasi = '%s'\
                     AND id_server = '%s'" % (cbKodeReport,id_organisasi_result[0],id_server_result[0]))
        jadwal_tanggal_result = [x[1] for x in curr.fetchall()]

        curr.execute("SELECT jadwal_bulan,jadwal_tanggal,jadwal_hari\
                     FROM [CMS_2].[dbo].[scheduling]\
                     WHERE kode_report = '%s'\
                     AND id_organisasi = '%s'\
                     AND id_server = '%s'" % (cbKodeReport,id_organisasi_result[0],id_server_result[0]))
        jadwal_hari_result = [x[2] for x in curr.fetchall()]

        worksheet.write(row2+11,1,'Schedule : %s %s %s' % (jadwal_bulan_result[0],jadwal_hari_result[0],jadwal_tanggal_result[0]),font_size)

        #penulisan note
        curr.execute("SELECT note\
                     FROM [CMS_2].[dbo].[scheduling]\
                     WHERE [kode_report] = '%s'\
                     AND [id_organisasi] = '%s'\
                     AND [id_server] = '%s'\
                     AND aktif = 'Y'"  % (cbKodeReport,id_organisasi_result[0],id_server_result[0]))
        note = [x[0] for x in curr.fetchall()]
        worksheet.write(row2+8,1,'Note : %s' % (note[0]),font_size)


        #penulisan process Time
        curr.execute("select left(getdate(),19)")
        process_time_result = [x[0] for x in curr.fetchall()]
        worksheet.write(row2+9,1,'Process Time : s/d %s' % (process_time_result[0]),font_size)

        #penulisan since
        curr.execute("select [created_date]\
                     FROM [CMS_2].[dbo].[report]\
                     WHERE [kode_report] = '%s'\
                     AND aktif = 'Y'" % (cbKodeReport))
        since = [x[0] for x in curr.fetchall()]
        worksheet.write(row2+10,1,'Since : %s' % (since[0]),font_size)
        
        #penulisan kategori
        curr.execute("SELECT kode_kategori\
                     FROM [CMS_2].[dbo].[scheduling]\
                     WHERE kode_report = '%s'\
                     AND id_organisasi = '%s'\
                     AND id_server = '%s'" % (cbKodeReport,id_organisasi_result[0],id_server_result[0]))
        kode_kategori_result = [x[0] for x in curr.fetchall()]
        
        curr.execute("SELECT [nama_kategori]\
                     FROM [CMS_2].[dbo].[kategori]\
                     WHERE Aktif = 'Y'\
                     AND [kode_kategori] = '%s'" % (kode_kategori_result[0]))

        kategori_result = [x[0] for x in curr.fetchall()]
        worksheet.write(1,count_header,'Category : %s' % (kategori_result[0]),category_style)
        
        ##################
        #msg = TK.messagebox.showinfo("Information!","Finish!")
        workbook.close()
        #root.destroy()
        #menuutama.menuutama(username)
######################################################################################################################################################
    elif (currqueryHeader_result[0] == 2):

        count_header = 0
        
        queryNamaPIC = "SELECT LEFT(cast([penerima] as varchar(100)), charindex('@', [penerima]) - 1)\
                        FROM [CMS_2].[dbo].[scheduling]\
                        WHERE kode_report = '%s'\
                        AND aktif = 'Y'" % (cbKodeReport)
        curr.execute(queryNamaPIC)
        queryNamaPIC_result = [x[0] for x in curr.fetchall()]
    
        
        sql1 = "SELECT kode_report,query,no_urut,nama_user\
                FROM CMS_2.dbo.query query\
                LEFT JOIN CMS_2.dbo.organisasi organisasi\
                ON query.id_organisasi = organisasi.id_organisasi\
                AND organisasi.aktif = 'Y'\
                AND organisasi.nama_organisasi = '%s'\
                LEFT JOIN CMS_2.dbo.server server\
                ON query.id_server = server.id_server\
                AND server.aktif = 'Y'\
                AND server.nama_server = '%s'\
                WHERE kode_report = '%s'" % (cbOrganisasi,cbServer,cbKodeReport)
        
        curr.execute(sql1)

        query = [x[1] for x in curr.fetchall()] #dari hasil sql1, kita mau ambil kolom query nya saja, kenapa tidak SELECT query nya saja ?, karena nnti untuk mengambil
                                                #atribut nama_user dst.

        lengthOfQuery = len(query) #mau ambil berapa panjang/berapa baris isi dari atribut query, untuk keperluan looping

        for i in range (lengthOfQuery):

            sql2 = "%s" % (query[i].replace("~","'"))
            curr.execute(sql2)
            #conn.commit()
            
        result = curr.fetchall()
        
        toExcel = []

        for i in result:
            toExcel.append(i)
        
        workbook = xlsxwriter.Workbook('%s.xls'% (cbKodeReport)) #untuk menulis nama file
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
        
        data = [] 
        data = toExcel #memindahkan data

        row = 0
        col = 0

        coloumn = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        row2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        
        curr.execute(";with		tmp(kode_report, DataItem, merge_cells)\
                     as (\
                     select		kode_report, CONVERT(varchar(100),LEFT(merge_cells, CHARINDEX(',',merge_cells+',')-1)),\
                     CONVERT(varchar(100),STUFF(merge_cells, 1, CHARINDEX(',',merge_cells+','), ''))\
                     from		[CMS_2].[dbo].[filter]\
                     union all\
                     select		kode_report, CONVERT(varchar(100),LEFT(merge_cells, CHARINDEX(',',merge_cells+',')-1)),\
                     CONVERT(varchar(100),STUFF(merge_cells, 1, CHARINDEX(',',merge_cells+','), ''))\
                     from tmp\
                     where		merge_cells > ''\
                     )\
                     select kode_report, DataItem\
                     into  #Schedule_Separate_Comma\
                     from tmp\
                     WHERE kode_report = '%s'\
                     order by DataItem\
                     SELECT	kode_report, STUFF(DataItem,3,1,':')MergeCells1\
                     into	#Schedule_Separate_Comma2\
                     FROM	#Schedule_Separate_Comma" % (cbKodeReport)) 
        
        conn.commit()

        curr.execute(";with		tmp2(kode_report, DataItem, MergeCells1)\
                     as (\
                     select		kode_report, CONVERT(varchar(100),LEFT(MergeCells1, CHARINDEX(':',MergeCells1+':')-1)),\
                     CONVERT(varchar(100),STUFF(MergeCells1, 1, CHARINDEX(':',MergeCells1+':'), ''))\
                     from		#Schedule_Separate_Comma2\
                     union all\
                     select		kode_report, CONVERT(varchar(100),LEFT(MergeCells1, CHARINDEX(':',MergeCells1+':')-1)),\
                     CONVERT(varchar(100),STUFF(MergeCells1, 1, CHARINDEX(':',MergeCells1+':'), ''))\
                     from tmp2\
                     where		MergeCells1 > ''\
                     )\
                     SELECT	kode_report, DataItem MergeCells2\
                     into	#Final3\
                     FROM	tmp2")
        conn.commit()

        curr.execute("select	*\
                     into	#Final4\
                     from	[CMS_2].[dbo].[detail_h]\
                     where	kode_report = '%s'\
                     AND		RIGHT(lokasi,9) = 6\
                     AND		lokasi NOT IN (select MergeCells2 from #Final3)" % (cbKodeReport))
        conn.commit()
        
        sql3 = "SELECT kode_report,nama_kolom,lokasi,format_kolom,lebar_kolom,grouping_flag,formula\
                FROM #Final4"
        curr.execute(sql3)
        nama_kolom = [x[1] for x in curr.fetchall()]

        curr.execute(sql3)
        lokasi = [x[2] for x in curr.fetchall()]
        
        lenLokasi = len(lokasi)
        listIndexCol = []
        for i in range(lenLokasi):
            if(lokasi[i] == 'B6        '):
                listIndexCol.append(1)
            elif(lokasi[i] == 'C6        '):
                listIndexCol.append(2)
            elif(lokasi[i] == 'D6        '):
                listIndexCol.append(3)
            elif(lokasi[i] == 'E6        '):
                listIndexCol.append(4)
            elif(lokasi[i] == 'F6        '):
                listIndexCol.append(5)
            elif(lokasi[i] == 'G6        '):
                listIndexCol.append(6)
            elif(lokasi[i] == 'H6        '):
                listIndexCol.append(7)
            elif(lokasi[i] == 'I6        '):
                listIndexCol.append(8)
            elif(lokasi[i] == 'J6        '):
                listIndexCol.append(9)
            elif(lokasi[i] == 'K6        '):
                listIndexCol.append(10)
            elif(lokasi[i] == 'L6        '):
                listIndexCol.append(11)
            elif(lokasi[i] == 'M6        '):
                listIndexCol.append(12)
            elif(lokasi[i] == 'N6        '):
                listIndexCol.append(13)
            elif(lokasi[i] == 'O6        '):
                listIndexCol.append(14)
            elif(lokasi[i] == 'P6        '):
                listIndexCol.append(15)

        maxColCount = 0
        
        for i in range(lenLokasi):
            worksheet.write(row + 6,listIndexCol[i],nama_kolom[i],fontsize_1stheader) #ini untuk menulis header yang tidak merge
            maxColCount = maxColCount + 1
            count_header = count_header + 1

        ##############################
        #merge 1st header
            
        sqlMergeCells = "SELECT kode_report,REPLACE(MergeCells1,'6','7')MergeCells1\
                        FROM #Schedule_Separate_Comma2"
        curr.execute(sqlMergeCells)
        sqlMergeCells_result = [x[1] for x in curr.fetchall()]

        curr.execute(sqlMergeCells)
        kode_report_mergeCells_result = [x[0] for x in curr.fetchall()]

        curr.execute("select	kode_report,left(MergeCells1,2) leftLokasi\
                     into	#Schedule_Separate_Comma3\
                     from	#Schedule_Separate_Comma2 \
                     select		a.kode_report,leftLokasi,b.nama_kolom\
                     into       #Schedule_Separate_Comma4\
                     from		#Schedule_Separate_Comma3 a\
                     left join	[CMS_2].[dbo].[detail_h] b\
                     on			a.kode_report = b.kode_report\
                     and			a.leftLokasi = b.lokasi")
        conn.commit()

        queryNamaKolomMerge = "SELECT kode_report,leftLokasi,nama_kolom\
                              FROM #Schedule_Separate_Comma4"
        curr.execute(queryNamaKolomMerge)
        queryNamaKolomMerge_result = [x[2] for x in curr.fetchall()] #pengen tau nama kolomnya
        
        
        lensqlMergeCells_result = len(sqlMergeCells_result)
        
        for i in range(lensqlMergeCells_result):
            print(queryNamaKolomMerge_result[i])
            print(sqlMergeCells_result[i])
            worksheet.merge_range('%s'%(sqlMergeCells_result[i]),'%s'%(queryNamaKolomMerge_result[i]), merge_format)
        #end 1st header merge
        
        #start 2nd header    
        querySecondHeader = "select	[kode_report],[nama_kolom],[lokasi]\
                            FROM [CMS_2].[dbo].[detail_h]\
                            WHERE [kode_report] = '%s'\
                            AND RIGHT(lokasi,9) = 7\
                            ORDER BY lokasi" % (cbKodeReport)
        curr.execute(querySecondHeader)
        querySecondHeader_nama_kolom_result = [x[1] for x in curr.fetchall()]

        curr.execute(querySecondHeader)
        querySecondHeader_lokasi_result = [x[2] for x in curr.fetchall()]

        #print(querySecondHeader_nama_kolom_result)
        #print(querySecondHeader_lokasi_result)
        
        lenquerySecondHeader_nama_kolom_result = len (querySecondHeader_nama_kolom_result)
        listSecondHeader = []
        for i in range(lenquerySecondHeader_nama_kolom_result):
            if(querySecondHeader_lokasi_result[i] == 'B7        '):
                listSecondHeader.append(1)
            elif(querySecondHeader_lokasi_result[i] == 'C7        '):
                listSecondHeader.append(2)
            elif(querySecondHeader_lokasi_result[i] == 'D7        '):
                listSecondHeader.append(3)
            elif(querySecondHeader_lokasi_result[i] == 'E7        '):
                listSecondHeader.append(4)
            elif(querySecondHeader_lokasi_result[i] == 'F7        '):
                listSecondHeader.append(5)
            elif(querySecondHeader_lokasi_result[i] == 'G7        '):
                listSecondHeader.append(6)
            elif(querySecondHeader_lokasi_result[i] == 'H7        '):
                listSecondHeader.append(7)
            elif(querySecondHeader_lokasi_result[i] == 'I7        '):
                listSecondHeader.append(8)
            elif(querySecondHeader_lokasi_result[i] == 'J7        '):
                listSecondHeader.append(9)
            elif(querySecondHeader_lokasi_result[i] == 'K7        '):
                listSecondHeader.append(10)
            elif(querySecondHeader_lokasi_result[i] == 'L7        '):
                listSecondHeader.append(11)
            elif(querySecondHeader_lokasi_result[i] == 'M7        '):
                listSecondHeader.append(12)
            elif(querySecondHeader_lokasi_result[i] == 'N7        '):
                listSecondHeader.append(13)
            elif(querySecondHeader_lokasi_result[i] == 'O7        '):
                listSecondHeader.append(14)
            elif(querySecondHeader_lokasi_result[i] == 'P7        '):
                listSecondHeader.append(15)

        #print(lenquerySecondHeader_nama_kolom_result)
        #print(listSecondHeader)
        
        
        worksheet.write(row+7,col, ' ',fontsize_2ndheader)
        worksheet.write(row+7,col+1, ' ',fontsize_2ndheader)
        
        for i in range(lenquerySecondHeader_nama_kolom_result):
            worksheet.write(row + 7,listSecondHeader[i],querySecondHeader_nama_kolom_result[i],fontsize_2ndheader)
            maxColCount = maxColCount + 1
            count_header = count_header + 1

        selisih = count_header - lenquerySecondHeader_nama_kolom_result


        if(selisih > 0):
            for i in range(selisih):
                worksheet.write(row+7,count_header,'',border_btm)
                count_header = count_header + 1

        #end 2nd header
                
        lengthOfData = [x[0] for x in data]
        lengthOfData2 = len(lengthOfData)
        num = 1
        
        for i in range(lengthOfData2+1): #untuk menulis penomoran 1 s/d banyak data
            if (i == 0):
                worksheet.write(row + 6,col,'No',fontsize_1stheader)
                row = row + 2
            else:
                worksheet.write(row + 6,col,num,font_number)
                row = row + 1
                num = num + 1

        m = 1
        row2 = 0
        
        
        for i in range(lengthOfData2): #untuk menulis data
            worksheet.write_row(row2+8,col+m,data[i],font_size)
            row2 = row2 + 1

        ###########################################
        #Mengatur bagian atas dari laporan
        
        listMaxCol = ['B1','C1','D1','E1','F1','G1','H1','I1','J1','K1','L1','N1','O1','P1']
        maxCol = (listMaxCol[maxColCount])

        sql4 = "SELECT kode_report,nama_report,filter,periode,jml_baris_footer \
                FROM CMS_2.dbo.report\
                WHERE kode_report = '%s'" % (cbKodeReport)
        curr.execute(sql4)
        report = curr.fetchone()

        queryWidth = "SELECT * \
                    FROM CMS_2.dbo.detail_h\
                    WHERE kode_report = '%s'" % (cbKodeReport)
        
        listColWidth =['B','C','D','E','F','G','H','I','J','K','L','N','O','P']
        colWidth = (listColWidth[0:maxColCount])
            
        worksheet.merge_range('A1:%s'%(maxCol),'%s'%(cbOrganisasi), merge_format2) 
        worksheet.write('A2','%s' % (report[1]),bold ) #nama report
        worksheet.write('A3','Report Code : %s' % (report[0]),font_size) #kode report
        worksheet.write('A4','PIC : %s' % (queryNamaPIC_result[0]),font_size)
        worksheet.write('A5','Filter : %s' % (report[2]), bold ) #filter
        worksheet.write('A6','Periode : %s' % (report[3]), font_size) #periode

        curr.execute(queryWidth)
        width = [x[4] for x in curr.fetchall()]

        #penulisan printed date
        curr.execute("select left(getdate(),19)")
        printed_date_result = [x[0] for x in curr.fetchall()]
        worksheet.write(2,2,'Printed Date : %s' % (printed_date_result[0]),font_size)

        for i in range(maxColCount):
            worksheet.set_column('%s:%s'%(colWidth[i],colWidth[i]), int(width[i]))
        ###########################################
        #footer    
        curr1 = conn.cursor()
        curr2 = conn.cursor()
        curr3 = conn.cursor()
        curr4 = conn.cursor()
        
        sql5 = "SELECT kode_report,nama_kolom,lokasi,urutan \
                FROM   CMS_2.dbo.detail_f\
                WHERE  kode_report = '%s'" % (cbKodeReport)
        curr1.execute(sql5)
        kodeReport = [a[0] for a in curr1.fetchall()]
        
        curr2.execute(sql5)
        namaKolom = [b[1] for b in curr2.fetchall()]
        
        curr3.execute(sql5)
        lokasi = [c[2] for c in curr3.fetchall()]
        
        curr4.execute(sql5)
        urutan = [d[3] for d in curr4.fetchall()]
        
        lokasiCurr = []
        countOfFooter = len(lokasi)

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
        countFooter = report[4]
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
        #print(countFooter)
        if (countFooter == 1):
            for i in range(lokasiCurr2Len):
                worksheet.write(row2+8,1,'%s' % (namaKolom[0]),font_size)
                worksheet.write(row2+8,lokasiCurr[0],'=SUM(%s8:%s%s)'% (lokasiCurr2[i],lokasiCurr2[i],totalRow+7),footer_format2)

        #penulisan creator        
        curr.execute("select id_organisasi\
                     FROM [CMS_2].[dbo].[organisasi]\
                     WHERE nama_organisasi = '%s'\
                     AND aktif = 'Y'" %(cbOrganisasi))
        id_organisasi_result = [x[0] for x in curr.fetchall()]

        curr.execute("select id_server\
                     FROM [CMS_2].[dbo].server\
                     WHERE nama_server = '%s'\
                     AND aktif = 'Y'" %(cbServer))
        id_server_result = [x[0] for x in curr.fetchall()]
        
        curr.execute("SELECT [nama_user]\
                     FROM [CMS_2].[dbo].[query]\
                     WHERE kode_report = '%s'\
                     AND id_organisasi = '%s'\
                     AND id_server = '%s'"%(cbKodeReport,id_organisasi_result[0],id_server_result[0]))
        creator_result = [x[0] for x in curr.fetchall()]
        worksheet.write(row2+9,count_header - 2,'CREATOR : %s' % (creator_result[0]),font_size)

        #penulisan schedule
        curr.execute("SELECT jadwal_bulan,jadwal_tanggal,jadwal_hari\
                     FROM [CMS_2].[dbo].[scheduling]\
                     WHERE kode_report = '%s'\
                     AND id_organisasi = '%s'\
                     AND id_server = '%s'" % (cbKodeReport,id_organisasi_result[0],id_server_result[0]))
        jadwal_bulan_result = [x[0] for x in curr.fetchall()]

        curr.execute("SELECT jadwal_bulan,jadwal_tanggal,jadwal_hari\
                     FROM [CMS_2].[dbo].[scheduling]\
                     WHERE kode_report = '%s'\
                     AND id_organisasi = '%s'\
                     AND id_server = '%s'" % (cbKodeReport,id_organisasi_result[0],id_server_result[0]))
        jadwal_tanggal_result = [x[1] for x in curr.fetchall()]

        curr.execute("SELECT jadwal_bulan,jadwal_tanggal,jadwal_hari\
                     FROM [CMS_2].[dbo].[scheduling]\
                     WHERE kode_report = '%s'\
                     AND id_organisasi = '%s'\
                     AND id_server = '%s'" % (cbKodeReport,id_organisasi_result[0],id_server_result[0]))
        jadwal_hari_result = [x[2] for x in curr.fetchall()]

        worksheet.write(row2+12,1,'Schedule : %s %s %s' % (jadwal_bulan_result[0],jadwal_hari_result[0],jadwal_tanggal_result[0]),font_size)

        #penulisan note
        curr.execute("SELECT note\
                     FROM [CMS_2].[dbo].[scheduling]\
                     WHERE [kode_report] = '%s'\
                     AND [id_organisasi] = '%s'\
                     AND [id_server] = '%s'\
                     AND aktif = 'Y'"  % (cbKodeReport,id_organisasi_result[0],id_server_result[0]))
        note = [x[0] for x in curr.fetchall()]
        worksheet.write(row2+9,1,'Note : %s' % (note[0]),font_size)


        #penulisan process Time
        curr.execute("select left(getdate(),19)")
        process_time_result = [x[0] for x in curr.fetchall()]
        worksheet.write(row2+10,1,'Process Time : s/d %s' % (process_time_result[0]),font_size)

        #penulisan since
        curr.execute("select [created_date]\
                     FROM [CMS_2].[dbo].[report]\
                     WHERE [kode_report] = '%s'\
                     AND aktif = 'Y'" % (cbKodeReport))
        since = [x[0] for x in curr.fetchall()]
        worksheet.write(row2+11,1,'Since : %s' % (since[0]),font_size)
        
        #penulisan kategori
        curr.execute("SELECT kode_kategori\
                     FROM [CMS_2].[dbo].[scheduling]\
                     WHERE kode_report = '%s'\
                     AND id_organisasi = '%s'\
                     AND id_server = '%s'" % (cbKodeReport,id_organisasi_result[0],id_server_result[0]))
        kode_kategori_result = [x[0] for x in curr.fetchall()]
        
        curr.execute("SELECT [nama_kategori]\
                     FROM [CMS_2].[dbo].[kategori]\
                     WHERE Aktif = 'Y'\
                     AND [kode_kategori] = '%s'" % (kode_kategori_result[0]))

        kategori_result = [x[0] for x in curr.fetchall()]
        worksheet.write(1,count_header,'Category : %s' % (kategori_result[0]),category_style)
        ##################

        #msg = TK.messagebox.showinfo("Information!","Finish!")

        workbook.close()
        #root.destroy()
        #menuutama.menuutama(username)

        
