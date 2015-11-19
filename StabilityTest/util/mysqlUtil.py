import MySQLdb
from StabilityTest import app


def connectdb():
    conn = MySQLdb.connect(host=app.config['MYSQL_HOST'], user=app.config['MYSQL_USERNAME'], passwd=app.config[
                           'MYSQL_PWD'], db=app.config['MYSQL_DB'], port=app.config['MYSQL_PORT'])
    cur = conn.cursor()
    return cur
