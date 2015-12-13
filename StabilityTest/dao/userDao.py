#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from StabilityTest.util import mysqlUtil


def getUserPwd(username):
    cur = mysqlUtil.connectdb()
    resultnum = cur.execute(
        'select password from user where username="' + username + '"')
    if resultnum == 1:
        alldata = cur.fetchall()
        return alldata[0][0]
    else:
        return 0

def getUser(username):
	cur=mysqlUtil.connectdb()
	resultnum = cur.execute('select id,username,password from user where username="' + username + '"')
	if resultnum == 1:
		alldata = cur.fetchall()
		return alldata[0]
	else:
		return 0