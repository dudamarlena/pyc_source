# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/FeatureServer/Service/HTML.py
# Compiled at: 2008-01-01 03:15:59
__author__ = 'MetaCarta'
__copyright__ = 'Copyright (c) 2006-2008 MetaCarta'
__license__ = 'Clear BSD'
__version__ = '$Id: HTML.py 412 2008-01-01 08:15:59Z crschmidt $'
from __init__ import Request
from __init__ import Action
from FeatureServer.Feature import Feature
from Cheetah.Template import Template

class HTML(Request):
    __module__ = __name__
    default_template = 'template/default.html'

    def _datasource(self):
        return self.service.datasources[self.datasource]

    def encode(self, result):
        template = self.template()
        output = Template(template, searchList=[{'actions': result}, self])
        return ('text/html; charset=utf-8', str(output).decode('utf-8'))

    def template(self):
        datasource = self._datasource()
        if hasattr(datasource, 'template'):
            template = datasource.template
        else:
            template = self.default_template
        return file(template).read()