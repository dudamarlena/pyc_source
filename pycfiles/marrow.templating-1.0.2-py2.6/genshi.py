# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/template/genshi.py
# Compiled at: 2012-05-23 13:18:32
from __future__ import unicode_literals, absolute_import
from os import path
from marrow.templating.core import Engine
try:
    from genshi.input import ET, HTML, XML
    from genshi.filters import Translator
    from genshi.template import TemplateLoader, TextTemplate, MarkupTemplate
except ImportError:
    raise ImportError(b'You must install the genshi package.')

__all__ = [
 b'Genshi']

class Genshi(Engine):

    def __init__(self, cache=25, **kw):
        super(Genshi, self).__init__(cache, **kw)
        self.genshi_monitor = self.monitor
        self.monitor = False

    def prepare(self, filename, kind=b'markup', i18n=None, **options):
        bpath = path.dirname(filename)

        def template_loaded(template):
            template.filters.insert(0, Translator(i18n))

        try:
            loader = self.cache[bpath]
        except KeyError:
            callback = template_loaded if i18n else None
            loader = self.cache[bpath] = TemplateLoader([bpath], auto_reload=self.genshi_monitor, callback=callback)

        return (loader, filename)

    def render(self, template, data, kind=b'markup', **options):
        method = options.get(b'method', b'text' if kind == b'text' else b'xhtml')
        content_type = options.get(b'content_type', b'text/plain' if kind == b'text' else b'text/html')
        kind = TextTemplate if kind == b'text' else MarkupTemplate
        data.update({b'ET': ET, b'HTML': HTML, b'XML': XML})
        (loader, template) = template
        tmpl = loader.load(template, cls=kind)
        return (
         content_type, tmpl.generate(**data).render(method))