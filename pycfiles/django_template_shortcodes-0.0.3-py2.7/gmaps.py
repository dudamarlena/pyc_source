# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/shortcodes/parsers/gmaps.py
# Compiled at: 2014-06-18 09:50:00
from django.template import Template, Context
from django.conf import settings

def parse(attrs, tag_content=None):
    url = attrs.get('url')
    width = int(attrs.get('width', getattr(settings, 'SHORTCODES_GMAPS_WIDTH', 556)))
    height = int(attrs.get('height', 313))
    html = '<iframe width="{{ width }}" height="{{ height }}" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="{{ url|safe }}&amp;ie=UTF8&amp;output=embed"></iframe>'
    template = Template(html)
    context = Context({'url': url, 
       'width': width, 
       'height': height})
    if url:
        return template.render(context)
    else:
        return 'Missing URL for Google Maps'