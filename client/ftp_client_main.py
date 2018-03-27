#!usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'pliu'

import socket
import os
import json

client = socket.socket()

client.connect(("0.0.0.0", 9999))


class FtpClient(object):

    def __init__(self):
        self.client = socket.socket()
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

    def interactive(self):
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

    def cmd_get(self):
        pass


if __name__ == "__main__":
    ftp = FtpClient()
    ftp.connect("localhost", 9996)
    ftp.interactive()
