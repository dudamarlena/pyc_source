# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Development\django2-propeller\django2_propeller\card.py
# Compiled at: 2019-04-26 08:32:14
# Size of source mod 2**32: 10322 bytes
"""This module contains classes for constructing propeller cards"""
from django.utils.safestring import mark_safe
from .utils import render_tag, add_css_class
from .components import Button, FAB, Image
from .text import text_concat
from .exceptions import PropellerException

class CardTitle(object):
    __doc__ = '\n    Renders a Card Title.\n\n    **Parameters**:\n\n        text\n            The display text for the title.\n\n        size\n            The size for the title as integer. Works with the h-tag, so size=1 is bigger than size=3.\n            Optional. (default=3)\n    '
    text = ''
    size = 3

    def as_html(self):
        """Returns card title as html"""
        tag = 'h%d' % self.size
        attrs = {'class': 'pmd-card-title-text'}
        content = self.text
        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))


class CardSubtitle(object):
    __doc__ = '\n    Renders a Card Subtitle.\n\n    **Parameters**:\n\n        text\n            The display text for the subtitle.\n    '
    text = ''

    def as_html(self):
        """Returns card subtitle as html"""
        tag = 'span'
        attrs = {'class': 'pmd-card-subtitle-text'}
        content = self.text
        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))


class CardBody(object):
    __doc__ = '\n    Renders a Card Body.\n\n    **Parameters**:\n\n        text\n            The text to display in the body.\n    '
    text = ''

    def as_html(self):
        """Returns card body as html"""
        tag = 'div'
        attrs = {'class': 'pmd-card-body'}
        content = self.text
        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))


class CardHeader(object):
    __doc__ = '\n    Renders a Card Header.\n\n    **Parameters**:\n\n        content_left\n            A list of items to display on the left of header. \n            May contain Button, FAB, Image, CardTitle, or CardSubtitle.\n\n        content_middle\n            A list of items to display in the middle of header. \n            May contain Button, FAB, Image, CardTitle, or CardSubtitle.\n    '
    content_left = []
    content_middle = []

    def get_left_content(self):
        """Returns left content of card header as html"""
        tag = 'div'
        attrs = {'class': 'media-left'}
        content = ''
        for itm in self.content_left:
            content = text_concat(content, mark_safe(itm.as_html()))

        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))

    def get_middle_content(self):
        """Returns middle content of card header as html"""
        tag = 'div'
        attrs = {'class': 'media-body media-middle'}
        content = ''
        for itm in self.content_middle:
            content = text_concat(content, mark_safe(itm.as_html()))

        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))

    def as_html(self):
        """Returns card header as html"""
        tag = 'div'
        attrs = {'class': 'pmd-card-title'}
        content = text_concat(self.get_left_content(), self.get_middle_content())
        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))


class CardMediaActions(object):
    __doc__ = '\n    Renders Card Media Actions.\n\n    **Parameters**:\n\n        items\n            A list of items to display in the Card Media Action section. \n            May contain Button or FAB.\n    '
    items = []

    def as_html(self):
        """Returns card media actions as html"""
        tag = 'div'
        attrs = {'class': 'pmd-card-actions'}
        content = ''
        for btn in self.items:
            if isinstance(btn, FAB):
                content = text_concat(content, mark_safe(btn.as_html()))

        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))


class CardActions(object):
    __doc__ = '\n    Renders Card Actions.\n\n    **Parameters**:\n\n        items\n            A list of items to display in the Card Action section. \n            May contain Button or FAB.\n    '
    items = []

    def as_html(self):
        """Returns card actions as html"""
        tag = 'div'
        attrs = {'class': 'pmd-card-actions'}
        content = ''
        for btn in self.items:
            if isinstance(btn, Button):
                content = text_concat(content, mark_safe(btn.as_html()))

        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))


class CardMediaImage(object):
    __doc__ = '\n    Renders a Card Media Image.\n\n    **Parameters**:\n\n        image\n            Must be an instance of an Image.\n    '
    image = None

    def as_html(self):
        """Returns card media image as html"""
        if isinstance(self.image, Image):
            return self.image.as_html()


