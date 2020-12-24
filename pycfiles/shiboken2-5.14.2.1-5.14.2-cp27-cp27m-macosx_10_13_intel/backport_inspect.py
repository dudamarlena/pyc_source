# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qt/work/pyside/pyside-setup/pyside2_install/py2.7-qt5.14.2-64bit-release/lib/python2.7/site-packages/shiboken2/files.dir/shibokensupport/backport_inspect.py
# Compiled at: 2020-04-24 02:55:46
from __future__ import print_function
__doc__ = '\n    signature() - get a Signature object for the callable\n'
import sys
from collections import OrderedDict
CO_OPTIMIZED = 1
CO_NEWLOCALS = 2
CO_VARARGS = 4
CO_VARKEYWORDS = 8
CO_NESTED = 16
CO_GENERATOR = 32
CO_NOFREE = 64

def formatannotation(annotation, base_module=None):
    if getattr(annotation, '__module__', None) == 'typing':
        return repr(annotation)
    else:
        if isinstance(annotation, type):
            if annotation.__module__ in ('__builtin__', base_module):
                return annotation.__name__
            return annotation.__module__ + '.' + annotation.__name__
        return repr(annotation)


def _signature_is_functionlike(obj):
    """Private helper to test if `obj` is a duck type of FunctionType.
    A good example of such objects are functions compiled with
    Cython, which have all attributes that a pure Python function
    would have, but have their code statically compiled.
    """
    if not callable(obj) or isclass(obj):
        return False
    name = getattr(obj, '__name__', None)
    code = getattr(obj, '__code__', None)
    defaults = getattr(obj, '__defaults__', _void)
    kwdefaults = getattr(obj, '__kwdefaults__', _void)
    annotations = getattr(obj, '__annotations__', None)
    return isinstance(code, types.CodeType) and isinstance(name, str) and (defaults is None or isinstance(defaults, tuple)) and (kwdefaults is None or isinstance(kwdefaults, dict)) and isinstance(annotations, dict)


def _signature_from_function(cls, func):
    """Private helper: constructs Signature for the given python function."""
    is_duck_function = False
    if not isfunction(func):
        if _signature_is_functionlike(func):
            is_duck_function = True
        else:
            raise TypeError(('{!r} is not a Python function').format(func))
    Parameter = cls._parameter_cls
    func_code = func.__code__
    pos_count = func_code.co_argcount
    arg_names = func_code.co_varnames
    positional = tuple(arg_names[:pos_count])
    keyword_only_count = 0
    keyword_only = arg_names[pos_count:pos_count + keyword_only_count]
    annotations = func.__annotations__
    defaults = func.__defaults__
    kwdefaults = func.__kwdefaults__
    if defaults:
        pos_default_count = len(defaults)
    else:
        pos_default_count = 0
    parameters = []
    non_default_count = pos_count - pos_default_count
    for name in positional[:non_default_count]:
        annotation = annotations.get(name, _empty)
        parameters.append(Parameter(name, annotation=annotation, kind=_POSITIONAL_OR_KEYWORD))

    for offset, name in enumerate(positional[non_default_count:]):
        annotation = annotations.get(name, _empty)
        parameters.append(Parameter(name, annotation=annotation, kind=_POSITIONAL_OR_KEYWORD, default=defaults[offset]))

    if func_code.co_flags & CO_VARARGS:
        name = arg_names[(pos_count + keyword_only_count)]
        annotation = annotations.get(name, _empty)
        parameters.append(Parameter(name, annotation=annotation, kind=_VAR_POSITIONAL))
    for name in keyword_only:
        default = _empty
        if kwdefaults is not None:
            default = kwdefaults.get(name, _empty)
        annotation = annotations.get(name, _empty)
        parameters.append(Parameter(name, annotation=annotation, kind=_KEYWORD_ONLY, default=default))

    if func_code.co_flags & CO_VARKEYWORDS:
        index = pos_count + keyword_only_count
        if func_code.co_flags & CO_VARARGS:
            index += 1
        name = arg_names[index]
        annotation = annotations.get(name, _empty)
        parameters.append(Parameter(name, annotation=annotation, kind=_VAR_KEYWORD))
    return cls(parameters, return_annotation=annotations.get('return', _empty), __validate_parameters__=is_duck_function)


