# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/version.py
# Compiled at: 2020-03-17 10:52:07
# Size of source mod 2**32: 499 bytes
ProgramName = 'SPIKE'
VersionName = 'Development version'
version = '0.99.15'
revision = '468'
rev_date = '17-03-2020'

def report():
    """prints version name when SPIKE starts"""
    return '\n    ========================\n          {0}\n    ========================\n    Version     : {1}\n    Date        : {2}\n    Revision Id : {3}\n    ========================'.format(ProgramName, version, rev_date, revision)


print(report())