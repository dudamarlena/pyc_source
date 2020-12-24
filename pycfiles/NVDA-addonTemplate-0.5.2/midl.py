# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\midl.py
# Compiled at: 2016-07-07 03:21:34
"""SCons.Tool.midl

Tool-specific initialization for midl (Microsoft IDL compiler).

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/midl.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Action, SCons.Builder, SCons.Defaults, SCons.Scanner.IDL, SCons.Util
from MSCommon import msvc_exists

def midl_emitter(target, source, env):
    """Produces a list of outputs from the MIDL compiler"""
    base, ext = SCons.Util.splitext(str(target[0]))
    tlb = target[0]
    incl = base + '.h'
    interface = base + '_i.c'
    t = [tlb, incl, interface]
    midlcom = env['MIDLCOM']
    if midlcom.find('/proxy') != -1:
        proxy = base + '_p.c'
        t.append(proxy)
    if midlcom.find('/dlldata') != -1:
        dlldata = base + '_data.c'
        t.append(dlldata)
    return (t, source)


idl_scanner = SCons.Scanner.IDL.IDLScan()
midl_action = SCons.Action.Action('$MIDLCOM', '$MIDLCOMSTR')
midl_builder = SCons.Builder.Builder(action=midl_action, src_suffix='.idl', suffix='.tlb', emitter=midl_emitter, source_scanner=idl_scanner)

def generate(env):
    """Add Builders and construction variables for midl to an Environment."""
    env['MIDL'] = 'MIDL.EXE'
    env['MIDLFLAGS'] = SCons.Util.CLVar('/nologo')
    env['MIDLCOM'] = '$MIDL $MIDLFLAGS /tlb ${TARGETS[0]} /h ${TARGETS[1]} /iid ${TARGETS[2]} /proxy ${TARGETS[3]} /dlldata ${TARGETS[4]} $SOURCE 2> NUL'
    env['BUILDERS']['TypeLibrary'] = midl_builder


def exists(env):
    return msvc_exists()