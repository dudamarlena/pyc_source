# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jpapouse/workspace/adaptive-learning/proso-apps/proso_common/templatetags/jsonify.py
# Compiled at: 2020-03-19 09:15:44
# Size of source mod 2**32: 898 bytes
from django import template
import json as simplejson
from django.utils.safestring import mark_safe
import re
register = template.Library()

def obj2json(value, indent=4):
    return simplejson.dumps(value, indent=indent)


def obj2richjson(value, indent=4):
    return mark_safe(url2link(space2nbsp(obj2json(value, indent))).replace('\n', '<br />'))


def url2link(value):
    p = re.compile('"(url|[^"]*_url)":(&nbsp;| )"/?([^"]*)"')
    return mark_safe(p.sub('"\\1": "<a href=\'/\\3\'>/\\3</a>"', value))


def space2nbsp(value):
    return mark_safe('&nbsp;'.join(value.split(' ')))


def drop_html_escape(value):
    return value.replace('&gt', '>').replace('&lt', '<')


register.filter('url2link', url2link)
register.filter('space2nbsp', space2nbsp)
register.filter('obj2json', obj2json)
register.filter('obj2richjson', obj2richjson)
register.filter('drop_html_escape', drop_html_escape)