# import json
# x = True
# y1 = json.dumps(x)
# print(y1)
# print("y1type:",type(y1))
# y2 = json.loads(y1)
# print(y2)
# print("y2type:",type(y2))
import pymysql
conn = pymysql.connect(host="localhost",user="root",password="password",database="python_socket_info",port=3306,charset="utf8")
cursor = conn.cursor()



def register():
    sql = "insert into user_info(username,password) value (%s,%s)"
    data = ('zxj','qwer')
    cursor.execute(sql,data)
    conn.commit()

x = {'username':'zxsj','password':'qwer'}


def login_sql(user_info):
    sql = "select * from user_info where username = %s and password = %s"
    data = tuple(user_info.values())
    cursor.execute(sql,data)
    con = cursor.fetchone()
    return con

    # while True:
    #     if user_info["username"] == 'zxj' and user_info["password"] == 'qwer':
    #         return True
    #     else:
    #         return False
# if login_sql(x):
#     print(666)
# else:
#     print('wu')


# sql = "select * from user_info where username = %s "
# data = 'zxj'
# cursor.execute(sql, data)
# conn = cursor.fetchone()
# print(conn)
# global func_str
# addr = input("IP地址:")
# port = int(input("端口号:"))
# secret_key = input("密钥:")



# def a():
#     addr = "127.0.0.1"
#     port = 8080
#     secret_key = 'zxj'
#
#
#     menu = [('注册', 'register'), ('登入', 'login'), ('退出', 'quit')]
#     for index, value in enumerate(menu, 1):
#         print(index, value[0])
#     return menu
#
#
#
# def main():
#     menu = a()
#     first_ui = ''
#     while True:
#         try:
#             ui = int(input(">>>"))
#             if ui < 1:
#                 raise IndexError
#             func_str = menu[ui - 1][1]
#             first_ui += func_str
#             # 发送状态 register, login, quit ... ...
#             break
#         except ValueError:
#             print("请输入数字")
#         except IndexError:
#             print("请输入合法数字")
#
#     print(first_ui,324)
#
# if __name__ == '__main__':
#     main()





import Client
print(hasattr(Client,"logidn"))
