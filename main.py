from Client import Client


def main():
    # global func_str
    # addr = input("IP地址:")
    # port = int(input("端口号:"))
    # secret_key = input("密钥:")

    addr = "127.0.0.1"
    port = 8080
    secret_key = 'zxj'
    client = Client(addr, port, secret_key)

    menu = [('注册', 'register'), ('登入', 'login'), ('退出', 'quit')]
    for index, value in enumerate(menu, 1):
        print(index, value[0])

    while True:
        try:
            ui = int(input(">>>"))
            if ui < 1:
                raise IndexError
            func_str = menu[ui - 1][1]
            # 发送状态 register, login, quit ... ...
            client.send_msg(func_str)
            break
        except ValueError:
            print("请输入数字")
        except IndexError:
            print("请输入合法数字")

    # 判断register, login, quit

    if hasattr(Client, func_str):
        func = getattr(Client, func_str)
        ud = func(client)
        print("ud", ud)
        if not ud:
            print('1234')
        else:

            if hasattr(Client, ud):
                print("you")
                ud_func = getattr(Client, ud)
                ud_func(client)

main()
