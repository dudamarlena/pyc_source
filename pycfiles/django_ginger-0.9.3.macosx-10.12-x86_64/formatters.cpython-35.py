# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/formatters/formatters.py
# Compiled at: 2016-12-22 04:56:36
# Size of source mod 2**32: 1768 bytes
from django.utils.formats import localize
from django.utils import timezone
from .base import Formatter

class ChoiceFormatter(Formatter):

    def format(self, value, name, source):
        parts = name.split('__')
        tail = parts.pop()
        while parts:
            item = parts.pop(0)
            source = getattr(source, item)

        return getattr(source, 'get_%s_display' % tail)()


class FileFormatter(Formatter):

    def __init__(self, **kwargs):
        kwargs.setdefault('variants', 'detail')
        super(FileFormatter, self).__init__(**kwargs)

    def format(self, value, name, source):
        if not value:
            return ''
        obj = value
        url = obj.url
        name = obj.name
        tag = "<a href='%s'>%s</a>" % (url, name)
        return tag


class ImageFormatter(Formatter):

    def __init__(self, **kwargs):
        self.width = kwargs.pop('width', 48)
        self.height = kwargs.pop('height', 48)
        kwargs.setdefault('variants', 'detail')
        super(ImageFormatter, self).__init__(**kwargs)

    def format(self, value, name, source):
        if not value:
            return ''
        url = value.url
        tag = "<img src='%s' width='%s' height='%s' >" % (url, self.width, self.height)
        return tag


class DateTimeFormatter(Formatter):

    def format(self, value, name, source):
        if value:
            if timezone.is_naive(value):
                value = timezone.make_aware(value)
            value = timezone.localtime(value)
        return localize(value)


class DateFormatter(Formatter):

    def format(self, value, name, source):
        return localize(value)


class TimeFormatter(Formatter):

    def format(self, value, name, source):
        return localize(value)