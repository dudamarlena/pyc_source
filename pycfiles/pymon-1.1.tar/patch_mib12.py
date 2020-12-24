# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/travis/build/WellDone/pymomo/pymomo/config/site_scons/site_tools/patch_mib12.py
# Compiled at: 2015-03-19 14:45:48
import SCons.Builder
_patch_mib12 = SCons.Builder.Builder(action='patch_mib12_api.py $MIB_API_BASE $SOURCES $TARGET')

def generate(env):
    env['BUILDERS']['patch_mib12'] = _patch_mib12


def exists(env):
    return 1