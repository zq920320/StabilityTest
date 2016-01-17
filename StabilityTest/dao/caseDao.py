#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from StabilityTest import app
from StabilityTest.util import mysqlUtil
from StabilityTest.util import fileUtil
import os
import time


def getcasebypid(psuiteid):
    cur = mysqlUtil.connectdb()
    resultnum = cur.execute(
        "select id,casename,casetype,intro,create_time from `case` where psuiteid=" + str(psuiteid))
    alldata = cur.fetchall()
    return alldata


def getcasebyid(id):
    cur = mysqlUtil.connectdb()
    resultnum = cur.execute(
        "select id,casename,casetype,intro,create_time,psuitepath from `case` where id=" + str(id))
    if resultnum == 1:
        alldata = cur.fetchall()
        return alldata
    else:
        return 0


TIMEFORMAT = '%Y-%m-%d %X'
# 文件类型 1=case 2=suite


def addcase(casename, casedata, intro, psuiteid):
    cur = mysqlUtil.connectdb()
    # 获取父级路径
    psuitepath = '/' + casename + '/'
    if psuiteid != 0:
        resultnum = cur.execute(
            "select psuitepath from `case` where id = '" + psuiteid + "'")
        if resultnum == 1:
            alldata = cur.fetchall()
            psuitepath = alldata[0][0] + casename + '/'

    # 数据库添加数据 case名称 case数据 父级id 创建时间 类型为case 所在路径
    timestr = time.strftime(TIMEFORMAT, time.localtime())
    sql = "insert into `stability`.`case` ( `create_time`, `casename`, `casedata`, `psuiteid`, `casetype`, `psuitepath`,`intro`) values ('" + \
          timestr + "', '" + casename + "', '" + casedata + "', '" + \
          str(psuiteid) + "', '1', '" + psuitepath + "','" + intro + "')"
    # sql = "insert into case (casename,casedata,psuiteid,create_time,casetype,psuitepath) VLAUES ('"+casename+"','"+casedata+"',"+str(psuiteid)+",'"+timestr+"',1,'"+psuitepath+"')"
    resultnum = cur.execute(sql)
    if resultnum == 1:
        fileUtil.addcase(casename, psuitepath, casedata)
        return 1
    else:
        return 0


def addsuite(suitename, suitedata, psuiteid, intro):
    cur = mysqlUtil.connectdb()
    # 获取父级路径
    if psuiteid != '0':
        resultnum = cur.execute(
            "select psuitepath from `case` where id = " + psuiteid)
        if resultnum == 1:
            alldata = cur.fetchall()
            psuitepath = alldata[0][0] + suitename + '/'
    else:
        psuitepath = suitename + '/'
    # 数据库添加数据 case名称 case数据 父级id 创建时间 类型为case 所在路径
    timestr = time.strftime(TIMEFORMAT, time.localtime())
    sql = "insert into `stability`.`case` ( `create_time`, `casename`, `casedata`, `psuiteid`, `casetype`, `psuitepath`,`intro`) values ('" + \
          timestr + "', '" + suitename + "', '" + suitedata + \
          "', '" + str(psuiteid) + "', '2', '" + psuitepath + "','" + intro + "')"
    resultnum = cur.execute(sql)
    if resultnum == 1:
        # 要添加的路径
        fileUtil.addsuite(suitename, psuitepath, suitedata)
        return 1
    else:
        return 0
    return 0


def delsuite(caseids):
    cur = mysqlUtil.connectdb()
    for caseid in caseids:
        resultnum = cur.execute(
            "select id from `case` where psuiteid=" + str(caseid))
        if resultnum == 0:
            cur.execute(
                "select psuitepath from `case` where id=" + str(caseid))
            alldata = cur.fetchall()
            psuitepath = alldata[0][0]
            fileUtil.delsuite(psuitepath)
            cur.execute("delete from `case` where id =" + str(caseid))
        else:

            newcaseids = cur.fetchall()
            newcaseidslist = []
            for newcaseid in newcaseids:
                newcaseidslist.append(newcaseid[0])
            delsuite(newcaseidslist)
            cur.execute(
                "select psuitepath from `case` where id=" + str(caseid))
            alldata = cur.fetchall()
            psuitepath = alldata[0][0]
            fileUtil.delsuite(psuitepath)
            cur.execute("delete from `case` where id =" + str(caseid))


def delcase(caseids):
    cur = mysqlUtil.connectdb()
    for caseid in caseids:
        cur.execute("select psuitepath from `case` where id=" + str(caseid))
        alldata = cur.fetchall()
        psuitepath = alldata[0][0]
        fileUtil.delcase(psuitepath)
        cur.execute("delete from `case` where id =" + str(caseid))
    return 1


# 统计所有case数量
def totalcase():
    cur = mysqlUtil.connectdb()
    cur.execute("select count(*) from `case` where casetype=1")
    alldata = cur.fetchall()
    return alldata[0][0]


# 统计新建case数量
def totalnewcase():
    cur = mysqlUtil.connectdb()
    timestr = time.strftime(TIMEFORMAT, time.localtime())
    oldtimestr = time.strftime(TIMEFORMAT, time.localtime(time.time() - 24 * 60 * 60))
    sql = "select count(*) from `case` where `case`.create_time between '" + oldtimestr + "' and '" + timestr + "'"
    cur.execute(sql)
    alldata = cur.fetchall()
    return alldata[0][0]


def getcase(caseid):
    cur = mysqlUtil.connectdb()
    sql = "select * from `case` where id=" + caseid
    cur.execute(sql)
    alldata = cur.fetchall()
    return alldata[0]


def updatecase(id, pageContent, intro):
    cur = mysqlUtil.connectdb()
    sql = "update `stability`.`case` set `casedata`='" + pageContent + "',`intro`='" + intro + "' where `id`=" + id
    n = cur.execute(sql)
    resultnum = cur.execute(
        "select psuitepath,casename from `case` where id = " + id)
    if resultnum == 1:
        alldata = cur.fetchall()
        psuitepath = alldata[0][0]
        fileUtil.updatecase(psuitepath, pageContent)
        return '1'
    else:
        return '1'
