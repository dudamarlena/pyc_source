# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/render.py
# Compiled at: 2017-01-15 13:25:40
"""
The Moya Render protocol

"""
from __future__ import unicode_literals
from __future__ import print_function
from .compat import text_type, implements_to_string
from .html import escape
import json

class HTML(text_type):
    html_safe = True

    def __repr__(self):
        return b'HTML(%s)' % super(HTML, self).__repr__()


class Safe(text_type):
    html_safe = True


class Unsafe(text_type):
    html_safe = False


class RenderList(list):
    """A list of renderables"""

    def moya_render(self, archive, context, target, options):
        return render_objects(self, archive, context, target, options)


def is_renderable(obj):
    """Check if an object complies to the render protocol"""
    return hasattr(obj, b'moya_render')


def is_safe(obj):
    return getattr(obj, b'html_safe', False)


def render_object(obj, archive, context, target, options=None):
    """Render an object"""
    if hasattr(obj, b'moya_render'):
        if hasattr(obj, b'moya_render_targets') and target not in obj.moya_render_targets:
            rendered = text_type(obj)
        else:
            rendered = obj.moya_render(archive, context, target, options or {})
    elif target == b'json':
        rendered = json.dumps(obj)
    elif target == b'html.linebreaks':
        rendered = HTML((b'<br>\n').join(escape(text_type(obj)).splitlines()))
    elif obj is None:
        rendered = b''
    else:
        rendered = obj
    if target in ('', 'html') and not getattr(rendered, b'html_safe', False):
        rendered = escape(rendered)
    return rendered


def render_objects(objects, archive, context, target, options=None, join=b'\n'):
    """Renders a sequence of objects and concatenates them together with carriage returns"""
    return HTML(join.join([ render_object(obj, archive, context, target, options=options) for obj in objects
                          ]))


if __name__ == b'__main__':
    text = HTML(b'<b>Hello</b>')
    print(repr(text))