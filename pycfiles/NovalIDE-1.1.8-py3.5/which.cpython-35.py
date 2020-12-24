# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/which.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 14082 bytes
r"""Find the full path to commands.

which(command, path=None, verbose=0, exts=None)
    Return the full path to the first match of the given command on the
    path.

whichall(command, path=None, verbose=0, exts=None)
    Return a list of full paths to all matches of the given command on
    the path.

whichgen(command, path=None, verbose=0, exts=None)
    Return a generator which will yield full paths to all matches of the
    given command on the path.
    
By default the PATH environment variable is searched (as well as, on
Windows, the AppPaths key in the registry), but a specific 'path' list
to search may be specified as well.  On Windows, the PATHEXT environment
variable is applied as appropriate.

If "verbose" is true then a tuple of the form
    (<fullpath>, <matched-where-description>)
is returned for each match. The latter element is a textual description
of where the match was found. For example:
    from PATH element 0
    from HKLM\SOFTWARE\...\perl.exe
"""
_cmdlnUsage = "\n    Show the full path of commands.\n\n    Usage:\n        which [<options>...] [<command-name>...]\n\n    Options:\n        -h, --help      Print this help and exit.\n        -V, --version   Print the version info and exit.\n\n        -a, --all       Print *all* matching paths.\n        -v, --verbose   Print out how matches were located and\n                        show near misses on stderr.\n        -q, --quiet     Just print out matches. I.e., do not print out\n                        near misses.\n\n        -p <altpath>, --path=<altpath>\n                        An alternative path (list of directories) may\n                        be specified for searching.\n        -e <exts>, --exts=<exts>\n                        Specify a list of extensions to consider instead\n                        of the usual list (';'-separate list, Windows\n                        only).\n\n    Show the full path to the program that would be run for each given\n    command name, if any. Which, like GNU's which, returns the number of\n    failed arguments, or -1 when no <command-name> was given.\n\n    Near misses include duplicates, non-regular files and (on Un*x)\n    files without executable access.\n"
__revision__ = '$Id$'
__version_info__ = (1, 1, 3)
__version__ = '.'.join(map(str, __version_info__))
__all__ = ['which', 'whichall', 'whichgen', 'WhichError']
import os, sys, getopt, stat, time

class WhichError(Exception):
    pass


def _getRegisteredExecutable(exeName):
    """Windows allow application paths to be registered in the registry."""
    registered = None
    if sys.platform.startswith('win'):
        if os.path.splitext(exeName)[1].lower() != '.exe':
            exeName += '.exe'
        try:
            import _winreg
        except:
            import winreg as _winreg

        try:
            key = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\' + exeName
            value = _winreg.QueryValue(_winreg.HKEY_LOCAL_MACHINE, key)
            registered = (value, 'from HKLM\\' + key)
        except _winreg.error:
            pass

        if registered and not os.path.exists(registered[0]):
            registered = None
    return registered


def _samefile(fname1, fname2):
    if sys.platform.startswith('win'):
        return os.path.normpath(os.path.normcase(fname1)) == os.path.normpath(os.path.normcase(fname2))
    else:
        return os.path.samefile(fname1, fname2)


def _cull(potential, matches, verbose=0):
    """Cull inappropriate matches. Possible reasons:
        - a duplicate of a previous match
        - not a disk file
        - not executable (non-Windows)
    If 'potential' is approved it is returned and added to 'matches'.
    Otherwise, None is returned.
    """
    for match in matches:
        if _samefile(potential[0], match[0]):
            if verbose:
                sys.stderr.write('duplicate: %s (%s)\n' % potential)
            return
    else:
        is_darwin_app = sys.platform == 'darwin' and potential[0].endswith('.app')
        if not is_darwin_app and not stat.S_ISREG(os.stat(potential[0]).st_mode):
            if verbose:
                sys.stderr.write('not a regular file: %s (%s)\n' % potential)
        else:
            if not is_darwin_app and sys.platform != 'win32' and not os.access(potential[0], os.X_OK):
                if verbose:
                    sys.stderr.write('no executable access: %s (%s)\n' % potential)
            else:
                matches.append(potential)
                return potential


g_listdir_cache = {}

