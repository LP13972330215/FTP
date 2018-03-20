#!usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'pliu'

import socketserver
from FTP.server.user.encyption import EncryptUtil


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        conn = self.request
        conn.send("welcome !!!".encode())
        while True:
            date = conn.recv().encode()
            pass


def main():
    server = socketserver.ThreadingTCPServer(("127.0.0.1", 8080), MyServer)
    server.serve_forever()


if __name__ == "__main__":
    main()