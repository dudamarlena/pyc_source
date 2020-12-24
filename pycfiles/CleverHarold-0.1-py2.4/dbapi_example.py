# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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