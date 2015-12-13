#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, url_for, g, session
from flask import render_template
from flask import request
from StabilityTest import app
from StabilityTest.dao import logDao

@app.route('/log', methods=['GET'])
def log():
	logs = logDao.getlog()
	result = {'floders': logs}
	print result
	return render_template('log.html',result=result)