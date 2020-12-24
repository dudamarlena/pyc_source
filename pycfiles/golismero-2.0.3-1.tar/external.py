# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/external.py
# Compiled at: 2013-12-09 06:41:16
"""
External tools API.

Use this module to run external tools and grab their output.
This makes an easy way to integrate GoLismero with any command line tools.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'run_external_tool',
 'get_tools_folder',
 'tempfile',
 'tempdir',
 'is_executable',
 'get_interpreter',
 'find_binary_in_path',
 'is_cygwin_binary',
 'get_cygwin_binary',
 'find_cygwin_binary_in_path',
 'win_to_cygwin_path',
 'cygwin_to_win_path']
from ..common import get_tools_folder
import contextlib, re, os, os.path, ntpath, subprocess, stat, shlex, sys
from shutil import rmtree
from tempfile import NamedTemporaryFile, mkdtemp
try:
    WindowsError
except NameError:

    class WindowsError(OSError):
        pass


class ExternalToolError(RuntimeError):
    """
    An error occurred when running an external tool.
    """

    def __init__(self, msg, errcode):
        super(ExternalToolError, self).__init__(self, msg)
        self.errcode = errcode


def run_external_tool(command, args=None, env=None, cwd=None, callback=None):
    r"""
    Run an external tool and optionally fetch the output.

    Standard output and standard error are combined into a single stream.
    Newline characters are always '\n' in all platforms.

    .. warning: SECURITY WARNING: Be *extremely* careful when passing
                data coming from the target servers to this function.
                Failure to properly validate the data may result in
                complete compromise of your machine! See:
                https://www.owasp.org/index.php/Command_Injection

    Example:
        >>> def callback(line):
        ...    print line
        ...
        >>> run_external_tool("uname", callback=callback)
        Linux

    :param command: Command to execute.
    :type command: str

    :param args: Arguments to be passed to the command.
    :type args: list(str)

    :param env: Environment variables to be passed to the command.
    :type env: dict(str -> str)

    :param cwd: Current directory while running the tool.
        This is useful for tools that require you to be standing on a specific
        directory when running them.
    :type cwd: str | None

    :param callback: Optional callback function. If given, it will be called
        once for each line of text printed by the external tool. The trailing
        newline character of each line is removed.
    :type callback: callable

    :returns: Return code from the external tool.
    :rtype: int

    :raises ExternalToolError: An error occurred when running an external tool.
    """
    if callback is not None and not callable(callback):
        raise TypeError('Expected function, got %r instead' % type(callback))
    if not cwd:
        cwd = None
    if not args:
        args = []
    else:
        args = list(args)
        if not command:
            command = args[0]
            del args[0]
        elif args and args[0] == command:
            del args[0]
    if not command:
        raise ValueError('Bad arguments for run_external_tool()')
    if not is_executable(command):
        try:
            interpreter = get_interpreter(command)
        except IOError:
            interpreter = None

        if interpreter:
            command = interpreter[0]
            args = interpreter[1:] + args
        else:
            binary_list = find_binary_in_path(command)
            if not binary_list:
                raise IOError('File not found: %r' % command)
            if os.path.sep == '\\':
                binary = get_cygwin_binary(binary_list)
                if binary:
                    command = binary
                else:
                    command = binary_list[0]
            else:
                command = binary_list[0]
    args.insert(0, command)
    if os.path.sep == '\\':
        if env is None:
            env = os.environ.copy()
        else:
            env = env.copy()
        cygwin = env.get('CYGWIN', '')
        if 'nodosfilewarning' not in cygwin:
            if cygwin:
                cygwin += ' '
            cygwin += 'nodosfilewarning'
        env['CYGWIN'] = cygwin
    if callback is None:
        return subprocess.check_call(args, executable=command, cwd=cwd, env=env, shell=False)
    else:
        proc = None
        try:
            try:
                proc = subprocess.Popen(args, executable=command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=0, shell=False)
            except OSError as e:
                msg = str(e)
                if isinstance(e, WindowsError):
                    if '%1' in msg:
                        msg = msg.replace('%1', command)
                    raise ExternalToolError(msg, e.winerror)
                raise ExternalToolError(msg, e.errno)

            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                if line.endswith('\n'):
                    line = line[:-1]
                callback(line)

        finally:
            if proc is not None and proc.poll() is None:
                proc.terminate()

        return proc.returncode


def is_executable(binary):
    """
    Tests if the given file exists and is executable.

    :param binary: Path to the binary.
    :type binary: str

    :returns: True if the file exists and is executable, False otherwise.
    :rtype: bool
    """
    return os.path.isfile(binary) and (os.path.sep == '\\' and binary.lower().endswith('.exe') or os.path.sep == '/' and os.stat(binary)[stat.ST_MODE] & stat.S_IXUSR != 0)


DEFAULT_INTERPRETER = {'.lua': [
          'lua'], 
   '.php': [
          'php', '-f'], 
   '.pl': [
         'perl'], 
   '.rb': [
         'ruby'], 
   '.sh': [
         'sh', '-c'], 
   '.tcl': [
          'tcl'], 
   '.py': [
         'python'], 
   '.pyc': [
          'python'], 
   '.pyo': [
          'python'], 
   '.pyw': [
          'python'], 
   '.js': [
         'WScript.exe'], 
   '.jse': [
          'WScript.exe'], 
   '.pls': [
          'WScript.exe'], 
   '.phps': [
           'WScript.exe'], 
   '.pys': [
          'WScript.exe'], 
   '.rbs': [
          'WScript.exe'], 
   '.tcls': [
           'WScript.exe'], 
   '.vbs': [
          'WScript.exe'], 
   '.vbe': [
          'WScript.exe'], 
   '.wsf': [
          'WScript.exe']}

def get_interpreter(script):
    """
    Get the correct interpreter for the given script.

    :param script: Path to the script file.
    :type script: str

    :returns: Command line arguments to replace the script with.
        Normally this will be the path to the interpreter followed
        by the path to the script, but not always.
    :rtype: list(str)
    :raises IOError: An error occurred, the file was not a script, or the
        interpreter was not found.
    """
    ext = os.path.splitext(script)[1].lower()
    if os.path.sep == '\\':
        if ext == '.exe':
            binary_list = find_binary_in_path(script)
            if binary_list:
                cygwin = get_cygwin_binary(binary_list)
                if cygwin:
                    return [
                     cygwin]
                return [binary_list[0]]
            return [script]
        if ext in ('.bat', '.cmd'):
            return [os.environ['COMSPEC'], '/C', script]
    elif is_executable(script):
        return [script]
    interpreter = DEFAULT_INTERPRETER.get(ext, None)
    if interpreter:
        interpreter = list(interpreter)
        if os.path.sep == '\\' and not interpreter[0].endswith('.exe'):
            interpreter[0] += '.exe'
        binary_list = find_binary_in_path(interpreter[0])
        if binary_list:
            cygwin = get_cygwin_binary(binary_list)
            if cygwin:
                interpreter[0] = cygwin
            else:
                interpreter[0] = binary_list[0]
        interpreter.append(script)
        return interpreter
    else:
        with open(script, 'rb') as (f):
            signature = f.read(128)
        signature = signature.strip()
        if signature and signature[:1] == '#!':
            signature = signature[1:].split('\n', 1)[0]
            signature = signature.strip()
            args = shlex.split(signature)
            if args:
                if is_executable(args[0]):
                    args.append(script)
                    return args
                for ext, interpreter in DEFAULT_INTERPRETER.iteritems():
                    regex = interpreter[0]
                    regex = ('').join((c if c.isalnum() else '\\' + c) for c in regex)
                    regex = '\\b%s\\b' % regex
                    if re.search(regex, args[0]):
                        return interpreter + [script]

                for ext, interpreter in DEFAULT_INTERPRETER.iteritems():
                    regex = interpreter[0]
                    if regex.isalpha():
                        regex = '\\b%s[0-9\\.]*\\b' % regex
                        if re.search(regex, args[0]):
                            return interpreter + [script]

        raise IOError('Interpreter not found for script: %s' % script)
        return


def find_binary_in_path(binary):
    """
    Find the given binary in the current environment PATH.

    :note:
        The location of the bundled tools is always prepended to the PATH,
        independently of the actual value of the environment variable.
        This means bundled tools will always be picked before system tools.

    :param path: Path to the binary.
    :type path: str

    :returns: List of full paths to the binary.
        If not found, the list will be empty.
    :rtype: list(str)
    """
    binary = os.path.split(binary)[1]
    tools_folder = get_tools_folder()
    locations = [ os.path.join(tools_folder, x) for x in os.listdir(tools_folder) ]
    locations.extend(os.path.abspath(x) for x in os.environ.get('PATH', '').split(os.path.pathsep))
    locations = [ x for x in locations if os.path.isdir(x) ]
    if sys.platform in ('win32', 'cygwin'):
        comspec = os.environ.get('ComSpec', 'C:\\Windows\\System32\\cmd.exe')
        comspec = os.path.split(comspec)[0]
        system_root = os.environ.get('SystemRoot', 'C:\\Windows')
        system_32 = os.path.join(system_root, 'System32')
        system_64 = os.path.join(system_root, 'SysWOW64')
        if comspec not in locations:
            locations.append(comspec)
        if system_root not in locations:
            locations.append(system_root)
        if system_32 not in locations:
            locations.append(system_32)
        if system_64 not in locations:
            locations.append(system_64)
    found = []
    for candidate in locations:
        if candidate:
            candidate = os.path.join(candidate, binary)
            if os.path.exists(candidate):
                found.append(candidate)

    if sys.platform in ('win32', 'cygwin'):
        if os.path.splitext(binary)[1] == '':
            binary += '.exe'
            for candidate in locations:
                if candidate:
                    candidate = os.path.join(candidate, binary)
                    if os.path.exists(candidate):
                        found.append(candidate)

        upper = [ x.upper() for x in found ]
        found = [ x for i, x in enumerate(found) if x.upper() not in upper[:i] ]
    elif os.path.splitext(binary)[1] != '':
        binary = os.path.splitext(binary)[0]
        for candidate in locations:
            if candidate:
                candidate = os.path.join(candidate, binary)
                if os.path.exists(candidate):
                    found.append(candidate)

    return found


def is_cygwin_binary(path):
    """
    Detects if the given binary is located in the Cygwin /bin directory.

    :param path: Windows path to the binary.
    :type path: str

    :returns: True if the binary belongs to Cygwin, False for native binaries.
    :rtype: bool
    """
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        path = os.path.split(path)[0]
    path = os.path.join(path, 'cygwin1.dll')
    return os.path.exists(path)


def get_cygwin_binary(binary_list):
    """
    Take the list of binaries returned by find_binary_in_path() and grab the
    one that belongs to Cygwin.

    This is useful for commands or scripts that work different/better on Cygwin
    than the native version (for example the "find" command).

    :param binary_list: List of paths to the binaries to test.
    :type binary_list: str(list)

    :returns: Path to the Cygwin binary, or None if not found.
    :type: str | None
    """
    for binary in binary_list:
        if is_cygwin_binary(binary):
            return binary


def find_cygwin_binary_in_path(binary):
    """
    Find the given binary in the current environment PATH,
    but only if it's the Cygwin version.

    This is useful for commands or scripts that work different/better on Cygwin
    than the native version (for example the "find" command).

    :param path: Path to the binary.
    :type path: str

    :returns: Path to the Cygwin binary, or None if not found.
    :type: str | None
    """
    return get_cygwin_binary(find_binary_in_path(binary))


def win_to_cygwin_path(path):
    """
    Converts a Windows path to a Cygwin path.

    :param path: Windows path to convert.
        Must be an absolute path.
    :type path: str

    :returns: Cygwin path.
    :rtype: str

    :raises ValueError: Cannot convert the path.
    """
    drive, path = ntpath.splitdrive(path)
    if not drive:
        raise ValueError('Not an absolute path!')
    t = {'\\': '/', '/': '\\/'}
    path = ('').join(t.get(c, c) for c in path)
    return '/cygdrive/%s%s' % (drive[0].lower(), path)


def cygwin_to_win_path(path):
    """
    Converts a Cygwin path to a Windows path.
    Only paths starting with "/cygdrive/" can be converted.

    :param path: Cygwin path to convert.
        Must be an absolute path.
    :type path: str

    :returns: Windows path.
    :rtype: str

    :raises ValueError: Cannot convert the path.
    """
    if not path.startswith('/cygdrive/'):
        raise ValueError('Only paths starting with "/cygdrive/" can be converted.')
    drive = path[10].upper()
    path = path[11:]
    i = 0
    r = []
    while i < len(path):
        c = path[i]
        if c == '\\':
            r.append(path[i + 1:i + 2])
            i += 2
            continue
        if c == '/':
            c = '\\'
        r.append(c)
        i += 1

    path = ('').join(r)
    return '%s:%s' % (drive, path)


@contextlib.contextmanager
def tempfile(*args, **kwargs):
    r"""
    Context manager that creates a temporary file.
    The file is deleted when leaving the context.

    Example:
        >>> with tempfile(prefix="tmp", suffix=".bat") as filename:
        ...     with open(filename, "w") as fd:
        ...         fd.write("@echo off\necho Hello World!\n")
        ...     print run_external_tool("cmd.exe", ["/C", filename])
        ...
        ('Hello World!', 0)

    The arguments are exactly the same used by the standard NamedTemporaryFile
    class (from the tempfile module).
    """
    if sys.platform in ('win32', 'cygwin'):
        kwargs['delete'] = False
        output_file = NamedTemporaryFile(*args, **kwargs)
        output = output_file.name
        output_file.close()
        yield output
        os.unlink(output_file.name)
    else:
        with NamedTemporaryFile(suffix='.xml') as (output_file):
            yield output_file.name


@contextlib.contextmanager
def tempdir():
    """
    Context manager that creates a temporary directory.
    The directory is deleted when leaving the context.

    Example:
        >>> with tempdir() as directory:
        ...     print run_external_tool("cmd.exe", ["dir", directory])
        ...
    """
    output_dir = mkdtemp()
    yield output_dir
    if os.path.isdir(output_dir):
        try:
            rmtree(output_dir)
        except Exception:
            pass