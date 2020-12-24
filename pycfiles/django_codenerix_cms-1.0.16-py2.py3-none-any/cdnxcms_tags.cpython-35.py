# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/www.django/makarthy/codenerix_cms/templatetags/cdnxcms_tags.py
# Compiled at: 2017-11-28 07:16:52
# Size of source mod 2**32: 1268 bytes
from django import template
from codenerix_cms.templatetags_tags import cdnx_slider, cdnx_staticheader

def f(x):
    return lambda *args, template='codenerix_cms/slider.html', lang, identifier, **args: x(identifier, lang, template, *args, **kwargs)


def d(x):
    return lambda *args, template='codenerix_cms/staticheader.html', lang, identifier, **args: x(identifier, lang, template, *args, **kwargs)


register = template.Library()
register.simple_tag(f(cdnx_slider), name='cdnx_slider')
register.simple_tag(d(cdnx_staticheader), name='cdnx_staticheader')