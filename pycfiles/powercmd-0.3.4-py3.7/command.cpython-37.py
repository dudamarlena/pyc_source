# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/powercmd/command.py
# Compiled at: 2019-01-13 18:05:41
# Size of source mod 2**32: 3113 bytes
"""
Utility classes for accessing type hints of function arguments.
"""
import collections, inspect, textwrap
from powercmd.extra_typing import OrderedMapping

class Parameter(collections.namedtuple('Parameter', ['name', 'type', 'default'])):
    __doc__ = '\n    Type-annotated function parameter.\n    '

    def __new__(cls, *args, **kwargs):
        param = (super().__new__)(cls, *args, **kwargs)
        if param.type == inspect._empty:
            raise ValueError('Type not specified for paramter %s' % param.name)
        return param

    def __str__(self):
        result = '%s: %s' % (self.name, self.type)
        if self.default is not None:
            result += ' = %s' % repr(self.default)
        return result


class Command(collections.namedtuple('Command', ['name', 'handler'])):
    __doc__ = '\n    Command handler: a powercmd.Cmd method with non-self parameters annotated\n    with type hints.\n    '

    def __new__(cls, *args, **kwargs):
        cmd = (super().__new__)(cls, *args, **kwargs)
        cmd.get_parameters()
        return cmd

    def _get_handler_params(self) -> OrderedMapping[(str, inspect.Parameter)]:
        """Returns a list of command parameters for given HANDLER."""
        params = inspect.signature(self.handler).parameters
        params = list(params.items())
        if params:
            if params[0][0] == 'self':
                params = params[1:]
        params = collections.OrderedDict(params)
        return params

    def get_parameters(self) -> OrderedMapping[(str, Parameter)]:
        """Returns an OrderedDict of command parameters."""
        try:
            params = self._get_handler_params()
            return collections.OrderedDict(((name, Parameter(name=name, type=(param.annotation), default=(param.default))) for name, param in params.items()))
        except ValueError as exc:
            try:
                raise ValueError('Unable to list parameters for handler: %s' % self.name) from exc
            finally:
                exc = None
                del exc

    @property
    def parameters(self) -> OrderedMapping[(str, Parameter)]:
        """Returns an OrderedDict of command parameters."""
        return self.get_parameters()

    @property
    def description(self) -> str:
        """Returns command handler docstring."""
        return self.handler.__doc__

    @property
    def short_description(self) -> str:
        """Returns the first line of command handler docstring."""
        if self.description is not None:
            return self.description.strip().split('\n', maxsplit=1)[0]

    @property
    def help(self):
        """Returns a help message for this command handler."""
        return '%s\n\nARGUMENTS: %s %s\n' % (
         textwrap.dedent(self.description or 'No details available.').strip(),
         self.name,
         ' '.join((str(param) for param in self.parameters)))