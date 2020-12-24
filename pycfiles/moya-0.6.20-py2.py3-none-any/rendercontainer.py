# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/template/rendercontainer.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals
from ..render import HTML

class RenderContainer(dict):
    """A dictionary subclass with template meta information"""
    moya_render_targets = [
     b'html', b'text']

    @classmethod
    def create(cls, app, **meta):
        rc = cls()
        rc._app = app
        rc._meta = meta
        return rc

    def moya_render(self, archive, context, target, options):
        meta = self._meta
        template = meta[b'template']
        engine = archive.get_template_engine(b'moya')
        rendered = engine.render(template, self, base_context=context, app=self._app)
        if target == b'html':
            return HTML(rendered)
        return rendered