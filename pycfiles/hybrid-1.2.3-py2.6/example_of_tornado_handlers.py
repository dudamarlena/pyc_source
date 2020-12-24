# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hybrid/skeleton/project/controllers/example_of_tornado_handlers.py
# Compiled at: 2016-01-10 03:08:01
from ..settings import tornadoapp
from .base_handler import BaseHandler

@tornadoapp.route('/tornado')
class TornadoHandler(BaseHandler):

    def get(self):
        self.render_func({'uri': self.request.uri, 'datetime': __import__('datetime').datetime.now()})