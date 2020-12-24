# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Util.py
# Compiled at: 2016-07-07 03:21:31
"""SCons.Util

Various utility functions go here.
"""
__revision__ = 'src/engine/SCons/Util.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os, sys, copy, re, types
from collections import UserDict, UserList, UserString
InstanceType = types.InstanceType
MethodType = types.MethodType
FunctionType = types.FunctionType
try:
    unicode
except NameError:
    UnicodeType = None
else:
    UnicodeType = unicode

def dictify(keys, values, result={}):
    for k, v in zip(keys, values):
        result[k] = v

    return result


_altsep = os.altsep
if _altsep is None and sys.platform == 'win32':
    _altsep = '/'
if _altsep:

    def rightmost_separator(path, sep):
        return max(path.rfind(sep), path.rfind(_altsep))


else:

    def rightmost_separator(path, sep):
        return path.rfind(sep)


def containsAny(str, set):
    """Check whether sequence str contains ANY of the items in set."""
    for c in set:
        if c in str:
            return 1

    return 0


def containsAll(str, set):
    """Check whether sequence str contains ALL of the items in set."""
    for c in set:
        if c not in str:
            return 0

    return 1


def containsOnly(str, set):
    """Check whether sequence str contains ONLY items in set."""
    for c in str:
        if c not in set:
            return 0

    return 1


def splitext(path):
    """Same as os.path.splitext() but faster."""
    sep = rightmost_separator(path, os.sep)
    dot = path.rfind('.')
    if dot > sep and not containsOnly(path[dot:], '0123456789.'):
        return (path[:dot], path[dot:])
    else:
        return (
         path, '')


def updrive(path):
    """
    Make the drive letter (if any) upper case.
    This is useful because Windows is inconsistent on the case
    of the drive letter, which can cause inconsistencies when
    calculating command signatures.
    """
    drive, rest = os.path.splitdrive(path)
    if drive:
        path = drive.upper() + rest
    return path


class NodeList(UserList):
    """This class is almost exactly like a regular list of Nodes
    (actually it can hold any object), with one important difference.
    If you try to get an attribute from this list, it will return that
    attribute from every item in the list.  For example:

    >>> someList = NodeList([ '  foo  ', '  bar  ' ])
    >>> someList.strip()
    [ 'foo', 'bar' ]
    """

    def __nonzero__(self):
        return len(self.data) != 0

    def __str__(self):
        return (' ').join(map(str, self.data))

    def __iter__(self):
        return iter(self.data)

    def __call__(self, *args, **kwargs):
        result = [ x(*args, **kwargs) for x in self.data ]
        return self.__class__(result)

    def __getattr__(self, name):
        result = [ getattr(x, name) for x in self.data ]
        return self.__class__(result)


_get_env_var = re.compile('^\\$([_a-zA-Z]\\w*|{[_a-zA-Z]\\w*})$')

def get_environment_var(varstr):
    """Given a string, first determine if it looks like a reference
    to a single environment variable, like "$FOO" or "${FOO}".
    If so, return that variable with no decorations ("FOO").
    If not, return None."""
    mo = _get_env_var.match(to_String(varstr))
    if mo:
        var = mo.group(1)
        if var[0] == '{':
            return var[1:-1]
        return var
    else:
        return
    return


class DisplayEngine(object):
    print_it = True

    def __call__(self, text, append_newline=1):
        if not self.print_it:
            return
        if append_newline:
            text = text + '\n'
        try:
            sys.stdout.write(unicode(text))
        except IOError:
            pass

    def set_mode(self, mode):
        self.print_it = mode


def render_tree(root, child_func, prune=0, margin=[0], visited=None):
    """
    Render a tree of nodes into an ASCII tree view.
    root - the root node of the tree
    child_func - the function called to get the children of a node
    prune - don't visit the same node twice
    margin - the format of the left margin to use for children of root.
       1 results in a pipe, and 0 results in no pipe.
    visited - a dictionary of visited nodes in the current branch if not prune,
       or in the whole tree if prune.
    """
    rname = str(root)
    if visited is None:
        visited = {}
    children = child_func(root)
    retval = ''
    for pipe in margin[:-1]:
        if pipe:
            retval = retval + '| '
        else:
            retval = retval + '  '

    if rname in visited:
        return retval + '+-[' + rname + ']\n'
    else:
        retval = retval + '+-' + rname + '\n'
        if not prune:
            visited = copy.copy(visited)
        visited[rname] = 1
        for i in range(len(children)):
            margin.append(i < len(children) - 1)
            retval = retval + render_tree(children[i], child_func, prune, margin, visited)
            margin.pop()

        return retval


