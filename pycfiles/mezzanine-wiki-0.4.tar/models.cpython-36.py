# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\landon\dropbox\documents\pycharmprojects\mezzanine-wiki\mezzanine_wiki\models.py
# Compiled at: 2018-01-31 10:14:18
# Size of source mod 2**32: 4112 bytes
from builtins import object
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Ownable, RichText, Slugged, TimeStamped
from mezzanine.generic.fields import CommentsField, RatingField
from mezzanine_wiki.fields import WikiTextField
from mezzanine_wiki import defaults as wiki_settings
from django.utils.timezone import now
from mezzanine_wiki.managers import DisplayableManager
WIKIPAGE_PERMISSIONS = (('view_wikipage', 'Can view wikipage'), ('change_wikipage_privacy', 'Can change wikipage privacy'))
WIKIPAGE_REVISION_PERMISSIONS = (('view_wikipage_revision', 'Can view wikipage revision'), )

class WikiPage(Displayable, Ownable):
    __doc__ = '\n    A wiki page.\n    '
    content = WikiTextField(_('Content'))
    categories = models.ManyToManyField('WikiCategory', verbose_name=(_('Categories')),
      blank=True,
      related_name='wikipages')
    allow_comments = models.BooleanField(verbose_name=(_('Allow comments')), default=True)
    comments = CommentsField(verbose_name=(_('Comments')))
    rating = RatingField(verbose_name=(_('Rating')))
    featured_image = FileField(verbose_name=(_('Featured Image')), null=True, upload_to='wiki',
      max_length=255,
      blank=True)
    search_fields = ('content', )
    objects = DisplayableManager()

    class Meta(object):
        verbose_name = _('Wiki page')
        verbose_name_plural = _('Wiki pages')
        ordering = ('title', )
        permissions = WIKIPAGE_PERMISSIONS

    def can_view_wikipage(self, user):
        return True

    def can_edit_wikipage(self, user):
        if settings.WIKI_PRIVACY == wiki_settings.WIKI_PRIVACY_OPENED:
            return True
        else:
            if settings.WIKI_PRIVACY == wiki_settings.WIKI_PRIVACY_REGISTERED:
                if user.is_authenticated():
                    return True
            else:
                if settings.WIKI_PRIVACY == wiki_settings.WIKI_PRIVACY_MODERATED:
                    if user.has_perm('mezzanine_wiki.change_wikipage'):
                        return True
                if self.user == user:
                    return True
            return False

    def get_absolute_url(self):
        return reverse('wiki_page_detail', kwargs={'slug': self.slug})


class WikiPageRevision(Ownable, TimeStamped):
    __doc__ = '\n    A wiki page revision.\n    '
    page = models.ForeignKey('WikiPage', verbose_name=(_('Wiki page')))
    content = WikiTextField(_('Content'))
    description = models.CharField((_('Description')), max_length=400,
      blank=True)

    class Meta(object):
        verbose_name = _('Wiki page revision')
        verbose_name_plural = _('Wiki page revisions')
        ordering = ('-created', )
        permissions = WIKIPAGE_REVISION_PERMISSIONS

    def __unicode__(self):
        return '%s' % self.created

    def get_absolute_url(self):
        return reverse('wiki_page_revision', kwargs={'slug':self.page.slug,  'rev_id':self.id})


class WikiCategory(Slugged):
    __doc__ = '\n    A category for grouping wiki pages.\n    '

    class Meta(object):
        verbose_name = _('Wiki Category')
        verbose_name_plural = _('Wiki Categories')

    def get_absolute_url(self):
        return reverse('wiki_page_list_category', kwargs={'slug': self.slug})