import mysql.connector
import sys
from PIL import Image
import base64
#import cStringIO
import PIL.Image

db = mysql.connector.connect(user='root', password='qwerty',
                              host='localhost',
                              database='cms_request')

#image = Image.open('C:/reportingSystem/app/static/images/sky.jpg')
#blob_value = open('C:/reportingSystem/app/static/images/sky.jpg', 'rb').read()  
#args = (blob_value, )
#sql = 'INSERT INTO tesGambar(img) values (%s)'
cursor=db.cursor()
#cursor.execute(sql,args)
sql1='select * from tesGambar'
cursor.execute(sql1)
data = cursor.fetchall()
#db.commit()
print (data[0][0])
#file_like=cStringIO.StringIO(data[0][0])
#img=PIL.Image.open(data[0])
#img.show()

db.close()
