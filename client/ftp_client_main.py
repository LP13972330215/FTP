#!usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'pliu'

import socket
import os
import json


class FtpClient(object):

    def __init__(self):
        self.client = socket.socket()
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.total_size = 0
        self.send_size = 0

    def connect(self, ip, port):
        self.client.connect((ip, port))

    def help(self):
        message = """
        ls
        pwd
        cd ..
        put filename
        get filename
        """
        print(message)

    def login(self):
        username = input("enter youname:").strip()
        password = input("enter passwd:").strip()
        if not len(username) or not len(password):
            return
        cmd = {
            "action": "authentication",
            "username": username,
            "password": password
        }
        self.client.send(json.dumps(cmd).encode('utf-8'))
        server_response = self.client.recv(1024).decode()
        if server_response != 'ok':
            print("login failed")
            return False
        print("login success")
        return True

    def cmd_cd(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            seat = cmd_split[1].strip()
            msg_dic = {
                "action": "cd",
                "seat": seat
            }
            self.client.send(json.dumps(msg_dic).encode('utf-8'))
            server_response = self.client.recv(1024).decode()
            if server_response == 'no':
                print("insufficient privilege")
                return
            print("you enter to:%s" % server_response)

    def interactive(self):
        login_result = self.login()
        if login_result:
            while True:
                cmd = input(">>>:").strip()
                if len(cmd) == 0:
                        continue
                cmd_str = cmd.split()[0]
                if hasattr(self, 'cmd_%s' % cmd_str):
                    func = getattr(self, 'cmd_%s' % cmd_str)
                    func(cmd)
                else:
                    self.help()

    def cmd_ls(self, *args):
        msg_dic = {
                "action": "ls"
            }
        self.client.send(str(json.dumps(msg_dic)).encode('utf-8'))
        server_response = self.client.recv(1024).decode()
        print("ls :\n", server_response)

    def cmd_put(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                filesize = os.stat(filename).st_size
                msg_dic = {
                    "action": "put",
                    "filename": filename,
                    "size": filesize,
                    "overridden": True,
                }
                self.client.send(json.dumps(msg_dic).encode('utf-8'))
                server_response = self.client.recv(1024).decode()
                if server_response == 'ok':
                    foo = open(filename, 'rb')
                    for line in foo:
                        self.client.send(line)
                    else:
                        print('file upload success!!!')
                        foo.close()
            else:
                print(filename, 'is not exits')

    def cmd_get(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            if os.path.exists(filename):
                print("file is exist, will over")
            msg_dic = {
                "action": "get",
                "filename": filename,
            }
            self.client.send(json.dumps(msg_dic).encode('utf-8'))
            server_response = self.client.recv(1024).decode()
            if server_response == "no":
                print("%s is not exist" % filename)
                return

            filesize = json.loads(server_response)['size']
            filename = json.loads(server_response)['filename']
            foo = open(filename, 'wb')
            recv_size = 0
            while recv_size < filesize:
                data = self.client.recv(1024)
                foo.write(data)
                recv_size += len(data)
            else:
                print("file [%s] download success" % filename)

    def cmd_pwd(self, *args):
            msg_dic = {
                "action": "pwd",
            }
            self.client.send(json.dumps(msg_dic).encode('utf-8'))
            server_response = self.client.recv(1024).decode()
            print("pwd:", server_response)


if __name__ == "__main__":
    ftp = FtpClient()
    ftp.connect("localhost", 9998)
    ftp.interactive()