IDX = lambda N: N and 1 or 0

def print_tree(root, child_func, prune=0, showtags=0, margin=[0], visited=None):
    """
    Print a tree of nodes.  This is like render_tree, except it prints
    lines directly instead of creating a string representation in memory,
    so that huge trees can be printed.

    root - the root node of the tree
    child_func - the function called to get the children of a node
    prune - don't visit the same node twice
    showtags - print status information to the left of each node line
    margin - the format of the left margin to use for children of root.
       1 results in a pipe, and 0 results in no pipe.
    visited - a dictionary of visited nodes in the current branch if not prune,
       or in the whole tree if prune.
    """
    rname = str(root)
    if visited is None:
        visited = {}
    if showtags:
        if showtags == 2:
            legend = ' E         = exists\n' + '  R        = exists in repository only\n' + '   b       = implicit builder\n' + '   B       = explicit builder\n' + '    S      = side effect\n' + '     P     = precious\n' + '      A    = always build\n' + '       C   = current\n' + '        N  = no clean\n' + '         H = no cache\n' + '\n'
            sys.stdout.write(unicode(legend))
        tags = ['[']
        tags.append(' E'[IDX(root.exists())])
        tags.append(' R'[IDX(root.rexists() and not root.exists())])
        tags.append(' BbB'[([0, 1][IDX(root.has_explicit_builder())] + [
         0, 2][IDX(root.has_builder())])])
        tags.append(' S'[IDX(root.side_effect)])
        tags.append(' P'[IDX(root.precious)])
        tags.append(' A'[IDX(root.always_build)])
        tags.append(' C'[IDX(root.is_up_to_date())])
        tags.append(' N'[IDX(root.noclean)])
        tags.append(' H'[IDX(root.nocache)])
        tags.append(']')
    else:
        tags = []

    def MMM(m):
        return [
         '  ', '| '][m]

    margins = list(map(MMM, margin[:-1]))
    children = child_func(root)
    if prune and rname in visited and children:
        sys.stdout.write(('').join(tags + margins + ['+-[', rname, ']']) + '\n')
        return
    else:
        sys.stdout.write(('').join(tags + margins + ['+-', rname]) + '\n')
        visited[rname] = 1
        if children:
            margin.append(1)
            idx = IDX(showtags)
            for C in children[:-1]:
                print_tree(C, child_func, prune, idx, margin, visited)

            margin[-1] = 0
            print_tree(children[(-1)], child_func, prune, idx, margin, visited)
            margin.pop()
        return


DictTypes = (
 dict, UserDict)
ListTypes = (list, UserList)
SequenceTypes = (list, tuple, UserList)
StringTypes = (
 str, unicode, UserString)
BaseStringTypes = (
 str, unicode)

def is_Dict(obj, isinstance=isinstance, DictTypes=DictTypes):
    return isinstance(obj, DictTypes)


def is_List(obj, isinstance=isinstance, ListTypes=ListTypes):
    return isinstance(obj, ListTypes)


def is_Sequence(obj, isinstance=isinstance, SequenceTypes=SequenceTypes):
    return isinstance(obj, SequenceTypes)


def is_Tuple(obj, isinstance=isinstance, tuple=tuple):
    return isinstance(obj, tuple)


def is_String(obj, isinstance=isinstance, StringTypes=StringTypes):
    return isinstance(obj, StringTypes)


def is_Scalar(obj, isinstance=isinstance, StringTypes=StringTypes, SequenceTypes=SequenceTypes):
    return isinstance(obj, StringTypes) or not isinstance(obj, SequenceTypes)


def do_flatten(sequence, result, isinstance=isinstance, StringTypes=StringTypes, SequenceTypes=SequenceTypes):
    for item in sequence:
        if isinstance(item, StringTypes) or not isinstance(item, SequenceTypes):
            result.append(item)
        else:
            do_flatten(item, result)


def flatten(obj, isinstance=isinstance, StringTypes=StringTypes, SequenceTypes=SequenceTypes, do_flatten=do_flatten):
    """Flatten a sequence to a non-nested list.

    Flatten() converts either a single scalar or a nested sequence
    to a non-nested list. Note that flatten() considers strings
    to be scalars instead of sequences like Python would.
    """
    if isinstance(obj, StringTypes) or not isinstance(obj, SequenceTypes):
        return [obj]
    result = []
    for item in obj:
        if isinstance(item, StringTypes) or not isinstance(item, SequenceTypes):
            result.append(item)
        else:
            do_flatten(item, result)

    return result


