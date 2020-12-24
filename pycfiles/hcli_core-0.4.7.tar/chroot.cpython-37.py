# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jeff/Documents/workspace/hcli/hcli_core/hcli_core/sample/hfm/cli/chroot.py
# Compiled at: 2019-06-30 00:01:52
# Size of source mod 2**32: 726 bytes
import os, inspect, re

class Chroot:
    root = os.path.dirname(inspect.getfile(lambda : None))
    chroot = root + '/chroot'
    pwd = chroot

    def __init__(self):
        if not os.path.exists(self.chroot):
            os.makedirs(self.chroot)

    def translate(self, path):
        newpath = path.strip()
        newpath = re.sub('\\.+/', '/', newpath)
        newpath = re.sub('/+', '/', newpath)
        newpath = newpath.rstrip('/')
        if newpath[:1] == '/':
            lockpath = self.chroot + '/' + newpath[1:]
            return lockpath
        return self.pwd + '/' + newpath