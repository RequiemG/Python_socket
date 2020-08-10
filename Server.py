import hashlib
import json
import os
import socketserver
import struct

import Server_sql

rand = os.urandom(3)

secret_key = b'zxj'

md5 = hashlib.md5(secret_key)
md5.update(rand)
verify_code = md5.hexdigest()


class MySocketServer(socketserver.BaseRequestHandler):

    # 验证客户端是否合法，并进行用户认证
    def setup(self):
        self.request.send(rand)
        ret = self.request.recv(1024).decode()
        if verify_code == ret:
            print("客户端合法")
            self.request.send("Authentication is successful".encode())
        else:
            print("非法客户端")
            self.request.send("".encode())
            self.request.close()

        # 得到登入,注册,退出的状态
        user_caozuo = self.request.recv(1024).decode()
        # print(user_caozuo)
        self.server_login_register(user_caozuo)

    def server_login_register(self, user_caozuo):
        # 登入
        if user_caozuo == 'login':
            while True:
                user_info = json.loads(self.request.recv(1024).decode())
                # print(user_info)

                if Server_sql.login_sql(user_info):
                    self.request.send("True".encode())
                    print(f"用户{self.client_address}{user_info['username']}登入")
                    os.chdir(fr"E:\Python_Socket_用户家目录\\{user_info['username']}")
                    # print(os.getcwd())
                    break
                else:
                    self.request.send("no".encode())

        # 注册
        if user_caozuo == 'register':
            while True:
                # 让用户输入账号
                username = self.request.recv(1024).decode()
                # 查询数据库,是否存在用户名
                # print(username)
                if Server_sql.register_exist(username):
                    # 发送用户存在的信息
                    self.request.send(json.dumps(False).encode())
                    # self.request.close()      --> oserror
                else:

                    self.request.send(json.dumps(True).encode())
                    password = self.request.recv(1024).decode()
                    # print("username:", username)
                    # print("password:", password)

                    # 把用户名密码存放到数据库
                    Server_sql.register(username, password)
                    # 创建用户家目录
                    # global dirname
                    # dirname = os.chdir("E:\Python_Socket_用户家目录")
                    os.chdir(r"E:\Python_Socket_用户家目录")
                    os.mkdir(username)
                    self.request.send(json.dumps(True).encode())
                    self.server_login_register("login")

    # count = 0
    # ucount = 0
    # dcount = 0

    # 实现上传下载功能
    def handle(self):

        up_or_down = self.request.recv(1024).decode()
        # self.count += 1
        #
        # print(f"走了{self.count}次handle")

        if up_or_down == 'upload':

            # self.ucount += 1
            # print(f"走了upload{self.ucount}次")
            #
            # print("用户选择了上传")
            # 得到正确的文件路径
            is_correct = json.loads(self.request.recv(1024).decode())
            if is_correct:
                # 得到报头长度
                masthead_len = struct.unpack("i", self.request.recv(4))[0]
                # print("报头长度: ", masthead_len)
                masthead = self.request.recv(masthead_len)
                # 得到报头内容
                masthead_content = json.loads(masthead)
                # print(masthead_content)

                # 下载文件
                size = 0
                if masthead_content['file_size'] > 0:  # ssssssssssssss
                    with open(f'{masthead_content["file_name"]}.down', 'wb') as f:
                        while int(masthead_content["file_size"]) > size:
                            data = self.request.recv(1024)
                            f.write(data)
                            size += len(data)
                        print("下载完成")
                        self.handle()
            else:
                self.handle()

        if up_or_down == 'download':

            # self.dcount += 1
            # print(f"走了download{self.dcount}次")

            # 该目录下所有的文件
            # print("down函数下:", os.getcwd())

            filepaths = []
            for root, dirs, files in os.walk(os.getcwd()):
                for file in files:
                    file_path = os.path.join(root, file)
                    filepaths.append(file_path)

            # print(filepaths)
            # 判断是否有文件, 如果为空,
            if len(filepaths) == 0:
                self.request.send(json.dumps(False).encode())
                self.handle()
            else:
                self.request.send(json.dumps(True).encode())
                # 发送所有文件的信息

                file_names = json.dumps(filepaths)
                file_info_len = struct.pack('i', len(file_names))
                self.request.send(file_info_len)
                self.request.send(file_names.encode())

                # 得到用户所要的文件名,并计算文件大小,制作报头发送
                selected = json.loads(self.request.recv(1024).decode())
                if selected:
                    # print("select:", selected)
                    file_size = os.path.getsize(selected)
                    send_file_info = {
                        "file_path": selected,
                        "file_size": file_size
                    }
                    send_file_info_json = json.dumps(send_file_info)
                    len_for_send_file = struct.pack('i', len(send_file_info_json))
                    self.request.send(len_for_send_file)
                    self.request.send(send_file_info_json.encode())

                    size = 0
                    with open(selected, 'rb') as f:
                        while file_size > size:
                            data = f.read(1024)
                            self.request.send(data)
                            size += len(data)
                        print('上传完成')
                else:
                    self.handle()


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8080), MySocketServer)
    server.serve_forever()