class CardMedia(object):
    __doc__ = '\n    Renders Card Media\n\n    **Parameters**:\n\n        content\n            if style_inline=True:\n                A list of items to display in the card media section. \n                May contain CardMediaImage, CardTitle, or CardSubtitle.\n            or if style_inline=False: (default)\n                A instance of CardMediaImage\n\n        style_inline\n            Display card with inline style if true. (Default: False)\n    '
    content = None
    style_inline = False

    def get_media_body_inline(self):
        """Returns media body inline as html"""
        tag = 'div'
        attrs = {'class': 'media-body'}
        content = ''
        if self.style_inline:
            if not isinstance(self.content, list):
                raise PropellerException('Propeller Card: content must be a list')
            for itm in self.content:
                if isinstance(itm, (CardTitle, CardSubtitle)):
                    content = text_concat(content, mark_safe(itm.as_html()))

            content = text_concat(content, mark_safe('</div>'))
            content = text_concat(content, mark_safe('<div class="media-right media-middle">'))
            for itm in self.content:
                if isinstance(itm, CardMediaImage):
                    content = text_concat(content, mark_safe(itm.as_html()))

        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))

    def get_media_body(self):
        """Returns media body as html"""
        if self.style_inline:
            return self.get_media_body_inline()
        tag = 'div'
        attrs = {'class': 'media-body'}
        content = ''
        if not isinstance(self.content, list):
            raise PropellerException('Propeller Card: content must be a list')
        for itm in self.content:
            if isinstance(itm, CardMediaImage):
                content = text_concat(content, mark_safe(itm.as_html()))

        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))

    def as_html(self):
        """Returns card media as html"""
        tag = 'div'
        attrs = {'class': 'pmd-card-media'}
        content = self.get_media_body()
        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))


class Card(object):
    __doc__ = '\n    Card is a class that generates a Propeller Card.\n\n    **Parameters**:\n\n        primary_title\n            An instance of CardTitle. Optional.\n\n        secondary_title\n            An instance of CardSubtitle. Optional.\n\n        header\n            An instance of CardHeader. Optional.\n\n        media\n            An instance of CardMedia. Optional.\n\n        body\n            An instance of CardBody. Optional.\n\n        actions\n            An instance of CardActions. Optional.\n\n        media_actions\n            An instance of CardMediaActions. Optional.\n\n        style_inverse\n            Display dark style if true. (Default: False)\n\n        style_inline\n            Display card with inline style if true. (Default: False)\n\n        width\n            Width of the card in Bootstrap grid (col-md) as integer. (Default: 4)\n    '
    primary_title = None
    secondary_title = None
    header = None
    media = None
    body = None
    actions = None
    media_actions = None
    style_inverse = False
    style_inline = False
    width = 4

    def get_actions(self):
        """Returns actions of card as html"""
        actions = ''
        if self.media_actions:
            actions = text_concat(actions, self.media_actions.as_html())
        if self.actions:
            actions = text_concat(actions, self.actions.as_html())
        return actions

    def get_content(self):
        """Returns content of card as html"""
        content = ''
        if self.header:
            if not self.style_inline:
                content = text_concat(content, self.header.as_html())
        if self.media:
            content = text_concat(content, self.media.as_html())
        if not self.style_inline:
            if self.primary_title or self.secondary_title:
                content = text_concat(content, '<div class="pmd-card-title">')
                if self.primary_title:
                    content = text_concat(content, self.primary_title.as_html())
                if self.secondary_title:
                    content = text_concat(content, self.secondary_title.as_html())
                content = text_concat(content, '</div>')
            if self.body:
                content = text_concat(content, self.body.as_html())
        content = text_concat(content, self.get_actions())
        return content

    def as_html(self):
        """Returns card as html"""
        tag = 'div'
        classes = 'pmd-card'
        if self.style_inline:
            classes = add_css_class(classes, 'pmd-card-media-inline')
        elif self.style_inverse:
            classes = add_css_class(classes, 'pmd-card-inverse')
        else:
            classes = add_css_class(classes, 'pmd-card-default')
        classes = add_css_class(classes, 'pmd-z-depth')
        classes = add_css_class(classes, 'col-md-%d' % self.width)
        attrs = {'class': classes}
        content = self.get_content()
        return render_tag(tag, attrs=attrs, content=(mark_safe(content)))