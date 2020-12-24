# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qt/work/pyside/pyside-setup/pyside2_install/py2.7-qt5.14.2-64bit-release/lib/python2.7/site-packages/shiboken2/files.dir/shibokensupport/signature/lib/enum_sig.py
# Compiled at: 2020-03-30 06:40:47
from __future__ import print_function, absolute_import
import sys
from shibokensupport.signature import inspect
from shibokensupport.signature import get_signature

class ExactEnumerator(object):
    """
    ExactEnumerator enumerates all signatures in a module as they are.

    This class is used for generating complete listings of all signatures.
    An appropriate formatter should be supplied, if printable output
    is desired.
    """

    def __init__(self, formatter, result_type=dict):
        global EnumType
        try:
            from PySide2.QtCore import Qt
            EnumType = type(Qt.Key)
        except ImportError:
            EnumType = None

        self.fmt = formatter
        self.result_type = result_type
        self.fmt.level = 0
        self.fmt.after_enum = self.after_enum
        self._after_enum = False
        return

    def after_enum(self):
        ret = self._after_enum
        self._after_enum = False

    def module(self, mod_name):
        __import__(mod_name)
        self.fmt.mod_name = mod_name
        with self.fmt.module(mod_name):
            module = sys.modules[mod_name]
            members = inspect.getmembers(module, inspect.isclass)
            functions = inspect.getmembers(module, inspect.isroutine)
            ret = self.result_type()
            self.fmt.class_name = None
            for class_name, klass in members:
                ret.update(self.klass(class_name, klass))

            if isinstance(klass, EnumType):
                raise SystemError('implement enum instances at module level')
            for func_name, func in functions:
                ret.update(self.function(func_name, func))

            return ret
        return

    def klass(self, class_name, klass):
        bases_list = []
        for base in klass.__bases__:
            name = base.__name__
            if name in ('object', 'type'):
                pass
            else:
                modname = base.__module__
                name = modname + '.' + base.__name__
            bases_list.append(name)

        class_str = ('{}({})').format(class_name, (', ').join(bases_list))
        ret = self.result_type()
        class_members = sorted(list(klass.__dict__.items()))
        subclasses = []
        functions = []
        enums = []
        for thing_name, thing in class_members:
            if inspect.isclass(thing):
                subclass_name = ('.').join((class_name, thing_name))
                subclasses.append((subclass_name, thing))
            elif inspect.isroutine(thing):
                func_name = thing_name.split('.')[0]
                signature = getattr(thing, '__signature__', None)
                if signature is not None:
                    functions.append((func_name, thing))
            elif type(type(thing)) is EnumType:
                enums.append((thing_name, thing))

        init_signature = getattr(klass, '__signature__', None)
        enums.sort(key=lambda tup: tup[1])
        self.fmt.have_body = bool(subclasses or functions or enums or init_signature)
        with self.fmt.klass(class_name, class_str):
            self.fmt.level += 1
            self.fmt.class_name = class_name
            if hasattr(self.fmt, 'enum'):
                for enum_name, value in enums:
                    with self.fmt.enum(class_name, enum_name, int(value)):
                        pass

            for subclass_name, subclass in subclasses:
                if klass == subclass:
                    print(('Warning: {class_name} points to itself via {subclass_name}, skipped!').format(**locals()))
                    continue
                ret.update(self.klass(subclass_name, subclass))
                self.fmt.class_name = class_name

            ret.update(self.function('__init__', klass))
            for func_name, func in functions:
                func_kind = get_signature(func, '__func_kind__')
                modifier = func_kind if func_kind in ('staticmethod', 'classmethod') else None
                ret.update(self.function(func_name, func, modifier))

            self.fmt.level -= 1
        return ret

    def function(self, func_name, func, modifier=None):
        self.fmt.level += 1
        ret = self.result_type()
        signature = func.__signature__
        if signature is not None:
            with self.fmt.function(func_name, signature, modifier) as (key):
                ret[key] = signature
        self.fmt.level -= 1
        return ret


def stringify(signature):
    if isinstance(signature, list):
        ret = set(stringify(sig) for sig in signature)
        if len(ret) > 1:
            return sorted(ret)
        return list(ret)[0]
    return tuple(str(pv) for pv in signature.parameters.values())


class SimplifyingEnumerator(ExactEnumerator):
    """
    SimplifyingEnumerator enumerates all signatures in a module filtered.

    There are no default values, no variable
    names and no self parameter. Only types are present after simplification.
    The functions 'next' resp. '__next__' are removed
    to make the output identical for Python 2 and 3.
    An appropriate formatter should be supplied, if printable output
    is desired.
    """

    def function(self, func_name, func, modifier=None):
        ret = self.result_type()
        signature = get_signature(func, 'existence')
        sig = stringify(signature) if signature is not None else None
        if sig is not None and func_name not in ('next', '__next__', '__div__'):
            with self.fmt.function(func_name, sig) as (key):
                ret[key] = sig
        return ret


class HintingEnumerator(ExactEnumerator):
    """
    HintingEnumerator enumerates all signatures in a module slightly changed.

    This class is used for generating complete listings of all signatures for
    hinting stubs. Only default values are replaced by "...".
    """

    def function(self, func_name, func, modifier=None):
        ret = self.result_type()
        signature = get_signature(func, 'hintingstub')
        if signature is not None:
            with self.fmt.function(func_name, signature, modifier) as (key):
                ret[key] = signature
        return ret