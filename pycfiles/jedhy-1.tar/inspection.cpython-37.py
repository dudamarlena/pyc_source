# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ekas/dev/jedhy/jedhy/inspection.hy
# Compiled at: 2019-06-05 15:54:00
# Size of source mod 2**32: 8765 bytes
"""Implements argspec inspection and formatting for various types."""
import hy.macros
from hy.core.language import comp, drop, drop_last, first, flatten, inc, is_instance, is_none, juxt, reduce, remove, repeat, rest, second, unmangle
from hy.core.shadow import _, hyx_in
hy.macros.require('jedhy.macros', None, assignments='ALL', prefix='')
from jedhy.macros import *
import inspect, hy

class Parameter(object):

    def __init__(self, symbol, default=None):
        self.symbol = unmangle(symbol)
        self.default = default
        return None

    def __str__(self):
        if is_none(self.default):
            return self.symbol
        return '[{} {}]'.format(self.symbol, self.default)


class Signature(object):

    def __init__(self, func):
        try:
            argspec = inspect.getfullargspec(func)
            _hy_anon_var_3 = None
        except TypeError as e:
            try:
                raise TypeError('Unsupported callable for hy Signature.')
                _hy_anon_var_3 = None
            finally:
                e = None
                del e

        self.func = func
        self.args, self.defaults, self.kwargs, self.varargs, self.varkw = juxt(self._args_from, self._defaults_from, self._kwargs_from, self._varargs_from, self._varkw_from)(argspec)
        return None

    @staticmethod
    def _parametrize(symbols, defaults=None):
        """Construct many Parameter for `symbols` with possibly defaults."""
        if symbols:
            return tuple(map(Parameter, symbols, defaults or repeat(None)))
        return None

    @classmethod
    def _args_from(cls, argspec):
        """Extract args without defined defaults from `argspec`."""
        symbols = drop_last(len(argspec.defaults or []), argspec.args)
        return cls._parametrize(symbols)

    @classmethod
    def _defaults_from(cls, argspec):
        """Extract args with defined defaults from `argspec`."""
        args_without_defaults = cls._args_from(argspec)
        symbols = drop(len(args_without_defaults), argspec.args)
        return cls._parametrize(symbols, argspec.defaults)

    @classmethod
    def _kwargsonly_from(cls, argspec):
        """Extract kwargs without defined defaults from `argspec`."""
        kwargs_with_defaults = (argspec.kwonlydefaults or {}).keys()
        symbols = remove(tz.flip(hyx_in, kwargs_with_defaults), argspec.kwonlyargs)
        return cls._parametrize(symbols)

    @classmethod
    def _kwonlydefaults_from(cls, argspec):
        """Extract kwargs with defined defaults from `argspec`."""
        if argspec.kwonlydefaults:
            symbols, defaults = zip(*argspec.kwonlydefaults.items())
            _hy_anon_var_9 = cls._parametrize(symbols, defaults)
        else:
            _hy_anon_var_9 = None
        return _hy_anon_var_9

    @classmethod
    def _kwargs_from(cls, argspec):
        """Chain kwargs with and without defaults, since `argspec` doesn't order."""
        return tuple(remove(is_none, flatten(juxt(cls._kwargsonly_from, cls._kwonlydefaults_from)(argspec))))

    @staticmethod
    def _varargs_from(argspec):
        return argspec.varargs and [unmangle(argspec.varargs)]

    @staticmethod
    def _varkw_from(argspec):
        return argspec.varkw and [unmangle(argspec.varkw)]

    @staticmethod
    def _format_args(args, opener):
        if not args:
            return ''
        _hy_anon_var_14 = None
        args = map(str, args)
        opener = opener + ' ' if opener else str()
        return opener + ' '.join(args)

    @classmethod
    def _acc_lispy_repr(cls, acc, args_opener):
        args, opener = args_opener
        delim = ' ' if (acc and args) else (str())
        return acc + delim + cls._format_args(args, opener)

    @property
    def _arg_opener_pairs(self):
        return [[self.args, None],
         [
          self.defaults, '&optional'],
         [
          self.varargs, '#*'],
         [
          self.varkw, '#**'],
         [
          self.kwargs, '&kwonly']]

    def __str__(self):
        return reduce(self._acc_lispy_repr, self._arg_opener_pairs, str())


