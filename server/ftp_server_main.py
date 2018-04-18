#!usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'pliu'

import socketserver
import json
import time
from server.user.encyption import EncryptUtil
from server.user.user import User_operation
import os
from server.config import setting


class Myserver(socketserver.BaseRequestHandler):
    '''ftp服务端'''
    def handle(self):
        try:
            self.conn = self.request
            while True:
                login_info = json.loads(self.conn.recv(1024).decode())    # 接收客户端发的的账号密码信息
                cmd = login_info['action']
                if hasattr(self, cmd):
                    getattr(self, cmd)
        except ConnectionResetError as e:
            self.conn.close()
            print(e)




def main():
    server = socketserver.ThreadingTCPServer(("localhost", 9999), Myserver)
    server.serve_forever()


if __name__ == "__main__":
    main()