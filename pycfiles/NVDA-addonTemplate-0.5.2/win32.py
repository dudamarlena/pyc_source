# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Platform\win32.py
# Compiled at: 2016-07-07 03:21:33
"""SCons.Platform.win32

Platform-specific initialization for Win32 systems.

There normally shouldn't be any need to import this module directly.  It
will usually be imported through the generic SCons.Platform.Platform()
selection method.
"""
__revision__ = 'src/engine/SCons/Platform/win32.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os, os.path, sys, tempfile
from SCons.Platform.posix import exitvalmap
from SCons.Platform import TempFileMunge
import SCons.Util
try:
    import msvcrt, win32api, win32con
    msvcrt.get_osfhandle
    win32api.SetHandleInformation
    win32con.HANDLE_FLAG_INHERIT
except ImportError:
    parallel_msg = 'you do not seem to have the pywin32 extensions installed;\n' + '\tparallel (-j) builds may not work reliably with open Python files.'
except AttributeError:
    parallel_msg = 'your pywin32 extensions do not support file handle operations;\n' + '\tparallel (-j) builds may not work reliably with open Python files.'
else:
    parallel_msg = None
    _builtin_file = file
    _builtin_open = open

    class _scons_file(_builtin_file):

        def __init__(self, *args, **kw):
            _builtin_file.__init__(self, *args, **kw)
            win32api.SetHandleInformation(msvcrt.get_osfhandle(self.fileno()), win32con.HANDLE_FLAG_INHERIT, 0)


    def _scons_open(*args, **kw):
        fp = _builtin_open(*args, **kw)
        win32api.SetHandleInformation(msvcrt.get_osfhandle(fp.fileno()), win32con.HANDLE_FLAG_INHERIT, 0)
        return fp


    file = _scons_file
    open = _scons_open

try:
    import threading
    spawn_lock = threading.Lock()

    def spawnve(mode, file, args, env):
        spawn_lock.acquire()
        try:
            if mode == os.P_WAIT:
                ret = os.spawnve(os.P_NOWAIT, file, args, env)
            else:
                ret = os.spawnve(mode, file, args, env)
        finally:
            spawn_lock.release()

        if mode == os.P_WAIT:
            pid, status = os.waitpid(ret, 0)
            ret = status >> 8
        return ret


except ImportError:

    def spawnve(mode, file, args, env):
        return os.spawnve(mode, file, args, env)


def piped_spawn(sh, escape, cmd, args, env, stdout, stderr):
    if not sh:
        sys.stderr.write('scons: Could not find command interpreter, is it in your PATH?\n')
        return 127
    tmpFileStdout = os.path.normpath(tempfile.mktemp())
    tmpFileStderr = os.path.normpath(tempfile.mktemp())
    stdoutRedirected = 0
    stderrRedirected = 0
    for arg in args:
        if arg.find('>', 0, 1) != -1 or arg.find('1>', 0, 2) != -1:
            stdoutRedirected = 1
        if arg.find('2>', 0, 2) != -1:
            stderrRedirected = 1

    if stdoutRedirected == 0:
        args.append('>' + str(tmpFileStdout))
    if stderrRedirected == 0:
        args.append('2>' + str(tmpFileStderr))
    try:
        args = [sh, '/C', escape((' ').join(args))]
        ret = spawnve(os.P_WAIT, sh, args, env)
    except OSError as e:
        try:
            ret = exitvalmap[e[0]]
        except KeyError:
            sys.stderr.write('scons: unknown OSError exception code %d - %s: %s\n' % (e[0], cmd, e[1]))

        if stderr is not None:
            stderr.write('scons: %s: %s\n' % (cmd, e[1]))

    if stdout is not None and stdoutRedirected == 0:
        try:
            stdout.write(open(tmpFileStdout, 'r').read())
            os.remove(tmpFileStdout)
        except (IOError, OSError):
            pass

    if stderr is not None and stderrRedirected == 0:
        try:
            stderr.write(open(tmpFileStderr, 'r').read())
            os.remove(tmpFileStderr)
        except (IOError, OSError):
            pass

    return ret
    return


def exec_spawn(l, env):
    try:
        result = spawnve(os.P_WAIT, l[0], l, env)
    except OSError as e:
        try:
            result = exitvalmap[e[0]]
            sys.stderr.write('scons: %s: %s\n' % (l[0], e[1]))
        except KeyError:
            result = 127
            if len(l) > 2:
                if len(l[2]) < 1000:
                    command = (' ').join(l[0:3])
                else:
                    command = l[0]
            else:
                command = l[0]
            sys.stderr.write("scons: unknown OSError exception code %d - '%s': %s\n" % (e[0], command, e[1]))

    return result


def spawn(sh, escape, cmd, args, env):
    if not sh:
        sys.stderr.write('scons: Could not find command interpreter, is it in your PATH?\n')
        return 127
    return exec_spawn([sh, '/C', escape((' ').join(args))], env)


def escape(x):
    if x[(-1)] == '\\':
        x = x + '\\'
    return '"' + x + '"'


_system_root = None

