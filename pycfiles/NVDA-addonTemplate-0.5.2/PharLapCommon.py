# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\PharLapCommon.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.PharLapCommon

This module contains common code used by all Tools for the
Phar Lap ETS tool chain.  Right now, this is linkloc and
386asm.

"""
__revision__ = 'src/engine/SCons/Tool/PharLapCommon.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os, os.path, SCons.Errors, SCons.Util, re

def getPharLapPath():
    """Reads the registry to find the installed path of the Phar Lap ETS
    development kit.

    Raises UserError if no installed version of Phar Lap can
    be found."""
    if not SCons.Util.can_read_reg:
        raise SCons.Errors.InternalError('No Windows registry module was found')
    try:
        k = SCons.Util.RegOpenKeyEx(SCons.Util.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Pharlap\\ETS')
        val, type = SCons.Util.RegQueryValueEx(k, 'BaseDir')
        idx = val.find('\x00')
        if idx >= 0:
            val = val[:idx]
        return os.path.normpath(val)
    except SCons.Util.RegError:
        raise SCons.Errors.UserError('Cannot find Phar Lap ETS path in the registry.  Is it installed properly?')


REGEX_ETS_VER = re.compile('#define\\s+ETS_VER\\s+([0-9]+)')

def getPharLapVersion():
    """Returns the version of the installed ETS Tool Suite as a
    decimal number.  This version comes from the ETS_VER #define in
    the embkern.h header.  For example, '#define ETS_VER 1010' (which
    is what Phar Lap 10.1 defines) would cause this method to return
    1010. Phar Lap 9.1 does not have such a #define, but this method
    will return 910 as a default.

    Raises UserError if no installed version of Phar Lap can
    be found."""
    include_path = os.path.join(getPharLapPath(), os.path.normpath('include/embkern.h'))
    if not os.path.exists(include_path):
        raise SCons.Errors.UserError('Cannot find embkern.h in ETS include directory.\nIs Phar Lap ETS installed properly?')
    mo = REGEX_ETS_VER.search(open(include_path, 'r').read())
    if mo:
        return int(mo.group(1))
    return 910


def addPharLapPaths(env):
    """This function adds the path to the Phar Lap binaries, includes,
    and libraries, if they are not already there."""
    ph_path = getPharLapPath()
    try:
        env_dict = env['ENV']
    except KeyError:
        env_dict = {}
        env['ENV'] = env_dict

    SCons.Util.AddPathIfNotExists(env_dict, 'PATH', os.path.join(ph_path, 'bin'))
    SCons.Util.AddPathIfNotExists(env_dict, 'INCLUDE', os.path.join(ph_path, 'include'))
    SCons.Util.AddPathIfNotExists(env_dict, 'LIB', os.path.join(ph_path, 'lib'))
    SCons.Util.AddPathIfNotExists(env_dict, 'LIB', os.path.join(ph_path, os.path.normpath('lib/vclib')))
    env['PHARLAP_PATH'] = getPharLapPath()
    env['PHARLAP_VERSION'] = str(getPharLapVersion())