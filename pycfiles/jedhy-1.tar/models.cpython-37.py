# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ekas/dev/jedhy/jedhy/models.hy
# Compiled at: 2019-06-05 15:22:23
# Size of source mod 2**32: 7147 bytes
"""Implements Namespace-dependent methods and structures."""
import hy.macros
from hy import HyExpression, HyList, HySymbol
from hy.core.language import butlast, chain, distinct, eval, is_instance, is_none, last, mangle, read_str, unmangle
hy.macros.require('jedhy.macros', None, assignments='ALL', prefix='')
from jedhy.macros import *
import builtins, hy, hy.compiler, hy.macros
import hy.compiler as _compile_table
from hy.core.language import *
from hy.core.macros import *
hy.eval(HyExpression([] + [HySymbol('import')] + [HySymbol('hy.macros')]))
hy.eval(HyExpression([] + [HySymbol('require')] + [HyList([] + [HySymbol('hy.extra.anaphoric')] + [HyList([] + [HySymbol('*')])])]))
from jedhy.macros import mangle

class Namespace(object):

    def __init__(self, globals_=None, locals_=None, macros_=None):
        self.globals = globals_ or globals()
        self.locals = locals_ or locals()
        self.macros = tz.keymap(unmangle, macros_ or __macros__)
        self.compile_table = self._collect_compile_table()
        self.shadows = self._collect_shadows()
        self.names = self._collect_names()
        return None

    @staticmethod
    def _to_names(key):
        """Function for converting keys (strs, functions, modules...) to names."""
        return unmangle(key if is_instance(str, key) else key.__name__)

    def _collect_compile_table(self):
        """Collect compile table as dict."""
        return tz.keymap(self._to_names, _compile_table)

    def _collect_shadows(self):
        """Collect shadows as a list, purely for annotation checks."""
        return tuple(map(self._to_names, dir(hy.core.shadow)))

    def _collect_names(self):
        """Collect all names from all places."""
        return tuple(distinct(map(self._to_names, chain(allkeys(self.globals), allkeys(self.locals), self.macros.keys(), self.compile_table.keys()))))

    def eval(self, mangled_symbol):
        """Evaluate `mangled-symbol' within the Namespace."""
        if not mangled_symbol:
            return None
            _hy_anon_var_6 = None
        else:
            _hy_anon_var_6 = None
        hy_tree = read_str(mangled_symbol)
        try:
            _hy_anon_var_7 = hy.eval(hy_tree, locals=(self.globals))
        except NameError as e:
            try:
                try:
                    _hy_anon_var_8 = hy.eval(hy_tree, locals=(self.locals))
                except:
                    _hy_anon_var_8 = None

                _hy_anon_var_7 = _hy_anon_var_8
            finally:
                e = None
                del e

        return _hy_anon_var_7


class Candidate(object):

    def __init__(self, symbol, namespace=None):
        self.symbol = unmangle(symbol)
        self.mangled = mangle(symbol)
        self.namespace = namespace or Namespace()
        return None

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return 'Candidate<(symbol={}>)'.format(self.symbol)

    def __eq__(self, other):
        if is_instance(Candidate, other):
            return self.symbol == other.symbol
        return None

    def __bool__(self):
        return bool(self.symbol)

    def is_compiler(self):
        """Is candidate a compile table construct and return it."""
        try:
            _hy_anon_var_15 = self.namespace.compile_table[self.symbol]
        except KeyError as e:
            try:
                _hy_anon_var_15 = None
            finally:
                e = None
                del e

        return _hy_anon_var_15

    def is_macro(self):
        """Is candidate a macro and return it."""
        try:
            _hy_anon_var_17 = self.namespace.macros[self.symbol]
        except KeyError as e:
            try:
                _hy_anon_var_17 = None
            finally:
                e = None
                del e

        return _hy_anon_var_17

    def is_evaled(self):
        """Is candidate evaluatable and return it."""
        try:
            _hy_anon_var_19 = self.namespace.eval(self.symbol)
        except Exception as e:
            try:
                _hy_anon_var_19 = None
            finally:
                e = None
                del e

        return _hy_anon_var_19

    def is_shadow(self):
        """Is candidate a shadowed operator, do *not* return it."""
        return self.symbol in self.namespace.shadows or None

    def get_obj(self):
        """Get object for underlying candidate."""
        return self.is_macro() or self.is_evaled() or self.is_compiler()

    def attributes(self):
        """Return attributes for obj if they exist."""
        obj = self.is_evaled()
        if obj:
            return tuple(map(unmangle, dir(obj)))
        return None

    @staticmethod
    def _translate_class(klass):
        """Return annotation given a name of a class."""
        if klass in ('function', 'builtin_function_or_method'):
            return 'def'
        if klass == 'type':
            return 'class'
        if klass == 'module':
            return 'module'
        return 'instance'

    def annotate(self):
        """Return annotation for a candidate."""
        obj = self.is_evaled()
        is_obj = not is_none(obj)
        annotation = 'shadowed' if self.is_shadow() else self._translate_class(obj.__class__.__name__) if is_obj else 'compiler' if self.is_compiler() else 'macro' if self.is_macro() else None
        return '<{} {}>'.format(annotation, self)


class Prefix(object):
    __doc__ = 'A completion candidate.'

    def __init__(self, prefix, namespace=None):
        self.prefix = prefix
        self.namespace = namespace or Namespace()
        self.candidate = self._hyx_prefix_XgreaterHthan_signXcandidate(prefix, self.namespace)
        self.attr_prefix = self._hyx_prefix_XgreaterHthan_signXattr_prefix(prefix)
        self.completions = tuple()
        return None

    def __repr__(self):
        return 'Prefix<(prefix={})>'.format(self.prefix)

    @staticmethod
    def _hyx_prefix_XgreaterHthan_signXcandidate(prefix, namespace):
        return Candidate(('.'.join(butlast(prefix.split('.')))), namespace=namespace)

    @staticmethod
    def _hyx_prefix_XgreaterHthan_signXattr_prefix(prefix):
        """Get prefix as str of everything after last dot if a dot is there."""
        return lambda hyx_Xpercent_signX1:         if hyx_Xpercent_signX1 == '_':
'-' # Avoid dead code: hyx_Xpercent_signX1(unmangle(last(prefix.split('.'))))

    @property
    def is_has_attr(self):
        """Does prefix reference an attr?"""
        return '.' in self.prefix

    @property
    def is_obj(self):
        """Is the prefix's candidate an object?"""
        return bool(self.candidate.get_obj())

    def complete_candidate(self, completion):
        """Given a potential string `completion`, attach to candidate."""
        if self.candidate:
            return str(self.candidate) + '.' + completion
        return completion

    def complete(self, cached_prefix=None):
        """Get candidates for a given Prefix."""
        if self.is_has_attr:
            self.completions = self.is_obj or tuple()
            return self.completions
            _hy_anon_var_33 = None
        else:
            _hy_anon_var_33 = None
        if cached_prefix and self.candidate == cached_prefix.candidate:
            self.completions = cached_prefix.completions
            _hy_anon_var_34 = None
        else:
            self.completions = self.candidate.attributes() or self.namespace.names
            _hy_anon_var_34 = None
        return tuple(map(self.complete_candidate, filter(tz.flip(str.startswith, self.attr_prefix), self.completions)))