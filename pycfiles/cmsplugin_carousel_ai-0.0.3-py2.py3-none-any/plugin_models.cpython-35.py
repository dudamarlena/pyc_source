# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/models/plugin_models.py
# Compiled at: 2017-08-31 05:41:42
# Size of source mod 2**32: 2336 bytes
from cms.models import CMSPlugin
from django.db import models
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum, EnumIntegerField
from softchoice.fields.language import LanguageField
from .categories import Category
from .tags import Tag
__all__ = ('ArticleListPlugin', 'TagFilterMode')

class TagFilterMode(Enum):
    ANY = 1
    ALL = 2
    EXACT = 3

    class Labels:
        ANY = _('Match articles with any of given tags')
        ALL = _('Match articles with all given tags')
        EXACT = _('Match articles with exact given tags')

    @property
    def as_url_encoded(self):
        """Returns an URL encoded value ready to be used as GET parameter"""
        return urlencode({'filter_mode': self.value})


class ArticleListPlugin(CMSPlugin):
    """ArticleListPlugin"""
    filter_mode = EnumIntegerField(TagFilterMode, verbose_name=_('filter'), default=TagFilterMode.ANY)
    category = models.ForeignKey(Category, verbose_name=_('category'), blank=True, null=True, related_name='+')
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), related_name='article_list_plugins')
    article_amount = models.PositiveSmallIntegerField(default=5, verbose_name=_('amount of articles'))
    language_filter = LanguageField(verbose_name=_('language filter'), default='', blank=True, help_text=_("Select a language if you want to list only articles written in specificlanguage. If you don't select a language, the listing includes all languages."))

    def __str__(self):
        return 'Article list (amount: %s)' % self.article_amount

    def copy_relations(self, oldinstance):
        self.tags = oldinstance.tags.all()