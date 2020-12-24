# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/templatetags/workon_thumbnail.py
# Compiled at: 2018-08-13 09:06:59
# Size of source mod 2**32: 2383 bytes
import re
from django import template
from django.conf import settings
import workon
__all__ = [
 'lazy_register']

def lazy_register(register):
    if 'sorl.thumbnail' in settings.INSTALLED_APPS:
        from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode
        from django.templatetags.static import static
        from django.contrib.staticfiles.storage import staticfiles_storage
        from django.contrib.staticfiles import finders
        from django.utils.six import text_type
        from sorl.thumbnail.shortcuts import get_thumbnail
        from sorl.thumbnail.images import ImageFile, DummyImageFile

        class StaticThumbnailNode(ThumbnailNode):
            child_nodelists = []

            def _render(self, context):
                file_ = self.file_.resolve(context)
                geometry = self.geometry.resolve(context)
                options = {}
                for key, expr in self.options:
                    noresolve = {'True':True, 
                     'False':False,  'None':None}
                    value = noresolve.get(text_type(expr), expr.resolve(context))
                    if key == 'options':
                        options.update(value)
                    else:
                        options[key] = value

                thumbnail = (workon.thumbnail_static)(file_, geometry, **options)
                if not thumbnail or isinstance(thumbnail, DummyImageFile) and self.nodelist_empty:
                    if self.nodelist_empty:
                        return self.nodelist_empty.render(context)
                    return ''
                else:
                    if self.as_var:
                        context.push()
                        context[self.as_var] = thumbnail
                        output = self.nodelist_file.render(context)
                        context.pop()
                    else:
                        output = thumbnail.url
                    return output

        @register.tag
        def thumbnail(parser, token):
            return ThumbnailNode(parser, token)

        @register.tag
        def thumbnail_static(parser, token):
            return StaticThumbnailNode(parser, token)

    else:

        @register.tag
        def thumbnail(parser, token):
            return parsed

        @register.tag
        def thumbnail_static(parsed, context, token):
            return parsed