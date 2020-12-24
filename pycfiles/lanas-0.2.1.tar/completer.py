# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: kanzen/kanzen/completer.py
# Compiled at: 2012-08-23 22:01:30
from __future__ import absolute_import
import sys, types, StringIO
_HELPOUT = StringIO.StringIO
_STDOUT = sys.stdout

def get_completions_per_type(object_dir):
    """Return info about function parameters"""
    if not object_dir:
        return {}
    else:
        result = {'attributes': [], 'modules': [], 'functions': [], 'classes': []}
        type_assign = {types.ClassType: 'classes', types.FunctionType: 'functions', 
           types.MethodType: 'functions', 
           types.ModuleType: 'modules', 
           types.LambdaType: 'functions'}
        for attr in object_dir:
            obj = None
            sig = ''
            try:
                obj = _load_symbol(attr, globals(), locals())
            except:
                return {}

            if type(obj) in (types.ClassType, types.TypeType):
                obj = _find_constructor(obj)
            elif type(obj) == types.MethodType:
                obj = obj.im_func
            if not sig:
                sig = attr[attr.rfind('.') + 1:]
            result[type_assign.get(type(obj), 'attributes')].append(sig)

        return result


def _load_symbol(s, dglobals, dlocals):
    sym = None
    dots = s.split('.')
    if not s or len(dots) == 1:
        sym = eval(s, dglobals, dlocals)
    else:
        for i in range(1, len(dots) + 1):
            s = ('.').join(dots[:i])
            if not s:
                continue
            try:
                sym = eval(s, dglobals, dlocals)
            except NameError:
                try:
                    sym = __import__(s, dglobals, dlocals, [])
                    dglobals[s] = sym
                except ImportError:
                    pass

            except AttributeError:
                try:
                    sym = __import__(s, dglobals, dlocals, [])
                except ImportError:
                    pass

    return sym


def _import_modules(imports, dglobals):
    """If given, execute import statements"""
    if imports is not None:
        for stmt in imports:
            try:
                exec stmt in dglobals
            except TypeError:
                raise TypeError('invalid type: %s' % stmt)
            except Exception:
                continue

    return


def get_all_completions(s, imports=None):
    """Return contextual completion of s (string of >= zero chars)"""
    dlocals = {}
    _import_modules(imports, globals())
    dots = s.rsplit('.', 1)
    sym = None
    for i in range(1, len(dots)):
        s = ('.').join(dots[:i])
        if not s:
            continue
        try:
            try:
                s = unicode(s)
                if s.startswith('PyQt4.') and s.endswith('()'):
                    s = s[:-2]
                sym = eval(s, globals(), dlocals)
            except NameError:
                try:
                    sym = __import__(s, globals(), dlocals, [])
                except ImportError:
                    if s.find('(') != -1 and s[(-1)] == ')':
                        s = s[:s.index('(')]
                    sym = eval(s, globals(), dlocals)
                except AttributeError:
                    try:
                        sym = __import__(s, globals(), dlocals, [])
                    except ImportError:
                        pass

        except (AttributeError, NameError, TypeError, SyntaxError):
            return {}

    if sym is not None:
        var = s
        s = dots[(-1)]
        return get_completions_per_type([ '%s.%s' % (var, k) for k in dir(sym) if k.startswith(s)
                                        ])
    return {}


def _find_constructor(class_ob):
    try:
        return class_ob.__init__.im_func
    except AttributeError:
        for base in class_ob.__bases__:
            rc = _find_constructor(base)
            if rc is not None:
                return rc

    return