def flatten_sequence(sequence, isinstance=isinstance, StringTypes=StringTypes, SequenceTypes=SequenceTypes, do_flatten=do_flatten):
    """Flatten a sequence to a non-nested list.

    Same as flatten(), but it does not handle the single scalar
    case. This is slightly more efficient when one knows that
    the sequence to flatten can not be a scalar.
    """
    result = []
    for item in sequence:
        if isinstance(item, StringTypes) or not isinstance(item, SequenceTypes):
            result.append(item)
        else:
            do_flatten(item, result)

    return result


def to_String(s, isinstance=isinstance, str=str, UserString=UserString, BaseStringTypes=BaseStringTypes):
    if isinstance(s, BaseStringTypes):
        return s
    else:
        if isinstance(s, UserString):
            return s.data
        return str(s)


def to_String_for_subst(s, isinstance=isinstance, str=str, to_String=to_String, BaseStringTypes=BaseStringTypes, SequenceTypes=SequenceTypes, UserString=UserString):
    if isinstance(s, BaseStringTypes):
        return s
    else:
        if isinstance(s, SequenceTypes):
            l = []
            for e in s:
                l.append(to_String_for_subst(e))

            return (' ').join(s)
        if isinstance(s, UserString):
            return s.data
        return str(s)


def to_String_for_signature(obj, to_String_for_subst=to_String_for_subst, AttributeError=AttributeError):
    try:
        f = obj.for_signature
    except AttributeError:
        return to_String_for_subst(obj)

    return f()


_semi_deepcopy_dispatch = d = {}

def semi_deepcopy_dict(x, exclude=[]):
    copy = {}
    for key, val in x.items():
        if key not in exclude:
            copy[key] = semi_deepcopy(val)

    return copy


d[dict] = semi_deepcopy_dict

def _semi_deepcopy_list(x):
    return list(map(semi_deepcopy, x))


d[list] = _semi_deepcopy_list

def _semi_deepcopy_tuple(x):
    return tuple(map(semi_deepcopy, x))


d[tuple] = _semi_deepcopy_tuple

def semi_deepcopy(x):
    copier = _semi_deepcopy_dispatch.get(type(x))
    if copier:
        return copier(x)
    else:
        if hasattr(x, '__semi_deepcopy__') and callable(x.__semi_deepcopy__):
            return x.__semi_deepcopy__()
        if isinstance(x, UserDict):
            return x.__class__(semi_deepcopy_dict(x))
        if isinstance(x, UserList):
            return x.__class__(_semi_deepcopy_list(x))
        return x


class Proxy(object):
    """A simple generic Proxy class, forwarding all calls to
    subject.  So, for the benefit of the python newbie, what does
    this really mean?  Well, it means that you can take an object, let's
    call it 'objA', and wrap it in this Proxy class, with a statement
    like this

                 proxyObj = Proxy(objA),

    Then, if in the future, you do something like this

                 x = proxyObj.var1,

    since Proxy does not have a 'var1' attribute (but presumably objA does),
    the request actually is equivalent to saying

                 x = objA.var1

    Inherit from this class to create a Proxy.

    Note that, with new-style classes, this does *not* work transparently
    for Proxy subclasses that use special .__*__() method names, because
    those names are now bound to the class, not the individual instances.
    You now need to know in advance which .__*__() method names you want
    to pass on to the underlying Proxy object, and specifically delegate
    their calls like this:

        class Foo(Proxy):
            __str__ = Delegate('__str__')
    """

    def __init__(self, subject):
        """Wrap an object as a Proxy object"""
        self._subject = subject

    def __getattr__(self, name):
        """Retrieve an attribute from the wrapped object.  If the named
           attribute doesn't exist, AttributeError is raised"""
        return getattr(self._subject, name)

    def get(self):
        """Retrieve the entire wrapped object"""
        return self._subject

    def __cmp__(self, other):
        if issubclass(other.__class__, self._subject.__class__):
            return cmp(self._subject, other)
        return cmp(self.__dict__, other.__dict__)


