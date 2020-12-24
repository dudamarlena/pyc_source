# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\386asm.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.386asm

Tool specification for the 386ASM assembler for the Phar Lap ETS embedded
operating system.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/386asm.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
from SCons.Tool.PharLapCommon import addPharLapPaths
import SCons.Util
as_module = __import__('as', globals(), locals(), [])

def generate(env):
    """Add Builders and construction variables for ar to an Environment."""
    as_module.generate(env)
    env['AS'] = '386asm'
    env['ASFLAGS'] = SCons.Util.CLVar('')
    env['ASPPFLAGS'] = '$ASFLAGS'
    env['ASCOM'] = '$AS $ASFLAGS $SOURCES -o $TARGET'
    env['ASPPCOM'] = '$CC $ASPPFLAGS $CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS $SOURCES -o $TARGET'
    addPharLapPaths(env)


def exists(env):
    return env.Detect('386asm')