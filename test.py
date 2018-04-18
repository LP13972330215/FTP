#!usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'pliu'
class a():
    def b(self):
        print("bbbb")
    def c(self):
        print ("ccc")
    def d(self):
        print ("123")
        if hasattr(self, "b"):
            getattr(self, "b")()
test = a()
test.d()

