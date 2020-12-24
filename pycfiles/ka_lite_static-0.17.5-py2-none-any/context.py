# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/template/context.py
# Compiled at: 2018-07-11 18:15:31
from copy import copy
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
_standard_context_processors = None
_builtin_context_processors = ('django.core.context_processors.csrf', )

class ContextPopException(Exception):
    """pop() has been called more times than push()"""
    pass


class BaseContext(object):

    def __init__(self, dict_=None):
        self._reset_dicts(dict_)

    def _reset_dicts(self, value=None):
        builtins = {'True': True, 'False': False, 'None': None}
        self.dicts = [builtins]
        if value is not None:
            self.dicts.append(value)
        return

    def __copy__(self):
        duplicate = copy(super(BaseContext, self))
        duplicate.dicts = self.dicts[:]
        return duplicate

    def __repr__(self):
        return repr(self.dicts)

    def __iter__(self):
        for d in reversed(self.dicts):
            yield d

    def push(self):
        d = {}
        self.dicts.append(d)
        return d

    def pop(self):
        if len(self.dicts) == 1:
            raise ContextPopException
        return self.dicts.pop()

    def __setitem__(self, key, value):
        """Set a variable in the current context"""
        self.dicts[(-1)][key] = value

    def __getitem__(self, key):
        """Get a variable's value, starting at the current context and going upward"""
        for d in reversed(self.dicts):
            if key in d:
                return d[key]

        raise KeyError(key)

    def __delitem__(self, key):
        """Delete a variable from the current context"""
        del self.dicts[(-1)][key]

    def has_key(self, key):
        for d in self.dicts:
            if key in d:
                return True

        return False

    def __contains__(self, key):
        return self.has_key(key)

    def get(self, key, otherwise=None):
        for d in reversed(self.dicts):
            if key in d:
                return d[key]

        return otherwise

    def new(self, values=None):
        """
        Returns a new context with the same properties, but with only the
        values given in 'values' stored.
        """
        new_context = copy(self)
        new_context._reset_dicts(values)
        return new_context


class Context(BaseContext):
    """A stack container for variable context"""

    def __init__(self, dict_=None, autoescape=True, current_app=None, use_l10n=None, use_tz=None):
        self.autoescape = autoescape
        self.current_app = current_app
        self.use_l10n = use_l10n
        self.use_tz = use_tz
        self.render_context = RenderContext()
        super(Context, self).__init__(dict_)

    def __copy__(self):
        duplicate = super(Context, self).__copy__()
        duplicate.render_context = copy(self.render_context)
        return duplicate

    def update(self, other_dict):
        """Pushes other_dict to the stack of dictionaries in the Context"""
        if not hasattr(other_dict, '__getitem__'):
            raise TypeError('other_dict must be a mapping (dictionary-like) object.')
        self.dicts.append(other_dict)
        return other_dict


class RenderContext(BaseContext):
    """
    A stack container for storing Template state.

    RenderContext simplifies the implementation of template Nodes by providing a
    safe place to store state between invocations of a node's `render` method.

    The RenderContext also provides scoping rules that are more sensible for
    'template local' variables. The render context stack is pushed before each
    template is rendered, creating a fresh scope with nothing in it. Name
    resolution fails if a variable is not found at the top of the RequestContext
    stack. Thus, variables are local to a specific template and don't affect the
    rendering of other templates as they would if they were stored in the normal
    template context.
    """

    def __iter__(self):
        for d in self.dicts[(-1)]:
            yield d

    def has_key(self, key):
        return key in self.dicts[(-1)]

    def get(self, key, otherwise=None):
        d = self.dicts[(-1)]
        if key in d:
            return d[key]
        return otherwise


def get_standard_processors():
    global _standard_context_processors
    from django.conf import settings
    if _standard_context_processors is None:
        processors = []
        collect = []
        collect.extend(_builtin_context_processors)
        collect.extend(settings.TEMPLATE_CONTEXT_PROCESSORS)
        for path in collect:
            i = path.rfind('.')
            module, attr = path[:i], path[i + 1:]
            try:
                mod = import_module(module)
            except ImportError as e:
                raise ImproperlyConfigured('Error importing request processor module %s: "%s"' % (module, e))

            try:
                func = getattr(mod, attr)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a "%s" callable request processor' % (module, attr))

            processors.append(func)

        _standard_context_processors = tuple(processors)
    return _standard_context_processors


class RequestContext(Context):
    """
    This subclass of template.Context automatically populates itself using
    the processors defined in TEMPLATE_CONTEXT_PROCESSORS.
    Additional processors can be specified as a list of callables
    using the "processors" keyword argument.
    """

    def __init__(self, request, dict_=None, processors=None, current_app=None, use_l10n=None, use_tz=None):
        Context.__init__(self, dict_, current_app=current_app, use_l10n=use_l10n, use_tz=use_tz)
        if processors is None:
            processors = ()
        else:
            processors = tuple(processors)
        for processor in get_standard_processors() + processors:
            self.update(processor(request))

        return