class Delegate(object):
    """A Python Descriptor class that delegates attribute fetches
    to an underlying wrapped subject of a Proxy.  Typical use:

        class Foo(Proxy):
            __str__ = Delegate('__str__')
    """

    def __init__(self, attribute):
        self.attribute = attribute

    def __get__(self, obj, cls):
        if isinstance(obj, cls):
            return getattr(obj._subject, self.attribute)
        else:
            return self


can_read_reg = 0
try:
    import winreg
    can_read_reg = 1
    hkey_mod = winreg
    RegOpenKeyEx = winreg.OpenKeyEx
    RegEnumKey = winreg.EnumKey
    RegEnumValue = winreg.EnumValue
    RegQueryValueEx = winreg.QueryValueEx
    RegError = winreg.error
except ImportError:
    try:
        import win32api, win32con
        can_read_reg = 1
        hkey_mod = win32con
        RegOpenKeyEx = win32api.RegOpenKeyEx
        RegEnumKey = win32api.RegEnumKey
        RegEnumValue = win32api.RegEnumValue
        RegQueryValueEx = win32api.RegQueryValueEx
        RegError = win32api.error
    except ImportError:

        class _NoError(Exception):
            pass


        RegError = _NoError

WinError = None

class PlainWindowsError(OSError):
    pass


try:
    WinError = WindowsError
except NameError:
    WinError = PlainWindowsError

if can_read_reg:
    HKEY_CLASSES_ROOT = hkey_mod.HKEY_CLASSES_ROOT
    HKEY_LOCAL_MACHINE = hkey_mod.HKEY_LOCAL_MACHINE
    HKEY_CURRENT_USER = hkey_mod.HKEY_CURRENT_USER
    HKEY_USERS = hkey_mod.HKEY_USERS

    def RegGetValue(root, key):
        r"""This utility function returns a value in the registry
        without having to open the key first.  Only available on
        Windows platforms with a version of Python that can read the
        registry.  Returns the same thing as
        SCons.Util.RegQueryValueEx, except you just specify the entire
        path to the value, and don't have to bother opening the key
        first.  So:

        Instead of:
          k = SCons.Util.RegOpenKeyEx(SCons.Util.HKEY_LOCAL_MACHINE,
                r'SOFTWARE\Microsoft\Windows\CurrentVersion')
          out = SCons.Util.RegQueryValueEx(k,
                'ProgramFilesDir')

        You can write:
          out = SCons.Util.RegGetValue(SCons.Util.HKEY_LOCAL_MACHINE,
                r'SOFTWARE\Microsoft\Windows\CurrentVersion\ProgramFilesDir')
        """
        p = key.rfind('\\') + 1
        keyp = key[:p - 1]
        val = key[p:]
        k = RegOpenKeyEx(root, keyp)
        return RegQueryValueEx(k, val)


else:
    HKEY_CLASSES_ROOT = None
    HKEY_LOCAL_MACHINE = None
    HKEY_CURRENT_USER = None
    HKEY_USERS = None

    def RegGetValue(root, key):
        raise WinError


    def RegOpenKeyEx(root, key):
        raise WinError


if sys.platform == 'win32':

    def WhereIs(file, path=None, pathext=None, reject=[]):
        if path is None:
            try:
                path = os.environ['PATH']
            except KeyError:
                return

        if is_String(path):
            path = path.split(os.pathsep)
        if pathext is None:
            try:
                pathext = os.environ['PATHEXT']
            except KeyError:
                pathext = '.COM;.EXE;.BAT;.CMD'

        if is_String(pathext):
            pathext = pathext.split(os.pathsep)
        for ext in pathext:
            if ext.lower() == file[-len(ext):].lower():
                pathext = [
                 '']
                break

        if not is_List(reject) and not is_Tuple(reject):
            reject = [
             reject]
        for dir in path:
            f = os.path.join(dir, file)
            for ext in pathext:
                fext = f + ext
                if os.path.isfile(fext):
                    try:
                        reject.index(fext)
                    except ValueError:
                        return os.path.normpath(fext)

                    continue

        return


elif os.name == 'os2':

    def WhereIs(file, path=None, pathext=None, reject=[]):
        if path is None:
            try:
                path = os.environ['PATH']
            except KeyError:
                return

        if is_String(path):
            path = path.split(os.pathsep)
        if pathext is None:
            pathext = [
             '.exe', '.cmd']
        for ext in pathext:
            if ext.lower() == file[-len(ext):].lower():
                pathext = [
                 '']
                break

        if not is_List(reject) and not is_Tuple(reject):
            reject = [
             reject]
        for dir in path:
            f = os.path.join(dir, file)
            for ext in pathext:
                fext = f + ext
                if os.path.isfile(fext):
                    try:
                        reject.index(fext)
                    except ValueError:
                        return os.path.normpath(fext)

                    continue

        return


