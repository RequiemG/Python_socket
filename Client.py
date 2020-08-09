import hashlib
import json
import os
import socket
import struct



class Client:
    def __init__(self, addr: str, port: int, secret_key):
        self.sk = socket.socket()
        self.addr = addr
        self.__port = port
        self.__secret_key = secret_key
        self.sk.connect((self.addr, self.__port))
        self.is_legal()

    def send_msg(self, msg):
        self.sk.send(msg.encode())

    # 验证合法客户端
    def is_legal(self):
        verify_code = self.sk.recv(1024)
        hslb = hashlib.md5(self.__secret_key.encode())
        hslb.update(verify_code)
        code = hslb.hexdigest().encode()
        self.sk.send(code)
        print(self.sk.recv(1024).decode())

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
                self.send_msg(username)
                # 再返回状态信息
                is_exist = json.loads(self.sk.recv(1024).decode())
                print(is_exist)
                print(type(is_exist))
                # 如果状态信息符合
                if is_exist:
                    while True:
                        password1 = input(">>>请输入密码:")
                        password2 = input(">>>请确认密码:")
                        if password1 != password2:
                            print("密码不一致")
                        else:
                            # 发送用户名密码到服务端,让服务端
                            self.send_msg(password2)
                            print("注册成功")
                            break
                    # self.login()
                    break
                else:
                    print("用户已存在")
            else:
                print("请输入合法用户名")

    # 用户选择退出状态
    # 服务端会操作


    def select_ud(self):
        ud_menu = [('上传', 'upload'), ('下载', 'download')]
        for index, value in enumerate(ud_menu, 1):
            print(index, value[0])
        while True:
            try:
                ui = int(input(">>>"))
                if ui < 1:
                    raise IndexError
                func_str = ud_menu[ui - 1][1]
                self.send_msg(func_str)
                return func_str
            except ValueError:
                print("请输入数字")
            except IndexError:
                print("请输入合法数字")


    def jindutiao(self, all_size):
        all_size = all_size
        recv_percent = 0
        while recv_percent <= 100:
            recv_size = yield
            new_percent = int((recv_size / all_size) * 100)
            if new_percent > recv_percent:
                print(f"\r{new_percent}%{int(new_percent * 0.6) * '*'}", end='', flush=True)
                recv_percent = new_percent


    def upload(self):
        # 得到用户要上传的文件描述信息
        dir_path = input("file_path:")
        file_name = input("file_name:")
        file_complete_path = os.path.join(dir_path, file_name)
        file_size = os.path.getsize(file_complete_path)
        file_info = {
            "dir_path": dir_path,
            "file_name": file_name,
            "complete_path": file_complete_path,
            "file_size": file_size
        }

        # 将文件描述信息封装成报头
        file_info_json = json.dumps(file_info)
        send_len_to_server = struct.pack("i", len(file_info_json))

        # 将报头的长度发送到服务端
        self.sk.send(send_len_to_server)

        # 将报头内容发送到服务端
        self.sk.send(file_info_json.encode())

        # 开始读取文件信息, 并上传
        size = 0
        with open(file_info["complete_path"], 'rb') as f:
            while size < file_size:
                data = f.read(1024)
                # 发送数据到服务端
                self.sk.send(data)
                size += len(data)
                c1 = self.jindutiao(file_size)
                c1.__next__()
                c1.send(size)
            print("上传完毕")

    def download(self):
        file_len = struct.unpack('i', self.sk.recv(4))[0]
        all_file = ''
        while file_len > 0:
            file_names = self.sk.recv(1024).decode()
            all_file += file_names
            file_len -= 1024
        all_file_list = json.loads(all_file)
        for i, j in enumerate(all_file_list, 1):
            print(i, j)
        user_select_file = int(input(">>>请选择文件编号:"))
        selected = all_file_list[user_select_file - 1]
        print("已选择:", selected)
        self.sk.send(selected.encode())
        len_for_file = struct.unpack('i', self.sk.recv(4))[0]
        print(len_for_file)
        dl_file_info = json.loads(self.sk.recv(len_for_file).decode())
        print(dl_file_info)
        dl_file_name = os.path.split(dl_file_info['file_path'])[1]
        dl_file_size = dl_file_info['file_size']
        print(dl_file_name)
        print(dl_file_size)

        user_file_path = input(">>>请输入存放的路径:")
        complete_path = os.path.join(user_file_path, dl_file_name)
        print(complete_path)
        size = 0
        with open(complete_path, 'wb') as f:
            while dl_file_size > size:
                data = self.sk.recv(1024)
                f.write(data)
                size += len(data)
            print("下载完成")