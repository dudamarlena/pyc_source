# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rito/Projects/inline/env/lib/python2.6/site-packages/inline.py
# Compiled at: 2015-11-19 08:57:26
import atexit, ctypes, distutils.ccompiler, os.path, platform, shutil, sys, tempfile
__version__ = '0.0.1'

def c(source, libraries=[]):
    """
    >>> c('int add(int a, int b) {return a + b;}').add(40, 2)
    42
    >>> sqrt = c('''
    ... #include <math.h>
    ... double _sqrt(double x) {return sqrt(x);}
    ... ''', ['m'])._sqrt
    >>> sqrt.restype = ctypes.c_double
    >>> sqrt(ctypes.c_double(400.0))
    20.0
    """
    path = _cc_build_shared_lib(source, '.c', libraries)
    return ctypes.cdll.LoadLibrary(path)


def cxx(source, libraries=[]):
    """
    >>> cxx('extern "C" { int add(int a, int b) {return a + b;} }').add(40, 2)
    42
    """
    path = _cc_build_shared_lib(source, '.cc', libraries)
    return ctypes.cdll.LoadLibrary(path)


cpp = cxx

def python(source):
    """
    >>> python('def add(a, b): return a + b').add(40, 2)
    42
    """
    obj = type('', (object,), {})()
    _exec(source, obj.__dict__, obj.__dict__)
    return obj


def _cc_build_shared_lib(source, suffix, libraries):
    tempdir = tempfile.mkdtemp()
    atexit.register(lambda : shutil.rmtree(tempdir))
    cc = distutils.ccompiler.new_compiler()
    with tempfile.NamedTemporaryFile('w+', suffix=suffix, dir=tempdir) as (f):
        f.write(source)
        f.seek(0)
        args = []
        if platform.system() == 'Linux':
            args.append('-fPIC')
        objs = cc.compile((f.name,), tempdir, extra_postargs=args)
    for library in libraries:
        cc.add_library(library)

    cc.link_shared_lib(objs, f.name, tempdir)
    filename = cc.library_filename(f.name, 'shared')
    return os.path.join(tempdir, filename)


def _exec(object, globals, locals):
    """
    >>> d = {}
    >>> exec('a = 0', d, d)
    >>> d['a']
    0
    """
    if sys.version_info < (3, ):
        exec 'exec object in globals, locals'
    else:
        exec (
         object, globals, locals)