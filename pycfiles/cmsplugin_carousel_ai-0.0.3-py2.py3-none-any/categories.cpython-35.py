# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/models/categories.py
# Compiled at: 2017-08-31 05:41:42
# Size of source mod 2**32: 1001 bytes
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
__all__ = ('Category', )

@python_2_unicode_compatible
class Category(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=200)
    slug = models.SlugField(max_length=200, verbose_name=_('URL slug'), unique=True, db_index=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Return the URL to the category's article list view.
        Note that this will raise NoReverseMatch if articles app hasn't
        been hooked to any CMS page.
        """
        return reverse('articles_in_category', kwargs={'category': self.slug})