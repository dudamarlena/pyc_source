# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/shaft/shaft/extras/jinja_helpers.py
# Compiled at: 2017-01-26 03:38:43
# Size of source mod 2**32: 3237 bytes
"""
Custom Jinja filters
"""
import re
from jinja2 import Markup
from . import md
from flask import url_for
import humanize, arrow
from shaft import init_app, get_config, local_datetime, utils

def format_datetime(dt, format):
    if not dt:
        return ''
    else:
        return arrow.get(dt).format(format)


def format_local_datetime(dt, format):
    if not dt:
        return ''
    else:
        return local_datetime(dt, get_config('DATETIME_TIMEZONE')).format(format)


def local_date_time(dt):
    f = get_config('DATETIME_DATE_TIME_FORMAT', 'MM/DD/YYYY h:mm a')
    return format_datetime(dt, f)


def local_date(dt):
    f = get_config('DATE_FORMAT', 'MM/DD/YYYY')
    return format_datetime(dt, f)


def nl2br(s):
    """
    {{ s | nl2br }}

    Convert newlines into <p> and <br />s.
    """
    if not isinstance(s, basestring):
        s = str(s)
    s = re.sub('\\r\\n|\\r|\\n', '\n', s)
    paragraphs = re.split('\n{2,}', s)
    paragraphs = ['<p>%s</p>' % p.strip().replace('\n', '<br />') for p in paragraphs]
    return '\n\n'.join(paragraphs)


def oembed(url, class_=''):
    """
    Create OEmbed link

    {{ url | oembed }}
    :param url:
    :param class_:
    :return:
    """
    o = '<a href="{url}" class="oembed {class_}" ></a>'.format(url=url, class_=class_)
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
    if not url.startswith('http://'):
        if not url.startswith('https://'):
            url = static_url(url)
    else:
        data_src = ''
        if responsive:
            class_ += ' responsive'
        if lazy_load:
            data_src = url
            url = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNgYAAAAAMAASsJTYQAAAAASUVORK5CYII='
            class_ += ' lazy'
    img = '<img src="{src}" class="{class_}" id="{id_}" data-src={data_src}>'.format(src=url,
      class_=class_,
      id_=id_,
      data_src=data_src)
    return Markup(img)


def static_url(url):
    """
    {{ url | static }}
    :param url:
    :return:
    """
    return url_for('static', filename=url)


FILTERS = {'slug':utils.slugify, 
 'int_comma':humanize.intcomma, 
 'strip_decimal':lambda d: d.split('.')[0], 
 'bool_to_yes':lambda b: 'Yes' if b else 'No', 
 'bool_to_int':lambda b: 1 if b else 0, 
 'markdown':lambda text: Markup(md.html(text)), 
 'markdown_toc':md.toc, 
 'nl2br':nl2br, 
 'format_local_date':format_local_datetime, 
 'local_date':local_date, 
 'local_date_time':local_date_time, 
 'date_since':humanize.naturaldate, 
 'time_since':humanize.naturaltime, 
 'oembed':oembed, 
 'img_src':img_src, 
 'static':static_url}

def jinja_helpers(app):
    app.jinja_env.filters.update(FILTERS)


init_app(jinja_helpers)