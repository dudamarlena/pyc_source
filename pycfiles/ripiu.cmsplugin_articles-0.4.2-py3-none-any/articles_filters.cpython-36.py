# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Urlugal/Users/geobaldi/src/ripiu/public/github/cmsplugin_articles/ripiu/cmsplugin_articles/templatetags/articles_filters.py
# Compiled at: 2018-02-22 07:42:44
# Size of source mod 2**32: 586 bytes
from django import template
register = template.Library()

@register.filter(name='split_parts')
def split_parts(children):
    head = None
    main = None
    leftover = []
    if children:
        for child in children:
            print('child: %s' % child.plugin_type)
            if child.plugin_type == 'HeaderPlugin':
                head = child
            else:
                if child.plugin_type == 'MainPlugin':
                    main = child
                else:
                    leftover.append(child)

    return {'head':head, 
     'main':main, 
     'leftover':leftover}