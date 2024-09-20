import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "",
                           port=3307,
                           db = "fileshareing")
    c = conn.cursor()

    return c, conn		
def inserquery(sql1):
     c, conn = connection()
     c.execute(sql1)
     conn.commit()
     conn.close()
def recoredselect(sql):
    c, conn = connection()
    c.execute(sql);
    result=c.fetchall();
    return result

login_check=0
