from Client import Client

def conn():
    addr = "127.0.0.1"
    port = 8080
    secret_key = 'zxj'
    client = Client(addr, port, secret_key)
    menu = [('注册', 'register'), ('登入', 'login'), ('退出', 'quit')]
    for index, value in enumerate(menu, 1):
        print(index, value[0])

    return (client,menu)



def select_menu(client,menu):
    first_ui = ''
    while True:
        try:
            ui = int(input(">>>"))
            if ui < 1:
                raise IndexError
            func_str = menu[ui - 1][1]
            first_ui += func_str
            # 发送状态 register, login, quit ... ...
            client.send_msg(func_str)
            return func_str
        except ValueError:
            print("请输入数字")
        except IndexError:
            print("请输入合法数字")


def main():

    client, menu = conn()
    func_str = select_menu(client,menu)
    # global func_str
    # addr = input("IP地址:")
    # port = int(input("端口号:"))
    # secret_key = input("密钥:")

    # addr = "127.0.0.1"
    # port = 8080
    # secret_key = 'zxj'
    # client = Client(addr, port, secret_key)
    #
    # menu = [('注册', 'register'), ('登入', 'login'), ('退出', 'quit')]
    # for index, value in enumerate(menu, 1):
    #     print(index, value[0])

    # first_ui = ''
    # while True:
    #     try:
    #         ui = int(input(">>>"))
    #         if ui < 1:
    #             raise IndexError
    #         func_str = menu[ui - 1][1]
    #         first_ui += func_str
    #         # 发送状态 register, login, quit ... ...
    #         client.send_msg(func_str)
    #         break
    #     except ValueError:
    #         print("请输入数字")
    #     except IndexError:
    #         print("请输入合法数字")

    # 判断register, login, quit
    if hasattr(Client, func_str):
        func = getattr(Client, func_str)#

        ud = func(client)       # select_ud, 用户已存在
        # print(ud)
        # print(type(ud))
        if ud == "用户已存在":
            main()
        else:
            if hasattr(Client,ud):
                upordown = getattr(Client,ud)      # 执行select_ud函数
                while True:
                    u_d = upordown(client)
                    print("main func name",u_d)  # 得到上传或者下载的函数名
                    if hasattr(Client,u_d):
                        exeud = getattr(Client,u_d)     # 得到上传下载的函数
                        print("main",exeud)
                        ret_info = exeud(client)        # 执行上传下载的函数
                        print("main 返回值:",ret_info)
                        if ret_info:
                            continue



            # xx = ud()
            # print(xx)
            # while True:
            #     udorexist = ud()        # 上传下载的函数名
            #     print("main 1ud",udorexist)
            #     if hasattr(Client, udorexist): # 执行上传下载函数
            #         print("main 2 ud",udorexist)
            #         f2 = getattr(Client,udorexist)
            #         f2info = f2(client)     # 执行download得到的返回值
            #         print(f2info)



if __name__ == '__main__':
    main()
