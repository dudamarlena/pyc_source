# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Owls/foam.py
# Compiled at: 2018-11-11 02:42:12
# Size of source mod 2**32: 1281 bytes
"""
Launchers for openfoam utilities

"""
import os, subprocess

def execute(cmd):
    return subprocess.check_call(cmd, shell=True) == 0


def execute_in_path(path, cmd, func=execute):
    print(os.getcwd())
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        ret = func(cmd)
    except:
        ret = False

    os.chdir(old_dir)
    return ret


class genericHook(object):

    def __init__(self, path, cmd):
        self.path = path
        self.cmd = cmd

    def execute(self):
        return execute_in_path(self.path, self.cmd)


class cellCentres(genericHook):

    def __init__(self, path):
        genericHook.__init__(self, path, 'writeCellCentres')


class decompose(genericHook):

    def __init__(self, path, latest=False):
        cmd = 'decomposePar'
        if latest:
            cmd += ' -latestTime'
        genericHook.__init__(self, path, cmd)


class reconstruct(genericHook):

    def __init__(self, path, latest=False):
        cmd = 'reconstructPar'
        if latest:
            cmd += ' -latestTime'
        genericHook.__init__(self, path, cmd)


class sample(genericHook):

    def __init__(self, path, latest=False):
        cmd = 'sample'
        if latest:
            cmd += ' -latestTime'
        genericHook.__init__(self, path, cmd)