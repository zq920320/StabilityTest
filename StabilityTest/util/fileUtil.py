#!/usr/bin/env python
# -*- coding: utf-8 -*-
from StabilityTest import app
from StabilityTest.util import mysqlUtil
import time
import os

TIMEFORMAT = '%Y-%m-%d %X'
# 文件类型 1=case 2=suite


def addcase(suitename, psuitepath, casedata):
    # 要添加的路径
    path = app.config['FITNESSE_ROOT'] + psuitepath
    os.mkdir(path)
    fp = open(path + 'content.txt', 'w')
    fp.write(casedata)
    fp.close()
    fp = open(path + 'properties.xml', 'w')
    fp.write('''<?xml version="1.0"?>
				<properties>
					<Edit/>
					<Files/>
					<Properties/>
					<RecentChanges/>
					<Refactor/>
					<Search/>
					<Test/>
					<Versions/>
					<WhereUsed/>
				</properties>
				''')
    fp.close()
    return 1




def delcase(psuitepath):

    path = app.config['FITNESSE_ROOT'] + psuitepath
    os.popen("rm -rf " + path)
    return 1


def addsuite(suitename, psuitepath, suitedata):

    # 要添加的路径
    path = app.config['FITNESSE_ROOT'] + psuitepath
    os.mkdir(path)
    fp = open(path + '/content.txt', 'w')
    fp.write(suitedata)
    fp.close()
    fp = open(path + '/properties.xml', 'w')
    fp.write('''<?xml version="1.0"?>
				<properties>
					<Edit/>
					<Files/>
					<Properties/>
					<RecentChanges/>
					<Refactor/>
					<Search/>
					<Suite/>
					<Versions/>
					<WhereUsed/>
				</properties>
				''')
    fp.close()

    return 0


def updatecase(casepath, casedata):
    path = app.config['FITNESSE_ROOT'] + casepath
    fp = open(path + '/content.txt', 'w')
    fp.write(casedata)
    fp.close()
    return 0




def delsuite(psuitepath):
    path = app.config['FITNESSE_ROOT'] + psuitepath
    os.popen("rm -rf " + path)
    return 1
