# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/mahmoudpkg/humans/person.py
# Compiled at: 2018-02-09 07:44:32
# Size of source mod 2**32: 264 bytes


class Person:

    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def __str__(self):
        return '%s is %s years old and lives in %s' % (self.name, self.age, self.address)