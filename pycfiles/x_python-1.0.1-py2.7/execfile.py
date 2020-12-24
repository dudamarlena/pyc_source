# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/execfile.py
# Compiled at: 2020-05-02 09:51:10
"""Execute files of Python code."""
import imp, os, sys, tokenize, mimetypes
from xdis import load_module, PYTHON_VERSION
SUPPORTED_PYTHON_VERSIONS = (2.5, 2.6, 2.7, 3.3, 3.2, 3.4, 3.5)
from xpython.pyvm2 import VirtualMachine
try:
    open_source = tokenize.open
except:

    def open_source(fname):
        """Open a source file the best way."""
        return open(fname, 'rU')


CannotCompile = WrongBytecode = NoSource = Exception

def exec_code_object(code, env, python_version=PYTHON_VERSION):
    vm = VirtualMachine(python_version)
    vm.run_code(code, f_globals=env)


try:
    BUILTINS = sys.modules['__builtin__']
except KeyError:
    BUILTINS = sys.modules['builtins']

def rsplit1(s, sep):
    """The same as s.rsplit(sep, 1), but works in 2.3"""
    parts = s.split(sep)
    return (sep.join(parts[:-1]), parts[(-1)])


def run_python_module(modulename, args):
    """Run a python module, as though with ``python -m name args...``.

    `modulename` is the name of the module, possibly a dot-separated name.
    `args` is the argument array to present as sys.argv, including the first
    element naming the module being executed.

    """
    openfile = None
    glo, loc = globals(), locals()
    try:
        try:
            if '.' in modulename:
                packagename, name = rsplit1(modulename, '.')
                package = __import__(packagename, glo, loc, ['__path__'])
                searchpath = package.__path__
            else:
                packagename, name = None, modulename
                searchpath = None
            openfile, pathname, _ = imp.find_module(name, searchpath)
            if openfile is None and pathname is None:
                raise NoSource('module does not live in a file: %r' % modulename)
            if openfile is None:
                packagename = modulename
                name = '__main__'
                package = __import__(packagename, glo, loc, ['__path__'])
                searchpath = package.__path__
                openfile, pathname, _ = imp.find_module(name, searchpath)
        except ImportError:
            _, err, _ = sys.exc_info()
            raise NoSource(str(err))

    finally:
        if openfile:
            openfile.close()

    args[0] = pathname
    run_python_file(pathname, args, package=packagename)
    return


def run_python_file(filename, args, package=None):
    """Run a python file as if it were the main program on the command line.

    `filename` is the path to the file to execute, it need not be a .py file.
    `args` is the argument array to present as sys.argv, including the first
    element naming the file being executed.  `package` is the name of the
    enclosing package, if any.

    """
    old_main_mod = sys.modules['__main__']
    main_mod = imp.new_module('__main__')
    sys.modules['__main__'] = main_mod
    main_mod.__file__ = filename
    if package:
        main_mod.__package__ = package
    main_mod.__builtins__ = BUILTINS
    old_argv = sys.argv
    old_path0 = sys.path[0]
    sys.argv = args
    if package:
        sys.path[0] = ''
    else:
        sys.path[0] = os.path.abspath(os.path.dirname(filename))
    try:
        try:
            mime = mimetypes.guess_type(filename)
            if mime == ('application/x-python-code', None):
                python_version, timestamp, magic_int, code, pypy, source_size, sip_hash = load_module(filename)
                if python_version not in SUPPORTED_PYTHON_VERSIONS:
                    raise WrongBytecode('We only support bytecode 2.5 - 2.7 and 3.2 - 3.5: %r is %2.1f bytecode' % (
                     filename, python_version))
            else:
                source_file = open_source(filename)
                try:
                    source = source_file.read()
                finally:
                    source_file.close()

                if PYTHON_VERSION not in SUPPORTED_PYTHON_VERSIONS:
                    raise CannotCompile('We need Python 2.5 - 2.7 or 3.2 - 3.5 to compile source code; you are running Python %s' % PYTHON_VERSION)
                if not source or source[(-1)] != '\n':
                    source += '\n'
                code = compile(source, filename, 'exec')
                python_version = PYTHON_VERSION
        except IOError:
            raise NoSource('No file to run: %r' % filename)

        exec_code_object(code, main_mod.__dict__, python_version)
    finally:
        sys.modules['__main__'] = old_main_mod
        sys.argv = old_argv
        sys.path[0] = old_path0

    return


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: execfile.py <filename> args'
        os.exit(1)
    run_python_file(sys.argv[1], sys.argv[2:])