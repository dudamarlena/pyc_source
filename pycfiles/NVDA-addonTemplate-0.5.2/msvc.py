# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\msvc.py
# Compiled at: 2016-07-07 03:21:33
"""engine.SCons.Tool.msvc

Tool-specific initialization for Microsoft Visual C/C++.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/msvc.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os.path, re, sys, SCons.Action, SCons.Builder, SCons.Errors, SCons.Platform.win32, SCons.Tool, SCons.Tool.msvs, SCons.Util, SCons.Warnings, SCons.Scanner.RC
from MSCommon import msvc_exists, msvc_setup_env_once
CSuffixes = [
 '.c', '.C']
CXXSuffixes = ['.cc', '.cpp', '.cxx', '.c++', '.C++']

def validate_vars(env):
    """Validate the PCH and PCHSTOP construction variables."""
    if 'PCH' in env and env['PCH']:
        if 'PCHSTOP' not in env:
            raise SCons.Errors.UserError('The PCHSTOP construction must be defined if PCH is defined.')
        if not SCons.Util.is_String(env['PCHSTOP']):
            raise SCons.Errors.UserError('The PCHSTOP construction variable must be a string: %r' % env['PCHSTOP'])


def pch_emitter(target, source, env):
    """Adds the object file target."""
    validate_vars(env)
    pch = None
    obj = None
    for t in target:
        if SCons.Util.splitext(str(t))[1] == '.pch':
            pch = t
        if SCons.Util.splitext(str(t))[1] == '.obj':
            obj = t

    if not obj:
        obj = SCons.Util.splitext(str(pch))[0] + '.obj'
    target = [pch, obj]
    return (
     target, source)


def object_emitter(target, source, env, parent_emitter):
    """Sets up the PCH dependencies for an object file."""
    validate_vars(env)
    parent_emitter(target, source, env)
    if 'PCH' in env:
        pch = env['PCH']
        if str(target[0]) != SCons.Util.splitext(str(pch))[0] + '.obj':
            env.Depends(target, pch)
    return (
     target, source)


def static_object_emitter(target, source, env):
    return object_emitter(target, source, env, SCons.Defaults.StaticObjectEmitter)


def shared_object_emitter(target, source, env):
    return object_emitter(target, source, env, SCons.Defaults.SharedObjectEmitter)


pch_action = SCons.Action.Action('$PCHCOM', '$PCHCOMSTR')
pch_builder = SCons.Builder.Builder(action=pch_action, suffix='.pch', emitter=pch_emitter, source_scanner=SCons.Tool.SourceFileScanner)
res_scanner = SCons.Scanner.RC.RCScan()
res_action = SCons.Action.Action('$RCCOM', '$RCCOMSTR')
res_builder = SCons.Builder.Builder(action=res_action, src_suffix='.rc', suffix='.res', src_builder=[], source_scanner=res_scanner)

def msvc_batch_key(action, env, target, source):
    """
    Returns a key to identify unique batches of sources for compilation.

    If batching is enabled (via the $MSVC_BATCH setting), then all
    target+source pairs that use the same action, defined by the same
    environment, and have the same target and source directories, will
    be batched.

    Returning None specifies that the specified target+source should not
    be batched with other compilations.
    """
    if 'MSVC_BATCH' not in env or env.subst('$MSVC_BATCH') in ('0', 'False', '', None):
        return None
    t = target[0]
    s = source[0]
    if os.path.splitext(t.name)[0] != os.path.splitext(s.name)[0]:
        return None
    else:
        return (
         id(action), id(env), t.dir, s.dir)


def msvc_output_flag(target, source, env, for_signature):
    """
    Returns the correct /Fo flag for batching.

    If batching is disabled or there's only one source file, then we
    return an /Fo string that specifies the target explicitly.  Otherwise,
    we return an /Fo string that just specifies the first target's
    directory (where the Visual C/C++ compiler will put the .obj files).
    """
    if 'MSVC_BATCH' not in env or env.subst('$MSVC_BATCH') in ('0', 'False', '', None):
        return '/Fo$TARGET'
    return '/Fo${TARGET.dir}' + os.sep
    return


CAction = SCons.Action.Action('$CCCOM', '$CCCOMSTR', batch_key=msvc_batch_key, targets='$CHANGED_TARGETS')
ShCAction = SCons.Action.Action('$SHCCCOM', '$SHCCCOMSTR', batch_key=msvc_batch_key, targets='$CHANGED_TARGETS')
CXXAction = SCons.Action.Action('$CXXCOM', '$CXXCOMSTR', batch_key=msvc_batch_key, targets='$CHANGED_TARGETS')
ShCXXAction = SCons.Action.Action('$SHCXXCOM', '$SHCXXCOMSTR', batch_key=msvc_batch_key, targets='$CHANGED_TARGETS')

def generate(env):
    """Add Builders and construction variables for MSVC++ to an Environment."""
    static_obj, shared_obj = SCons.Tool.createObjBuilders(env)
    static_obj.cmdgen.source_ext_match = False
    shared_obj.cmdgen.source_ext_match = False
    for suffix in CSuffixes:
        static_obj.add_action(suffix, CAction)
        shared_obj.add_action(suffix, ShCAction)
        static_obj.add_emitter(suffix, static_object_emitter)
        shared_obj.add_emitter(suffix, shared_object_emitter)

    for suffix in CXXSuffixes:
        static_obj.add_action(suffix, CXXAction)
        shared_obj.add_action(suffix, ShCXXAction)
        static_obj.add_emitter(suffix, static_object_emitter)
        shared_obj.add_emitter(suffix, shared_object_emitter)

    env['CCPDBFLAGS'] = SCons.Util.CLVar(['${(PDB and "/Z7") or ""}'])
    env['CCPCHFLAGS'] = SCons.Util.CLVar(['${(PCH and "/Yu%s \\"/Fp%s\\""%(PCHSTOP or "",File(PCH))) or ""}'])
    env['_MSVC_OUTPUT_FLAG'] = msvc_output_flag
    env['_CCCOMCOM'] = '$CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS $CCPCHFLAGS $CCPDBFLAGS'
    env['CC'] = 'cl'
    env['CCFLAGS'] = SCons.Util.CLVar('/nologo')
    env['CFLAGS'] = SCons.Util.CLVar('')
    env['CCCOM'] = '${TEMPFILE("$CC $_MSVC_OUTPUT_FLAG /c $CHANGED_SOURCES $CFLAGS $CCFLAGS $_CCCOMCOM","$CCCOMSTR")}'
    env['SHCC'] = '$CC'
    env['SHCCFLAGS'] = SCons.Util.CLVar('$CCFLAGS')
    env['SHCFLAGS'] = SCons.Util.CLVar('$CFLAGS')
    env['SHCCCOM'] = '${TEMPFILE("$SHCC $_MSVC_OUTPUT_FLAG /c $CHANGED_SOURCES $SHCFLAGS $SHCCFLAGS $_CCCOMCOM","$SHCCCOMSTR")}'
    env['CXX'] = '$CC'
    env['CXXFLAGS'] = SCons.Util.CLVar('$( /TP $)')
    env['CXXCOM'] = '${TEMPFILE("$CXX $_MSVC_OUTPUT_FLAG /c $CHANGED_SOURCES $CXXFLAGS $CCFLAGS $_CCCOMCOM","$CXXCOMSTR")}'
    env['SHCXX'] = '$CXX'
    env['SHCXXFLAGS'] = SCons.Util.CLVar('$CXXFLAGS')
    env['SHCXXCOM'] = '${TEMPFILE("$SHCXX $_MSVC_OUTPUT_FLAG /c $CHANGED_SOURCES $SHCXXFLAGS $SHCCFLAGS $_CCCOMCOM","$SHCXXCOMSTR")}'
    env['CPPDEFPREFIX'] = '/D'
    env['CPPDEFSUFFIX'] = ''
    env['INCPREFIX'] = '/I'
    env['INCSUFFIX'] = ''
    env['STATIC_AND_SHARED_OBJECTS_ARE_THE_SAME'] = 1
    env['RC'] = 'rc'
    env['RCFLAGS'] = SCons.Util.CLVar('')
    env['RCSUFFIXES'] = ['.rc', '.rc2']
    env['RCCOM'] = '$RC $_CPPDEFFLAGS $_CPPINCFLAGS $RCFLAGS /fo$TARGET $SOURCES'
    env['BUILDERS']['RES'] = res_builder
    env['OBJPREFIX'] = ''
    env['OBJSUFFIX'] = '.obj'
    env['SHOBJPREFIX'] = '$OBJPREFIX'
    env['SHOBJSUFFIX'] = '$OBJSUFFIX'
    msvc_setup_env_once(env)
    env['CFILESUFFIX'] = '.c'
    env['CXXFILESUFFIX'] = '.cc'
    env['PCHPDBFLAGS'] = SCons.Util.CLVar(['${(PDB and "/Yd") or ""}'])
    env['PCHCOM'] = '$CXX /Fo${TARGETS[1]} $CXXFLAGS $CCFLAGS $CPPFLAGS $_CPPDEFFLAGS $_CPPINCFLAGS /c $SOURCES /Yc$PCHSTOP /Fp${TARGETS[0]} $CCPDBFLAGS $PCHPDBFLAGS'
    env['BUILDERS']['PCH'] = pch_builder
    if 'ENV' not in env:
        env['ENV'] = {}
    if 'SystemRoot' not in env['ENV']:
        env['ENV']['SystemRoot'] = SCons.Platform.win32.get_system_root()


def exists(env):
    return msvc_exists()