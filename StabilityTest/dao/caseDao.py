#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from StabilityTest import app
from StabilityTest.util import mysqlUtil
from StabilityTest.util import fileUtil
import os
import time


def getcase(psuiteid):
    cur = mysqlUtil.connectdb()
    resultnum = cur.execute(
        "select id,casename,casetype from `case` where psuiteid=" + str(psuiteid))
    alldata = cur.fetchall()
    return alldata


TIMEFORMAT = '%Y-%m-%d %X'
# 文件类型 1=case 2=suite


def addcase(casename, casedata, psuiteid):
    cur = mysqlUtil.connectdb()
    # 获取父级路径
    if psuiteid != 0:
        resultnum = cur .execute(
            "select psuitepath from `case` where id = '" + psuiteid + "'")
        if resultnum == 1:
            alldata = cur.fetchall()
            psuitepath = alldata[0][0] + casename + '/'
    else:
        psuitepath = '/'
    # 数据库添加数据 case名称 case数据 父级id 创建时间 类型为case 所在路径
    timestr = time.strftime(TIMEFORMAT, time.localtime())
    sql = "insert into `stability`.`case` ( `creat_time`, `casename`, `casedata`, `psuiteid`, `casetype`, `psuitepath`) values ('" + \
        timestr + "', '" + casename + "', '" + casedata + "', '" + \
        str(psuiteid) + "', '1', '" + psuitepath + "')"
    # sql = "insert into case (casename,casedata,psuiteid,create_time,casetype,psuitepath) VLAUES ('"+casename+"','"+casedata+"',"+str(psuiteid)+",'"+timestr+"',1,'"+psuitepath+"')"
    resultnum = cur.execute(sql)
    if resultnum == 1:
        fileUtil.addcase(casename, psuitepath, casedata)
        return 1
    else:
        return 0


def addsuite(suitename, suitedata, psuiteid):
    cur = mysqlUtil.connectdb()
    # 获取父级路径
    if psuiteid != '0':
        resultnum = cur .execute(
            "select psuitepath from `case` where id = " + psuiteid)
        if resultnum == 1:
            alldata = cur.fetchall()
            psuitepath = alldata[0][0] + suitename + '/'
    else:
        psuitepath = suitename + '/'
    # 数据库添加数据 case名称 case数据 父级id 创建时间 类型为case 所在路径
    timestr = time.strftime(TIMEFORMAT, time.localtime())
    sql = "insert into `stability`.`case` ( `creat_time`, `casename`, `casedata`, `psuiteid`, `casetype`, `psuitepath`) values ('" + \
        timestr + "', '" + suitename + "', '" + suitedata + \
        "', '" + str(psuiteid) + "', '2', '" + psuitepath + "')"
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
