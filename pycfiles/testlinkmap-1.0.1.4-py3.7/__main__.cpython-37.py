# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/testlinkmap/__main__.py
# Compiled at: 2019-02-15 10:09:55
# Size of source mod 2**32: 251 bytes
import sys
import testlinkmap.find_macho_linkmap as entry
if __name__ == '__main__':
    entry(sys.argv[1:])