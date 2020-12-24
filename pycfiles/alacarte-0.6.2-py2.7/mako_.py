# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-fat3/egg/alacarte/template/mako_.py
# Compiled at: 2010-08-27 14:44:15
from alacarte.core import Engine
from alacarte.resolver import Resolver
try:
    from mako.template import Template
except ImportError:
    raise ImportError('You must install the mako package.')

__all__ = [
 'Mako']
resolve = Resolver()

class Mako(Engine):

    def prepare(self, filename, **options):
        return self.get_template(filename)

    def render(self, template, data, **options):
        return (
         options.get('content_type', 'text/html'), template.render_unicode(**data))

    def get_template(self, uri):
        filename = resolve(uri)[1]
        return Template(filename=filename, lookup=self)

    def adjust_uri(self, uri, relativeto):
        return uri