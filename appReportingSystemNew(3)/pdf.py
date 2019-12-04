from db import databaseCMS
from fpdf import FPDF








db 		= databaseCMS.db_request()
cursor 	= db.cursor()
cursor.execute('SELECT user_name, user_id, user_password FROM m_user')
result 	= cursor.fetchall()

k=0
for i in result:
	pdf = FPDF()
	pdf.set_font('Arial',size=8)
	pdf.set_left_margin(0.5)
	pdf.add_page()
	pdf.cell(200, 10, txt="No Kwitansi                   : ", ln=2, align="L")
	pdf.cell(200, 10, txt="Telah Diterima Dari       : "+i[0], ln=4, align="L")
	pdf.cell(200, 10, txt="Sejumlah                       : "+i[1], ln=6, align="L")
	pdf.cell(200, 10, txt="Untuk Pembayaran       : "+i[2], ln=10, align="L")

	pdf.cell(50,10,'text',1,0,'C')
	pdf.set_line_width(1)
	k=k+1
	pdf.output('Kwitansi'+str(k)+'.pdf')