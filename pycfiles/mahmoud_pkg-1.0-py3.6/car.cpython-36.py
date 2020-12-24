# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/mahmoudpkg/vehicles/car.py
# Compiled at: 2018-02-09 08:38:31
# Size of source mod 2**32: 307 bytes


class Car:

    def __init__(self, color, type, make, license):
        self.color = color
        self.type = type
        self.make = make
        self.license = license

    def __str__(self):
        return 'A %s %s %s with license number %s' % (self.color, self.type, self.make, self.license)