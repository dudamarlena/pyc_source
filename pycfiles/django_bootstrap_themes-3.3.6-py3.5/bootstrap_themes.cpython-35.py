# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bootstrap_themes/templatetags/bootstrap_themes.py
# Compiled at: 2016-03-24 10:20:11
# Size of source mod 2**32: 875 bytes
from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.safestring import mark_safe
from .. import get_script, get_styles
register = template.Library()

@register.simple_tag
def bootstrap_script(use_min=True):
    return mark_safe('<script type="text/javascript" src="%(script_file)s"></script>' % dict(script_file=get_script(use_min)))


@register.simple_tag
def bootstrap_styles(theme='default', type='min.css'):
    if type == 'min.css' or type == 'css':
        subdir = 'css'
        fileext = type
        mimetype = 'text/css'
    elif type == 'less':
        subdir = type
        fileext = type
        mimetype = 'text/less'
    return mark_safe('<link rel="stylesheet" href="%(theme_file)s" type="%(mimetype)s">' % dict(theme_file=get_styles(theme, subdir, fileext), mimetype=mimetype))