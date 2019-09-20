import datetime
import pymysql
import mysql.connector
from flask import Flask, render_template, redirect, url_for, request, json, session, flash
from mysql.connector import Error

def getUserName():
    username = request.form['username']
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

        cursor.execute(''.join(['select user_name from m_user where user_id = "'+username+'"']))

        record = cursor.fetchone()
        clear = str(record).replace("('",'').replace("',)",'')
        return clear

    except Error as e :
        print("Error while connecting file MySQL", e)
    finally:
            #Closing DB Connection.
                if(connection.is_connected()):
                    cursor.close()
                    connection.close()
                print("MySQL connection is closed")

def auth_login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        error = None
        #getId = getUserId()

        # try:
        connection = mysql.connector.connect(
        host='localhost',
        database='cms_request',
        user='root',
        password='qwerty')
        if connection.is_connected():
            db_Info= connection.get_server_info()
        print("Connected to MySQL database...",db_Info)

        cursor = connection.cursor()

        cursor.execute(''.join(['SELECT user_Id, user_name, user_password, user_flag, user_id  FROM m_user WHERE user_id ="'+username+'"']))
        user = cursor.fetchall()

        global row
        for row in user:
            global userId
            userId= row[0]
            global userName
            userName = row[1]
            global userPass
            userPass= row[2]
            global userFlag
            userFlag = row[3]


            if username != userId or password != userPass:
                error = "Invalid username/password"

            if error is None:
                # store the user id in a new session and return to the index
                session.clear()
                session['user_id'] = request.form['username']
                session['username'] = getUserName()

                #session["user_id"] = row[4]

                if userFlag == 'User':
                    return redirect(url_for('user'))
                elif userFlag == 'Admin':
                    return redirect(url_for('task'))
                else:
                    return redirect(url_for('atasan'))

            flash(error)
            # except Error as e :
            #     print("Error while connecting file MySQL", e)
            # finally:
            #         #Closing DB Connection.
            #             if(connection.is_connected()):
            #                 cursor.close()
            #                 connection.close()
            #             print("MySQL connection is closed")


    return render_template("login.html")


def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
