# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/flasik/ext/jinja_helpers.py
# Compiled at: 2019-08-24 19:08:58
"""
Custom Jinja filters
"""
import re
from jinja2 import Markup
from . import md
from flask import url_for
import humanize, arrow, flasik
from flasik import extends, config, utils, functions

def nl2br(s):
    """
    {{ s | nl2br }}

    Convert newlines into <p> and <br />s.
    """
    if not isinstance(s, basestring):
        s = str(s)
    s = re.sub('\\r\\n|\\r|\\n', '\n', s)
    paragraphs = re.split('\n{2,}', s)
    paragraphs = [ '<p>%s</p>' % p.strip().replace('\n', '<br />') for p in paragraphs
                 ]
    return ('\n\n').join(paragraphs)


def oembed(url, class_=''):
    """
    Create OEmbed link

    {{ url | oembed }}
    :param url:
    :param class_:
    :return:
    """
    o = ('<a href="{url}" class="oembed {class_}" ></a>').format(url=url, class_=class_)
    return Markup(o)


def img_src(url, class_='', responsive=False, lazy_load=False, id_=''):
    """
    Create an image src

    {{ xyz.jpg | img_src }}

    :param url:
    :param class_:
    :param responsive:
    :param lazy_load:
    :param id_:
    :return:
    """
    if not url.startswith('http://') and not url.startswith('https://'):
        url = static_url(url)
    data_src = ''
    if responsive:
        class_ += ' responsive'
    if lazy_load:
        data_src = url
        url = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNgYAAAAAMAASsJTYQAAAAASUVORK5CYII='
        class_ += ' lazy'
    img = ('<img src="{src}" class="{class_}" id="{id_}" data-src={data_src}>').format(src=url, class_=class_, id_=id_, data_src=data_src)
    return Markup(img)


def static_url(url):
    """
    {{ url | static }}
    :param url:
    :return:
    """
    return url_for('static', filename=url)


@flasik.extends
def jinja_helpers(app):
    app.jinja_env.filters.update({'slug': utils.slugify, 
       'int_comma': humanize.intcomma, 
       'strip_decimal': lambda d: d.split('.')[0], 
       'markdown': lambda text: Markup(md.html(text)), 
       'nl2br': nl2br, 
       'format_datetime': functions.format_datetime, 
       'time_since': lambda dt: functions.format_datetime(dt, False).humanize(), 
       'oembed': oembed, 
       'img_src': img_src, 
       'static': static_url})