# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/tales/expressions.py
# Compiled at: 2007-12-02 16:26:58
"""Basic Page Template expression types.

$Id: expressions.py 40271 2005-11-20 13:35:28Z shh $
"""
import re
from salamoia.tales.tales import _valid_name, _parse_expr, NAME_RE, Undefined
Undefs = (
 Undefined, AttributeError, KeyError, TypeError, IndexError)
_marker = object()
namespace_re = re.compile('(\\w+):(.+)')

def simpleTraverse(object, path_items, econtext):
    """Traverses a sequence of names, first trying attributes then items.
    """
    for name in path_items:
        next = getattr(object, name, _marker)
        if next is not _marker:
            object = next
        elif hasattr(object, '__getitem__'):
            object = object[name]
        else:
            object = getattr(object, name)

    return object


class SubPathExpr(object):
    __module__ = __name__

    def __init__(self, path, traverser, engine):
        self._traverser = traverser
        self._engine = engine
        compiledpath = []
        currentpath = []
        for element in str(path).strip().split('/'):
            if not element:
                raise engine.getCompilerError()('Path element may not be empty in %r' % path)
            if element.startswith('?'):
                if currentpath:
                    compiledpath.append(tuple(currentpath))
                    currentpath = []
                if not _valid_name(element[1:]):
                    raise engine.getCompilerError()('Invalid variable name "%s"' % element[1:])
                compiledpath.append(element[1:])
            else:
                match = namespace_re.match(element)
                if match:
                    if currentpath:
                        compiledpath.append(tuple(currentpath))
                        currentpath = []
                    (namespace, functionname) = match.groups()
                    if not _valid_name(namespace):
                        raise engine.getCompilerError()('Invalid namespace name "%s"' % namespace)
                    try:
                        compiledpath.append(self._engine.getFunctionNamespace(namespace))
                    except KeyError:
                        raise engine.getCompilerError()('Unknown namespace "%s"' % namespace)
                    else:
                        currentpath.append(functionname)
                else:
                    currentpath.append(element)

        if currentpath:
            compiledpath.append(tuple(currentpath))
        first = compiledpath[0]
        base = first[0]
        if callable(first):
            raise engine.getCompilerError()('Namespace function specified in first subpath element')
        elif isinstance(first, basestring):
            raise engine.getCompilerError()('Dynamic name specified in first subpath element')
        if base and not _valid_name(base):
            raise engine.getCompilerError()('Invalid variable name "%s"' % element)
        self._base = base
        compiledpath[0] = first[1:]
        self._compiled_path = tuple(compiledpath)

    def _eval(self, econtext, isinstance=isinstance):
        vars = econtext.vars
        compiled_path = self._compiled_path
        base = self._base
        if base == 'CONTEXTS' or not base:
            ob = econtext.contexts
        else:
            ob = vars[base]
        if isinstance(ob, DeferWrapper):
            ob = ob()
        for element in compiled_path:
            if isinstance(element, tuple):
                ob = self._traverser(ob, element, econtext)
            elif isinstance(element, basestring):
                val = vars[element]
                if isinstance(val, basestring):
                    val = (
                     val,)
                ob = self._traverser(ob, val, econtext)
            elif callable(element):
                ob = element(ob)
                if ITALESFunctionNamespace.providedBy(ob):
                    ob.setEngine(econtext)
            else:
                raise ValueError(repr(element))

        return ob


class PathExpr(object):
    """One or more subpath expressions, separated by '|'."""
    __module__ = __name__
    _default_type_names = ('standard', 'path', 'exists', 'nocall')

    def __init__(self, name, expr, engine, traverser=simpleTraverse):
        self._s = expr
        self._name = name
        paths = expr.split('|')
        self._subexprs = []
        add = self._subexprs.append
        for i in range(len(paths)):
            path = paths[i].lstrip()
            if _parse_expr(path):
                add(engine.compile(('|').join(paths[i:]).lstrip()))
                break
            add(SubPathExpr(path, traverser, engine)._eval)

    def _exists(self, econtext):
        for expr in self._subexprs:
            try:
                expr(econtext)
            except Undefs:
                pass
            else:
                return 1

        return 0

    def _eval(self, econtext):
        for expr in self._subexprs[:-1]:
            try:
                ob = expr(econtext)
            except Undefs:
                pass
            else:
                break
        else:
            ob = self._subexprs[(-1)](econtext)

        if self._name == 'nocall':
            return ob
        if hasattr(ob, '__call__'):
            return ob()
        return ob

    def __call__(self, econtext):
        if self._name == 'exists':
            return self._exists(econtext)
        return self._eval(econtext)

    def __str__(self):
        return '%s expression (%s)' % (self._name, `(self._s)`)

    def __repr__(self):
        return '<PathExpr %s:%s>' % (self._name, `(self._s)`)


_interp = re.compile('\\$(%(n)s)|\\${(%(n)s(?:/[^}]*)*)}' % {'n': NAME_RE})

class StringExpr(object):
    __module__ = __name__

    def __init__(self, name, expr, engine):
        self._s = expr
        if '%' in expr:
            expr = expr.replace('%', '%%')
        self._vars = vars = []
        if '$' in expr:
            path_type = engine.getTypes()['path']
            parts = []
            for exp in expr.split('$$'):
                if parts:
                    parts.append('$')
                m = _interp.search(exp)
                while m is not None:
                    parts.append(exp[:m.start()])
                    parts.append('%s')
                    vars.append(path_type('path', m.group(1) or m.group(2), engine))
                    exp = exp[m.end():]
                    m = _interp.search(exp)

                if '$' in exp:
                    raise engine.getCompilerError()('$ must be doubled or followed by a simple path')
                parts.append(exp)

            expr = ('').join(parts)
        self._expr = expr
        return

    def __call__(self, econtext):
        vvals = []
        for var in self._vars:
            v = var(econtext)
            vvals.append(v)

        return self._expr % tuple(vvals)

    def __str__(self):
        return 'string expression (%s)' % `(self._s)`

    def __repr__(self):
        return '<StringExpr %s>' % `(self._s)`


class NotExpr(object):
    __module__ = __name__

    def __init__(self, name, expr, engine):
        self._s = expr = expr.lstrip()
        self._c = engine.compile(expr)

    def __call__(self, econtext):
        return int(not econtext.evaluateBoolean(self._c))

    def __repr__(self):
        return '<NotExpr %s>' % `(self._s)`


class DeferWrapper(object):
    __module__ = __name__

    def __init__(self, expr, econtext):
        self._expr = expr
        self._econtext = econtext

    def __str__(self):
        return str(self())

    def __call__(self):
        return self._expr(self._econtext)


class DeferExpr(object):
    __module__ = __name__

    def __init__(self, name, expr, compiler):
        self._s = expr = expr.lstrip()
        self._c = compiler.compile(expr)

    def __call__(self, econtext):
        return DeferWrapper(self._c, econtext)

    def __repr__(self):
        return '<DeferExpr %s>' % `(self._s)`


class SimpleModuleImporter(object):
    """Minimal module importer with no security."""
    __module__ = __name__

    def __getitem__(self, module):
        mod = self._get_toplevel_module(module)
        path = module.split('.')
        for name in path[1:]:
            mod = getattr(mod, name)

        return mod

    def _get_toplevel_module(self, module):
        return __import__(module)


from salamoia.tests import *
runDocTests()