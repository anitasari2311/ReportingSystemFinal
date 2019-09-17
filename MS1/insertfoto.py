import mysql.connector
from mysql.connector import Error
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData
def insertBLOB(foto):
    print("Inserting BLOB into uploadfoto table")
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='cms_request',
                                             user='root',
                                             password='qwerty')
        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO uploadfoto
                          (foto) VALUES (%s)"""
        empPicture = convertToBinaryData(foto)
        
        # Convert data into tuple format
        insert_blob_tuple = (foto)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into python_employee table", result)
    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