def whichgen(command, path=None, verbose=0, exts=None):
    """Return a generator of full paths to the given command.
    
    "command" is a the name of the executable to search for.
    "path" is an optional alternate path list to search. The default it
        to use the PATH environment variable.
    "verbose", if true, will cause a 2-tuple to be returned for each
        match. The second element is a textual description of where the
        match was found.
    "exts" optionally allows one to specify a list of extensions to use
        instead of the standard list for this system. This can
        effectively be used as an optimization to, for example, avoid
        stat's of "foo.vbs" when searching for "foo" and you know it is
        not a VisualBasic script but ".vbs" is on PATHEXT. This option
        is only supported on Windows.

    This method returns a generator which yields either full paths to
    the given command or, if verbose, tuples of the form (<path to
    command>, <where path found>).
    """
    matches = []
    if path is None:
        usingGivenPath = 0
        path = os.environ.get('PATH', '').split(os.pathsep)
        if sys.platform.startswith('win'):
            path.insert(0, os.curdir)
        if sys.platform == 'darwin':
            path.insert(0, '/Network/Applications')
            path.insert(0, '/Applications')
    else:
        usingGivenPath = 1
    if sys.platform.startswith('win'):
        if exts is None:
            exts = os.environ.get('PATHEXT', '').split(os.pathsep)
            for ext in exts:
                if ext.lower() == '.exe':
                    break
            else:
                exts = [
                 '.com', '.exe', '.bat', '.cmd']

        elif not isinstance(exts, list):
            raise TypeError("'exts' argument must be a list or None")
        exts = list(map(os.path.normcase, exts))
    else:
        if sys.platform == 'darwin':
            if exts is None:
                exts = [
                 '.app']
        else:
            if exts is not None:
                raise WhichError("'exts' argument is not supported on platform '%s'" % sys.platform)
            exts = []
        if os.sep in command or os.altsep and os.altsep in command:
            if os.path.exists(command):
                match = _cull((command, 'explicit path given'), matches, verbose)
                if verbose:
                    yield match
                else:
                    yield match[0]
        else:
            time_now = time.time()
            for i in range(len(path)):
                dirName = path[i]
                if sys.platform.startswith('win') and len(dirName) >= 2 and dirName[0] == '"' and dirName[(-1)] == '"':
                    dirName = dirName[1:-1]
                entry = g_listdir_cache.get(dirName)
                if entry is None or time_now - entry.get('timestamp', 0) > 5:
                    try:
                        names = os.listdir(dirName)
                    except OSError:
                        names = []

                    names = map(os.path.normcase, names)
                    g_listdir_cache[dirName] = {'timestamp': time_now, 'names': names}
                else:
                    names = g_listdir_cache.get(dirName).get('names')
                for ext in [''] + exts:
                    name = command + ext
                    if name not in names:
                        pass
                    else:
                        absName = os.path.abspath(os.path.normpath(os.path.join(dirName, command + ext)))
                        if os.path.isfile(absName) or sys.platform == 'darwin' and absName.endswith('.app') and os.path.isdir(absName):
                            if usingGivenPath:
                                fromWhere = 'from given path element %d' % i
                            else:
                                if not sys.platform.startswith('win'):
                                    fromWhere = 'from PATH element %d' % i
                                else:
                                    if i == 0:
                                        fromWhere = 'from current directory'
                                    else:
                                        fromWhere = 'from PATH element %d' % (i - 1)
                                    match = _cull((absName, fromWhere), matches, verbose)
                                    if match:
                                        if verbose:
                                            yield match
                                        else:
                                            yield match[0]

            match = _getRegisteredExecutable(command)
            if match is not None:
                pass
            match = _cull(match, matches, verbose)
            if match:
                if verbose:
                    yield match
            else:
                yield match[0]


def which(command, path=None, verbose=0, exts=None):
    """Return the full path to the first match of the given command on
    the path.
    
    "command" is a the name of the executable to search for.
    "path" is an optional alternate path list to search. The default it
        to use the PATH environment variable.
    "verbose", if true, will cause a 2-tuple to be returned. The second
        element is a textual description of where the match was found.
    "exts" optionally allows one to specify a list of extensions to use
        instead of the standard list for this system. This can
        effectively be used as an optimization to, for example, avoid
        stat's of "foo.vbs" when searching for "foo" and you know it is
        not a VisualBasic script but ".vbs" is on PATHEXT. This option
        is only supported on Windows.

    If no match is found for the command, a WhichError is raised.
    """
    try:
        match = whichgen(command, path, verbose, exts).next()
    except StopIteration:
        return

    return match


def whichall(command, path=None, verbose=0, exts=None):
    """Return a list of full paths to all matches of the given command
    on the path.  

    "command" is a the name of the executable to search for.
    "path" is an optional alternate path list to search. The default it
        to use the PATH environment variable.
    "verbose", if true, will cause a 2-tuple to be returned for each
        match. The second element is a textual description of where the
        match was found.
    "exts" optionally allows one to specify a list of extensions to use
        instead of the standard list for this system. This can
        effectively be used as an optimization to, for example, avoid
        stat's of "foo.vbs" when searching for "foo" and you know it is
        not a VisualBasic script but ".vbs" is on PATHEXT. This option
        is only supported on Windows.
    """
    return list(whichgen(command, path, verbose, exts))


def main(argv):
    all = 0
    verbose = 0
    altpath = None
    exts = None
    try:
        optlist, args = getopt.getopt(argv[1:], 'haVvqp:e:', [
         'help', 'all', 'version', 'verbose', 'quiet', 'path=', 'exts='])
    except getopt.GetoptError as msg:
        sys.stderr.write('which: error: %s. Your invocation was: %s\n' % (
         msg, argv))
        sys.stderr.write("Try 'which --help'.\n")
        return 1

    for opt, optarg in optlist:
        if opt in ('-h', '--help'):
            print(_cmdlnUsage)
            return 0
        if opt in ('-V', '--version'):
            print('which %s' % __version__)
            return 0
        if opt in ('-a', '--all'):
            all = 1
        elif opt in ('-v', '--verbose'):
            verbose = 1
        else:
            if opt in ('-q', '--quiet'):
                verbose = 0
            else:
                if opt in ('-p', '--path'):
                    if optarg:
                        altpath = optarg.split(os.pathsep)
                    else:
                        altpath = []
                elif opt in ('-e', '--exts'):
                    if optarg:
                        exts = optarg.split(os.pathsep)
                    else:
                        exts = []

    if len(args) == 0:
        return -1
    failures = 0
    for arg in args:
        nmatches = 0
        for match in whichgen(arg, path=altpath, verbose=verbose, exts=exts):
            if verbose:
                print('%s (%s)' % match)
            else:
                print(match)
            nmatches += 1
            if not all:
                break

        if not nmatches:
            failures += 1

    return failures


def GuessPath(executable_name):
    matchs = []
    for match in whichgen(executable_name):
        matchs.append(match)

    if 0 == len(matchs):
        return executable_name
    return matchs[0]


if __name__ == '__main__':
    sys.exit(main(sys.argv))