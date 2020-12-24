# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/avatar.py
# Compiled at: 2019-08-16 17:27:46
"""
Note: Also see letterAvatar.jsx. Anything changed in this file (how colors are
      selected, the svg, etc) will also need to be changed there.
"""
from __future__ import absolute_import
import six
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.encoding import force_text
from django.utils.html import escape
from six.moves.urllib.parse import urlencode
from sentry.utils.hashlib import md5_text
from sentry.http import safe_urlopen

def get_gravatar_url(email, size=None, default='mm'):
    if email is None:
        email = ''
    gravatar_url = '%s/avatar/%s' % (
     settings.SENTRY_GRAVATAR_BASE_URL,
     md5_text(email.lower()).hexdigest())
    properties = {}
    if size:
        properties['s'] = six.text_type(size)
    if default:
        properties['d'] = default
    if properties:
        gravatar_url += '?' + urlencode(properties)
    return gravatar_url


LETTER_AVATAR_COLORS = [
 '#4674ca',
 '#315cac',
 '#57be8c',
 '#3fa372',
 '#f9a66d',
 '#ec5e44',
 '#e63717',
 '#f868bc',
 '#6c5fc7',
 '#4e3fb4',
 '#57b1be',
 '#847a8c']
COLOR_COUNT = len(LETTER_AVATAR_COLORS)

def hash_user_identifier(identifier):
    identifier = force_text(identifier, errors='replace')
    return sum(map(ord, identifier))


def get_letter_avatar_color(identifier):
    hashed_id = hash_user_identifier(identifier)
    return LETTER_AVATAR_COLORS[(hashed_id % COLOR_COUNT)]


def get_letter_avatar(display_name, identifier, size=None, use_svg=True):
    display_name = (display_name or '').strip() or '?'
    names = display_name.split(' ')
    initials = '%s%s' % (names[0][0], names[(-1)][0] if len(names) > 1 else '')
    initials = escape(initials.upper())
    color = get_letter_avatar_color(identifier)
    if use_svg:
        size_attrs = 'height="%s" width="%s"' % (size, size) if size else ''
        return ('<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" {size_attrs}><rect x="0" y="0" width="120" height="120" rx="15" ry="15" fill={color}></rect><text x="50%" y="50%" font-size="65" dominant-baseline="central" text-anchor="middle" fill="#FFFFFF">{initials}</text></svg>').format(color=color, initials=initials, size_attrs=size_attrs)
    else:
        size_attrs = 'height:%spx;width:%spx;' % (size, size) if size else ''
        font_size = 'font-size:%spx;' % (size / 2) if size else ''
        line_height = 'line-height:%spx;' % size if size else ''
        return ('<span class="html-avatar" style="background-color:{color};{size_attrs}{font_size}{line_height}">{initials}</span>').format(color=color, initials=initials, size_attrs=size_attrs, font_size=font_size, line_height=line_height)


def get_email_avatar(display_name, identifier, size=None, try_gravatar=True):
    if try_gravatar:
        try:
            validate_email(identifier)
        except ValidationError:
            pass
        else:
            try:
                resp = safe_urlopen(get_gravatar_url(identifier, default=404))
            except Exception:
                pass
            else:
                if resp.status_code == 200:
                    gravatar_url = get_gravatar_url(identifier, size=size)
                    return ('<img class="avatar" src="{url}">').format(url=gravatar_url)

    return get_letter_avatar(display_name, identifier, size, use_svg=False)