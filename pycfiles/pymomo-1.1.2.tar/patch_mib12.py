# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/WellDone/pymomo/pymomo/config/site_scons/site_tools/patch_mib12.py
# Compiled at: 2015-03-19 14:45:48
import SCons.Builder
_patch_mib12 = SCons.Builder.Builder(action='patch_mib12_api.py $MIB_API_BASE $SOURCES $TARGET')

def generate(env):
    env['BUILDERS']['patch_mib12'] = _patch_mib12


def exists(env):
    return 1