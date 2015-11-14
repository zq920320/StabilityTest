from flask import Flask,url_for,g,session
from flask import render_template
from flask import request
import urllib2
import xml.dom.minidom
from StabilityTest import app
from StabilityTest.dao import userDao
from StabilityTest.util import CaseUtil
from lxml import etree

@app.route('/runcase',methods=['GET'])
def runcase():
	return render_template('admin-user.html')

@app.route('/run',methods=['POST'])
def run():
	s= urllib2.urlopen('http://localhost/StabilityTest.PartnerTest?test&format=xml').read()  
	doc = xml.dom.minidom.parseString(s)
	nodes = doc.getElementsByTagName("finalCounts")
	right = nodes[0].getElementsByTagName("right")[0].childNodes[0].nodeValue
	wrong = nodes[0].getElementsByTagName("wrong")[0].childNodes[0].nodeValue
	ignores = nodes[0].getElementsByTagName("ignores")[0].childNodes[0].nodeValue
	return "right:"+right+"wrong:"+wrong+"ignores:"+ignores

@app.route('/cases',methods=['GET'])
def getcaseFloder(floder=None):
	floders = CaseUtil.getFloder('')
	return render_template('case.html',floders=floders)


@app.route('/casedetail/<casename>',methods=['GET'])
def getcasedetail(casename):
	s= urllib2.urlopen('http://localhost:8080/SlimTest.'+casename).read() 
	tree = etree.HTML(s)
	nodes = tree.xpath('/html/body/article/table')
	tables=[]
	# tmp = etree.tostring(''.join(nodes))
	for node in nodes:
		tables.append(etree.tostring(node))
	print tables
	return render_template('casedetail.html',tables=tables)
@app.route('/addtest',methods=['GET'])
def addtest():
	return render_template('addcase.html')

@app.route('/addsuite',methods=['GET'])
def addsuite():
	return render_template('addsuite.html')