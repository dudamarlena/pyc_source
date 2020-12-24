# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/version_rev.py
# Compiled at: 2020-04-27 11:26:59
# Size of source mod 2**32: 713 bytes
from subprocess import Popen, PIPE
import re
try:
    hg = Popen(['hg', 'summary'], stdout=PIPE).communicate()[0]
    revision = re.search('^parent: ([\\d]*):', hg, re.MULTILINE).group(1)
except:
    revision = '--not determined--'

ProgramName = 'SPIKE'
VersionName = 'Development version'
version = '0.99.17'
rev_date = '27-04-2020'

def report():
    """prints version name when SPIKE starts"""
    return '\n    ========================\n          {0}\n    ========================\n    Version     : {1}\n    Date        : {2}\n    Revision Id : {3}\n    ========================'.format(ProgramName, version, rev_date, revision)


print(report())