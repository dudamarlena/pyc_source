# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/template/kajiki_.py
# Compiled at: 2012-05-23 13:16:55
from __future__ import unicode_literals
from os import path
from marrow.templating.core import Engine
from marrow.templating.resolver import Resolver
try:
    from kajiki.loader import FileLoader
except ImportError:
    raise ImportError(b'You must install the Kajiki package.')

__all__ = [
 b'Kajiki']
resolve = Resolver()

class Kajiki(Engine):
    extmap = dict(xml=b'xml', htm=b'html', html=b'html', xhtml=b'xml', html5=b'html5', txt=b'text', text=b'text', kajiki=b'xml')
    mimetypes = dict(xml=b'text/xml', html=b'text/html', html5=b'text/html', text=b'text/plain')

    def prepare(self, filename, i18n=None, autoescape=False, **options):
        loader = FileLoader(None)
        loader._filename = self._filename
        template = loader.load(filename)
        return template

    def render(self, template, data, **options):
        kind = self.extmap.get(path.splitext(template.filename)[1][1:], b'text')
        result = template(data).render()
        return (
         options.get(b'content_type', self.mimetypes[kind]), result)

    def _filename(self, name):
        return resolve(name)[1]