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

        print(user_caozuo)


        while True:
            if user_caozuo == 'login':
                user_info = json.loads(self.request.recv(1024).decode())
                print(user_info)
                if Server_sql.login(user_info):
                    self.request.send("True".encode())
                    print(f"用户{self.client_address}{user_info['username']}登入")
                    break
            if user_caozuo == 'register':
                # 让用户输入用户名密码
                username = self.request.recv(1024).decode()
                # 查询数据库,是否存在用户名
                if username == 'zxj':
                    self.request.send(json.dumps(False).encode())
                else:
                    self.request.send(json.dumps(True).encode())
                    password = self.request.recv(1024).decode()
                    print("username:", username)
                    print("password:", password)
                    break



        '''if user_caozuo == 'login':
        # 登入:
            while True:
                user_info = json.loads(self.request.recv(1024).decode())
                print(user_info)
                if Server_sql.login(user_info):
                    self.request.send("True".encode())
                    print(f"用户{self.client_address}{user_info['username']}登入")
                    break

        if user_caozuo == 'register':
        # 注册
            while True:
                # 让用户输入用户名密码
                username = self.request.recv(1024).decode()
                # 查询数据库,是否存在用户名
                if username == 'zxj':
                    self.request.send(json.dumps(False).encode())
                else:
                    self.request.send(json.dumps(True').encode())
                    password = self.request.recv(1024).decode()
                    print("username:",username)
                    print("password:",password)
                    break

        # if user_caozuo == 'quit':
        # 退出

'''



    # 实现上传下载功能
    def handle(self):
        up_or_down = self.request.recv(1024).decode()
        if up_or_down == 'upload':
            # 得到报头长度
            masthead_len = struct.unpack("i", self.request.recv(4))[0]
            print("报头长度: ", masthead_len)
            masthead = self.request.recv(masthead_len)
            # 得到报头内容
            masthead_content = json.loads(masthead)
            print(masthead_content)

            # 下载文件
            size = 0
            with open(f'{masthead_content["file_name"]}.down', 'wb') as f:
                while int(masthead_content["file_size"]) > size:
                    data = self.request.recv(1024)
                    f.write(data)
                    size += len(data)
                print("下载完成")

        if up_or_down == 'download':
            # 该目录下所有的文件
            filepaths = []
            for root, dirs, files in os.walk(os.getcwd()):
                for file in files:
                    file_path = os.path.join(root, file)
                    filepaths.append(file_path)

            # 发送所有文件的信息
            file_names = json.dumps(filepaths)
            file_info_len = struct.pack('i', len(file_names))
            self.request.send(file_info_len)
            self.request.send(file_names.encode())

            # 得到用户所要的文件名,并计算文件大小,制作报头发送
            selected = self.request.recv(1024).decode()
            print(selected)
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

    # 上传下载文件
    # def finish(self):
    #     try:
    #         while True:
    #             ret = self.request.recv(1024).decode()
    #             if len(ret) == 0:
    #                 print(f"{self.client_address}正常退出.........")
    #                 break
    #             print(f"来自{self.client_address}:的信息:{ret}")
    #     except ConnectionResetError:
    #         print(f"{self.client_address}断开连接")


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8080), MySocketServer)
    server.serve_forever()