def _split_docs(docs):
    """Partition docs string into pre/-/post-args strings."""
    arg_start = inc(docs.index('('))
    arg_end = docs.index(')')
    return [
     docs[0:arg_start:None],
     docs[arg_start:arg_end:None],
     docs[arg_end:None:None]]


def _argstring_to_param(arg_string):
    """Convert an arg string to a Parameter."""
    if '=' not in arg_string:
        return Parameter(arg_string)
    _hy_anon_var_20 = None
    arg_name, _, default = arg_string.partition('=')
    if 'None' == default:
        return Parameter(arg_name)
    return Parameter(arg_name, default)


def _optional_arg_idx(args_strings):
    """First idx of an arg with a default in list of args strings."""

    def _is_at_arg_with_default(idx_arg):
        if '=' in second(idx_arg):
            return first(idx_arg)
        return None

    return first(remove(is_none, map(_is_at_arg_with_default, enumerate(args_strings))))


def _insert_optional(args):
    """Insert &optional into list of args strings."""
    optional_idx = _optional_arg_idx(args)
    args.insert(optional_idx, '&optional') if not is_none(optional_idx) else None
    return args


def builtin_docs_to_lispy_docs(docs):
    """Convert built-in-styled docs string into a lispy-format."""
    return '(' in docs and ')' in docs or docs
    _hy_anon_var_25 = None
    replacements = [
     [
      '...', '#* args'],
     [
      '*args', '#* args'],
     [
      '**kwargs', '#** kwargs'],
     [
      '\n', 'newline'],
     [
      '-->', '- return']]
    pre_args, _, post_args = docs.partition('(')
    pre_args, args, post_args = _split_docs(reduce(lambda s, old_new: s.replace(first(old_new), second(old_new)), replacements, '{}: ({}'.format(pre_args, post_args)))
    args = args
    args = args.split(',')
    args = map(str.strip, args)
    args = list(args)
    args = _insert_optional(args)
    args = map(comp(str, _argstring_to_param), args)
    args = ' '.join(args)
    return pre_args + args + post_args


class Inspect(object):

    def __init__(self, obj):
        self.obj = obj
        return None

    @property
    def _docs_first_line(self):
        return self.obj.__doc__ and first(self.obj.__doc__.splitlines()) or ''

    @property
    def _docs_rest_lines(self):
        return self.obj.__doc__ and '\n'.join(rest(self.obj.__doc__.splitlines())) or ''

    @property
    def _args_docs_delim(self):
        return self.obj.__doc__ and ' - ' or ''

    def _cut_obj_name_maybe(self, docs):
        if self.is_class or self.is_method_wrapper:
            return docs.replace('self ', '').replace('self', '')
        return docs

    def _cut_method_wrapper_maybe(self, docs):
        if self.is_method_wrapper:
            return 'method-wrapper' + docs[docs.index(':'):None:None]
        return docs

    def _format_docs(self, docs):
        return self._cut_method_wrapper_maybe(self._cut_obj_name_maybe(docs))

    @property
    def obj_name(self):
        return unmangle(self.obj.__name__)

    @property
    def is_lambda(self):
        """Is object a lambda?"""
        return self.obj_name == '<lambda>'

    @property
    def is_class(self):
        """Is object a class?"""
        return inspect.isclass(self.obj)

    @property
    def is_method_wrapper(self):
        """Is object of type 'method-wrapper'?"""
        return is_instance(type(print.__str__), self.obj)

    @property
    def is_compile_table(self):
        """Is object a Hy compile table construct?"""
        return self._docs_first_line == 'Built-in immutable sequence.'

    def signature(self):
        """Return object's signature if it exists."""
        try:
            _hy_anon_var_39 = Signature(self.obj)
        except TypeError as e:
            try:
                _hy_anon_var_39 = None
            finally:
                e = None
                del e

        return _hy_anon_var_39

    def docs(self):
        """Formatted first line docs for object."""
        signature = self.signature()
        return self._format_docs('{name}: ({args}){delim}{docs}'.format(name=(self.obj_name),
          args=signature,
          delim=(self._args_docs_delim),
          docs=(self._docs_first_line)) if signature and not self.is_compile_table else ('Compile table' if self.is_compile_table else builtin_docs_to_lispy_docs(self._docs_first_line)))

    def full_docs(self):
        """Formatted full docs for object."""
        if not self.is_compile_table:
            return '{}\n\n{}'.format(self.docs(), self._docs_rest_lines) if self._docs_rest_lines else self.docs()
        return None