# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-places/vkontakte_places/models.py
# Compiled at: 2015-02-19 12:23:17
import logging
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.db.models.query import QuerySet
from django.utils.encoding import python_2_unicode_compatible
from vkontakte_api import fields
from vkontakte_api.api import api_call
from vkontakte_api.models import VkontakteManager, VkontakteIDModel
from vkontakte_api.decorators import fetch_all
log = logging.getLogger('vkontakte_places')

class PlacesManager(VkontakteManager):

    def api_call(self, *args, **kwargs):
        if 'ids' in kwargs and 'get_by_ids' in self.methods:
            kwargs['cids'] = (',').join(map(lambda i: str(i), kwargs.pop('ids')))
            method = self.methods['get_by_ids']
        else:
            if 'country' in kwargs and isinstance(kwargs['country'], Country):
                kwargs['country'] = kwargs['country'].remote_id
            method = self.methods['get']
        return api_call((self.model.methods_namespace + '.' + method), **kwargs)

    def get(self, *args, **kwargs):
        """
        Apply country param request to all instances in reponse
        """
        country = None
        if 'country' in kwargs and self.model._meta.get_field('country'):
            if isinstance(kwargs['country'], Country):
                country = kwargs['country']
            else:
                country = Country.objects.get(remote_id=kwargs['country'])
        instances = super(PlacesManager, self).get(*args, **kwargs)
        if country:
            for instance in instances:
                instance.country = country

        return instances

    @fetch_all
    def fetch(self, *args, **kwargs):
        return super(PlacesManager, self).fetch(*args, **kwargs)


class PlacesModel(VkontakteIDModel):
    methods_namespace = 'places'

    class Meta:
        abstract = True

    def parse(self, response):
        super(PlacesModel, self).parse(response)
        if 'title' in response and not self.name:
            self.name = response['title']


@python_2_unicode_compatible
class Country(PlacesModel):
    remote_pk_field = 'cid'
    name = models.CharField(max_length=50)
    remote = PlacesManager(remote_pk=('remote_id', ), methods={'get': 'getCountries', 
       'get_by_ids': 'getCountryById'})

    class Meta:
        verbose_name = 'Страна Вконтакте'
        verbose_name_plural = 'Страны Вконтакте'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class City(PlacesModel):
    remote_pk_field = 'cid'
    country = models.ForeignKey(Country, null=True, related_name='cities', help_text='Страна')
    name = models.CharField(max_length=50)
    area = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    remote = PlacesManager(remote_pk=('remote_id', ), methods={'get': 'getCities', 
       'get_by_ids': 'getCityById'})

    class Meta:
        verbose_name = 'Город Вконтакте'
        verbose_name_plural = 'Города Вконтакте'

    def __str__(self):
        name = [
         self.name]
        if self.region:
            name += [self.region]
        if self.area:
            name += [self.area]
        return (', ').join(name)


@python_2_unicode_compatible
class Region(PlacesModel):
    remote_pk_field = 'region_id'
    country = models.ForeignKey(Country, related_name='regions', help_text='Страна')
    name = models.CharField(max_length=50)
    remote = PlacesManager(remote_pk=('remote_id', ), methods={'get': 'getRegions'})

    class Meta:
        verbose_name = 'Регион Вконтакте'
        verbose_name_plural = 'Регионы Вконтакте'

    def __str__(self):
        return self.name