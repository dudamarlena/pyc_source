# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ifacetools\fbtest\user.py
# Compiled at: 2019-08-12 20:51:57
# Size of source mod 2**32: 379 bytes
import factory

class User:

    def __init__(self, name, num, age, school, city, phone):
        self.name, self.num, self.age, self.school, self.city, self.phone = (
         name, num, age, school, city, phone)