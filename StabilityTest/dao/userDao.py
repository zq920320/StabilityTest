
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
