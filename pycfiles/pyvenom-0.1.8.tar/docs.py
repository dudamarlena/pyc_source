# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Larco/Documents/Github/pyvenom/framework/venom/routing/docs.py
# Compiled at: 2016-04-26 14:29:46
import os
from wsgi_entry import WSGIEntryPoint
from google.appengine.ext.webapp import template
__all__ = 'Documentation'

class Documentation(WSGIEntryPoint):

    def __init__(self, application):
        super(Documentation, self).__init__()
        self.application = application

    def dispatch(self, request, response, error):
        template_values = {'version': self.application.version}
        path = os.path.join(os.path.dirname(__file__), 'docs/index.html')
        response.write(template.render(path, template_values))