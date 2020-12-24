# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/shortcodes/parsers/youtube.py
# Compiled at: 2014-06-18 11:17:19
from django.template import Template, Context
from django.conf import settings

def parse(attrs, tag_contents=None):
    tag_atts = {}
    if 'src' not in attrs.keys():
        if 'idval' in attrs.keys() and attrs['idval'][:1] == '=':
            tag_atts['src'] = attrs['idval'][1:]
    else:
        tag_atts['src'] = attrs['src']
    tag_atts['width'] = int(attrs.get('width', getattr(settings, 'SHORTCODES_YOUTUBE_WIDTH', 425)))
    tag_atts['height'] = int(attrs.get('height', 0))
    if tag_atts['height'] == 0:
        tag_atts['height'] = int(round(tag_atts['width'] / 425.0 * 344.0))
    html = '<iframe width="{{ width }}" height="{{ height }}" '
    html += 'src="{{ src }}" frameborder="0" allowfullscreen></iframe>'
    template = Template(html)
    context = Context(tag_atts)
    if 'src' in tag_atts:
        return template.render(context)
    else:
        return 'Video not found'