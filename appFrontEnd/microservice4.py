from flask import Flask, render_template, redirect, url_for, request, session, flash, json, jsonify
from base64 import b64encode
import auth
# from microservice1 import RequestLaporan
# from templatelaporan import TemplateLaporan
import pymysql
import mysql.connector
from mysql.connector import Error
import requests
import datetime
#from PIL import Image

app = Flask(__name__, static_folder='app/static')
app.static_folder = 'static'
app.secret_key = 'ms4'

@app.route('/Main_ReadReport/<uId>', methods=['POST'])
def Main_ReadReport(uid):


def ReadReport():


def ListenNewSchedul;


if __name__ == "__main__":
    app.run(debug=True, port='5004')