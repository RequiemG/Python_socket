import json
# 用户选择登入状态
def login(self):
    while True:
        # username = input("username:")
        # password = input("password:")
        username = "zxj"
        password = "qwer"

        verify_msg = {"username": username, "password": password}
        self.sk.send(json.dumps(verify_msg).encode())
        # 服务器返回验证信息
        server_verify_info = self.sk.recv(1024).decode()
        if server_verify_info == "True":
            print("登入成功")
            break
        else:
            print("登入失败")
    # 登入成功后要做的, 选择上传或者下载
    return self.select_ud()


# 用户选择注册状态
def register(self):
    while True:
        username = input(">>>请输入账号:")
        if username:
            # 发送账号到服务端, 验证是已经存在
            # 再返回状态信息
            # 如果状态信息符合
            while True:
                password1 = input(">>>请输入密码:")
                password2 = input(">>>请确认密码:")
                if password1 != password2:
                    print("密码不一致")
                else:
                    # 发送用户名密码到服务端,让服务端记载
                    print("注册成功")
                    break
            break
        else:
            print("账号不能为空,请重新输入")

# 用户选择退出状态
# 服务端会操作
