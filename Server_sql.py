import pymysql
conn = pymysql.connect(host="localhost",user="root",password="password",database="python_socket_info",port=3306,charset="utf8")
cursor = conn.cursor()


def register_exist(data):
    sql = "select * from user_info where username = %s "
    data = data
    cursor.execute(sql, data)
    conn = cursor.fetchone()
    return conn

def register(a,b):
    sql = "insert into user_info(username,password) value (%s,%s)"
    data = [a,b]
    cursor.execute(sql,data)
    conn.commit()


def login_sql(user_info):
    sql = "select * from user_info where username = %s and password = %s"
    data = tuple(user_info.values())
    try:
        cursor.execute(sql,data)
        conn = cursor.fetchone()
        if conn:
            return True
    except:
        return False

