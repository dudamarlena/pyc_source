# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thorsten/code/django-propeller/django_propeller/components.py
# Compiled at: 2017-03-24 13:36:01
from __future__ import unicode_literals
from django.utils.safestring import mark_safe
from django_propeller.exceptions import PropellerError
from django_propeller.utils import render_tag, add_css_class
from .text import text_value, text_concat

def render_icon(icon, size=b'sm', **kwargs):
    """Render a Google icon"""
    attrs = {b'class': add_css_class((b'material-icons pmd-{size}').format(size=size), kwargs.get(b'extra_classes', b''))}
    title = kwargs.get(b'title')
    if title:
        attrs[b'title'] = title
    return render_tag(b'i', attrs=attrs, content=icon)


def render_bootstrap_icon(icon, **kwargs):
    """Render a Bootstrap glyphicon icon"""
    attrs = {b'class': add_css_class((b'glyphicon glyphicon-{icon}').format(icon=icon), kwargs.get(b'extra_classes', b''))}
    title = kwargs.get(b'title')
    if title:
        attrs[b'title'] = title
    return render_tag(b'span', attrs=attrs)


def render_alert(content, alert_type=None, dismissable=True):
    """Render a Bootstrap alert"""
    button = b''
    if not alert_type:
        alert_type = b'info'
    css_classes = [
     b'alert', b'alert-' + text_value(alert_type)]
    if dismissable:
        css_classes.append(b'alert-dismissable')
        button = b'<button type="button" class="close" ' + b'data-dismiss="alert" aria-hidden="true">&times;</button>'
    button_placeholder = b'__BUTTON__'
    return mark_safe(render_tag(b'div', attrs={b'class': (b' ').join(css_classes)}, content=button_placeholder + text_value(content)).replace(button_placeholder, button))


class Image(object):
    """Render an image object"""
    source = b''
    link = None
    width = None
    height = None
    responsive = False
    avatar = False

    def __init__(self, source=b'', link=None, width=None, height=None, responsive=False, avatar=False):
        self.source = source
        self.link = link
        self.width = width
        self.height = height
        self.responsive = responsive
        self.avatar = avatar

    def as_html(self):
        img_str = b''
        if self.link:
            img_str += b'<a'
            if self.avatar:
                img_str += b' class="avatar-list-img"'
            img_str += b'>'
        img_str += b'<img src="%s"' % self.source
        if self.width:
            img_str += b' width="%d"' % int(self.width)
        if self.height:
            img_str += b' height="%d"' % int(self.height)
        if self.responsive:
            img_str += b' class="img-responsive"'
        img_str += b'>'
        if self.link:
            img_str += b'</a>'
        return img_str


class Button(object):
    """Render a button with content"""
    attrs = {}
    content = b''
    classes = []

    def __init__(self, content, button_type=b'button', icon=None, button_class=None, size=None, href=None, name=None, value=None, title=None, style=b'default', extra_classes=b'', _id=b''):
        pmd_class = b'pmd-ripple-effect'
        if not button_class:
            button_class = b'btn-default'
        self.classes = add_css_class(b'btn', button_class)
        self.classes = add_css_class(self.classes, pmd_class)
        size = text_value(size).lower().strip()
        self.content = content
        if size == b'xs':
            self.classes = add_css_class(self.classes, b'btn-xs')
        elif size == b'sm' or size == b'small':
            self.classes = add_css_class(self.classes, b'btn-sm')
        elif size == b'lg' or size == b'large':
            self.classes = add_css_class(self.classes, b'btn-lg')
        elif size == b'md' or size == b'medium':
            pass
        elif size:
            raise PropellerError(b'Parameter "size" should be "xs", "sm", "lg" or ' + (b'empty ("{}" given).').format(size))
        if button_type:
            if button_type not in ('submit', 'reset', 'button', 'link'):
                raise PropellerError(b'Parameter "button_type" should be "submit", "reset", ' + (b'"button", "link" or empty  ("{}" given).').format(button_type))
            self.attrs[b'type'] = button_type
        if style not in ('default', 'raised', 'flat', 'outline'):
            raise PropellerError(b'Parameter "style" should be "default", "raised", ' + (b'"flat", "outline" or empty  ("{}" given).').format(style))
        else:
            self.classes = add_css_class(self.classes, b'pmd-btn-%s' % style)
            self.classes = add_css_class(self.classes, extra_classes)
        self.icon_content = render_icon(icon) if icon else b''
        if href:
            self.attrs[b'href'] = href
            self.tag = b'a'
        else:
            self.tag = b'button'
        if _id:
            self.attrs[b'id'] = _id
        if name:
            self.attrs[b'name'] = name
        if value:
            self.attrs[b'value'] = value
        if title:
            self.attrs[b'title'] = title

    def as_html(self):
        self.attrs[b'class'] = self.classes
        return render_tag(self.tag, attrs=self.attrs, content=mark_safe(text_concat(self.icon_content, self.content, separator=b' ')))


class FAB(object):
    """Render a floating action button"""
    attrs = {}
    content = b''
    classes = []

    def __init__(self, content, button_type=b'button', icon=None, button_class=None, size=None, href=None, name=None, value=None, title=None, style=b'default', extra_classes=b'', _id=b''):
        pmd_class = b'pmd-ripple-effect'
        if not button_class:
            button_class = b'btn-default'
        self.classes = add_css_class(b'', b'btn')
        size = text_value(size).lower().strip()
        self.content = content
        if size == b'xs':
            self.classes = add_css_class(self.classes, b'btn-xs')
        elif size == b'sm' or size == b'small':
            self.classes = add_css_class(self.classes, b'btn-sm')
        elif size == b'lg' or size == b'large':
            self.classes = add_css_class(self.classes, b'btn-lg')
        elif size == b'md' or size == b'medium':
            pass
        elif size:
            raise PropellerError(b'Parameter "size" should be "xs", "sm", "lg" or ' + (b'empty ("{}" given).').format(size))
        self.classes = add_css_class(self.classes, b'pmd-btn-fab')
        if button_type:
            if button_type not in ('submit', 'reset', 'button', 'link'):
                raise PropellerError(b'Parameter "button_type" should be "submit", "reset", ' + (b'"button", "link" or empty  ("{}" given).').format(button_type))
            self.attrs[b'type'] = button_type
        if style not in ('default', 'raised', 'flat', 'outline'):
            raise PropellerError(b'Parameter "style" should be "default", "raised", ' + (b'"flat", "outline" or empty  ("{}" given).').format(style))
        else:
            self.classes = add_css_class(self.classes, b'pmd-btn-%s' % style)
        self.classes = add_css_class(self.classes, pmd_class)
        self.classes = add_css_class(self.classes, extra_classes)
        self.icon_content = render_icon(icon) if icon else b''
        if href:
            self.attrs[b'href'] = href
            self.tag = b'a'
        else:
            self.tag = b'button'
        if _id:
            self.attrs[b'id'] = _id
        if name:
            self.attrs[b'name'] = name
        if value:
            self.attrs[b'value'] = value
        if title:
            self.attrs[b'title'] = title
        self.classes = add_css_class(self.classes, button_class)

    def as_html(self):
        self.attrs[b'class'] = self.classes
        return render_tag(self.tag, attrs=self.attrs, content=mark_safe(text_concat(self.icon_content, self.content, separator=b' ')))