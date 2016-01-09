#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, url_for, g, session,redirect
from flask import render_template
from flask import request
from StabilityTest import app
from StabilityTest.dao import userDao
from StabilityTest.dao import caseDao
from StabilityTest.dao import logDao

@app.route('/', methods=['GET', 'POST'])
def login(name=None):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = userDao.getUser(username)
        if user[2] == password:
            session['logged_in'] = True
            return render_template('admin-index.html')
            # return  redirect(url_for('shouye'))
        else:

            return render_template('login.html', name="error")
    else:
        print app.config['SECRET_KEY']
        return render_template('login.html')


@app.route('/admin', methods=['GET'])
def index():

    return render_template('admin-index.html')


@app.route('/shouye', methods=['GET'])
def shouye():
    totalcases = caseDao.totalcase()
    totalaccesses = logDao.totalaccess()
    totalwarns = logDao.totalwarn()
    totalnewcases = caseDao.totalnewcase()
    result = {'totalcases': totalcases, 'totalaccesses': totalaccesses,'totalwarns':totalwarns,'totalnewcases':totalnewcases}
    return render_template('shouye.html',result=result)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return render_template('login.html')