else:

    def WhereIs(file, path=None, pathext=None, reject=[]):
        import stat
        if path is None:
            try:
                path = os.environ['PATH']
            except KeyError:
                return

        if is_String(path):
            path = path.split(os.pathsep)
        if not is_List(reject) and not is_Tuple(reject):
            reject = [
             reject]
        for d in path:
            f = os.path.join(d, file)
            if os.path.isfile(f):
                try:
                    st = os.stat(f)
                except OSError:
                    continue

                if stat.S_IMODE(st[stat.ST_MODE]) & 73:
                    try:
                        reject.index(f)
                    except ValueError:
                        return os.path.normpath(f)

                    continue

        return


def PrependPath(oldpath, newpath, sep=os.pathsep, delete_existing=1, canonicalize=None):
    """This prepends newpath elements to the given oldpath.  Will only
    add any particular path once (leaving the first one it encounters
    and ignoring the rest, to preserve path order), and will
    os.path.normpath and os.path.normcase all paths to help assure
    this.  This can also handle the case where the given old path
    variable is a list instead of a string, in which case a list will
    be returned instead of a string.

    Example:
      Old Path: "/foo/bar:/foo"
      New Path: "/biz/boom:/foo"
      Result:   "/biz/boom:/foo:/foo/bar"

    If delete_existing is 0, then adding a path that exists will
    not move it to the beginning; it will stay where it is in the
    list.

    If canonicalize is not None, it is applied to each element of 
    newpath before use.
    """
    orig = oldpath
    is_list = 1
    paths = orig
    if not is_List(orig) and not is_Tuple(orig):
        paths = paths.split(sep)
        is_list = 0
    if is_String(newpath):
        newpaths = newpath.split(sep)
    else:
        if not is_List(newpath) and not is_Tuple(newpath):
            newpaths = [
             newpath]
        else:
            newpaths = newpath
        if canonicalize:
            newpaths = list(map(canonicalize, newpaths))
        if not delete_existing:
            result = []
            normpaths = []
            for path in paths:
                if not path:
                    continue
                normpath = os.path.normpath(os.path.normcase(path))
                if normpath not in normpaths:
                    result.append(path)
                    normpaths.append(normpath)

            newpaths.reverse()
            for path in newpaths:
                if not path:
                    continue
                normpath = os.path.normpath(os.path.normcase(path))
                if normpath not in normpaths:
                    result.insert(0, path)
                    normpaths.append(normpath)

            paths = result
        else:
            newpaths = newpaths + paths
            normpaths = []
            paths = []
            for path in newpaths:
                normpath = os.path.normpath(os.path.normcase(path))
                if path and normpath not in normpaths:
                    paths.append(path)
                    normpaths.append(normpath)

    if is_list:
        return paths
    else:
        return sep.join(paths)


def AppendPath(oldpath, newpath, sep=os.pathsep, delete_existing=1, canonicalize=None):
    """This appends new path elements to the given old path.  Will
    only add any particular path once (leaving the last one it
    encounters and ignoring the rest, to preserve path order), and
    will os.path.normpath and os.path.normcase all paths to help
    assure this.  This can also handle the case where the given old
    path variable is a list instead of a string, in which case a list
    will be returned instead of a string.

    Example:
      Old Path: "/foo/bar:/foo"
      New Path: "/biz/boom:/foo"
      Result:   "/foo/bar:/biz/boom:/foo"

    If delete_existing is 0, then adding a path that exists
    will not move it to the end; it will stay where it is in the list.

    If canonicalize is not None, it is applied to each element of 
    newpath before use.
    """
    orig = oldpath
    is_list = 1
    paths = orig
    if not is_List(orig) and not is_Tuple(orig):
        paths = paths.split(sep)
        is_list = 0
    if is_String(newpath):
        newpaths = newpath.split(sep)
    else:
        if not is_List(newpath) and not is_Tuple(newpath):
            newpaths = [
             newpath]
        else:
            newpaths = newpath
        if canonicalize:
            newpaths = list(map(canonicalize, newpaths))
        if not delete_existing:
            result = []
            normpaths = []
            for path in paths:
                if not path:
                    continue
                result.append(path)
                normpaths.append(os.path.normpath(os.path.normcase(path)))

            for path in newpaths:
                if not path:
                    continue
                normpath = os.path.normpath(os.path.normcase(path))
                if normpath not in normpaths:
                    result.append(path)
                    normpaths.append(normpath)

            paths = result
        else:
            newpaths = paths + newpaths
            newpaths.reverse()
            normpaths = []
            paths = []
            for path in newpaths:
                normpath = os.path.normpath(os.path.normcase(path))
                if path and normpath not in normpaths:
                    paths.append(path)
                    normpaths.append(normpath)

        paths.reverse()
    if is_list:
        return paths
    else:
        return sep.join(paths)


