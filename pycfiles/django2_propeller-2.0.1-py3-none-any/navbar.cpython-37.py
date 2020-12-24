# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Development\django2-propeller\django2_propeller\navbar.py
# Compiled at: 2019-04-26 11:29:13
# Size of source mod 2**32: 8035 bytes
"""This module contains classes for constructing propeller navbars"""
from django.utils.safestring import mark_safe
from .utils import render_tag, add_css_class
from .text import text_concat
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

class NavBarLinkItem(object):
    __doc__ = "\n    Generates a Link navbar item or a Link DropDown item.\n\n    **Parameters**:\n\n        name\n            The display name for the item. (for example: 'Home')\n\n        url\n            The address for the link item. Can be a absolute URL or a resolvable Django url.\n            (for example: 'http://example.org' or 'home'). Optional.\n\n        icon\n            not yet supported\n    "
    name = None
    url = None
    icon = None

    def __init__(self, name='', url=None, icon=None):
        """

        """
        self.name = name
        self.url = url
        self.icon = icon

    def get_url(self):
        """
        Returns the url set in the attribute.

        **Returns**

            ``javascript:void(0);`` if ``url = None``

            or

            an absolute URL if ``url`` starts with 'http'

            or

            an relative URL if ``url`` is a resolvable Django url
        """
        if self.url:
            if not str(self.url).startswith('http'):
                return reverse(self.url)
            return self.url
        return 'javascript:void(0);'

    def as_html(self):
        """Returns navbar link item as html"""
        tag = 'a'
        attrs = {'class':'pmd-ripple-effect',  'href':self.get_url()}
        content = self.name
        return '<li>' + render_tag(tag, attrs=attrs, content=(mark_safe(content))) + '</li>'


class NavBarDropDownDivider(object):
    __doc__ = 'Generates a DropDown Divider item.'

    @staticmethod
    def as_html():
        """Returns navbar dropdown divider as html"""
        tag = 'li'
        attrs = {'role':'separator',  'class':'divider'}
        return render_tag(tag, attrs=attrs)


class NavBarDropDownItem(NavBarLinkItem):
    __doc__ = "\n    Generates a DropDown navbar item.\n\n    **Parameters**:\n\n        name\n            The display name for the item. (for example: 'Home')\n\n        url\n            The address for the link item. Can be a absolute URL or a resolvable Django url.\n            (for example: 'http://example.org' or 'home'). Optional.\n\n        icon\n            not yet supported\n\n        items\n            A list containing NavBarLinkItems and/or NavBarDropDownDivider. Optional.\n    "
    items = []

    def __init__(self, name='', items=None, url=None):
        super(NavBarDropDownItem, self).__init__(name, url)
        if items:
            self.items = items

    def as_html(self):
        """Returns navbar dropdown item as html"""
        tag = 'li'
        attrs = {'class': 'dropdown pmd-dropdown'}
        content = '<a data-toggle="dropdown" class="pmd-ripple-effect dropdown-toggle" data-sidebar="true" href="%s">%s<span class="caret"></span></a>' % (
         self.url, self.name)
        content = text_concat(content, '<ul class="dropdown-menu">')
        for itm in self.items:
            content = text_concat(content, itm.as_html())

        content = text_concat(content, '</ul>')
        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))


class NavBar(object):
    __doc__ = "\n    NavBar is a class that generates a NavBar.\n\n    **Parameters**:\n\n        brandname\n            The brand shown on the very left of the navbar.\n\n        brandurl\n            The address for the brand name. Can be a absolute URL or a resolvable Django url.\n            (for example: 'http://example.org' or 'home'). Optional.\n\n        items\n            A list containing NavBarLinkItems and/or NavBarDropDownItems. Optional.\n\n        style_inverse\n            Generate a dark navbar if true (default) or a light navbar if false.\n\n        style_static\n            Sets the static style for the navbar. Static if true (default) or floating on top if false.\n    "
    brandname = ''
    brandurl = None
    items = []
    style_inverse = True
    style_static = True

    def get_brand_url(self):
        """
        Returns the brand url set in the attribute.

        **Returns**

            ``javascript:void(0);`` if ``brandurl = None``

            or

            an absolute URL if ``brandurl`` starts with 'http'

            or

            an relative URL if ``brandurl`` is a resolvable Django url
        """
        if self.brandurl:
            if not str(self.brandurl).startswith('http'):
                return reverse(self.brandurl)
            return self.brandurl
        return 'javascript:void(0);'

    @staticmethod
    def render_toggle():
        """Returns navbar toggle as html (for responsive)"""
        tag = 'button'
        attrs = {'class':'navbar-toggle collapsed', 
         'type':'button', 
         'data-toggle':'collapse', 
         'aria-expanded':'false'}
        content = '<span class="sr-only">Toggle navigation</span>'
        content = text_concat(content, '<span class="icon-bar"></span>')
        content = text_concat(content, '<span class="icon-bar"></span>')
        content = text_concat(content, '<span class="icon-bar"></span>')
        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))

    def render_header(self):
        """Returns navbar header as html"""
        tag = 'div'
        attrs = {'class': 'navbar-header'}
        content = self.render_toggle()
        content = text_concat(content, '<a href="%s" class="navbar-brand navbar-brand-custome">%s</a>' % (
         self.get_brand_url(), self.brandname))
        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))

    def render_items(self):
        """Returns navbar items as html (for item container)"""
        tag = 'ul'
        attrs = {'class': 'nav navbar-nav'}
        content = ''
        for itm in self.items:
            content = text_concat(content, itm.as_html())

        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))

    def render_item_container(self):
        """Returns navbar items as html"""
        tag = 'div'
        attrs = {'class': 'collapse navbar-collapse'}
        content = self.render_items()
        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))

    def render_content(self):
        """Returns navbar content as html"""
        tag = 'div'
        attrs = {'class': 'container-fluid'}
        content = self.render_header()
        content = text_concat(content, self.render_item_container())
        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))

    def as_html(self):
        """Returns navbar as html"""
        tag = 'nav'
        classes = 'navbar'
        if self.style_inverse:
            classes = add_css_class(classes, 'navbar-inverse')
        elif self.style_static:
            classes = add_css_class(classes, 'navbar-static')
        else:
            classes = add_css_class(classes, 'navbar-top')
        classes = add_css_class(classes, 'pmd-navbar')
        classes = add_css_class(classes, 'pmd-z-depth')
        attrs = {'class': classes}
        content = self.render_content()
        content = text_concat(content, '<div class="pmd-sidebar-overlay"></div>')
        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))


class CustomItem(object):
    __doc__ = '\n    Returns a custom NavBar item.\n\n    Just assign some raw HTML code to `html` attribute.\n    '
    html = ''

    def __init__(self, html=''):
        self.html = html

    def as_html(self):
        return self.html