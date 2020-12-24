# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/mahmoudpkg/humans/driver.py
# Compiled at: 2018-02-09 08:29:53
# Size of source mod 2**32: 324 bytes
from .person import Person

class Driver(Person):

    def __init__(self, name, age, address, licenseType, licenseNu):
        Person.__init__(self, name, age, address)
        self.licenseType = licenseType
        slef.licenseNu = licenseNu

    def get_licence_details(self):
        return (
         licenseType, licenseNu)