# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/halit/pytr/pytrorg/src/sources/models.py
# Compiled at: 2012-09-09 10:22:49
from django.db import models
from django.contrib.auth.models import User
from unidecode import unidecode
from tagging.fields import TagField, Tag

class Categories(models.Model):
    title = models.CharField(max_length=255, verbose_name='Baslik')
    sef_title = models.CharField(max_length=255, blank=True, editable=False)
    slug = models.SlugField(max_length=255, verbose_name='Slug')
    description = models.CharField(max_length=255, verbose_name='Aciklama')
    sef_description = models.CharField(max_length=255, blank=True, editable=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Kategoriler'

    def get_absolute_url(self):
        return '/kaynak/kategori/%s/' % self.slug

    def save(self, *args, **kwargs):
        self.sef_title = unidecode(self.title)
        super(Categories, self).save(*args, **kwargs)
        self.sef_description = unidecode(self.description)
        super(Categories, self).save(*args, **kwargs)


class Types(models.Model):
    title = models.CharField(max_length=255, verbose_name='Baslik')
    sef_title = models.CharField(max_length=255, blank=True, editable=False)
    slug = models.SlugField(max_length=255, verbose_name='Slug')
    description = models.CharField(max_length=255, verbose_name='Aciklama')
    sef_description = models.CharField(max_length=255, blank=True, editable=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Turler'

    def get_absolute_url(self):
        return '/kaynak/tur/%s/' % self.slug

    def save(self, *args, **kwargs):
        self.sef_title = unidecode(self.title)
        super(Types, self).save(*args, **kwargs)
        self.sef_description = unidecode(self.description)
        super(Types, self).save(*args, **kwargs)


class Sources(models.Model):
    title = models.CharField(max_length=255, verbose_name='Baslik')
    sef_title = models.CharField(max_length=255, blank=True, editable=False)
    slug = models.SlugField(max_length=255, verbose_name='Slug')
    description = models.CharField(max_length=255, verbose_name='Aciklama')
    sef_description = models.CharField(max_length=255, blank=True, editable=False)
    categories = models.ManyToManyField(Categories, verbose_name='Kategoriler', blank=True)
    types = models.ManyToManyField(Types, verbose_name='Turler', blank=True)
    link = models.URLField(verbose_name='Linki', blank=False)
    isonline = models.BooleanField(verbose_name='Kaynak yayinlansin mi?', default=False)
    tags = TagField(verbose_name='Etiketler')
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Olusturulma')
    edited = models.DateTimeField(auto_now=True, editable=False, verbose_name='Degistirilme')
    author = models.ForeignKey(User, verbose_name='Yazar')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Kaynaklar'

    def get_absolute_url(self):
        return '/kaynak/%s/' % self.slug

    def save(self, *args, **kwargs):
        self.sef_title = unidecode(self.title)
        super(Sources, self).save(*args, **kwargs)
        self.sef_description = unidecode(self.description)
        super(Sources, self).save(*args, **kwargs)

    def get_tags(self):
        return Tag.objects.get_for_object(self)