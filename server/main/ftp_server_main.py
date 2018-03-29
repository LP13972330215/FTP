#!usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'pliu'

import socketserver
import json
import os
import time
from server.user.encyption import EncryptUtil
from server.user.user import User


class MyServer(socketserver.BaseRequestHandler):

    user_basic_path = None
    user_current_path = None

    def put(self, *args):
        cmd_dic = args[0]
        filename = cmd_dic['filename']
        filesize = cmd_dic['size']
        if os.path.isfile(filename):
            f = open(filename + '.new', 'wb')
        else:
            f = open(filename, 'wb')

        self.request.send("ok".encode('utf-8'))
        recv_size = 0
        while recv_size < filesize:
            data = self.request.recv(1024)
            f.write(data)
            recv_size += len(data)
        else:
            print("file [%s] has uploaded" % filename)

    def get(self, *args):
        cmd_dic = args[0]
        filename = cmd_dic['filename']
        if not os.path.isfile(filename):
            self.request.send("no".encode('utf-8'))
            print("file is not exist")
            return
        filesize = os.stat(filename).st_size
        msg_dic = {
            "filename": filename,
            "size": filesize,
        }
        self.request.send(json.dumps(msg_dic).encode('utf-8'))
        time.sleep(0.1)
        foo = open(filename, 'rb')
        for line in foo:
            self.request.send(line)
        else:
            print('file [%s] download success!!!' % filename)
            foo.close()

    def authentication(self, *args):
        cmd_dict = args[0]
        username = cmd_dict["username"]
        password = cmd_dict["password"]
        encrypt_password = EncryptUtil().sha1_salt_enc(password)
        result, path = User(username, encrypt_password).login()

        if result:
            self.request.send("ok".encode('utf-8'))
            MyServer.user_basic_path = path
            MyServer.user_current_path = path
        else:
            self.request.send('no'.encode('utf-8'))

    def pwd(self, *args):
        cmd_dict = args[0]
        action = cmd_dict["action"]
        if action == "pwd":
            print(MyServer.user_current_path)
            self.request.send(MyServer.user_current_path.encode('utf-8'))

    def ls(self, *args):
        cmd_dict = args[0]
        action = cmd_dict["action"]
        if action == "ls":
            print(MyServer.user_current_path)
            self.request.send(str(os.listdir(MyServer.user_current_path)).encode('utf-8'))

    def cd(self, *args):
        result = False
        cmd_dict = args[0]
        action = cmd_dict["action"]
        cd_seat = cmd_dict["seat"].strip()
        if action == 'cd':
            if cd_seat == '/':
                print(MyServer.user_current_path, MyServer.user_basic_path)
                MyServer.user_current_path = MyServer.user_basic_path
                result = True
            if cd_seat == '..':
                res = os.path.dirname(MyServer.user_current_path)
                if res == MyServer.user_current_path:
                    self.request.send("no".encode('utf-8'))
                    return
                MyServer.user_current_path = res
                result = True
            if os.path.exists(MyServer.user_current_path + '/' + cd_seat):
                MyServer.user_current_path = MyServer.user_current_path + '/' + cd_seat
                result = True
            if result:
                self.request.send(str(MyServer.user_current_path).encode('utf-8'))
            else:
                self.request.send("no".encode('utf-8'))


    def handle(self):
        while True:
            try:
                print("waiting...")
                self.data = self.request.recv(1024).strip()
                print("{} wrote:".format(self.client_address[0]))
                print(self.data)
                cmd_dic = json.loads(self.data.decode())
                action = cmd_dic['action']
                if hasattr(self, action):
                    func = getattr(self, action)
                    func(cmd_dic)
            except ConnectionResetError as e:
                print(e)


def main():
    server = socketserver.ThreadingTCPServer(("localhost", 9998), MyServer)
    server.serve_forever()


if __name__ == "__main__":
    main()