class _void(object):
    """A private marker - used in Parameter & Signature."""
    pass


class _empty(object):
    """Marker object for Signature.empty and Parameter.empty."""
    pass


class _ParameterKind(object):
    POSITIONAL_ONLY = 0
    POSITIONAL_OR_KEYWORD = 1
    VAR_POSITIONAL = 2
    KEYWORD_ONLY = 3
    VAR_KEYWORD = 4

    def __str__(self):
        return self._name_


_POSITIONAL_ONLY = _ParameterKind.POSITIONAL_ONLY
_POSITIONAL_OR_KEYWORD = _ParameterKind.POSITIONAL_OR_KEYWORD
_VAR_POSITIONAL = _ParameterKind.VAR_POSITIONAL
_KEYWORD_ONLY = _ParameterKind.KEYWORD_ONLY
_VAR_KEYWORD = _ParameterKind.VAR_KEYWORD

class Parameter(object):
    """Represents a parameter in a function signature.

    Has the following public attributes:

    * name : str
        The name of the parameter as a string.
    * default : object
        The default value for the parameter if specified.  If the
        parameter has no default value, this attribute is set to
        `Parameter.empty`.
    * annotation
        The annotation for the parameter if specified.  If the
        parameter has no annotation, this attribute is set to
        `Parameter.empty`.
    * kind : str
        Describes how argument values are bound to the parameter.
        Possible values: `Parameter.POSITIONAL_ONLY`,
        `Parameter.POSITIONAL_OR_KEYWORD`, `Parameter.VAR_POSITIONAL`,
        `Parameter.KEYWORD_ONLY`, `Parameter.VAR_KEYWORD`.
    """
    __slots__ = ('_name', '_kind', '_default', '_annotation')
    POSITIONAL_ONLY = _POSITIONAL_ONLY
    POSITIONAL_OR_KEYWORD = _POSITIONAL_OR_KEYWORD
    VAR_POSITIONAL = _VAR_POSITIONAL
    KEYWORD_ONLY = _KEYWORD_ONLY
    VAR_KEYWORD = _VAR_KEYWORD
    empty = _empty

    def __init__(self, name, kind, default=_empty, annotation=_empty):
        if kind not in (_POSITIONAL_ONLY, _POSITIONAL_OR_KEYWORD,
         _VAR_POSITIONAL, _KEYWORD_ONLY, _VAR_KEYWORD):
            raise ValueError("invalid value for 'Parameter.kind' attribute")
        self._kind = kind
        if default is not _empty:
            if kind in (_VAR_POSITIONAL, _VAR_KEYWORD):
                msg = ('{} parameters cannot have default values').format(kind)
                raise ValueError(msg)
        self._default = default
        self._annotation = annotation
        if name is _empty:
            raise ValueError('name is a required attribute for Parameter')
        if not isinstance(name, str):
            raise TypeError(('name must be a str, not a {!r}').format(name))
        if name[0] == '.' and name[1:].isdigit():
            if kind != _POSITIONAL_OR_KEYWORD:
                raise ValueError(('implicit arguments must be passed in as {}').format(_POSITIONAL_OR_KEYWORD))
            self._kind = _POSITIONAL_ONLY
            name = ('implicit{}').format(name[1:])
        if not True:
            raise ValueError(('{!r} is not a valid parameter name').format(name))
        self._name = name

    def __reduce__(self):
        return (
         type(self),
         (
          self._name, self._kind),
         {'_default': self._default, '_annotation': self._annotation})

    def __setstate__(self, state):
        self._default = state['_default']
        self._annotation = state['_annotation']

    @property
    def name(self):
        return self._name

    @property
    def default(self):
        return self._default

    @property
    def annotation(self):
        return self._annotation

    @property
    def kind(self):
        return self._kind

    def replace(self, name=_void, kind=_void, annotation=_void, default=_void):
        """Creates a customized copy of the Parameter."""
        if name is _void:
            name = self._name
        if kind is _void:
            kind = self._kind
        if annotation is _void:
            annotation = self._annotation
        if default is _void:
            default = self._default
        return type(self)(name, kind, default=default, annotation=annotation)

    def __str__(self):
        kind = self.kind
        formatted = self._name
        if self._annotation is not _empty:
            formatted = ('{}: {}').format(formatted, formatannotation(self._annotation))
        if self._default is not _empty:
            formatted = ('{}={}').format(formatted, repr(self._default))
        if kind == _VAR_POSITIONAL:
            formatted = '*' + formatted
        elif kind == _VAR_KEYWORD:
            formatted = '**' + formatted
        return formatted

    def __repr__(self):
        return ('<{} "{}">').format(self.__class__.__name__, self)

    def __hash__(self):
        return hash((self.name, self.kind, self.annotation, self.default))

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Parameter):
            return NotImplemented
        return self._name == other._name and self._kind == other._kind and self._default == other._default and self._annotation == other._annotation


