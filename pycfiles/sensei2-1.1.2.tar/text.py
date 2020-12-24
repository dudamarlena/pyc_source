# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/xacce/addit/Projects/inventory/venv/src/sensei2/sensei2/sensei/handlers/text.py
# Compiled at: 2015-11-09 14:24:15
from random import randint, choice
from autoslug import AutoSlugField
from pytils.translit import slugify
from sensei2.sensei.handlers.base import BaseHandler
from django.db import models

class CharFieldHandler(BaseHandler):

    def __init__(self):
        super(CharFieldHandler, self).__init__()
        self.handled_class = models.CharField

    def prepare_value(self, obj, field, sensei):
        if field.choices:
            return choice([ x[0] for x in field.choices ])
        if field.attname == 'full_name':
            value = (' ').join([
             sensei.get_from_data('surnames'), sensei.get_from_data('names'), sensei.get_from_data('patronymics')])
        elif field.attname in ('last_name', 'surname'):
            value = sensei.get_from_data('surnames')
        elif field.attname in ('first_name', 'name'):
            value = sensei.get_from_data('names')
        elif field.attname in ('patronymic', ):
            value = sensei.get_from_data('patronymics')
        elif field.attname in ('town', 'city', 'district', 'region'):
            value = sensei.get_from_data('cities')
        elif field.attname in ('country', ):
            value = sensei.get_from_data('countries')
        elif field.attname in ('currency', 'money', 'valuta'):
            value = sensei.get_from_data('currency')
        else:
            value = sensei.get_from_data('subjects')
        return value[:getattr(field, 'max_length')]


class TextFieldHandler(BaseHandler):

    def __init__(self):
        super(TextFieldHandler, self).__init__()
        self.handled_class = models.TextField

    def is_my_field(self, field):
        return isinstance(field, self.handled_class)

    def prepare_value(self, obj, field, sensei):
        value = sensei.get_from_data('paragraphs')
        if hasattr(field, 'max_length'):
            length = getattr(field, 'max_length')
            if len(value) <= length:
                return value
            return value[:length]
        else:
            return value


class EmailFieldHnadler(BaseHandler):

    def __init__(self):
        super(EmailFieldHnadler, self).__init__()
        self.handled_class = models.EmailField

    def prepare_value(self, obj, field, sensei):
        return sensei.get_random_email()


class SlugFieldHandler(BaseHandler):

    def __init__(self):
        super(SlugFieldHandler, self).__init__()
        self.handled_class = models.SlugField

    def prepare_value(self, obj, field, sensei):
        return slugify(unicode(obj))


class AutoSlugFieldHandler(BaseHandler):

    def __init__(self):
        super(AutoSlugFieldHandler, self).__init__()
        self.handled_class = AutoSlugField

    def pre_handle(self, obj, field, sensei):
        pass


class URLFieldHandler(BaseHandler):

    def __init__(self):
        super(URLFieldHandler, self).__init__()
        self.handled_class = models.URLField

    def prepare_value(self, obj, field, sensei):
        return sensei.get_random_url()


class IPAddressFieldHandler(BaseHandler):

    def __init__(self):
        super(IPAddressFieldHandler, self).__init__()
        self.handled_class = models.IPAddressField

    def prepare_value(self, obj, field, sensei):
        print 'Field type IPAddressField is deprecated. Use GenericIPAddressField instead'
        return sensei.get_random_ipv4()


class GenericIPAddressField(BaseHandler):

    def __init__(self):
        super(GenericIPAddressField, self).__init__()
        self.handled_class = models.GenericIPAddressField

    def prepare_value(self, obj, field, sensei):
        protocol = getattr(field, 'protocol')
        if protocol == 'IPv4':
            return sensei.get_random_ipv4()
        else:
            if protocol == 'IPv6':
                return sensei.get_random_ipv6()
            if randint(0, 1):
                return sensei.get_random_ipv6()
            return sensei.get_random_ipv4()