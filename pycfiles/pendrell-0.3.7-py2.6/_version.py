# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pendrell/_version.py
# Compiled at: 2010-12-26 01:14:14
try:
    from twisted.python.versions import Version
except ImportError:

    class Version(object):

        def __init__(self, package, major, minor, nano, pre=None):
            self.package = package
            self.major = major
            self.minor = minor
            self.nano = nano
            self.pre = pre

        def short(self):
            fmt = '{0.major}.{0.minor}.{0.nano}'
            if self.pre:
                fmt += 'pre{0.pre}'
            return fmt.format(self)


copyright = 'Copyright (c) 2008-2010 Oliver V. Gould.  All rights reserved.'
version = Version('pendrell', 0, 3, 7)
del Version