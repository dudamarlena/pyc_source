# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/apljungquist/docs/2020/nopy/public/src/nopy/__init__.py
# Compiled at: 2020-01-25 13:41:26
# Size of source mod 2**32: 1215 bytes
import logging
logger = logging.getLogger(__name__)

def load_py(attr_name):
    from nopy import fib_py
    return getattr(fib_py, attr_name)


def load_pyx(attr_name):
    from nopy import fib_pyx
    return getattr(fib_pyx, attr_name)


def load_c(attr_name):
    import nopy._fib_c as fib_c
    return getattr(fib_c, attr_name)


def load_wasm(path):
    import importlib.resources as pkg_resources
    import wasmer
    instance = wasmer.Instance(pkg_resources.read_binary('nopy', path))
    return instance.exports.fib


def load_with_fallback(load_func, *args):
    try:
        return load_func(*args)
    except Exception as e:
        try:
            logger.warning('Failed to load implementation', exc_info=True)
            return e
        finally:
            e = None
            del e


fibs = {'py python lru_cache':load_with_fallback(load_py, 'fib_cached'), 
 'py python simple':load_with_fallback(load_py, 'fib_naive'), 
 'pyx cython cdef':load_with_fallback(load_pyx, 'fib_typed'), 
 'pyx cython simple':load_with_fallback(load_pyx, 'fib_untyped'), 
 'c cffi simple':load_with_fallback(load_c, 'fib'), 
 'rs wasm simple':load_with_fallback(load_wasm, 'fib_rs.wasm'), 
 'c wasm simple':load_with_fallback(load_wasm, 'fib_c.wasm')}