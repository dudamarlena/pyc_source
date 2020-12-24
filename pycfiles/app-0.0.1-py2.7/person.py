# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\app\person.py
# Compiled at: 2016-07-26 21:50:00


class Person(object):

    def __init__(self, pid, name, age, sex):
        self.pid = pid
        self.name = name
        self.age = age
        self.sex = sex

    def eating(self):
        return 'People need to eat!'

    def sleeping(self):
        return 'People need to sleep!'

    def walking(self):
        return 'People can walk!'