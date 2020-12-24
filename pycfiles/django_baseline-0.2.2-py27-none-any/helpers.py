# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lib/utils/templatetags/helpers.py
# Compiled at: 2014-03-19 13:14:41
from __future__ import unicode_literals
from decimal import Decimal
import urllib
from django import template
from django.db.models import Model
from django.forms import ModelForm
from django.conf import settings
from django.core.urlresolvers import reverse
from utils import html
register = template.Library()

@register.simple_tag
def table(rows):
    """
    Output a simple table with several columns.
    """
    output = b'<table>'
    for row in rows:
        output += b'<tr>'
        for column in row:
            output += (b'<td>{s}</td>').format(s=column)

        output += b'</tr>'

    output += b'</table>'
    return output


@register.simple_tag
def link(url, text=b'', classes=b'', target=b'', get=b'', **kwargs):
    """
    Output a link tag.
    """
    if not (url.startswith(b'http') or url.startswith(b'/')):
        urlargs = {}
        for arg, val in kwargs.items():
            if arg[:4] == b'url_':
                urlargs[arg[4:]] = val

        url = reverse(url, kwargs=urlargs)
        if get:
            url += b'?' + get
    return html.tag(b'a', text or url, {b'class': classes, b'target': target, b'href': url})


@register.simple_tag
def jsfile(url):
    """
    Output a script tag to a js file.
    """
    if not url.startswith(b'http://') and not url[:1] == b'/':
        url = settings.STATIC_URL + url
    return (b'<script type="text/javascript" src="{src}"></script>').format(src=url)


@register.simple_tag
def cssfile(url):
    """
    Output a link tag to a css stylesheet.
    """
    if not url.startswith(b'http://') and not url[:1] == b'/':
        url = settings.STATIC_URL + url
    return (b'<link href="{src}" rel="stylesheet">').format(src=url)


@register.simple_tag
def img(url, alt=b'', classes=b'', style=b''):
    """
    Image tag helper.
    """
    if not url.startswith(b'http://') and not url[:1] == b'/':
        url = settings.STATIC_URL + url
    attr = {b'class': classes, 
       b'alt': alt, 
       b'style': style, 
       b'src': url}
    return html.tag(b'img', b'', attr)


def valid_numeric(arg):
    if isinstance(arg, (int, float, Decimal)):
        return arg
    try:
        return int(arg)
    except ValueError:
        return float(arg)


@register.filter
def sub(value, arg):
    """Subtract the arg from the value."""
    try:
        return valid_numeric(value) - valid_numeric(arg)
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return b''


sub.is_safe = False

@register.filter
def mul(value, arg):
    """Multiply the arg with the value."""
    try:
        return valid_numeric(value) * valid_numeric(arg)
    except (ValueError, TypeError):
        try:
            return value * arg
        except Exception:
            return b''


mul.is_safe = False

@register.filter
def div(value, arg):
    """Divide the arg by the value."""
    try:
        return valid_numeric(value) / valid_numeric(arg)
    except (ValueError, TypeError):
        try:
            return value / arg
        except Exception:
            return b''


div.is_safe = False

@register.filter(name=b'abs')
def absolute(value):
    """Return the absolute value."""
    try:
        return abs(valid_numeric(value))
    except (ValueError, TypeError):
        try:
            return abs(value)
        except Exception:
            return b''


absolute.is_safe = False

@register.filter
def mod(value, arg):
    """Return the modulo value."""
    try:
        return valid_numeric(value) % valid_numeric(arg)
    except (ValueError, TypeError):
        try:
            return value % arg
        except Exception:
            return b''


mod.is_safe = False

@register.filter
def model_verbose(obj, capitalize=True):
    """
    Return the verbose name of a model.
    The obj argument can be either a Model instance, or a ModelForm instance.
    This allows to retrieve the verbose name of the model of a ModelForm
    easily, without adding extra context vars.
    """
    if isinstance(obj, ModelForm):
        name = obj._meta.model._meta.verbose_name
    else:
        if isinstance(obj, Model):
            name = obj._meta.verbose_name
        else:
            raise Exception(b'Unhandled type: ' + type(obj))
        if capitalize:
            return name.capitalize()
    return name


model_verbose.is_safe = False

@register.filter
def user_can_edit(obj, user):
    """
    If a model implements the user_can_edit method,
    this filter returns the result of the method.
    """
    if hasattr(obj, b'user_can_edit'):
        return obj.user_can_edit(user)
    else:
        return