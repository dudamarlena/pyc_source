# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/futurefinity/routing.py
# Compiled at: 2016-06-10 18:06:56
# Size of source mod 2**32: 4405 bytes
from typing import Optional
import re, collections

class RoutingRule(collections.namedtuple('RoutingRule', ('handler', 'path_args', 'path_kwargs'))):
    __doc__ = '\n    Basic Routing Rule for Routing, which contains a handler, path_args,\n    and a path_kwargs. It can be either a stored rule in a routing locator,\n    or a matched rule that will be returned to the application.\n\n    :arg handler: should be a ``futurefinity.web.RequestHandler`` object.\n    :arg path_args: is a tuple or list that contains the positional arguments.\n    :arg path_kwargs: is a dict that contains the keyword arguments.\n    '


class RoutingLocator:
    __doc__ = '\n    A Routing Locator.\n\n    :arg default_handler: should be a ``futurefinity.web.RequestHandler``\n        object, which will be returned if a handler cannot be found during the\n        path matching.\n    '

    def __init__(self, default_handler: Optional[object]=None):
        self.handlers_dict = collections.OrderedDict()
        self.links_dict = collections.OrderedDict()
        self.default_handler = default_handler

    def add(self, path: str, handler: object, *args, name: str=None, **kwargs):
        r"""
        Add a routing rule to the locator.

        :arg path: is a regular expression of the path that will be matched.
        :arg handler: should be a ``futurefinity.web.RequestHandler``.
        :arg \*args: all the other positional arguments will be come the
            path_args of the routing rule. The arguments passed here always
            have a higher priority in the matched routing rule, which means
            that all the positional arguments passed here will be the first
            part of the matched object.
        :arg name: the name of the routing rule.
        :arg \*\*kwargs: all the other keyword arguments will be come the
            path_kwargs of the routing rule. The arguments passed here always
            have a higher priority in the matched routing rule, which means
            that if the same key also exsits in the regular expression,
            this one will override the one in the path.
        """
        if isinstance(path, str):
            path = re.compile(path)
        if name is not None:
            self.links_dict[name] = path
        self.handlers_dict[path] = RoutingRule(handler=handler, path_args=list(args), path_kwargs=kwargs)

    def find(self, path: str) -> RoutingRule:
        """
        Find a handler that matches the path.

        If a handler that matches the path cannot be found, the handler will be
        the default_handler.

        It returns a ``RoutingRule``.

        For the path_args and path_kwargs, the one passes though add method
        will have a higher priority.
        """
        for key, value in self.handlers_dict.items():
            matched_obj = key.fullmatch(path)
            if matched_obj is None:
                pass
            continue
            path_args = []
            path_args.extend(value.path_args)
            link_args = matched_obj.groups()
            if link_args is not None:
                path_args.extend(link_args)
            path_kwargs = {}
            link_kwargs = matched_obj.groupdict()
            if link_kwargs is not None:
                path_kwargs.update(link_kwargs)
            path_kwargs.update(value.path_kwargs)
            return RoutingRule(handler=value.handler, path_args=path_args, path_kwargs=path_kwargs)
        else:
            return RoutingRule(handler=self.default_handler, path_args=[], path_kwargs={})