# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/buffetxslt/xsltsupport.py
# Compiled at: 2006-01-17 07:48:31
import os, Ft
from Ft.Xml.Xslt import Processor
from Ft.Lib.Uri import OsPathToUri
from Ft.Xml import InputSource

class BuffetXSLTPlugin(object):
    __module__ = __name__
    extension = 'xsl'

    def __init__(self, extra_vars_func=None, config=None):
        self.get_extra_vars = extra_vars_func
        if config:
            self.config = config
        else:
            self.config = dict()
        self.processor = Processor.Processor()

    def load_template(self, template_path):
        parts = template_path.split('.')
        true_path = '%s.%s' % (os.path.join(*parts), self.extension)
        stylesheet_as_uri = OsPathToUri(true_path)
        transform = InputSource.DefaultFactory.fromUri(stylesheet_as_uri)
        return transform

    def render(self, info, format='html', fragment=False, template=None):
        transform = self.load_template(template)
        document = info.get('xml', '<root />')
        source = InputSource.DefaultFactory.fromString(document, 'http://none.xml')
        self.processor.appendStylesheet(transform)
        output = self.processor.run(source, topLevelParams=info)
        self.processor = Processor.Processor()
        return output

    def transform(self, info, template):
        pass