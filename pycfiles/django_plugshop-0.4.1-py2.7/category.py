# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plugshop/models/category.py
# Compiled at: 2014-08-09 03:47:51
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager
from plugshop.utils import get_categories, is_default_model

class CategoryAbstractManager(TreeManager):

    def get_by_path(self, path):
        path_patterns = path.split('/')
        slug = path_patterns[(-1)]
        return self.get(slug=slug)


class CategoryAbstract(MPTTModel):
    objects = CategoryAbstractManager()

    class Meta:
        abstract = True
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    class MPTTMeta:
        ordering = [
         'pk', 'lft']

    parent = TreeForeignKey('self', null=True, blank=True, verbose_name=_('parent node'))
    name = models.CharField(_('name'), blank=False, max_length=80)
    slug = models.SlugField(_('slug'), blank=False, unique=True)

    def __unicode__(self):
        return self.name

    def get_ancestor_list(self):
        categories = get_categories()
        return [ n for n in categories if n.lft <= self.lft and n.rght >= self.rght and n.tree_id == self.tree_id
               ]

    def get_path(self):
        ancestors = self.get_ancestor_list()
        return ('/').join([ a.slug for a in ancestors ])

    @models.permalink
    def get_absolute_url(self):
        return ('plugshop-category', None, {'category_path': self.get_path()})


if is_default_model('CATEGORY'):

    class Category(CategoryAbstract):

        class Meta:
            verbose_name = _('category')
            verbose_name_plural = _('categories')
            app_label = 'plugshop'