def AddPathIfNotExists(env_dict, key, path, sep=os.pathsep):
    """This function will take 'key' out of the dictionary
    'env_dict', then add the path 'path' to that key if it is not
    already there.  This treats the value of env_dict[key] as if it
    has a similar format to the PATH variable...a list of paths
    separated by tokens.  The 'path' will get added to the list if it
    is not already there."""
    try:
        is_list = 1
        paths = env_dict[key]
        if not is_List(env_dict[key]):
            paths = paths.split(sep)
            is_list = 0
        if os.path.normcase(path) not in list(map(os.path.normcase, paths)):
            paths = [
             path] + paths
        if is_list:
            env_dict[key] = paths
        else:
            env_dict[key] = sep.join(paths)
    except KeyError:
        env_dict[key] = path


if sys.platform == 'cygwin':

    def get_native_path(path):
        """Transforms an absolute path into a native path for the system.  In
        Cygwin, this converts from a Cygwin path to a Windows one."""
        return os.popen('cygpath -w ' + path).read().replace('\n', '')


else:

    def get_native_path(path):
        """Transforms an absolute path into a native path for the system.
        Non-Cygwin version, just leave the path alone."""
        return path


display = DisplayEngine()

def Split(arg):
    if is_List(arg) or is_Tuple(arg):
        return arg
    if is_String(arg):
        return arg.split()
    else:
        return [
         arg]


class CLVar(UserList):
    """A class for command-line construction variables.

    This is a list that uses Split() to split an initial string along
    white-space arguments, and similarly to split any strings that get
    added.  This allows us to Do the Right Thing with Append() and
    Prepend() (as well as straight Python foo = env['VAR'] + 'arg1
    arg2') regardless of whether a user adds a list or a string to a
    command-line construction variable.
    """

    def __init__(self, seq=[]):
        UserList.__init__(self, Split(seq))

    def __add__(self, other):
        return UserList.__add__(self, CLVar(other))

    def __radd__(self, other):
        return UserList.__radd__(self, CLVar(other))

    def __coerce__(self, other):
        return (self, CLVar(other))

    def __str__(self):
        return (' ').join(self.data)


class OrderedDict(UserDict):

    def __init__(self, dict=None):
        self._keys = []
        UserDict.__init__(self, dict)

    def __delitem__(self, key):
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        if key not in self._keys:
            self._keys.append(key)

    def clear(self):
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        dict = OrderedDict()
        dict.update(self)
        return dict

    def items(self):
        return list(zip(self._keys, list(self.values())))

    def keys(self):
        return self._keys[:]

    def popitem(self):
        try:
            key = self._keys[(-1)]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]
        return (
         key, val)

    def setdefault(self, key, failobj=None):
        UserDict.setdefault(self, key, failobj)
        if key not in self._keys:
            self._keys.append(key)

    def update(self, dict):
        for key, val in dict.items():
            self.__setitem__(key, val)

    def values(self):
        return list(map(self.get, self._keys))


class Selector(OrderedDict):
    """A callable ordered dictionary that maps file suffixes to
    dictionary values.  We preserve the order in which items are added
    so that get_suffix() calls always return the first suffix added."""

    def __call__(self, env, source, ext=None):
        if ext is None:
            try:
                ext = source[0].get_suffix()
            except IndexError:
                ext = ''

        try:
            return self[ext]
        except KeyError:
            s_dict = {}
            for k, v in self.items():
                if k is not None:
                    s_k = env.subst(k)
                    if s_k in s_dict:
                        raise KeyError(s_dict[s_k][0], k, s_k)
                    s_dict[s_k] = (
                     k, v)

            try:
                return s_dict[ext][1]
            except KeyError:
                try:
                    return self[None]
                except KeyError:
                    return

        return


if sys.platform == 'cygwin':

    def case_sensitive_suffixes(s1, s2):
        return 0


