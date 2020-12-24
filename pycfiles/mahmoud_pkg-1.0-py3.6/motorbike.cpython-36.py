# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/mahmoudpkg/vehicles/motorbike.py
# Compiled at: 2018-02-09 07:39:45
# Size of source mod 2**32: 275 bytes


class MotorBikes:

    def __init__(self, color, make, license):
        self.color = color
        self.make = make
        self.license = license

    def __str__(self):
        return 'A %s %s motorbike with license number %s.' % (self.color, self.make, self.license)