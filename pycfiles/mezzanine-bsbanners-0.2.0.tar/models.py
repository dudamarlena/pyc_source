# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/alan/projects/mldemo-po/mezzanine_bsbanners/models.py
# Compiled at: 2018-11-16 08:16:10
"""
Mezzanine BS Banners
Making it easier to manage attention grabbing and compelling banners
"""
from __future__ import unicode_literals
from django.db import models
from django.db.models import Max
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.models import Slugged, RichText
from mezzanine_bsbanners import settings

@python_2_unicode_compatible
class Banners(Slugged):
    """
    Banners are the top of a page banner block and include scripts settings
    {% load ... staticfiles bsbanners_tags %}
    {% bsbanner "home" %}
    """
    BANNERTYPE_CAROUSEL = 1
    BANNERTYPE_JUMBOTRON = 2
    BANNERTYPE_IMAGE = 3
    BANNERTYPE_CHOICES = (
     (
      BANNERTYPE_CAROUSEL, _(b'Carousel')),
     (
      BANNERTYPE_JUMBOTRON, _(b'Jumbotron')),
     (
      BANNERTYPE_IMAGE, _(b'Image')))
    BUTTON_SIZE_LG = b'lg'
    BUTTON_SIZE_DEFAULT = b'default'
    BUTTON_SIZE_SM = b'sm'
    BUTTON_SIZE_XS = b'xs'
    BUTTON_SIZE_CHOICES = (
     (
      BUTTON_SIZE_LG, _(b'Large')),
     (
      BUTTON_SIZE_DEFAULT, _(b'Default')),
     (
      BUTTON_SIZE_SM, _(b'Small')),
     (
      BUTTON_SIZE_XS, _(b'Extra small')))
    CONTENT_STATUS_DRAFT = 1
    CONTENT_STATUS_PUBLISHED = 2
    CONTENT_STATUS_CHOICES = (
     (
      CONTENT_STATUS_DRAFT, _(b'Draft')),
     (
      CONTENT_STATUS_PUBLISHED, _(b'Published')))
    CTACHEVRON_NONE = b'none'
    CTACHEVRON_LEFT = b'left'
    CTACHEVRON_RIGHT = b'right'
    CTACHEVRON_CHOICES = (
     (
      CTACHEVRON_NONE, _(b'None')),
     (
      CTACHEVRON_LEFT, _(b'Left')),
     (
      CTACHEVRON_RIGHT, _(b'Right')))
    bannertype = models.SmallIntegerField(choices=BANNERTYPE_CHOICES, default=BANNERTYPE_CAROUSEL)
    ctachevron = models.CharField(_(b'Button chevrons'), choices=CTACHEVRON_CHOICES, default=CTACHEVRON_NONE, max_length=5, help_text=_(b'Add a chevron to call to action buttons'))
    buttonsize = models.CharField(_(b'Button size'), choices=BUTTON_SIZE_CHOICES, default=BUTTON_SIZE_DEFAULT, max_length=7, help_text=_(b'Size of call to action buttons'))
    interval = models.IntegerField(b'interval', help_text=_(b'The amount of time (in milliseconds) to delay between automatically cycling an item'), default=5000)
    wrap = models.BooleanField(b'wrap', help_text=_(b'Whether the carousel should cycle continuously or have hard stops'), default=True)
    pause = models.BooleanField(b'pause', help_text=_(b'Pauses the cycling of the carousel on mouseenter and resumes the cycling of the carousel on mouseleave'), default=True)
    showindicators = models.BooleanField(_(b'Show indicators'), default=True)
    animate = models.BooleanField(_(b'Animate transitions'), default=True)
    status = models.SmallIntegerField(_(b'Status'), choices=CONTENT_STATUS_CHOICES, default=CONTENT_STATUS_PUBLISHED, help_text=_(b'With Draft chosen, will only be shown for admin users on the site.'))

    def __str__(self):
        return self.title

    class Meta(object):
        """
        Meta class for Banners
        """
        verbose_name = _(b'Banner')
        verbose_name_plural = _(b'Banners')
        ordering = [b'title']


@python_2_unicode_compatible
class Slides(RichText):
    """
    Slides to render in a Banner block
    """
    BUTTON_TYPE_DEFAULT = b'default'
    BUTTON_TYPE_PRIMARY = b'primary'
    BUTTON_TYPE_SUCCESS = b'success'
    BUTTON_TYPE_INFO = b'info'
    BUTTON_TYPE_WARNING = b'warning'
    BUTTON_TYPE_DANGER = b'danger'
    BUTTON_TYPE_CHOICES = (
     (
      BUTTON_TYPE_DEFAULT, _(b'default')),
     (
      BUTTON_TYPE_PRIMARY, _(b'primary')),
     (
      BUTTON_TYPE_SUCCESS, _(b'success')),
     (
      BUTTON_TYPE_INFO, _(b'info')),
     (
      BUTTON_TYPE_WARNING, _(b'warning')),
     (
      BUTTON_TYPE_DANGER, _(b'danger')))
    CONTENT_STATUS_DRAFT = 1
    CONTENT_STATUS_PUBLISHED = 2
    CONTENT_STATUS_CHOICES = (
     (
      CONTENT_STATUS_DRAFT, _(b'Draft')),
     (
      CONTENT_STATUS_PUBLISHED, _(b'Published')))
    title = models.CharField(_(b'Title'), max_length=200, help_text=_(b'Slide/Jumbotron title'))
    show_title = models.BooleanField(_(b'Show title'), help_text=_(b'If checked, show slide/jumbotron title.'), default=True)
    cta = models.CharField(_(b'Call to action'), max_length=200, help_text=_(b'Text used for the call to action button'), blank=True, null=True)
    link_url = models.CharField(_(b'Link'), max_length=200, help_text=_(b'Link for the image and call to action button'), blank=True, null=True)
    buttontype = models.CharField(_(b'Button type'), choices=BUTTON_TYPE_CHOICES, default=BUTTON_TYPE_DEFAULT, max_length=7, help_text=_(b'Call to action button type (colour)'))
    banner = models.ForeignKey(Banners, on_delete=models.CASCADE)
    image = models.FileField(_(b'Image'), upload_to=settings.MEDIA, max_length=255, null=True, blank=True)
    status = models.SmallIntegerField(_(b'Status'), choices=CONTENT_STATUS_CHOICES, default=CONTENT_STATUS_PUBLISHED, help_text=_(b'With Draft chosen, will only be shown for admin users on the site.'))
    sort_order = models.SmallIntegerField(editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Set the initial ordering value.
        """
        if self.sort_order is None:
            aggregate = Slides.objects.filter(banner_id=self.banner_id).aggregate(Max(b'sort_order'))
            if aggregate[b'sort_order__max']:
                self.sort_order = aggregate[b'sort_order__max'] + 1
            else:
                self.sort_order = 1
        super(Slides, self).save(*args, **kwargs)
        return

    def delete(self, *args, **kwargs):
        """
        Deletes associated media
        """
        self.image.delete()
        super(Slides, self).delete(*args, **kwargs)

    class Meta(object):
        """
        Meta class for Slide
        """
        verbose_name = _(b'Slide')
        verbose_name_plural = _(b'Slides')
        ordering = [b'sort_order']