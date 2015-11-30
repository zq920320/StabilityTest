#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, url_for, g, session
from flask import render_template
from flask import request
import urllib2
import xml.dom.minidom
from StabilityTest import app
from StabilityTest.dao import userDao
from StabilityTest.dao import caseDao
from StabilityTest.util import CaseUtil
from lxml import etree


@app.route('/run', methods=['GET'])
def run():
    floders = caseDao.getcasebypid(0)
    result = {'psuiteid': 0, 'floders': floders}
    return render_template('caserun.html',result=result)


@app.route('/runcase/<id>', methods=['GET'])
def runcase(id):
    
    print id
    case = caseDao.getcasebyid(id)
    print case[0][5][:-1]
    url = "http://localhost/"+case[0][5][:-1].replace('/','.')+"?test&format=xml"
    print url
    s = urllib2.urlopen(url).read()
    doc = xml.dom.minidom.parseString(s)
    nodes = doc.getElementsByTagName("finalCounts")
    right = nodes[0].getElementsByTagName("right")[0].childNodes[0].nodeValue
    wrong = nodes[0].getElementsByTagName("wrong")[0].childNodes[0].nodeValue
    ignores = nodes[0].getElementsByTagName(
        "ignores")[0].childNodes[0].nodeValue
    return "right:" + right + "wrong:" + wrong + "ignores:" + ignores

@app.route('/runsuite/<id>', methods=['GET'])
def runsuite(id):
    print id
    case = caseDao.getcasebyid(id)
    print case[0][5][:-1]
    url = "http://localhost/"+case[0][5][:-1].replace('/','.')+"?suite&format=xml"
    print url
    s = urllib2.urlopen(url).read()
    doc = xml.dom.minidom.parseString(s)
    nodes = doc.getElementsByTagName("finalCounts")
    right = nodes[0].getElementsByTagName("right")[0].childNodes[0].nodeValue
    wrong = nodes[0].getElementsByTagName("wrong")[0].childNodes[0].nodeValue
    ignores = nodes[0].getElementsByTagName(
        "ignores")[0].childNodes[0].nodeValue
    return "right:" + right + "wrong:" + wrong + "ignores:" + ignores


@app.route('/cases', methods=['GET'])
def getcaseFloder():
    floders = caseDao.getcasebypid(0)
    result = {'psuiteid': 0, 'floders': floders}
    return render_template('case.html', result=result)


@app.route('/cases/<suiteid>', methods=['GET'])
def getsuiteFloder(suiteid):
    floders = caseDao.getcasebypid(suiteid)
    result = {'psuiteid': suiteid, 'floders': floders}

    return render_template('case.html', result=result)


@app.route('/delcase', methods=['POST'])
def delcase():
    caseid = request.form['caseid']
    caseids = [caseid]
    caseDao.delcase(caseids)
    return '1'


@app.route('/delsuite', methods=['POST'])
def delsuite():
    suiteid = request.form['suiteid']
    suiteids = [suiteid]
    caseDao.delsuite(suiteids)
    return '1'


@app.route('/casedetail/<casename>', methods=['GET'])
def getcasedetail(casename):
    s = urllib2.urlopen('http://localhost:8080/SlimTest.' + casename).read()
    tree = etree.HTML(s)
    nodes = tree.xpath('/html/body/article/table')
    tables = []
    # tmp = etree.tostring(''.join(nodes))
    for node in nodes:
        tables.append(etree.tostring(node))
    return render_template('casedetail.html', tables=tables)


@app.route('/addcase/<psuiteid>', methods=['GET', 'POST'])
def addtest(psuiteid):
    if request.method == 'GET':
        return render_template('addcase.html', psuiteid=psuiteid)
    else:
        pageName = request.form['pageName']
        pageContent = request.form['pageContent']
        intro = request.form['intro']
        caseDao.addcase(pageName, pageContent,intro, psuiteid)
        return '1'


@app.route('/addsuite/<psuiteid>', methods=['GET', 'POST'])
def addsuite(psuiteid):
    if request.method == 'GET':
        return render_template('addsuite.html', psuiteid=psuiteid)
    else:
        pageName = request.form['pageName']
        pageContent = request.form['pageContent']
        # psuiteid = request.form['psuiteid']
        intro = request.form['intro']
        caseDao.addsuite(pageName, pageContent, psuiteid,intro)
        return '1'
