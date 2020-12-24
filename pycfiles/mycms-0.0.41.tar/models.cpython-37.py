# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/models.py
# Compiled at: 2019-02-26 14:57:21
# Size of source mod 2**32: 10300 bytes
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from django.db.models.signals import post_save
from django.db.utils import OperationalError
import pathlib
from datetime import datetime
import django.core.cache as cache
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from mycms.creole import creole2html
from rest_framework.authtoken.models import Token
from loremipsum import generate_paragraphs

class CMSPaths(models.Model):
    path = models.CharField(max_length=2000, null=True)
    parent = models.ForeignKey('CMSPaths', null=True, blank=True, on_delete=(models.DO_NOTHING))

    def __str__(self):
        return self.path


class CMSTags(models.Model):
    name = models.CharField(max_length=256, default='NotSet')

    def __str__(self):
        return self.name


class CMSMarkUps(models.Model):
    markup = models.CharField(max_length=128, default='Creole')

    def __str__(self):
        return self.markup


class CMSContents(models.Model):
    title = models.CharField(max_length=1024, null=True, blank=True)
    content = models.TextField(max_length=20480, default='Empty')
    timestamp = models.DateTimeField(auto_now=True)
    markup = models.ForeignKey(CMSMarkUps, null=True, on_delete=(models.DO_NOTHING))
    meta_description = models.TextField(max_length=20480, default='', blank=True)
    tags = models.ManyToManyField(CMSTags, blank=True)
    page = models.IntegerField(default=1)

    def __str__(self):
        return self.content

    @property
    def html(self):
        from mycms.view_handlers.formatters import CreoleFormatter
        return CreoleFormatter(self.content).html()


class CMSTemplates(models.Model):
    name = models.CharField(max_length=1024, default='page.html')
    template = models.TextField(max_length=10240, default='empty template')

    def __str__(self):
        return self.name


class CMSPageTypes(models.Model):
    page_type = models.CharField(max_length=64, default='DefaultType')
    text = models.CharField(max_length=128, default='default class')
    view_class = models.CharField(max_length=256, default='DefaultView')
    view_template = models.CharField(max_length=32, default=None)

    def save(self, *args, **kwargs):
        if self.view_template is None:
            self.view_template = 'DefaultView.html'
        (super(CMSPageTypes, self).save)(*args, **kwargs)

    def __str__(self):
        return self.text


def get_admin_user():
    try:
        admin = User.objects.get(username='admin')
        return admin
    except OperationalError as e:
        try:
            return 1
        finally:
            e = None
            del e


class CMSEntries(models.Model):
    title = models.CharField(max_length=1024, default=None)
    path = models.ForeignKey(CMSPaths, null=True,
      on_delete=(models.DO_NOTHING))
    slug = models.SlugField(max_length=1024, unique=True)
    content = models.ManyToManyField(CMSContents, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    page_type = models.ForeignKey('CMSPageTypes', null=True,
      on_delete=(models.DO_NOTHING))
    template = models.ForeignKey(CMSTemplates, null=True,
      blank=True,
      on_delete=(models.DO_NOTHING))
    frontpage = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    lists_include = models.BooleanField(default=True)
    page_number = models.IntegerField(default=1)
    created_by = models.ForeignKey(User, null=True,
      blank=True,
      on_delete=(models.DO_NOTHING))
    logo_url = models.CharField(default='/static/mycms/images/png/default.png', null=True,
      blank=True,
      max_length=1024)

    def toggle_published(self):
        if self.published:
            self.published = False
        else:
            self.published = True

    def toggle_frontpage(self):
        if self.frontpage:
            self.frontpage = False
        else:
            self.frontpage = True

    def on_create(self):
        view_object = self.view
        if hasattr(view_object, 'on_create'):
            view_object.on_create()

    def parent(self):
        parent_entry = CMSEntries.objects.get(path=(self.path.parent))
        return parent_entry

    def html_content(self):
        return self.view.html_content

    def __str__(self):
        return self.title

    @property
    def date_created_str(self):
        """"""
        value = self.date_created
        return value

    @property
    def date_modified_str(self):
        """"""
        value = self.date_modified.strftime('%Y%m%d %H:%M')
        return value

    @property
    def view(self):
        from mycms.view_handlers import ViewObject
        view_object = ViewObject(page_object=self)
        return view_object

    @property
    def view_object(self):
        return self.view

    def get_absolute_url(self):
        cms_base_path = getattr(settings, 'YACMS_BASEPATH', None)
        if not cms_base_path:
            cms_base_path = '/cms'
        if not cms_base_path.endswith('/'):
            cms_base_path = cms_base_path.rstrip('/')
        return '{}{}'.format(cms_base_path, self.path.path)

    def get_parent_paths(self, path_str):
        x = path_str.rfind('/')
        if x == 0:
            return [path_str]
        return self.get_parent_paths(path_str[:x]) + [path_str]

    def parents_list(self):
        path_str = self.path.path
        p = self.get_parent_paths(path_str)
        pl = []
        for path_str in p:
            pl.append(CMSEntries.objects.get(path__path=path_str))

        return pl

    def categories(self):
        c = CMSEntries.objects.filter(path__parent=(self.path), page_type__page_type='CATEGORY',
          published=True)
        return c

    def save(self, *args, **kwargs):
        if self.pk is None:
            (super(CMSEntries, self).save)(*args, **kwargs)
        else:
            (super(CMSEntries, self).save)(*args, **kwargs)


class CMSArchivesIndex(models.Model):
    month = models.IntegerField(default=0)
    year = models.IntegerField(default=1975)
    entries = models.ManyToManyField(CMSEntries, blank=True)


@receiver(post_save, sender=(settings.AUTH_USER_MODEL))
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)