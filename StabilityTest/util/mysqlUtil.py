#!/usr/bin/env python
# -*- coding: utf-8 -*-
import MySQLdb
from StabilityTest import app


def connectdb():
    conn = MySQLdb.connect(host=app.config['MYSQL_HOST'], user=app.config['MYSQL_USERNAME'], passwd=app.config[
                           'MYSQL_PWD'], db=app.config['MYSQL_DB'], port=app.config['MYSQL_PORT'],charset = "utf8")
    cur = conn.cursor()
    return cur
