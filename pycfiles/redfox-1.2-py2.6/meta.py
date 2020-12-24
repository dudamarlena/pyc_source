# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/redfox/meta.py
# Compiled at: 2009-10-20 11:31:56
"""The bowels of redfox. This is where the metaclass that makes Redfox
app class instances into WSGI applications lives.
"""
from werkzeug.routing import Map, Rule, RuleFactory
from werkzeug import ClosingIterator
from werkzeug.exceptions import HTTPException
from redfox.request import Request
from redfox.routing import routes

def __call__(self, environ, start_response):
    """WSGI entry point. Routes requests to methods decorated by ``@route``
    and friends, then chains to the WSGI application (normally a
    ``werkzeug.Response``) returned by the endpoint method.
    
    The WSGI request environment is encapsulated in a ``Request`` object,
    for convenience. The original WSGI environment and the URL adapter
    used to dispatch the request are both attached to the request, for use
    in application-level handler methods.
    """
    adapter = self.__rule_map__.bind_to_environ(environ)
    try:
        (endpoint, values) = adapter.match()
        environ['wsgiorg.routing_args'] = ((), values)
        request = Request(adapter, environ)
        handler = getattr(self, endpoint)
        response = handler(request, **values)
    except HTTPException, e:
        response = e

    return ClosingIterator(response(environ, start_response))


class WebApplication(type):
    """Instances of this metaclass are given the following attributes:
    
    ``__rule_map__``
        A ``werkzeug.routing.Map`` object for identifying the appropriate
        method for each request. The ``Map`` is populated using rules from
        both the class's own routable methods and from any parents that look
        like they might have rule definitions.
    
    ``__call__``
        A WSGI entry point method that uses ``__rule_map__`` to route requests.
    
    If the class has a ``__rules__`` member, it's assumed to be a sequence of
    Rule (or RuleFactory) objects, and takes precendence when routing requests.
    Other Rules are built by introspecting the class's members to determine
    which members are routable. Finally, any parent classes which have a
    ``__rule_map__`` are included, to ensure inheritance relationships function
    properly (whether or not the new class defines any rules).
    """

    def __new__(meta, name, bases, dict):
        explicit_rules = list(dict.get('__rules__', []))
        introspected_rule_defs = list(meta.extract_rule_defs(dict))
        introspected_rules = [ Rule(*args, **kwargs) for (args, kwargs) in introspected_rule_defs ]
        parent_rules = [ MapRuleFactory(base.__rule_map__) for base in bases if hasattr(base, '__rule_map__') ]
        dict['__rule_map__'] = Map(explicit_rules + introspected_rules + parent_rules)
        dict['__call__'] = __call__
        return type.__new__(meta, name, bases, dict)

    @classmethod
    def extract_rule_defs(meta, attributes):
        """Extracts rule definitions from all routable objects in the
        ``attributes`` dictionary and returns them in a flat sequence.
        """
        for (name, method) in attributes.iteritems():
            for rule in meta.to_rules(name, method):
                yield rule

    @classmethod
    def to_rules(meta, name, method):
        """Extracts the route definitions from a method, adding some
        metadata necessary to route requests to methods.
        """
        return routes(method, endpoint=name)

    @classmethod
    def rule_map(meta, self):
        """Returns the rule map for an object. This is designed to be
        used as an optional method in classes derived from this metaclass.
        """
        return self.__rule_map__


class MapRuleFactory(RuleFactory):
    """A Werkzeug RuleFactory backed by an existing Map."""

    def __init__(self, source_map):
        self.source_map = source_map

    def get_rules(self, map):
        for rule in self.source_map.iter_rules():
            yield rule.empty()