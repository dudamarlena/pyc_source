# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/control/routing.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2424 bytes
from ..project import construct
from ..util import deprecated, flatten
from .action import ActionList
from .receiver import Receiver

class Routing(Receiver):
    __doc__ = '\n    A dict that routes a message to an ActionList.\n    '

    def __init__(self, routing, default, python_path):
        """
        :param dict routing: `routing` is a dict that maps addresses
           to lists of actions.

           The values in the input dictionary `routing` are recursively visited
           to build the routing table:

           * values that are strings or lists are used to construct ActionLists
           * dictionaries that contain "typename" or "datatype" keys are
             used to construct a class of that type.
           * otherwise, dictionaries are visited recursively
           * all other types are forbidden
        """

        def make(x):
            if isinstance(x, (list, str)):
                return ActionList(x)
            else:
                assert isinstance(x, dict)
                if 'datatype' in x or 'typename' in x:
                    x = dict(default, **x)
                    return construct.construct_type(x, python_path)
                return {k:make(v) for k, v in x.items()}

        routing = flatten.unflatten(routing)
        self.routing = make(routing)

    def set_project(self, project):
        """Set the base project for routing."""

        def visit(x):
            set_project = getattr(x, 'set_project', None)
            if set_project:
                set_project(project)
            values = getattr(x, 'values', lambda : ())
            for v in values():
                visit(v)

        visit(self.routing)

    def receive(self, msg):
        """
        Returns a (receiver, msg) pair, where receiver is `None` if no route for
        the message was found, or otherwise an object with a `receive` method
        that can accept that `msg`.
        """
        x = self.routing
        while not isinstance(x, ActionList):
            if not x or not msg:
                return (
                 None, msg)
            if not isinstance(x, dict):
                raise ValueError('Unexpected type %s' % type(x))
            _, value = msg.popitem(last=False)
            x = x.get(str(value))

        return (x, msg)

    def __bool__(self):
        return bool(self.routing)

    def __str__(self):
        return str(self.routing)