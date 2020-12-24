# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/backup.py
# Compiled at: 2008-04-20 13:19:45
__revision__ = '$Rev$'
import os.path, shutil

def backup(ifname):
    if not os.path.exists(ifname):
        return
    idx = 1
    while True:
        newfname = '%s.%i.bak' % (ifname, idx)
        if not os.path.exists(newfname):
            break
        else:
            idx += 1

    shutil.copy(ifname, newfname)