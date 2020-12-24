# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tornado_swirl/_parser_model.py
# Compiled at: 2019-12-17 19:27:20
# Size of source mod 2**32: 1216 bytes
"""Parser FSM models."""

class PathSpec(object):
    __doc__ = 'Represents the path specification of an REST API endpoint.'

    def __init__(self):
        self.summary = ''
        self.description = ''
        self.query_params = {}
        self.path_params = {}
        self.body_params = {}
        self.header_params = {}
        self.form_params = {}
        self.cookie_params = {}
        self.responses = {}
        self.properties = {}
        self.tags = {}
        self.deprecated = False
        self.security = {}


class SchemaSpec(object):
    __doc__ = 'Represents a REST API component schema.'

    def __init__(self):
        self.name = ''
        self.summary = ''
        self.description = ''
        self.deprecated = False
        self.properties = {}
        self.example = None
        self.examples = None


class Param(object):
    __doc__ = 'REST API section parameter'

    def __init__(self, name, dtype='string', ptype='path', required=False, description=None, order=0):
        self.name = name
        self.type = dtype
        self.ptype = ptype
        self.required = required
        self.description = description
        self.order = order
        self.kwargs = {}