class BoundArguments(object):
    """Result of `Signature.bind` call.  Holds the mapping of arguments
    to the function's parameters.

    Has the following public attributes:

    * arguments : OrderedDict
        An ordered mutable mapping of parameters' names to arguments' values.
        Does not contain arguments' default values.
    * signature : Signature
        The Signature object that created this instance.
    * args : tuple
        Tuple of positional arguments values.
    * kwargs : dict
        Dict of keyword arguments values.
    """
    __slots__ = ('arguments', '_signature', '__weakref__')

    def __init__(self, signature, arguments):
        self.arguments = arguments
        self._signature = signature

    @property
    def signature(self):
        return self._signature

    @property
    def args(self):
        args = []
        for param_name, param in self._signature.parameters.items():
            if param.kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
                break
            try:
                arg = self.arguments[param_name]
            except KeyError:
                break
            else:
                if param.kind == _VAR_POSITIONAL:
                    args.extend(arg)
                else:
                    args.append(arg)

        return tuple(args)

    @property
    def kwargs(self):
        kwargs = {}
        kwargs_started = False
        for param_name, param in self._signature.parameters.items():
            if not kwargs_started:
                if param.kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
                    kwargs_started = True
                elif param_name not in self.arguments:
                    kwargs_started = True
                    continue
            if not kwargs_started:
                continue
            try:
                arg = self.arguments[param_name]
            except KeyError:
                pass
            else:
                if param.kind == _VAR_KEYWORD:
                    kwargs.update(arg)
                else:
                    kwargs[param_name] = arg

        return kwargs

    def apply_defaults(self):
        """Set default values for missing arguments.

        For variable-positional arguments (*args) the default is an
        empty tuple.

        For variable-keyword arguments (**kwargs) the default is an
        empty dict.
        """
        arguments = self.arguments
        new_arguments = []
        for name, param in self._signature.parameters.items():
            try:
                new_arguments.append((name, arguments[name]))
            except KeyError:
                if param.default is not _empty:
                    val = param.default
                elif param.kind is _VAR_POSITIONAL:
                    val = ()
                elif param.kind is _VAR_KEYWORD:
                    val = {}
                else:
                    continue
                new_arguments.append((name, val))

        self.arguments = OrderedDict(new_arguments)

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, BoundArguments):
            return NotImplemented
        return self.signature == other.signature and self.arguments == other.arguments

    def __setstate__(self, state):
        self._signature = state['_signature']
        self.arguments = state['arguments']

    def __getstate__(self):
        return {'_signature': self._signature, 'arguments': self.arguments}

    def __repr__(self):
        args = []
        for arg, value in self.arguments.items():
            args.append(('{}={!r}').format(arg, value))

        return ('<{} ({})>').format(self.__class__.__name__, (', ').join(args))