def get_system_root():
    global _system_root
    if _system_root is not None:
        return _system_root
    else:
        val = os.environ.get('SystemRoot', 'C:\\WINDOWS')
        if SCons.Util.can_read_reg:
            try:
                k = SCons.Util.RegOpenKeyEx(SCons.Util.hkey_mod.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows NT\\CurrentVersion')
                val, tok = SCons.Util.RegQueryValueEx(k, 'SystemRoot')
            except SCons.Util.RegError:
                try:
                    k = SCons.Util.RegOpenKeyEx(SCons.Util.hkey_mod.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows\\CurrentVersion')
                    val, tok = SCons.Util.RegQueryValueEx(k, 'SystemRoot')
                except KeyboardInterrupt:
                    raise
                except:
                    pass

        _system_root = val
        return val


def get_program_files_dir():
    val = ''
    if SCons.Util.can_read_reg:
        try:
            k = SCons.Util.RegOpenKeyEx(SCons.Util.hkey_mod.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows\\CurrentVersion')
            val, tok = SCons.Util.RegQueryValueEx(k, 'ProgramFilesDir')
        except SCons.Util.RegError:
            val = ''

    if val == '':
        val = os.path.join(os.path.dirname(get_system_root()), 'Program Files')
    return val


class ArchDefinition(object):
    """
    A class for defining architecture-specific settings and logic.
    """

    def __init__(self, arch, synonyms=[]):
        self.arch = arch
        self.synonyms = synonyms


SupportedArchitectureList = [
 ArchDefinition('x86', [
  'i386', 'i486', 'i586', 'i686']),
 ArchDefinition('x86_64', [
  'AMD64', 'amd64', 'em64t', 'EM64T', 'x86_64']),
 ArchDefinition('ia64', [
  'IA64'])]
SupportedArchitectureMap = {}
for a in SupportedArchitectureList:
    SupportedArchitectureMap[a.arch] = a
    for s in a.synonyms:
        SupportedArchitectureMap[s] = a

def get_architecture(arch=None):
    """Returns the definition for the specified architecture string.

    If no string is specified, the system default is returned (as defined
    by the PROCESSOR_ARCHITEW6432 or PROCESSOR_ARCHITECTURE environment
    variables).
    """
    if arch is None:
        arch = os.environ.get('PROCESSOR_ARCHITEW6432')
        if not arch:
            arch = os.environ.get('PROCESSOR_ARCHITECTURE')
    return SupportedArchitectureMap.get(arch, ArchDefinition('', ['']))


def generate(env):
    cmd_interp = ''
    if SCons.Util.can_read_reg:
        try:
            k = SCons.Util.RegOpenKeyEx(SCons.Util.hkey_mod.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows NT\\CurrentVersion')
            val, tok = SCons.Util.RegQueryValueEx(k, 'SystemRoot')
            cmd_interp = os.path.join(val, 'System32\\cmd.exe')
        except SCons.Util.RegError:
            try:
                k = SCons.Util.RegOpenKeyEx(SCons.Util.hkey_mod.HKEY_LOCAL_MACHINE, 'Software\\Microsoft\\Windows\\CurrentVersion')
                val, tok = SCons.Util.RegQueryValueEx(k, 'SystemRoot')
                cmd_interp = os.path.join(val, 'command.com')
            except KeyboardInterrupt:
                raise
            except:
                pass

    if not cmd_interp:
        systemroot = get_system_root()
        tmp_path = systemroot + os.pathsep + os.path.join(systemroot, 'System32')
        tmp_pathext = '.com;.exe;.bat;.cmd'
        if 'PATHEXT' in os.environ:
            tmp_pathext = os.environ['PATHEXT']
        cmd_interp = SCons.Util.WhereIs('cmd', tmp_path, tmp_pathext)
        if not cmd_interp:
            cmd_interp = SCons.Util.WhereIs('command', tmp_path, tmp_pathext)
    if not cmd_interp:
        cmd_interp = env.Detect('cmd')
        if not cmd_interp:
            cmd_interp = env.Detect('command')
    if 'ENV' not in env:
        env['ENV'] = {}
    import_env = [
     'SystemDrive', 'SystemRoot', 'TEMP', 'TMP']
    for var in import_env:
        v = os.environ.get(var)
        if v:
            env['ENV'][var] = v

    if 'COMSPEC' not in env['ENV']:
        v = os.environ.get('COMSPEC')
        if v:
            env['ENV']['COMSPEC'] = v
    env.AppendENVPath('PATH', get_system_root() + '\\System32')
    env['ENV']['PATHEXT'] = '.COM;.EXE;.BAT;.CMD'
    env['OBJPREFIX'] = ''
    env['OBJSUFFIX'] = '.obj'
    env['SHOBJPREFIX'] = '$OBJPREFIX'
    env['SHOBJSUFFIX'] = '$OBJSUFFIX'
    env['PROGPREFIX'] = ''
    env['PROGSUFFIX'] = '.exe'
    env['LIBPREFIX'] = ''
    env['LIBSUFFIX'] = '.lib'
    env['SHLIBPREFIX'] = ''
    env['SHLIBSUFFIX'] = '.dll'
    env['LIBPREFIXES'] = ['$LIBPREFIX']
    env['LIBSUFFIXES'] = ['$LIBSUFFIX']
    env['PSPAWN'] = piped_spawn
    env['SPAWN'] = spawn
    env['SHELL'] = cmd_interp
    env['TEMPFILE'] = TempFileMunge
    env['TEMPFILEPREFIX'] = '@'
    env['MAXLINELENGTH'] = 2048
    env['ESCAPE'] = escape
    env['HOST_OS'] = 'win32'
    env['HOST_ARCH'] = get_architecture().arch