# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\stuc400\PycharmProjects\smart_preprocess\dmreader\trait_base.py
# Compiled at: 2018-07-26 09:42:17
# Size of source mod 2**32: 14132 bytes
""" Defines common, low-level capabilities needed by the Traits package.
"""
import os, sys
from os import getcwd
from os.path import dirname, exists, join
from . import _py2to3
from .etsconfig.api import ETSConfig
enumerate = enumerate
vi = sys.version_info
python_version = vi[0] + float(vi[1]) / 10.0
ClassTypes = _py2to3.ClassTypes
SequenceTypes = (
 list, tuple)
ComplexTypes = (
 float, int)
TypeTypes = (
 str, str, int, int, float, complex, list, tuple, dict, bool)
TraitNotifier = '__trait_notifier__'
TraitsCache = '_traits_cache_'
Uninitialized = None

class _Uninitialized(object):
    __doc__ = " The singleton value of this class represents the uninitialized state\n        of a trait and is specified as the 'old' value in the trait change\n        notification that occurs when the value of a trait is read before being\n        set.\n    "

    def __new__(cls):
        if Uninitialized is not None:
            return Uninitialized
        else:
            self = object.__new__(cls)
            return self

    def __repr__(self):
        return '<uninitialized>'

    def __reduce_ex__(self, protocol):
        return (
         _Uninitialized, ())


Uninitialized = _Uninitialized()
Undefined = None

class _Undefined(object):
    __doc__ = " Singleton 'Undefined' object (used as undefined trait name and/or value)\n    "

    def __new__(cls):
        if Undefined is not None:
            return Undefined
        else:
            self = object.__new__(cls)
            return self

    def __repr__(self):
        return '<undefined>'

    def __reduce_ex__(self, protocol):
        return (
         _Undefined, ())

    def __eq__(self, other):
        return type(self) is type(other)

    def __hash__(self):
        return hash(type(self))

    def __ne__(self, other):
        return type(self) is not type(other)


Undefined = _Undefined()

class Missing(object):
    __doc__ = " Singleton 'Missing' object (used as missing method argument marker).\n    "

    def __repr__(self):
        return '<missing>'


Missing = Missing()

class Self(object):
    __doc__ = " Singleton 'Self' object (used as object reference to current 'object').\n    "

    def __repr__(self):
        return '<self>'


Self = Self()

def strx(arg):
    """ Wraps the built-in str() function to raise a TypeError if the
    argument is not of a type in StringTypes.
    """
    if isinstance(arg, StringTypes):
        return str(arg)
    raise TypeError


StringTypes = (
 str, str, int, int, float, complex)
CoercableTypes = {int: (11, int, int), 
 float: (11, float, int), 
 complex: (11, complex, float, int), 
 str: (11, str, str)}

def class_of(object):
    """ Returns a string containing the class name of an object with the
    correct indefinite article ('a' or 'an') preceding it (e.g., 'an Image',
    'a PlotValue').
    """
    if isinstance(object, str):
        return add_article(object)
    else:
        return add_article(object.__class__.__name__)


def add_article(name):
    """ Returns a string containing the correct indefinite article ('a' or 'an')
    prefixed to the specified string.
    """
    if name[:1].lower() in 'aeiou':
        return 'an ' + name
    else:
        return 'a ' + name


def user_name_for(name):
    """ Returns a "user-friendly" version of a string, with the first letter
    capitalized and with underscore characters replaced by spaces. For example,
    ``user_name_for('user_name_for')`` returns ``'User name for'``.
    """
    name = name.replace('_', ' ')
    result = ''
    last_lower = False
    for c in name:
        if c.isupper():
            if last_lower:
                result += ' '
        last_lower = c.islower()
        result += c

    return result.capitalize()


_traits_home = None

def traits_home():
    """ Gets the path to the Traits home directory.
    """
    global _traits_home
    if _traits_home is None:
        _traits_home = verify_path(join(ETSConfig.application_data, 'traits'))
    return _traits_home


def verify_path(path):
    """ Verify that a specified path exists, and try to create it if it
        does not exist.
    """
    if not exists(path):
        try:
            os.mkdir(path)
        except:
            pass

    return path


def get_module_name(level=2):
    """ Returns the name of the module that the caller's caller is located in.
    """
    return sys._getframe(level).f_globals.get('__name__', '__main__')


def get_resource_path(level=2):
    """Returns a resource path calculated from the caller's stack.
    """
    module = sys._getframe(level).f_globals.get('__name__', '__main__')
    path = None
    if module != '__main__':
        try:
            path = dirname(getattr(sys.modules.get(module), '__file__'))
        except:
            pass

    if path is None:
        for path in [dirname(sys.argv[0]), getcwd()]:
            if exists(path):
                break

    frozen = getattr(sys, 'frozen', False)
    if frozen:
        if frozen == 'macosx_app':
            root = os.environ['RESOURCEPATH']
        else:
            if frozen in ('dll', 'windows_exe', 'console_exe'):
                root = os.path.dirname(sys.executable)
            else:
                root = os.path.dirname(sys.executable)
            if '.zip/' in path:
                zippath, image_path = path.split('.zip/')
                path = os.path.join(root, image_path)
    return path


def xgetattr(object, xname, default=Undefined):
    """ Returns the value of an extended object attribute name of the form:
        name[.name2[.name3...]].
    """
    names = xname.split('.')
    for name in names[:-1]:
        if default is Undefined:
            object = getattr(object, name)
        else:
            object = getattr(object, name, None)
            if object is None:
                return default

    if default is Undefined:
        return getattr(object, names[(-1)])
    else:
        return getattr(object, names[(-1)], default)


def xsetattr(object, xname, value):
    """ Sets the value of an extended object attribute name of the form:
        name[.name2[.name3...]].
    """
    names = xname.split('.')
    for name in names[:-1]:
        object = getattr(object, name)

    setattr(object, names[(-1)], value)


def is_none(value):
    return value is None


def not_none(value):
    return value is not None


def not_false(value):
    return value is not False


def not_event(value):
    return value != 'event'


def is_str(value):
    return isinstance(value, str)