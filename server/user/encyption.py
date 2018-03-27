#!usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'pliu'

import hashlib

sha1_salt = '51cto'


class EncryptUtil(object):

    def __init__(self):
        pass

    @staticmethod
    def __sha1_enc(origin):
        enc_obj = hashlib.sha1()
        enc_obj.update(origin.encode("utf-8"))
        return enc_obj.hexdigest()

    @staticmethod
    def sha1_salt_enc(origin):
        return EncryptUtil.__sha1_enc(sha1_salt+origin)