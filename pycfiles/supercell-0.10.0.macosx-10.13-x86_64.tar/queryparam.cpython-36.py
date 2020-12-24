# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jannis/Documents/code/rtr-supercell/supercell/env3/lib/python3.6/site-packages/supercell/queryparam.py
# Compiled at: 2019-01-08 09:09:15
# Size of source mod 2**32: 2996 bytes
"""Simple decorator for dealing with typed query parameters."""
from __future__ import absolute_import, division, print_function, with_statement
from schematics.exceptions import ConversionError, ValidationError
import supercell.api as s
from supercell._compat import error_messages

class QueryParams(s.Middleware):
    __doc__ = "Simple middleware for ensuring types in query parameters.\n\n    A simple example::\n\n        @QueryParams((\n            ('limit', IntType()),\n            ('q', StringType())\n            )\n        )\n        @s.async\n        def get(self, *args, **kwargs):\n            limit = kwargs.get('limit', 0)\n            q = kwargs.get('q', None)\n            ...\n\n    If a param is required, simply set the `required` property for the\n    schematics type definition::\n\n        @QueryParams((\n            ('limit', IntType(required=True)),\n            ('q', StringType())\n            )\n        )\n        ...\n\n    If the parameter is missing, a HTTP 400 error is raised.\n\n    By default the dictionary containing the typed query parameters is added\n    to the `kwargs` of the method with the key *query*. In order to change\n    that, simply change the key in the definition::\n\n        @QueryParams((\n            ...\n            ),\n            kwargs_name='myquery'\n        )\n        ...\n    "

    def __init__(self, params, kwargs_name='query'):
        super(QueryParams, self).__init__()
        self.params = params
        self.kwargs_name = kwargs_name

    @s.coroutine
    def before(self, handler, args, kwargs):
        kwargs[self.kwargs_name] = q = {}
        for name, typedef in self.params:
            if handler.get_argument(name, None):
                try:
                    parsed = typedef(handler.get_argument(name))
                    q[name] = parsed
                except (ConversionError, ValidationError) as e:
                    validation_errors = {name: error_messages(e)}
                    raise s.Error(additional=validation_errors)

            else:
                if typedef.required and not handler.get_argument(name, None):
                    raise s.Error(additional={'msg': 'Missing required argument "%s"' % name})

    @s.coroutine
    def after(self, handler, args, kwargs, result):
        pass