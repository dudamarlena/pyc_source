# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Platform\posix.py
# Compiled at: 2016-07-07 03:21:32
"""SCons.Platform.posix

Platform-specific initialization for POSIX (Linux, UNIX, etc.) systems.

There normally shouldn't be any need to import this module directly.  It
will usually be imported through the generic SCons.Platform.Platform()
selection method.
"""
__revision__ = 'src/engine/SCons/Platform/posix.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import errno, os, os.path, subprocess, sys, select, SCons.Util
from SCons.Platform import TempFileMunge
exitvalmap = {2: 127, 
   13: 126}

def escape(arg):
    """escape shell special characters"""
    slash = '\\'
    special = '"$'
    arg = arg.replace(slash, slash + slash)
    for c in special:
        arg = arg.replace(c, slash + c)

    return '"' + arg + '"'


def exec_subprocess(l, env):
    proc = subprocess.Popen(l, env=env, close_fds=True)
    return proc.wait()


def subprocess_spawn(sh, escape, cmd, args, env):
    return exec_subprocess([sh, '-c', (' ').join(args)], env)


def exec_popen3(l, env, stdout, stderr):
    proc = subprocess.Popen(l, env=env, close_fds=True, stdout=stdout, stderr=stderr)
    return proc.wait()


def piped_env_spawn(sh, escape, cmd, args, env, stdout, stderr):
    return exec_popen3([sh, '-c', (' ').join(args)], env, stdout, stderr)


def generate(env):
    spawn = subprocess_spawn
    pspawn = piped_env_spawn
    if 'ENV' not in env:
        env['ENV'] = {}
    env['ENV']['PATH'] = '/usr/local/bin:/opt/bin:/bin:/usr/bin'
    env['OBJPREFIX'] = ''
    env['OBJSUFFIX'] = '.o'
    env['SHOBJPREFIX'] = '$OBJPREFIX'
    env['SHOBJSUFFIX'] = '$OBJSUFFIX'
    env['PROGPREFIX'] = ''
    env['PROGSUFFIX'] = ''
    env['LIBPREFIX'] = 'lib'
    env['LIBSUFFIX'] = '.a'
    env['SHLIBPREFIX'] = '$LIBPREFIX'
    env['SHLIBSUFFIX'] = '.so'
    env['LIBPREFIXES'] = ['$LIBPREFIX']
    env['LIBSUFFIXES'] = ['$LIBSUFFIX', '$SHLIBSUFFIX']
    env['PSPAWN'] = pspawn
    env['SPAWN'] = spawn
    env['SHELL'] = 'sh'
    env['ESCAPE'] = escape
    env['TEMPFILE'] = TempFileMunge
    env['TEMPFILEPREFIX'] = '@'
    env['MAXLINELENGTH'] = 128072
    env['__RPATH'] = '$_RPATH'
    env['__DRPATH'] = '$_DRPATH'