#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, url_for, g, session
from flask import render_template
from flask import request
import urllib2
import threading
import xml.dom.minidom
from StabilityTest import app
from StabilityTest.dao import userDao
from StabilityTest.dao import caseDao
from StabilityTest.dao import logDao
from StabilityTest.util import CaseUtil
from lxml import etree
import time



# case运行thread 1通过 2为未通过 0运行中
def casethread(casetype, id, count, runtime):
    rights = 0
    wrongs = 0
    ignores = 0
    dbid = logDao.addlog(id)
    status = '1'
    if count != '':
        case = caseDao.getcasebyid(id)
        url = "http://" + app.config['FITNESSE_IP'] + "/" + case[0][5][:-1].replace('/',
                                                                                    '.') + "?" + casetype + "&format=xml"
        for i in range(int(count)):
            s = urllib2.urlopen(url).read()
            doc = xml.dom.minidom.parseString(s)
            nodes = doc.getElementsByTagName("finalCounts")
            right = nodes[0].getElementsByTagName("right")[0].childNodes[0].nodeValue
            rights = rights + int(right)
            wrong = nodes[0].getElementsByTagName("wrong")[0].childNodes[0].nodeValue
            wrongs = wrongs + int(wrong)
            ignore = nodes[0].getElementsByTagName(
                "ignores")[0].childNodes[0].nodeValue
            ignores = ignores + int(ignore)
            logDao.updatelog(dbid)
        if wrongs != 0:
            status = '2'
        logDao.caseover(dbid, status)
        result = "right:" + str(rights) + "wrong:" + str(wrongs) + "ignores:" + str(ignores)
    else:
        finishtime = int(time.time()) + int(runtime) * 60
        case = caseDao.getcasebyid(id)
        url = "http://" + app.config['FITNESSE_IP'] + "/" + case[0][5][:-1].replace('/',
                                                                                    '.') + "?" + casetype + "&format=xml"
        while (finishtime > int(time.time())):
            s = urllib2.urlopen(url).read()
            doc = xml.dom.minidom.parseString(s)
            nodes = doc.getElementsByTagName("finalCounts")
            right = nodes[0].getElementsByTagName("right")[0].childNodes[0].nodeValue
            rights = rights + int(right)
            wrong = nodes[0].getElementsByTagName("wrong")[0].childNodes[0].nodeValue
            wrongs = wrongs + int(wrong)
            ignore = nodes[0].getElementsByTagName(
                "ignores")[0].childNodes[0].nodeValue
            ignores = ignores + int(ignore)
            logDao.updatelog(dbid)
        if wrongs != 0:
            status = '2'
        logDao.caseover(dbid, status)
        result = "right:" + str(rights) + "wrong:" + str(wrongs) + "ignores:" + str(ignores)
    return result


# 根据id运行case
@app.route('/runcase', methods=['POST'])
def runcase():
    caseid = request.form['caseid']
    count = request.form['count']
    runtime = request.form['time']
    caset = threading.Thread(target=casethread, args=("test", caseid, count, runtime))
    caset.setDaemon(True)
    caset.start()
    return '1'


# 根据id运行suite
@app.route('/runsuite', methods=['POST'])
def runsuite():
    suiteid = request.form['suiteid']
    count = request.form['count']
    runtime = request.form['time']
    caset = threading.Thread(target=casethread, args=("suite", suiteid, count, runtime))
    caset.setDaemon(True)
    caset.start()
    return '1'


# case管理
@app.route('/cases', methods=['GET'])
def getcaseFloder():
    floders = caseDao.getcasebypid(0)
    result = {'psuiteid': 0, 'floders': floders, 'action': ''}
    return render_template('case.html', result=result)


# 根据suiteid找到其下面的内容
@app.route('/cases/<suiteid>', methods=['GET'])
def getsuiteFloder(suiteid):
    floders = caseDao.getcasebypid(suiteid)
    result = {'psuiteid': suiteid, 'floders': floders, 'action': ''}
    print floders
    return render_template('case.html', result=result)


# 删除case
@app.route('/delcase', methods=['POST'])
def delcase():
    caseid = request.form['caseid']
    caseids = [caseid]
    caseDao.delcase(caseids)
    return '1'


# 删除suite
@app.route('/delsuite', methods=['POST'])
def delsuite():
    suiteid = request.form['suiteid']
    suiteids = [suiteid]
    caseDao.delsuite(suiteids)
    return '1'


# #显示case详情
# @app.route('/casedetail/<casename>', methods=['GET'])
# def getcasedetail(casename):
#     s = urllib2.urlopen('http://localhost:8080/SlimTest.' + casename).read()
#     tree = etree.HTML(s)
#     nodes = tree.xpath('/html/body/article/table')
#     tables = []
#     # tmp = etree.tostring(''.join(nodes))
#     for node in nodes:
#         tables.append(etree.tostring(node))
#     return render_template('casedetail.html', tables=tables)

# 添加case type 1添加 2修改
@app.route('/addcase/<psuiteid>', methods=['GET', 'POST'])
def addcase(psuiteid):
    if request.method == 'GET':
        result = {'type': 1, 'data': {'psuiteid': psuiteid}}
        return render_template('addcase.html', result=result)
    else:
        pageName = request.form['pageName']
        pageContent = request.form['pageContent']
        intro = request.form['intro']
        caseDao.addcase(pageName, pageContent, intro, psuiteid)
        return '1'


# 添加suite
@app.route('/addsuite/<psuiteid>', methods=['GET', 'POST'])
def addsuite(psuiteid):
    if request.method == 'GET':
        result = {'type': 1, 'data': {'psuiteid': psuiteid}}
        return render_template('addsuite.html', result=result)
    else:
        pageName = request.form['pageName']
        pageContent = request.form['pageContent']
        # psuiteid = request.form['psuiteid']
        intro = request.form['intro']
        caseDao.addsuite(pageName, pageContent, psuiteid, intro)
        return '1'


# 编辑更新suite
@app.route('/updatesuite/<suiteid>', methods=['GET', 'POST'])
def editsuite(suiteid):
    if request.method == 'GET':
        suitedata = caseDao.getcase(suiteid)
        result = {'type': 2,
                  'data': {'id': suiteid, 'casename': suitedata[1], 'intro': suitedata[7], 'casedata': suitedata[2]}}
        return render_template('addsuite.html', result=result)
        # return '1'
    else:
        pageContent = request.form['pageContent']
        # psuiteid = request.form['psuiteid']
        intro = request.form['intro']
        caseDao.updatecase(suiteid, pageContent, intro)
        return '1'


# 编辑更新case
@app.route('/updatecase/<caseid>', methods=['GET', 'POST'])
def editcase(caseid):
    if request.method == 'GET':
        casedata = caseDao.getcase(caseid)
        result = {'type': 2,
                  'data': {'id': caseid, 'casename': casedata[1], 'intro': casedata[7], 'casedata': casedata[2]}}
        return render_template('addcase.html', result=result)
    else:
        pageContent = request.form['pageContent']
        # psuiteid = request.form['psuiteid']
        intro = request.form['intro']
        caseDao.updatecase(caseid, pageContent, intro)
        return '1'
