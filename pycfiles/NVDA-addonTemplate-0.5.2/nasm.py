# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\nasm.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.nasm

Tool-specific initialization for nasm, the famous Netwide Assembler.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/nasm.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Defaults, SCons.Tool, SCons.Util
ASSuffixes = [
 '.s', '.asm', '.ASM']
ASPPSuffixes = ['.spp', '.SPP', '.sx']
if SCons.Util.case_sensitive_suffixes('.s', '.S'):
    ASPPSuffixes.extend(['.S'])
else:
    ASSuffixes.extend(['.S'])

def generate(env):
    """Add Builders and construction variables for nasm to an Environment."""
    static_obj, shared_obj = SCons.Tool.createObjBuilders(env)
    for suffix in ASSuffixes:
        static_obj.add_action(suffix, SCons.Defaults.ASAction)
        static_obj.add_emitter(suffix, SCons.Defaults.StaticObjectEmitter)

    for suffix in ASPPSuffixes:
        static_obj.add_action(suffix, SCons.Defaults.ASPPAction)
        static_obj.add_emitter(suffix, SCons.Defaults.StaticObjectEmitter)

    env['AS'] = 'nasm'
    env['ASFLAGS'] = SCons.Util.CLVar('')
    env['ASPPFLAGS'] = '$ASFLAGS'
    env['ASCOM'] = '$AS $ASFLAGS -o $TARGET $SOURCES'
    env['ASPPCOM'] = '$CC $ASPPFLAGS $CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS -c -o $TARGET $SOURCES'


def exists(env):
    return env.Detect('nasm')