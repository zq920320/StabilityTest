#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
import time
from StabilityTest.util import mysqlUtil
TIMEFORMAT = '%Y-%m-%d %X'
def addlog(caseid):
    cur = mysqlUtil.connectdb()
    timestr = time.strftime(TIMEFORMAT, time.localtime())
    resultnum = cur.execute(
        "insert into `log` (`runtime`,`starttime`,`status`,`caseid`) values (0,'"+timestr+"','0','"+caseid+"') ")
    
    newid = cur.execute("SELECT LAST_INSERT_ID()")
    return str(cur.fetchall()[0][0])

def updatelog(id):
	cur = mysqlUtil.connectdb()
	resultnum = cur.execute(
		"update `log` set `runtime`=`runtime`+1 where id = '"+id+"'")
	return 1

def caseover(id,status):
	cur = mysqlUtil.connectdb()
	timestr = time.strftime(TIMEFORMAT, time.localtime())
	resultnum = cur.execute(
		"update `log` set `endtime`='"+timestr+"' , `status` = '"+status+"' where id = '"+id+"'")
	return 1

def getlog():
	cur = mysqlUtil.connectdb()
	resultnum = cur.execute(
	    "select * from `log`")
	alldata = cur.fetchall()
	return alldata


#统计通过case数量
def totalaccess():
    cur = mysqlUtil.connectdb()
    cur.execute("select count(*) from `log` where status=1")
    alldata = cur.fetchall()
    print alldata
    print alldata[0][0]
    return alldata[0][0]

#统计失败case数量
def totalwarn():
    cur = mysqlUtil.connectdb()
    cur.execute("select count(*) from `log` where status=2")
    alldata = cur.fetchall()
    print alldata
    print alldata[0][0]
    return alldata[0][0]