class Signature(object):
    """A Signature object represents the overall signature of a function.
    It stores a Parameter object for each parameter accepted by the
    function, as well as information specific to the function itself.

    A Signature object has the following public attributes and methods:

    * parameters : OrderedDict
        An ordered mapping of parameters' names to the corresponding
        Parameter objects (keyword-only arguments are in the same order
        as listed in `code.co_varnames`).
    * return_annotation : object
        The annotation for the return type of the function if specified.
        If the function has no annotation for its return type, this
        attribute is set to `Signature.empty`.
    * bind(*args, **kwargs) -> BoundArguments
        Creates a mapping from positional and keyword arguments to
        parameters.
    * bind_partial(*args, **kwargs) -> BoundArguments
        Creates a partial mapping from positional and keyword arguments
        to parameters (simulating 'functools.partial' behavior.)
    """
    __slots__ = ('_return_annotation', '_parameters')
    _parameter_cls = Parameter
    _bound_arguments_cls = BoundArguments
    empty = _empty

    def __init__(self, parameters=None, return_annotation=_empty, __validate_parameters__=True):
        """Constructs Signature from the given list of Parameter
        objects and 'return_annotation'.  All arguments are optional.
        """
        if parameters is None:
            params = OrderedDict()
        elif __validate_parameters__:
            params = OrderedDict()
            top_kind = _POSITIONAL_ONLY
            kind_defaults = False
            for idx, param in enumerate(parameters):
                kind = param.kind
                name = param.name
                if kind < top_kind:
                    msg = 'wrong parameter order: {!r} before {!r}'
                    msg = msg.format(top_kind, kind)
                    raise ValueError(msg)
                elif kind > top_kind:
                    kind_defaults = False
                    top_kind = kind
                if kind in (_POSITIONAL_ONLY, _POSITIONAL_OR_KEYWORD):
                    if param.default is _empty:
                        if kind_defaults:
                            msg = 'non-default argument follows default argument'
                            raise ValueError(msg)
                    else:
                        kind_defaults = True
                if name in params:
                    msg = ('duplicate parameter name: {!r}').format(name)
                    raise ValueError(msg)
                params[name] = param

        else:
            params = OrderedDict((param.name, param) for param in parameters)
        self._parameters = params
        self._return_annotation = return_annotation
        return

    @classmethod
    def from_function(cls, func):
        """Constructs Signature for the given python function."""
        warnings.warn('inspect.Signature.from_function() is deprecated, use Signature.from_callable()', DeprecationWarning, stacklevel=2)
        return _signature_from_function(cls, func)

    @classmethod
    def from_builtin(cls, func):
        """Constructs Signature for the given builtin function."""
        warnings.warn('inspect.Signature.from_builtin() is deprecated, use Signature.from_callable()', DeprecationWarning, stacklevel=2)
        return _signature_from_builtin(cls, func)

    @classmethod
    def from_callable(cls, obj, follow_wrapped=True):
        """Constructs Signature for the given callable object."""
        return _signature_from_callable(obj, sigcls=cls, follow_wrapper_chains=follow_wrapped)

    @property
    def parameters(self):
        return self._parameters

    @property
    def return_annotation(self):
        return self._return_annotation

    def replace(self, parameters=_void, return_annotation=_void):
        """Creates a customized copy of the Signature.
        Pass 'parameters' and/or 'return_annotation' arguments
        to override them in the new copy.
        """
        if parameters is _void:
            parameters = self.parameters.values()
        if return_annotation is _void:
            return_annotation = self._return_annotation
        return type(self)(parameters, return_annotation=return_annotation)

    def _hash_basis(self):
        params = tuple(param for param in self.parameters.values() if param.kind != _KEYWORD_ONLY)
        kwo_params = {param.name:param for param in self.parameters.values() if param.kind == _KEYWORD_ONLY if param.kind == _KEYWORD_ONLY}
        return (
         params, kwo_params, self.return_annotation)

    def __hash__(self):
        params, kwo_params, return_annotation = self._hash_basis()
        kwo_params = frozenset(kwo_params.values())
        return hash((params, kwo_params, return_annotation))

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Signature):
            return NotImplemented
        return self._hash_basis() == other._hash_basis()

    def _bind(self, args, kwargs, partial=False):
        """Private method. Don't use directly."""
        arguments = OrderedDict()
        parameters = iter(self.parameters.values())
        parameters_ex = ()
        arg_vals = iter(args)
        while True:
            try:
                arg_val = next(arg_vals)
            except StopIteration:
                try:
                    param = next(parameters)
                except StopIteration:
                    break
                else:
                    if param.kind == _VAR_POSITIONAL:
                        break
                    elif param.name in kwargs:
                        if param.kind == _POSITIONAL_ONLY:
                            msg = '{arg!r} parameter is positional only, but was passed as a keyword'
                            msg = msg.format(arg=param.name)
                            raise TypeError(msg)
                        parameters_ex = (
                         param,)
                        break
                    elif param.kind == _VAR_KEYWORD or param.default is not _empty:
                        parameters_ex = (
                         param,)
                        break
                    elif partial:
                        parameters_ex = (
                         param,)
                        break
                    else:
                        msg = 'missing a required argument: {arg!r}'
                        msg = msg.format(arg=param.name)
                        raise TypeError(msg)
            else:
                try:
                    param = next(parameters)
                except StopIteration:
                    raise TypeError('too many positional arguments')
                else:
                    if param.kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
                        raise TypeError('too many positional arguments')
                    if param.kind == _VAR_POSITIONAL:
                        values = [
                         arg_val]
                        values.extend(arg_vals)
                        arguments[param.name] = tuple(values)
                        break
                    if param.name in kwargs:
                        raise TypeError(('multiple values for argument {arg!r}').format(arg=param.name))
                    arguments[param.name] = arg_val

        kwargs_param = None
        for param in itertools.chain(parameters_ex, parameters):
            if param.kind == _VAR_KEYWORD:
                kwargs_param = param
                continue
            if param.kind == _VAR_POSITIONAL:
                continue
            param_name = param.name
            try:
                arg_val = kwargs.pop(param_name)
            except KeyError:
                if not partial and param.kind != _VAR_POSITIONAL and param.default is _empty:
                    raise TypeError(('missing a required argument: {arg!r}').format(arg=param_name))
            else:
                if param.kind == _POSITIONAL_ONLY:
                    raise TypeError(('{arg!r} parameter is positional only, but was passed as a keyword').format(arg=param.name))
                arguments[param_name] = arg_val

        if kwargs:
            if kwargs_param is not None:
                arguments[kwargs_param.name] = kwargs
            else:
                raise TypeError(('got an unexpected keyword argument {arg!r}').format(arg=next(iter(kwargs))))
        return self._bound_arguments_cls(self, arguments)

    def bind(*args, **kwargs):
        """Get a BoundArguments object, that maps the passed `args`
        and `kwargs` to the function's signature.  Raises `TypeError`
        if the passed arguments can not be bound.
        """
        return args[0]._bind(args[1:], kwargs)

    def bind_partial(*args, **kwargs):
        """Get a BoundArguments object, that partially maps the
        passed `args` and `kwargs` to the function's signature.
        Raises `TypeError` if the passed arguments can not be bound.
        """
        return args[0]._bind(args[1:], kwargs, partial=True)

    def __reduce__(self):
        return (
         type(self),
         (
          tuple(self._parameters.values()),), {'_return_annotation': self._return_annotation})

    def __setstate__(self, state):
        self._return_annotation = state['_return_annotation']

    def __repr__(self):
        return ('<{} {}>').format(self.__class__.__name__, self)

    def __str__(self):
        result = []
        render_pos_only_separator = False
        render_kw_only_separator = True
        for param in self.parameters.values():
            formatted = str(param)
            kind = param.kind
            if kind == _POSITIONAL_ONLY:
                render_pos_only_separator = True
            elif render_pos_only_separator:
                result.append('/')
                render_pos_only_separator = False
            if kind == _VAR_POSITIONAL:
                render_kw_only_separator = False
            elif kind == _KEYWORD_ONLY and render_kw_only_separator:
                result.append('*')
                render_kw_only_separator = False
            result.append(formatted)

        if render_pos_only_separator:
            result.append('/')
        rendered = ('({})').format((', ').join(result))
        if self.return_annotation is not _empty:
            anno = formatannotation(self.return_annotation)
            rendered += (' -> {}').format(anno)
        return rendered


def signature(obj, follow_wrapped=True):
    """Get a signature object for the passed callable."""
    return Signature.from_callable(obj, follow_wrapped=follow_wrapped)