# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/filebrowser/templatetags/fb_csrf.py
# Compiled at: 2014-11-22 02:35:14
from django.template import Node
from django.template import Library
from django.utils.safestring import mark_safe
register = Library()

class CsrfTokenNode(Node):

    def render(self, context):
        csrf_token = context.get('csrf_token', None)
        if csrf_token:
            if csrf_token == 'NOTPROVIDED':
                return mark_safe('')
            else:
                return mark_safe("<div style='display:none'><input type='hidden' name='csrfmiddlewaretoken' value='%s' /></div>" % csrf_token)

        else:
            from django.conf import settings
            if settings.DEBUG:
                import warnings
                warnings.warn('A {% csrf_token %} was used in a template, but the context did not provide the value.  This is usually caused by not using RequestContext.')
            return ''
        return


def fb_csrf_token(parser, token):
    return CsrfTokenNode()


register.tag(fb_csrf_token)