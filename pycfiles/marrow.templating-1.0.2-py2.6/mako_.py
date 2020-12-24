# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/marrow/templating/template/mako_.py
# Compiled at: 2012-05-23 13:16:55
from __future__ import unicode_literals
from marrow.templating.core import Engine
from marrow.templating.resolver import Resolver
try:
    from mako.template import Template
except ImportError:
    raise ImportError(b'You must install the mako package.')

__all__ = [
 b'Mako']
resolve = Resolver()

class Mako(Engine):

    def prepare(self, filename, **options):
        return self.get_template(filename, options)

    def render(self, template, data, **options):
        return (
         options.get(b'content_type', b'text/html'), template.render_unicode(**data))

    def get_template(self, uri, options):
        filename = resolve(uri)[1]
        options.pop(b'content_type', None)
        return Template(filename=filename, lookup=self, **options)

    def adjust_uri(self, uri, relativeto):
        return uri