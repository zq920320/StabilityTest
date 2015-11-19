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


@app.route('/runcase', methods=['GET'])
def runcase():
    return render_template('admin-user.html')


@app.route('/run', methods=['POST'])
def run():
    s = urllib2.urlopen(
        'http://localhost/StabilityTest.PartnerTest?test&format=xml').read()
    doc = xml.dom.minidom.parseString(s)
    nodes = doc.getElementsByTagName("finalCounts")
    right = nodes[0].getElementsByTagName("right")[0].childNodes[0].nodeValue
    wrong = nodes[0].getElementsByTagName("wrong")[0].childNodes[0].nodeValue
    ignores = nodes[0].getElementsByTagName(
        "ignores")[0].childNodes[0].nodeValue
    return "right:" + right + "wrong:" + wrong + "ignores:" + ignores


@app.route('/cases', methods=['GET'])
def getcaseFloder():
    floders = caseDao.getcase(0)
    result = {'psuiteid': 0, 'floders': floders}
    return render_template('case.html', result=result)


@app.route('/cases/<suiteid>', methods=['GET'])
def getsuiteFloder(suiteid):
    floders = caseDao.getcase(suiteid)
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
        caseDao.addcase(pageName, pageContent, psuiteid)
        return '1'


@app.route('/addsuite/<psuiteid>', methods=['GET', 'POST'])
def addsuite(psuiteid):
    if request.method == 'GET':
        return render_template('addsuite.html', psuiteid=psuiteid)
    else:
        pageName = request.form['pageName']
        pageContent = request.form['pageContent']
        # psuiteid = request.form['psuiteid']
        caseDao.addsuite(pageName, pageContent, psuiteid)
        return '1'
