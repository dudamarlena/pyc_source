# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\DCommon.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.DCommon

Common code for the various D tools.

Coded by Russel Winder (russel@winder.org.uk)
2012-09-06
"""
__revision__ = 'src/engine/SCons/Tool/DCommon.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os.path

def isD(env, source):
    if not source:
        return 0
    for s in source:
        if s.sources:
            ext = os.path.splitext(str(s.sources[0]))[1]
            if ext == '.d':
                return 1

    return 0


def addDPATHToEnv(env, executable):
    dPath = env.WhereIs(executable)
    if dPath:
        phobosDir = dPath[:dPath.rindex(executable)] + '/../src/phobos'
        if os.path.isdir(phobosDir):
            env.Append(DPATH=[phobosDir])