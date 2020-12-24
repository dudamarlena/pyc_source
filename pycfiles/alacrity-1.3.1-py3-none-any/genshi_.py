# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/alacarte/template/genshi_.py
# Compiled at: 2010-08-24 20:33:30
from os import path
from alacarte.core import Engine
try:
    from genshi.input import ET, HTML, XML
    from genshi.filters import Translator
    from genshi.template import TemplateLoader, TextTemplate, MarkupTemplate
except ImportError:
    raise ImportError('You must install the genshi package.')

__all__ = [
 'Genshi']

class Genshi(Engine):

    def __init__(self, cache=25, **kw):
        super(Genshi, self).__init__(cache, **kw)
        self.genshi_monitor = self.monitor
        self.monitor = False

    def prepare(self, filename, kind='markup', i18n=None, **options):
        bpath = path.dirname(filename)

        def template_loaded(template):
            template.filters.insert(0, Translator(i18n.ugettext))

        try:
            loader = self.cache[bpath]
        except KeyError:
            loader = self.cache[bpath] = TemplateLoader([bpath], auto_reload=self.genshi_monitor, callback=None if i18n is None else template_loaded)

        return (
         loader, filename)

    def render(self, template, data, kind='markup', **options):
        method = options.get('method', 'text' if kind == 'text' else 'xhtml')
        content_type = options.get('content_type', 'text/plain' if kind == 'text' else 'text/html')
        kind = TextTemplate if kind == 'text' else MarkupTemplate
        data.update({'ET': ET, 'HTML': HTML, 'XML': XML})
        loader, template = template
        tmpl = loader.load(template, cls=kind)
        return (
         content_type, tmpl.generate(**data).render(method))