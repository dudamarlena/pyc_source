# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/mole/lib/python2.7/site-packages/mole/action/set.py
# Compiled at: 2012-07-13 05:39:01
import types
from mole.event import Event
from mole.action import Action, ActionSyntaxError
import mole.helper.eval as mole_eval

class ActionSet(Action):
    """This action set fields to events in pipeline according to a
    value.

    Paramters for set is passed as dict in the form key=expression
    """
    REQUIRE_PARSER = True

    def _eval(self, expr, context={}):
        for k, v in context.iteritems():
            if v.isdigit():
                context[k] = int(v)

        return eval(expr, context, self.environ)

    def _func(self, module):
        """Return a mapping of functions in module."""
        return map(lambda x: (x, getattr(module, x)), filter(lambda x: isinstance(getattr(module, x), types.FunctionType) or isinstance(getattr(module, x), types.BuiltinFunctionType), dir(module)))

    def __init__(self, *args, **kwargs):
        self.fields = kwargs
        self.environ = dict(self._func(mole_eval))

    def __call__(self, pipeline):
        for event in pipeline:
            for x, y in self.fields.iteritems():
                if x in event:
                    if isinstance(event[x], list):
                        event[x].append(self._eval(y, dict(event)))
                    else:
                        event[x] = [
                         event[x], self._eval(y, dict(event))]
                else:
                    event[x] = self._eval(y, dict(event))

            yield event