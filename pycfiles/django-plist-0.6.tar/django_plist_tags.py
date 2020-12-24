# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/steingrd/Django/django-plist/django_plist/templatetags/django_plist_tags.py
# Compiled at: 2010-05-20 04:21:40
from datetime import date, datetime, time
from xml.sax.saxutils import escape as xml_escape
from django import template
from django.db.models import Model
from django.db.models.query import QuerySet
register = template.Library()

class PropertyListSerializationFailedError(Exception):

    def __init__(self, obj):
        message = 'Failed to serialize object of type "%s"' % str(type(obj))
        super(PropertyListSerializationFailedError, self).__init__(message)


@register.tag(name='render_plist_object')
def do_render_plist_object(parser, token):
    try:
        (tag_name, plist_object) = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, 'render_plist_object requires a single argument'

    return RenderPlistObjectNode(plist_object)


class RenderPlistObjectNode(template.Node):

    def __init__(self, plist_object_name):
        self.plist_object_name = template.Variable(plist_object_name)

    def render(self, context):
        plist_object = self.plist_object_name.resolve(context)
        return self._render_unknown_object(plist_object)

    def _render_unknown_object(self, obj):
        if obj is None:
            return self._render_string('None')
        else:
            if isinstance(obj, basestring):
                return self._render_string(obj)
            if isinstance(obj, bool):
                return self._render_boolean(obj)
            if isinstance(obj, (int, long)):
                return self._render_integer(obj)
            if isinstance(obj, float):
                return self._render_real(obj)
            if isinstance(obj, dict):
                return self._render_dictionary(obj)
            if isinstance(obj, (list, tuple, QuerySet)):
                return self._render_array(obj)
            if isinstance(obj, (date, datetime)):
                return self._render_datetime(obj)
            if isinstance(obj, time):
                return self._render_time(obj)
            if hasattr(obj, 'as_plist'):
                return self._render_unknown_object(obj.as_plist())
            if Model in obj.__class__.__bases__:
                return self._render_dictionary(obj.__dict__)
            raise PropertyListSerializationFailedError(obj)
            return

    def _render_boolean(self, obj):
        if obj:
            return '<true/>'
        else:
            return '<false/>'

    def _render_time(self, obj):
        return '<string>%s</string>' % obj.strftime('%H:%M:%S')

    def _render_datetime(self, obj):
        return '<date>%s</date>' % obj.strftime('%Y-%m-%dT%H:%M:%SZ')

    def _render_string(self, obj):
        escaped_str = xml_escape('%s' % obj)
        return '<string>%s</string>' % escaped_str

    def _render_integer(self, obj):
        return '<integer>%s</integer>' % obj

    def _render_real(self, obj):
        return '<real>%s</real>' % obj

    def _render_array(self, obj):
        xml = '<array>'
        for elm in obj:
            xml += self._render_unknown_object(elm)

        xml += '</array>'
        return xml

    def _render_dictionary(self, obj):
        xml = '<dict>'
        for (key, val) in obj.items():
            if key.startswith('_'):
                continue
            escaped_key = xml_escape('%s' % key)
            xml += '<key>%s</key>' % escaped_key
            xml += self._render_unknown_object(val)

        xml += '</dict>'
        return xml