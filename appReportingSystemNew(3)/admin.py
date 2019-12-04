from flask import Flask, render_template, redirect, url_for, request, session, flash, json, jsonify, send_from_directory,Blueprint
import requests
import datetime

adminBP = Blueprint('admin', __name__,)


@adminBP.route('/testAdmin')
def index():
    return redirect(url_for('login'))


@adminBP.route('/admin/home')
def admin():
    if session.get('user_id') is None:
        return render_template('ms1login.html')
    else:
        now = datetime.datetime.now()

        day = now.strftime("%A")
        clock = now.strftime("%H:%M:%S")

        print("=== [ homeAdmin ] ===")
        print('ID   : ',session['user_id']),print('Name : ',session['username'])
        print('Time : ',datetime.datetime.now().strftime('%X'))
        print("=====================")
        return render_template('ms2home.html', day=day, clock=clock)