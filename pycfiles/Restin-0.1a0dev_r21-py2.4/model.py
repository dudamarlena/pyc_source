# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/restin/controllers/model.py
# Compiled at: 2007-05-04 19:49:10
from restin.lib.base import *
from paste.deploy.converters import asbool

class ModelController(RestController):
    __module__ = __name__

    def index(self):
        self.application.model_entities
        return self._render_response()

    def _init_entity(self):
        pass