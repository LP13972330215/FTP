#!usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'pliu'

import socketserver
import json
import os
import time
from FTP.server.user.encyption import EncryptUtil


class MyServer(socketserver.BaseRequestHandler):

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
        password_new = EncryptUtil(password)




    def handle(self):
        while True:
            try:
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
            except KeyboardInterrupt as e:
                print("server close")


def main():
    server = socketserver.ThreadingTCPServer(("localhost", 9996), MyServer)
    server.serve_forever()


if __name__ == "__main__":
    main()