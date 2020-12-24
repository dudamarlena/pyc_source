# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ir4y/projects/python/virtualenv/miniature_ve/miniature_ironman/miniature/models/mixins.py
# Compiled at: 2014-04-11 02:06:12
import pytils
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from miniature.models.fields import AutoSlugField
from miniature.models.utils import create_model
__author__ = 'ir4y'

class ActiveManager(models.Manager):

    def active(self):
        return super(ActiveManager, self).get_queryset().filter(is_active='True')


class ActiveMixin(models.Model):
    is_active = models.BooleanField(verbose_name=_('Активно'), default=False)
    objects = ActiveManager()

    class Meta:
        abstract = True


class CreateUpdateMixin(models.Model):
    create = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    update = models.DateTimeField(auto_now=True, verbose_name=_('Дата изменения'))

    class Meta:
        abstract = True


class SEOTagsMixin(models.Model):
    keywords = models.TextField(verbose_name=_('Ключевые слова'), blank=True, null=True)
    description = models.TextField(verbose_name=_('Описание'), blank=True, null=True)

    class Meta:
        abstract = True


class GenericRelationMixin(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


def SlugTraits(base_filed_name='name'):
    u"""
    Функция генерирующая Mixin к модели
    Добавлющий _slug поле к указанному полю
    При сохраении в это поле записывается slug от указанного поля
    Описание класса на метаязыке
    class SlugMixin(models.Model):
        base_filed_name + '_slug' = models.CharField(
            verbose_name=_(u'Название для url'),max_length=150,
            blank=True,null=True)
        class Meta:
            abstract = True
    """
    fileld_name = base_filed_name + '_slug'
    fields = {fileld_name: AutoSlugField(verbose_name=_('Название для url'), populate_from='{' + base_filed_name + '}', max_length=150, blank=True, null=True)}
    _SlugMixin = create_model('SlugMixin', fields=fields, module='miniature.models.mixins', options={'abstract': True})
    return _SlugMixin