else:

    def case_sensitive_suffixes(s1, s2):
        return os.path.normcase(s1) != os.path.normcase(s2)


def adjustixes(fname, pre, suf, ensure_suffix=False):
    if pre:
        path, fn = os.path.split(os.path.normpath(fname))
        if fn[:len(pre)] != pre:
            fname = os.path.join(path, pre + fn)
    if suf and fname[-len(suf):] != suf and (ensure_suffix or not splitext(fname)[1]):
        fname = fname + suf
    return fname


def unique(s):
    """Return a list of the elements in s, but without duplicates.

    For example, unique([1,2,3,1,2,3]) is some permutation of [1,2,3],
    unique("abcabc") some permutation of ["a", "b", "c"], and
    unique(([1, 2], [2, 3], [1, 2])) some permutation of
    [[2, 3], [1, 2]].

    For best speed, all sequence elements should be hashable.  Then
    unique() will usually work in linear time.

    If not possible, the sequence elements should enjoy a total
    ordering, and if list(s).sort() doesn't raise TypeError it's
    assumed that they do enjoy a total ordering.  Then unique() will
    usually work in O(N*log2(N)) time.

    If that's not possible either, the sequence elements must support
    equality-testing.  Then unique() will usually work in quadratic
    time.
    """
    n = len(s)
    if n == 0:
        return []
    u = {}
    try:
        for x in s:
            u[x] = 1

    except TypeError:
        pass
    else:
        return list(u.keys())

    del u
    try:
        t = sorted(s)
    except TypeError:
        pass
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti = lasti + 1
            i = i + 1

        return t[:lasti]

    del t
    u = []
    for x in s:
        if x not in u:
            u.append(x)

    return u


def uniquer(seq, idfun=None):
    if idfun is None:

        def idfun(x):
            return x

    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        if marker in seen:
            continue
        seen[marker] = 1
        result.append(item)

    return result


def uniquer_hashables(seq):
    seen = {}
    result = []
    for item in seq:
        if item not in seen:
            seen[item] = 1
            result.append(item)

    return result


def logical_lines(physical_lines, joiner=('').join):
    logical_line = []
    for line in physical_lines:
        stripped = line.rstrip()
        if stripped.endswith('\\'):
            logical_line.append(stripped[:-1])
        else:
            logical_line.append(line)
            yield joiner(logical_line)
            logical_line = []

    if logical_line:
        yield joiner(logical_line)


class LogicalLines(object):
    """ Wrapper class for the logical_lines method.
    
        Allows us to read all "logical" lines at once from a
        given file object.
    """

    def __init__(self, fileobj):
        self.fileobj = fileobj

    def readlines(self):
        result = [ l for l in logical_lines(self.fileobj) ]
        return result


class UniqueList(UserList):

    def __init__(self, seq=[]):
        UserList.__init__(self, seq)
        self.unique = True

    def __make_unique(self):
        if not self.unique:
            self.data = uniquer_hashables(self.data)
            self.unique = True

    def __lt__(self, other):
        self.__make_unique()
        return UserList.__lt__(self, other)

    def __le__(self, other):
        self.__make_unique()
        return UserList.__le__(self, other)

    def __eq__(self, other):
        self.__make_unique()
        return UserList.__eq__(self, other)

    def __ne__(self, other):
        self.__make_unique()
        return UserList.__ne__(self, other)

    def __gt__(self, other):
        self.__make_unique()
        return UserList.__gt__(self, other)

    def __ge__(self, other):
        self.__make_unique()
        return UserList.__ge__(self, other)

    def __cmp__(self, other):
        self.__make_unique()
        return UserList.__cmp__(self, other)

    def __len__(self):
        self.__make_unique()
        return UserList.__len__(self)

    def __getitem__(self, i):
        self.__make_unique()
        return UserList.__getitem__(self, i)

    def __setitem__(self, i, item):
        UserList.__setitem__(self, i, item)
        self.unique = False

    def __getslice__(self, i, j):
        self.__make_unique()
        return UserList.__getslice__(self, i, j)

    def __setslice__(self, i, j, other):
        UserList.__setslice__(self, i, j, other)
        self.unique = False

    def __add__(self, other):
        result = UserList.__add__(self, other)
        result.unique = False
        return result

    def __radd__(self, other):
        result = UserList.__radd__(self, other)
        result.unique = False
        return result

    def __iadd__(self, other):
        result = UserList.__iadd__(self, other)
        result.unique = False
        return result

    def __mul__(self, other):
        result = UserList.__mul__(self, other)
        result.unique = False
        return result

    def __rmul__(self, other):
        result = UserList.__rmul__(self, other)
        result.unique = False
        return result

    def __imul__(self, other):
        result = UserList.__imul__(self, other)
        result.unique = False
        return result

    def append(self, item):
        UserList.append(self, item)
        self.unique = False

    def insert(self, i):
        UserList.insert(self, i)
        self.unique = False

    def count(self, item):
        self.__make_unique()
        return UserList.count(self, item)

    def index(self, item):
        self.__make_unique()
        return UserList.index(self, item)

    def reverse(self):
        self.__make_unique()
        UserList.reverse(self)

    def sort(self, *args, **kwds):
        self.__make_unique()
        return UserList.sort(self, *args, **kwds)

    def extend(self, other):
        UserList.extend(self, other)
        self.unique = False


