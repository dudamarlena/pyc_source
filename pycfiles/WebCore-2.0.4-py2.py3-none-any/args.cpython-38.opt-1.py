# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/ext/args.py
# Compiled at: 2020-05-11 19:18:00
# Size of source mod 2**32: 7042 bytes
"""Argument handling extensions for WebCore applications.

These allow you to customize the behaviour of the arguments passed to endpoints.
"""
from inspect import isroutine, ismethod, getcallargs
from webob.exc import HTTPNotFound
from web.core.util import safe_name
log = __import__('logging').getLogger(__name__)

class ArgumentExtension(object):
    __doc__ = 'Not for direct use.'

    @staticmethod
    def _process_flat_kwargs(source, kwargs):
        """Apply a flat namespace transformation to recreate (in some respects) a rich structure.
                
                This applies several transformations, which may be nested:
                
                `foo` (singular): define a simple value named `foo`
                `foo` (repeated): define a simple value for placement in an array named `foo`
                `foo[]`: define a simple value for placement in an array, even if there is only one
                `foo.<id>`: define a simple value to place in the `foo` array at the identified index
                
                By nesting, you may define deeper, more complex structures:
                
                `foo.bar`: define a value for the named element `bar` of the `foo` dictionary
                `foo.<id>.bar`: define a `bar` dictionary element on the array element marked by that ID
                
                References to `<id>` represent numeric "attributes", which makes the parent reference be treated as an array,
                not a dictionary. Exact indexes might not be able to be preserved if there are voids; Python lists are not
                sparse.
                
                No validation of values is performed.
                """
        ordered_arrays = []
        for name, value in source.items():
            container = kwargs
            if '.' in name:
                parts = name.split('.')
                name = name.rpartition('.')[2]
                for target, following in zip(parts[:-1], parts[1:]):
                    if following.isnumeric():
                        container.setdefault(target, [{}])
                        if container[target] not in ordered_arrays:
                            ordered_arrays.append(container[target])
                        container = container[target][0]
                    else:
                        container = container.setdefault(target, {})

            else:
                if name.endswith('[]'):
                    name = name[:-2]
                    container.setdefault(name, [])
                    container[name].append(value)
            if name.isnumeric() and container is not kwargs:
                container[int(name)] = value
            elif name in container:
                if not isinstance(container[name], list):
                    container[name] = [
                     container[name]]
                container[name].append(value)
            else:
                container[name] = value
        else:
            for container in ordered_arrays:
                elements = container[0]
                del container[:]
                container.extend((value for name, value in sorted(elements.items())))

    @staticmethod
    def _process_rich_kwargs(source, kwargs):
        """Apply a nested structure to the current kwargs."""
        kwargs.update(source)


class ValidateArgumentsExtension(object):
    __doc__ = 'Use this to enable validation of endpoint arguments.\n\t\n\tYou can determine when validation is executed (never, always, or development) and what action is taken when a\n\tconflict occurs.\n\t'
    last = True
    provides = {
     'args.validation', 'kwargs.validation'}

    def __init__(self, enabled='development', correct=False):
        """Configure when validation is performed and the action performed.
                
                If `enabled` is `True` validation will always be performed, if `False`, never. If set to `development` the
                callback will not be assigned and no code will be executed during runtime.
                
                When `correct` is falsy (the default), an `HTTPNotFound` will be raised if a conflict occurs. If truthy the
                conflicting arguments are removed, with positional taking precedence to keyword.
                """
        if enabled is True or enabled == 'development':
            self.mutate = self._mutate

    def _mutate(self, context, endpoint, args, kw):
        try:
            if callable(endpoint):
                if not isroutine(endpoint):
                    endpoint = endpoint.__call__
            getcallargs(endpoint, *args, **kw)
        except TypeError as e:
            try:
                log.error((str(e).replace(endpoint.__name__, safe_name(endpoint))), extra=dict(request=(id(context)),
                  endpoint=(safe_name(endpoint)),
                  endpoint_args=args,
                  endpoint_kw=kw))
                raise HTTPNotFound('Incorrect endpoint arguments: ' + str(e))
            finally:
                e = None
                del e


class ContextArgsExtension(ArgumentExtension):
    __doc__ = 'Add the context as the first positional argument, possibly conditionally.'
    first = True
    provides = {'args.context'}

    def __init__(self, always=False):
        """Configure the conditions under which the context is added to endpoint positional arguments.
                
                When `always` is truthy the context is always included, otherwise it's only included for callables that are
                not bound methods.
                """
        self.always = always

    def mutate(self, context, endpoint, args, kw):
        if not self.always:
            if isroutine(endpoint):
                if ismethod(endpoint):
                    if getattr(endpoint, '__self__', None) is not None:
                        return
        args.insert(0, context)


class RemainderArgsExtension(ArgumentExtension):
    __doc__ = 'Add any unprocessed path segments as positional arguments.'
    first = True
    needs = {'request'}
    uses = {'args.context'}
    provides = {'args.remainder'}

    def mutate(self, context, endpoint, args, kw):
        if not context.request.remainder:
            return
        args.extend(context.request.remainder)


class QueryStringArgsExtension(ArgumentExtension):
    __doc__ = 'Add query string arguments ("GET") as keyword arguments.'
    first = True
    needs = {'request'}
    provides = {'kwargs.get'}

    def mutate(self, context, endpoint, args, kw):
        self._process_flat_kwargs(context.request.GET, kw)


class FormEncodedKwargsExtension(ArgumentExtension):
    __doc__ = 'Add form-encoded or MIME mmultipart ("POST") arguments as keyword arguments.'
    first = True
    needs = {'request'}
    uses = {'kwargs.get'}
    provides = {'kwargs.post'}

    def mutate(self, context, endpoint, args, kw):
        self._process_flat_kwargs(context.request.POST, kw)


class JSONKwargsExtension(ArgumentExtension):
    __doc__ = 'Add JSON-encoded arguments from the request body as keyword arguments.'
    first = True
    needs = {'request'}
    uses = {'kwargs.get'}
    provides = {'kwargs.json'}

    def mutate(self, context, endpoint, args, kw):
        if not context.request.content_type == 'application/json':
            return
        else:
            return context.request.body or None
        self._process_rich_kwargs(context.request.json, kw)