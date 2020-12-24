# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/project/+package+/models/dbapi_example.py
# Compiled at: 2006-08-02 05:57:51


class Person:
    __module__ = __name__
    create = 'CREATE TABLE person (firstName TEXT, middleInitial TEXT, lastName TEXT)'
    drop = 'DROP TABLE person'


class Address:
    __module__ = __name__
    create = 'CREATE TABLE address (street TEXT, city TEXT, state TEXT, zip TEXT)'
    drop = 'DROP TABLE address'