class Unbuffered(object):
    """
    A proxy class that wraps a file object, flushing after every write,
    and delegating everything else to the wrapped object.
    """

    def __init__(self, file):
        self.file = file
        self.softspace = 0

    def write(self, arg):
        try:
            self.file.write(arg)
            self.file.flush()
        except IOError:
            pass

    def __getattr__(self, attr):
        return getattr(self.file, attr)


def make_path_relative(path):
    """ makes an absolute path name to a relative pathname.
    """
    if os.path.isabs(path):
        drive_s, path = os.path.splitdrive(path)
        import re
        if not drive_s:
            path = re.compile('/*(.*)').findall(path)[0]
        else:
            path = path[1:]
    assert not os.path.isabs(path), path
    return path


def AddMethod(obj, function, name=None):
    """
    Adds either a bound method to an instance or an unbound method to
    a class. If name is ommited the name of the specified function
    is used by default.
    Example:
      a = A()
      def f(self, x, y):
        self.z = x + y
      AddMethod(f, A, "add")
      a.add(2, 4)
      print a.z
      AddMethod(lambda self, i: self.l[i], a, "listIndex")
      print a.listIndex(5)
    """
    if name is None:
        name = function.func_name
    else:
        function = RenameFunction(function, name)
    if hasattr(obj, '__class__') and obj.__class__ is not type:
        setattr(obj, name, MethodType(function, obj, obj.__class__))
    else:
        setattr(obj, name, MethodType(function, None, obj))
    return


def RenameFunction(function, name):
    """
    Returns a function identical to the specified function, but with
    the specified name.
    """
    return FunctionType(function.func_code, function.func_globals, name, function.func_defaults)


md5 = False

def MD5signature(s):
    return str(s)


def MD5filesignature(fname, chunksize=65536):
    f = open(fname, 'rb')
    result = f.read()
    f.close()
    return result


try:
    import hashlib
except ImportError:
    pass

if hasattr(hashlib, 'md5'):
    md5 = True

    def MD5signature(s):
        m = hashlib.md5()
        m.update(str(s))
        return m.hexdigest()


    def MD5filesignature(fname, chunksize=65536):
        m = hashlib.md5()
        f = open(fname, 'rb')
        while True:
            blck = f.read(chunksize)
            if not blck:
                break
            m.update(str(blck))

        f.close()
        return m.hexdigest()


def MD5collect(signatures):
    """
    Collects a list of signatures into an aggregate signature.

    signatures - a list of signatures
    returns - the aggregate signature
    """
    if len(signatures) == 1:
        return signatures[0]
    else:
        return MD5signature((', ').join(signatures))


def silent_intern(x):
    """
    Perform sys.intern() on the passed argument and return the result.
    If the input is ineligible (e.g. a unicode string) the original argument is
    returned and no exception is thrown.
    """
    try:
        return sys.intern(x)
    except TypeError:
        return x


class Null(object):
    """ Null objects always and reliably "do nothing." """

    def __new__(cls, *args, **kwargs):
        if '_instance' not in vars(cls):
            cls._instance = super(Null, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self

    def __repr__(self):
        return 'Null(0x%08X)' % id(self)

    def __nonzero__(self):
        return False

    def __getattr__(self, name):
        return self

    def __setattr__(self, name, value):
        return self

    def __delattr__(self, name):
        return self


class NullSeq(Null):

    def __len__(self):
        return 0

    def __iter__(self):
        return iter(())

    def __getitem__(self, i):
        return self

    def __delitem__(self, i):
        return self

    def __setitem__(self, i, v):
        return self


del __revision__