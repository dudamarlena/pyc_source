# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/util.py
# Compiled at: 2020-05-07 05:52:35
"""
This module contains some useful functions for Strings, XML or Lists.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import collections, datetime, errno, fnmatch, glob, logging, os, shutil, signal, stat, subprocess, sys, time
from ctypes.util import find_library
import ctypes
from xml.etree import ElementTree
try:
    from shlex import quote as escape_string_shell
except ImportError:
    from pipes import quote as escape_string_shell

try:
    read_monotonic_time = time.monotonic
except AttributeError:
    read_monotonic_time = time.time

try:
    glob.iglob(b'/', recursive=True)
except TypeError:

    def maybe_recursive_iglob(pathname, recursive=False):
        """Workaround for glob.iglob not accepting parameter recursive on Python <= 3.4"""
        return glob.iglob(pathname)


else:
    maybe_recursive_iglob = glob.iglob

_BYTE_FACTOR = 1000

def printOut(value, end=b'\n'):
    """
    This function prints the given String immediately and flushes the output.
    """
    sys.stdout.write(value)
    sys.stdout.write(end)
    sys.stdout.flush()


def is_code(filename):
    """
    This function returns True, if  a line of the file contains bracket '{'.
    """
    with open(filename, b'r') as (file):
        for line in file:
            if not is_comment(line) and b'{' in line:
                if b'${' not in line:
                    return True

    return False


def is_comment(line):
    return not line or line.startswith(b'#') or line.startswith(b'//')


def remove_all(list_, elemToRemove):
    return [ elem for elem in list_ if elem != elemToRemove ]


def flatten(iterable, exclude=[]):
    return [ value for sublist in iterable for value in sublist if value not in exclude ]


def get_list_from_xml(elem, tag=b'option', attributes=[b'name']):
    """
    This function searches for all "option"-tags and returns a list with all attributes and texts.
    """
    return flatten(([ option.get(attr) for attr in attributes ] + [option.text] for option in elem.findall(tag)), exclude=[
     None])


def get_single_child_from_xml(elem, tag):
    """
    Get a single child tag from an XML element.
    Similar to "elem.find(tag)", but warns if there are multiple child tags with the given name.
    """
    children = elem.findall(tag)
    if not children:
        return None
    else:
        if len(children) > 1:
            logging.warning(b'Tag "%s" has more than one child tags with name "%s" in input file, ignoring all but the first.', elem.tag, tag)
        return children[0]


def text_or_none(elem):
    """
    Retrieve the text content of an XML tag, or None if the element itself is None
    """
    if elem is not None:
        return elem.text
    else:
        return


def copy_of_xml_element(elem):
    """
    This method returns a shallow copy of a XML-Element.
    This method is for compatibility with Python 2.6 or earlier..
    In Python 2.7 you can use  'copyElem = elem.copy()'  instead.
    """
    copyElem = ElementTree.Element(elem.tag, elem.attrib)
    for child in elem:
        copyElem.append(child)

    return copyElem


def decode_to_string(toDecode):
    """
    This function is needed for Python 3,
    because a subprocess can return bytes instead of a string.
    """
    try:
        return toDecode.decode(b'utf-8')
    except AttributeError:
        return toDecode


def format_number(number, number_of_digits):
    """
    The function format_number() return a string-representation of a number
    with a number of digits after the decimal separator.
    If the number has more digits, it is rounded.
    If the number has less digits, zeros are added.

    @param number: the number to format
    @param digits: the number of digits
    """
    if number is None:
        return b''
    else:
        return (b'%.{0}f').format(number_of_digits) % number


def parse_int_list(s):
    """
    Parse a comma-separated list of strings.
    The list may additionally contain ranges such as "1-5",
    which will be expanded into "1,2,3,4,5".
    """
    result = []
    for item in s.split(b','):
        item = item.strip().split(b'-')
        if len(item) == 1:
            result.append(int(item[0]))
        elif len(item) == 2:
            start, end = item
            result.extend(range(int(start), int(end) + 1))
        else:
            raise ValueError((b"invalid range: '{0}'").format(s))

    return result


def split_number_and_unit(s):
    """Parse a string that consists of a integer number and an optional unit.
    @param s a non-empty string that starts with an int and is followed by some letters
    @return a triple of the number (as int) and the unit
    """
    if not s:
        raise ValueError(b'empty value')
    s = s.strip()
    pos = len(s)
    while pos and not s[(pos - 1)].isdigit():
        pos -= 1

    number = int(s[:pos])
    unit = s[pos:].strip()
    return (number, unit)


def parse_memory_value(s):
    """Parse a string that contains a number of bytes, optionally with a unit like MB.
    @return the number of bytes encoded by the string
    """
    number, unit = split_number_and_unit(s)
    if not unit or unit == b'B':
        return number
    if unit == b'kB':
        return number * _BYTE_FACTOR
    if unit == b'MB':
        return number * _BYTE_FACTOR * _BYTE_FACTOR
    if unit == b'GB':
        return number * _BYTE_FACTOR * _BYTE_FACTOR * _BYTE_FACTOR
    if unit == b'TB':
        return number * _BYTE_FACTOR * _BYTE_FACTOR * _BYTE_FACTOR * _BYTE_FACTOR
    raise ValueError((b'unknown unit: {} (allowed are B, kB, MB, GB, and TB)').format(unit))


def parse_timespan_value(s):
    """Parse a string that contains a time span, optionally with a unit like s.
    @return the number of seconds encoded by the string
    """
    number, unit = split_number_and_unit(s)
    if not unit or unit == b's':
        return number
    if unit == b'min':
        return number * 60
    if unit == b'h':
        return number * 60 * 60
    if unit == b'd':
        return number * 24 * 60 * 60
    raise ValueError((b'unknown unit: {} (allowed are s, min, h, and d)').format(unit))


def expand_filename_pattern(pattern, base_dir):
    """
    Expand a file name pattern containing wildcards, environment variables etc.

    @param pattern: The pattern string to expand.
    @param base_dir: The directory where relative paths are based on.
    @return: A list of file names (possibly empty).
    """
    pattern = os.path.normpath(os.path.join(base_dir, pattern))
    pattern = os.path.expandvars(os.path.expanduser(pattern))
    fileList = glob.glob(pattern)
    return fileList


def get_files(paths):
    changed = False
    result = []
    for path in paths:
        if os.path.isfile(path):
            result.append(path)
        elif os.path.isdir(path):
            changed = True
            for currentPath, dirs, files in os.walk(path):
                files = [ f for f in files if not f.startswith(b'.') ]
                dirs[:] = [ d for d in dirs if not d.startswith(b'.') ]
                result.extend(os.path.join(currentPath, f) for f in files)

    if changed:
        return result
    return paths


def substitute_vars(template, replacements):
    """Replace certain keys with respective values in a string.
    @param template: the string in which replacements should be made
    @param replacements: a dict or a list of pairs of keys and values
    """
    result = template
    for key, value in replacements:
        result = result.replace(b'${' + key + b'}', value)

    if b'${' in result:
        logging.warning(b"A variable was not replaced in '%s'.", result)
    return result


def find_executable(program, fallback=None, exitOnError=True, use_current_dir=True):
    dirs = os.environ[b'PATH'].split(os.path.pathsep)
    if use_current_dir:
        dirs.append(os.path.curdir)
    found_non_executable = []
    for dir_ in dirs:
        name = os.path.join(dir_, program)
        if os.path.isfile(name):
            if os.access(name, os.X_OK):
                return name
            found_non_executable.append(name)

    if fallback is not None and os.path.isfile(fallback):
        if os.access(fallback, os.X_OK):
            return fallback
        found_non_executable.append(name)
    if exitOnError:
        if found_non_executable:
            sys.exit((b"ERROR: Could not find '{0}' executable, but found file '{1}' that is not executable.").format(program, found_non_executable[0]))
        else:
            sys.exit((b"ERROR: Could not find '{0}' executable.").format(program))
    else:
        return fallback
    return


def common_base_dir(l):
    return os.path.dirname(os.path.commonprefix(l))


def relative_path(destination, start):
    return os.path.relpath(destination, os.path.dirname(start))


def path_is_below(path, target_path):
    """
    Check whether path is below target_path.
    Works for bytes and strings, but both arguments need to have same type.
    """
    empty_path = path[:0]
    path = os.path.join(path, empty_path)
    target_path = os.path.join(target_path, empty_path)
    return path.startswith(target_path)


def log_rmtree_error(func, arg, exc_info):
    """Suited as onerror handler for (sh)util.rmtree() that logs a warning."""
    logging.warning(b"Failure during '%s(%s)': %s", func.__name__, arg, exc_info[1])


def makedirs(name, exist_ok=False):
    """create a leaf directory and all intermediate ones Works like os.mkdirs, except
    that no OSError is raised in case the target directory already exists and exist_ok
    is set to True.
    """
    try:
        os.makedirs(name)
    except OSError:
        if not exist_ok or not os.path.isdir(name):
            raise


def rmtree(path, ignore_errors=False, onerror=None):
    """Same as shutil.rmtree, but supports directories without write or execute permissions."""
    if ignore_errors:

        def onerror(*args):
            pass

    else:
        if onerror is None:

            def onerror(*args):
                raise

        for root, dirs, unused_files in os.walk(path):
            for directory in dirs:
                try:
                    abs_directory = os.path.join(root, directory)
                    os.chmod(abs_directory, stat.S_IRWXU)
                except EnvironmentError as e:
                    onerror(os.chmod, abs_directory, e)

    shutil.rmtree(path, ignore_errors=ignore_errors, onerror=onerror)
    return


def copy_all_lines_from_to(inputFile, outputFile):
    """Copy all lines from an input file object to an output file object."""
    currentLine = inputFile.readline()
    while currentLine:
        outputFile.write(currentLine)
        currentLine = inputFile.readline()


def write_file(content, *path):
    """
    Simply write some content to a file, overriding the file if necessary.
    """
    with open(os.path.join(*path), b'w') as (file):
        return file.write(content)


def shrink_text_file(filename, max_size, removal_marker=None):
    """Shrink a text file to approximately maxSize bytes
    by removing lines from the middle of the file.
    """
    file_size = os.path.getsize(filename)
    assert file_size > max_size
    with open(filename, b'r+b') as (output_file):
        with open(filename, b'rb') as (input_file):
            output_file.seek(max_size // 2)
            output_file.readline()
            if output_file.tell() == file_size:
                return
            if removal_marker:
                output_file.write(removal_marker.encode())
            input_file.seek(-max_size // 2, os.SEEK_END)
            input_file.readline()
            copy_all_lines_from_to(input_file, output_file)
            output_file.truncate()


def read_file(*path):
    """
    Read the full content of a file.
    """
    with open(os.path.join(*path)) as (f):
        return f.read().strip()


def try_read_file(*path):
    """Read the full content of a file if possible, return None otherwise."""
    try:
        return read_file(*path).strip()
    except OSError:
        return

    return


def read_key_value_pairs_from_file(*path):
    """
    Read key value pairs from a file (each pair on a separate line).
    Key and value are separated by ' ' as often used by the kernel.
    @return a generator of tuples
    """
    with open(os.path.join(*path)) as (f):
        for line in f:
            yield line.split(b' ', 1)


class ProcessExitCode(collections.namedtuple(b'ProcessExitCode', b'raw value signal')):
    """Tuple for storing the exit status indication given by a os.wait() call.
    Only value or signal are present, not both
    (a process cannot return a value when it is killed by a signal).
    """

    @classmethod
    def from_raw(cls, exitcode):
        if not 0 <= exitcode < 65536:
            raise ValueError(b'invalid exitcode ' + str(exitcode))
        exitsignal = exitcode & 127
        returnvalue = exitcode >> 8
        if exitsignal == 0:
            exitsignal = None
        else:
            assert returnvalue == 0, (b'returnvalue {}, although exitsignal is {}').format(returnvalue, exitsignal)
            returnvalue = None
        return cls(exitcode, returnvalue, exitsignal)

    @classmethod
    def create(cls, value=None, signal=None):
        """
        Create an instance of either a return value or an exit signal.
        The other parameter must be None.
        """
        if value is None and signal is None:
            raise ValueError(b'Need return value or exit signal for ProcessExitCode')
        if value is not None and signal is not None:
            raise ValueError(b'Cannot create ProcessExitCode with both value and signal')
        if value is not None and not 0 <= value <= 255:
            raise ValueError((b'Invalid value {} for return value').format(value))
        if signal is not None and not 1 <= signal <= 127:
            raise ValueError((b'Invalid value {} for exit signal').format(value))
        exitcode = (value or 0) * 256 + (signal or 0)
        return cls(exitcode, value, signal)

    def __str__(self):
        if self.signal:
            return b'exit signal ' + str(self.signal)
        return b'return value ' + str(self.value)

    def __bool__(self):
        return bool(self.signal or self.value)

    def __nonzero__(self):
        return self.__bool__()


def kill_process(pid, sig=None):
    """Try to send signal to given process."""
    if sig is None:
        sig = signal.SIGKILL
    try:
        os.kill(pid, sig)
    except OSError as e:
        if e.errno == errno.ESRCH:
            logging.debug(b'Failure %s while killing process %s with signal %s: %s', e.errno, pid, sig, e.strerror)
        else:
            logging.warning(b'Failure %s while killing process %s with signal %s: %s', e.errno, pid, sig, e.strerror)

    return


def dummy_fn(*args, **kwargs):
    """Dummy function that accepts all parameters but does nothing."""
    pass


def add_files_to_git_repository(base_dir, files, description):
    """
    Add and commit all files given in a list into a git repository in the
    base_dir directory. Nothing is done if the git repository has
    local changes.

    @param files: the files to commit
    @param description: the commit message
    """
    if not os.path.isdir(base_dir):
        printOut(b'Output path is not a directory, cannot add files to git repository.')
        return
    gitRoot = subprocess.Popen([
     b'git', b'rev-parse', b'--show-toplevel'], cwd=base_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = gitRoot.communicate()[0]
    if gitRoot.returncode != 0:
        printOut(b'Cannot commit results to repository: git rev-parse failed, perhaps output path is not a git directory?')
        return
    gitRootDir = decode_to_string(stdout).splitlines()[0]
    gitStatus = subprocess.Popen([
     b'git', b'status', b'--porcelain', b'--untracked-files=no'], cwd=gitRootDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = gitStatus.communicate()
    if gitStatus.returncode != 0:
        printOut(b'Git status failed! Output was:\n' + decode_to_string(stderr))
        return
    if stdout:
        printOut(b'Git repository has local changes, not commiting results.')
        return
    files = [ os.path.realpath(file) for file in files ]
    gitAdd = subprocess.Popen([b'git', b'add', b'--force', b'--'] + files, cwd=gitRootDir)
    if gitAdd.wait() != 0:
        printOut(b'Git add failed, will not commit results!')
        return
    printOut(b'Committing results files to git repository in ' + gitRootDir)
    gitCommit = subprocess.Popen([
     b'git', b'commit', b'--file=-', b'--quiet'], cwd=gitRootDir, stdin=subprocess.PIPE)
    gitCommit.communicate(description.encode(b'UTF-8'))
    if gitCommit.returncode != 0:
        printOut(b'Git commit failed!')
        return


def wildcard_match(word, wildcard):
    return word and fnmatch.fnmatch(word, wildcard)


def read_local_time():
    """Get "aware" datetime.datetime instance with local time (including time zone)."""
    return datetime.datetime.now(datetime.timezone.utc).astimezone()


def should_color_output():
    """Determine whether we want colored output to stdout."""
    return sys.stdout.isatty() and b'NO_COLOR' not in os.environ


def setup_logging(fmt=b'%(asctime)s - %(levelname)s - %(message)s', level=b'INFO'):
    """Setup the logging framework with a basic configuration"""
    if should_color_output():
        try:
            import coloredlogs
            coloredlogs.install(fmt=fmt, level=level)
            return
        except ImportError:
            pass

    logging.basicConfig(format=fmt, level=level)


def _debug_current_process(sig, current_frame):
    """Interrupt running process, and provide a python prompt for interactive debugging.
    This code is based on http://stackoverflow.com/a/133384/396730
    """
    import code, traceback, readline, threading
    d = {b'_frame': current_frame}
    d.update(current_frame.f_globals)
    d.update(current_frame.f_locals)
    i = code.InteractiveConsole(d)
    message = b'Signal received : entering python shell.\n'
    threads = {thread.ident:thread for thread in threading.enumerate()}
    current_thread = threading.current_thread()
    for thread_id, frame in sys._current_frames().items():
        if current_thread.ident != thread_id:
            message += (b'\nTraceback of thread {}:\n').format(threads[thread_id])
            message += (b'').join(traceback.format_stack(frame))

    message += (b'\nTraceback of current thread {}:\n').format(current_thread)
    message += (b'').join(traceback.format_stack(current_frame))
    i.interact(message)


def activate_debug_shell_on_signal():
    """Install a signal handler for USR1 that dumps stack traces
    and gives an interactive debugging shell.
    """
    signal.signal(signal.SIGUSR1, _debug_current_process)


def get_capability(filename):
    """
        Get names of capabilities and the corresponding capability set for given filename.

            @filename: The complete path to the file
    """
    res = {b'capabilities': [], b'set': [], b'error': False}
    try:
        libcap_path = find_library(b'cap')
        libcap = ctypes.cdll.LoadLibrary(libcap_path)
    except OSError:
        res[b'error'] = True
        logging.warning((b'Unable to find capabilities for {0}').format(filename))
        return res

    cap_t = libcap.cap_get_file(ctypes.create_string_buffer(filename.encode(b'utf-8')))
    libcap.cap_to_text.restype = ctypes.c_char_p
    cap_object = libcap.cap_to_text(cap_t, None)
    libcap.cap_free(cap_t)
    if cap_object is not None:
        cap_string = cap_object.decode(b'utf-8')
        res[b'capabilities'] = cap_string.split(b'+')[0][2:].split(b',')
        res[b'set'] = list(cap_string.split(b'+')[1])
    return res


def check_msr():
    """
        Checks if the msr driver is loaded and if the user executing
        benchexec has the read and write permissions for msr.
    """
    res = {b'loaded': False, b'write': False, b'read': False}
    loaded_modules = subprocess.check_output([b'lsmod']).decode(b'utf-8').split(b'\n')
    if any(b'msr' in module for module in loaded_modules):
        res[b'loaded'] = True
    if res[b'loaded']:
        cpu_dirs = os.listdir(b'/dev/cpu')
        cpu_dirs.remove(b'microcode')
        if all(os.access((b'/dev/cpu/{}/msr').format(cpu), os.R_OK) for cpu in cpu_dirs):
            res[b'read'] = True
        if all(os.access((b'/dev/cpu/{}/msr').format(cpu), os.W_OK) for cpu in cpu_dirs):
            res[b'write'] = True
    return res