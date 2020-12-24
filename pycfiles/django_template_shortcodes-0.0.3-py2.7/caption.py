# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/shortcodes/parsers/caption.py
# Compiled at: 2014-06-19 05:16:18
from django.template import Template, Context
from django.utils.safestring import mark_safe
from django.conf import settings
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup

def parse(tag_atts, tag_contents):
    """
    From wordpress source: https://github.com/WordPress/WordPress/blob/master/wp-includes/media.php#L620
    return '<div ' . $id . 'class="wp-caption ' . esc_attr($align) . '" style="width: ' . (10 + (int) $width) . 'px">'
    . do_shortcode( $content ) . '<p class="wp-caption-text">' . $caption . '</p></div>';
    
    """
    tag_atts['content'] = mark_safe(tag_contents)
    if tag_contents:
        try:
            soup = BeautifulSoup(tag_contents)
            image = soup.img.extract()
            if image:
                tag_atts['content'] = mark_safe(str(image))
                caption = (' ').join(soup.stripped_strings)
                if caption:
                    tag_atts['caption'] = caption
        except:
            pass

    context = Context(tag_atts)
    t = Template('\n        {% spaceless %}\n        <figure {% if id %}id="{{ id }}"{% endif %}{% if align %}class="align-{{ align }}"{% endif %}{% if width %}style="width: {{ width }}px"{% endif %}>\n            {{ content|safe }}\n            {% if caption %}\n            <figcaption>\n                <p>{{ caption|safe }}</p>\n            </figcaption>{% endif %}\n        </figure>\n        {% endspaceless %}')
    return t.render(context)