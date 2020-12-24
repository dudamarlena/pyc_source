# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qt/work/pyside/pyside-setup/pyside2_install/py2.7-qt5.14.2-64bit-release/lib/python2.7/site-packages/shiboken2/files.dir/shibokensupport/signature/loader.py
# Compiled at: 2020-03-30 06:40:47
from __future__ import print_function, absolute_import
import sys, os, traceback, types
try:
    ModuleNotFoundError
except NameError:
    ModuleNotFoundError = ImportError

def formatannotation(annotation, base_module=None):
    if isinstance(annotation, type):
        if annotation.__module__ in ('builtins', base_module):
            return annotation.__qualname__
        return annotation.__module__ + '.' + annotation.__qualname__
    return repr(annotation)


def pyside_type_init(type_key, sig_strings):
    return parser.pyside_type_init(type_key, sig_strings)


def create_signature(props, key):
    return layout.create_signature(props, key)


def seterror_argument(args, func_name):
    return errorhandler.seterror_argument(args, func_name)


def make_helptext(func):
    return errorhandler.make_helptext(func)


def finish_import(module):
    return importhandler.finish_import(module)


import signature_bootstrap
from shibokensupport import signature
signature.get_signature = signature_bootstrap.get_signature
del signature_bootstrap

def _get_modname(mod):
    if getattr(mod, '__spec__', None):
        return mod.__spec__.name
    else:
        return mod.__name__


def _set_modname(mod, name):
    if getattr(mod, '__spec__', None):
        mod.__spec__.name = name
    else:
        mod.__name__ = name
    return


def put_into_package(package, module, override=None):
    name = (override if override else _get_modname(module)).rsplit('.', 1)[(-1)]
    if package:
        setattr(package, name, module)
    fullname = ('{}.{}').format(_get_modname(package), name) if package else name
    _set_modname(module, fullname)
    sys.modules[fullname] = module


def list_modules(message):
    ext_modules = {key:value for key, value in sys.modules.items() if hasattr(value, '__file__') if hasattr(value, '__file__')}
    print('SYS.MODULES', message, len(sys.modules), len(ext_modules))
    for name, module in sorted(ext_modules.items()):
        print(('  {:23}').format(name), repr(module)[:70])


orig_typing = True
if sys.version_info >= (3, ):
    import typing, inspect
    inspect.formatannotation = formatannotation
else:
    if 'typing' not in sys.modules:
        orig_typing = False
        from shibokensupport import typing27 as typing
        sys.modules['typing'] = typing
    else:
        import typing
    import inspect
    namespace = inspect.__dict__
    from shibokensupport import backport_inspect as inspect
    _doc = inspect.__doc__
    inspect.__dict__.update(namespace)
    inspect.__doc__ += _doc
    inspect.__all__ = list(x for x in dir(inspect) if not x.startswith('_'))
for name, obj in typing.__dict__.items():
    if hasattr(obj, '__module__'):
        try:
            obj.__module__ = 'typing'
        except (TypeError, AttributeError):
            pass

import shibokensupport
put_into_package(shibokensupport.signature, typing, 'typing')
put_into_package(shibokensupport.signature, inspect, 'inspect')

def move_into_pyside_package():
    import PySide2
    try:
        import PySide2.support
    except ModuleNotFoundError:
        PySide2.support = types.ModuleType('PySide2.support')

    put_into_package(PySide2.support, signature)
    put_into_package(PySide2.support.signature, mapping)
    put_into_package(PySide2.support.signature, errorhandler)
    put_into_package(PySide2.support.signature, layout)
    put_into_package(PySide2.support.signature, lib)
    put_into_package(PySide2.support.signature, parser)
    put_into_package(PySide2.support.signature, importhandler)
    put_into_package(PySide2.support.signature.lib, enum_sig)
    put_into_package(None if orig_typing else PySide2.support.signature, typing)
    put_into_package(PySide2.support.signature, inspect)
    return


from shibokensupport.signature import mapping
from shibokensupport.signature import errorhandler
from shibokensupport.signature import layout
from shibokensupport.signature import lib
from shibokensupport.signature import parser
from shibokensupport.signature import importhandler
from shibokensupport.signature.lib import enum_sig
if 'PySide2' in sys.modules:
    move_into_pyside_package()