# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/models/tags.py
# Compiled at: 2017-07-21 05:10:28
# Size of source mod 2**32: 1052 bytes
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
__all__ = ('Tag', 'TagQuerySet')

class TagQuerySet(models.QuerySet):

    @property
    def as_url_encoded(self):
        """
        Return queryset as URL encoded string that is compatible with
        the article views.
        """
        tag_pks = list(sorted(self.values_list('pk', flat=True)))
        return urlencode({'filter_tags': ','.join(str(pk) for pk in tag_pks)})


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=200, unique=True)
    slug = models.SlugField(verbose_name=_('slug'), max_length=200, unique=True)
    objects = TagQuerySet.as_manager()

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        ordering = ('name', )

    def __str__(self):
        return self.name