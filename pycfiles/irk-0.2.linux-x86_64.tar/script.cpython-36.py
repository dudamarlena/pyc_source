# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/installers/script.py
# Compiled at: 2018-06-21 16:26:03
# Size of source mod 2**32: 945 bytes
import os, subprocess, tempfile
from irk.installers.common import Installer, InstallerState

class ScriptInstaller(Installer):

    def __init__(self, script_contents, package):
        self.script_contents = script_contents
        self.package = package

    def install(self, dry_run):
        if dry_run:
            print('Would run a custom script, unable to show contents.')
            return InstallerState.OK
        else:
            f, n = tempfile.mkstemp(text=True)
            os.write(f, bytes((self.script_contents), encoding='ascii'))
            os.chmod(n, 509)
            os.close(f)
            code = subprocess.call((n + ' ' + self.package), shell=True)
            os.unlink(n)
            if code == 0:
                return InstallerState.OK
            if code == 101:
                return InstallerState.INVALID_NAME
            return InstallerState.FAILED

    def remove(self, dry_run):
        print("NOTIMPL: You can't remove script-based things yet..")