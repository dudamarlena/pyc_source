# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/home/alan/projects/mldemo-po/mezzanine_bsbanners/models.py
# Compiled at: 2019-02-28 07:55:06
# Size of source mod 2**32: 7469 bytes
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
    __doc__ = '\n    Banners are the top of a page banner block and include scripts settings\n    {% load ... staticfiles bsbanners_tags %}\n    {% bsbanner "home" %}\n    '
    BANNERTYPE_CAROUSEL = 1
    BANNERTYPE_JUMBOTRON = 2
    BANNERTYPE_IMAGE = 3
    BANNERTYPE_CHOICES = (
     (
      BANNERTYPE_CAROUSEL, _('Carousel')),
     (
      BANNERTYPE_JUMBOTRON, _('Jumbotron')),
     (
      BANNERTYPE_IMAGE, _('Image')))
    BUTTON_SIZE_LG = 'lg'
    BUTTON_SIZE_DEFAULT = 'default'
    BUTTON_SIZE_SM = 'sm'
    BUTTON_SIZE_XS = 'xs'
    BUTTON_SIZE_CHOICES = (
     (
      BUTTON_SIZE_LG, _('Large')),
     (
      BUTTON_SIZE_DEFAULT, _('Default')),
     (
      BUTTON_SIZE_SM, _('Small')),
     (
      BUTTON_SIZE_XS, _('Extra small')))
    CONTENT_STATUS_DRAFT = 1
    CONTENT_STATUS_PUBLISHED = 2
    CONTENT_STATUS_CHOICES = (
     (
      CONTENT_STATUS_DRAFT, _('Draft')),
     (
      CONTENT_STATUS_PUBLISHED, _('Published')))
    CTACHEVRON_NONE = 'none'
    CTACHEVRON_LEFT = 'left'
    CTACHEVRON_RIGHT = 'right'
    CTACHEVRON_CHOICES = (
     (
      CTACHEVRON_NONE, _('None')),
     (
      CTACHEVRON_LEFT, _('Left')),
     (
      CTACHEVRON_RIGHT, _('Right')))
    CAROUSEL_TRANSITION_SLIDE = 'slide'
    CAROUSEL_TRANSITION_FADE = 'fade'
    CAROUSEL_TRANSITION_CHOICES = (
     (
      CAROUSEL_TRANSITION_SLIDE, _('Slide')),
     (
      CAROUSEL_TRANSITION_FADE, _('Fade')))
    bannertype = models.SmallIntegerField(choices=BANNERTYPE_CHOICES,
      default=BANNERTYPE_CAROUSEL)
    ctachevron = models.CharField((_('Button chevrons')),
      choices=CTACHEVRON_CHOICES,
      default=CTACHEVRON_NONE,
      max_length=5,
      help_text=(_('Add a chevron to call to action buttons')))
    buttonsize = models.CharField((_('Button size')),
      choices=BUTTON_SIZE_CHOICES,
      default=BUTTON_SIZE_DEFAULT,
      max_length=7,
      help_text=(_('Size of call to action buttons')))
    interval = models.IntegerField('interval',
      help_text=(_('The amount of time (in milliseconds) to delay between automatically cycling an item')),
      default=5000)
    wrap = models.BooleanField('wrap',
      help_text=(_('Whether the carousel should cycle continuously or have hard stops')),
      default=True)
    pause = models.BooleanField('pause',
      help_text=(_('Pauses the cycling of the carousel on mouseenter and resumes the cycling of the carousel on mouseleave')),
      default=True)
    showindicators = models.BooleanField((_('Show indicators')), default=True)
    animate = models.BooleanField((_('Animate transitions')), default=True)
    carouseltransition = models.CharField((_('Carousel transition')),
      choices=CAROUSEL_TRANSITION_CHOICES,
      default=CAROUSEL_TRANSITION_SLIDE,
      max_length=5,
      help_text=(_('Animate slides with a slide or fade transition.')))
    status = models.SmallIntegerField((_('Status')),
      choices=CONTENT_STATUS_CHOICES,
      default=CONTENT_STATUS_PUBLISHED,
      help_text=(_('With Draft chosen, will only be shown for admin users on the site.')))

    def __str__(self):
        return self.title

    class Meta(object):
        __doc__ = '\n        Meta class for Banners\n        '
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')
        ordering = ['title']


@python_2_unicode_compatible
class Slides(RichText):
    __doc__ = '\n    Slides to render in a Banner block\n    '
    BUTTON_TYPE_DEFAULT = 'default'
    BUTTON_TYPE_PRIMARY = 'primary'
    BUTTON_TYPE_SUCCESS = 'success'
    BUTTON_TYPE_INFO = 'info'
    BUTTON_TYPE_WARNING = 'warning'
    BUTTON_TYPE_DANGER = 'danger'
    BUTTON_TYPE_CHOICES = (
     (
      BUTTON_TYPE_DEFAULT, _('default')),
     (
      BUTTON_TYPE_PRIMARY, _('primary')),
     (
      BUTTON_TYPE_SUCCESS, _('success')),
     (
      BUTTON_TYPE_INFO, _('info')),
     (
      BUTTON_TYPE_WARNING, _('warning')),
     (
      BUTTON_TYPE_DANGER, _('danger')))
    CONTENT_STATUS_DRAFT = 1
    CONTENT_STATUS_PUBLISHED = 2
    CONTENT_STATUS_CHOICES = (
     (
      CONTENT_STATUS_DRAFT, _('Draft')),
     (
      CONTENT_STATUS_PUBLISHED, _('Published')))
    title = models.CharField((_('Title')),
      max_length=200,
      help_text=(_('Slide/Jumbotron title')))
    show_title = models.BooleanField((_('Show title')),
      help_text=(_('If checked, show slide/jumbotron title.')),
      default=True)
    cta = models.CharField((_('Call to action')),
      max_length=200,
      help_text=(_('Text used for the call to action button')),
      blank=True,
      null=True)
    link_url = models.CharField((_('Link')),
      max_length=200,
      help_text=(_('Link for the image and call to action button')),
      blank=True,
      null=True)
    buttontype = models.CharField((_('Button type')),
      choices=BUTTON_TYPE_CHOICES,
      default=BUTTON_TYPE_DEFAULT,
      max_length=7,
      help_text=(_('Call to action button type (colour)')))
    banner = models.ForeignKey(Banners, on_delete=(models.CASCADE))
    image = models.FileField((_('Image')),
      upload_to=(settings.MEDIA),
      max_length=255,
      null=True,
      blank=True)
    status = models.SmallIntegerField((_('Status')),
      choices=CONTENT_STATUS_CHOICES,
      default=CONTENT_STATUS_PUBLISHED,
      help_text=(_('With Draft chosen, will only be shown for admin users on the site.')))
    sort_order = models.SmallIntegerField(editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.sort_order is None:
            aggregate = Slides.objects.filter(banner_id=(self.banner_id)).aggregate(Max('sort_order'))
            if aggregate['sort_order__max']:
                self.sort_order = aggregate['sort_order__max'] + 1
            else:
                self.sort_order = 1
        (super(Slides, self).save)(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        (super(Slides, self).delete)(*args, **kwargs)

    class Meta(object):
        __doc__ = '\n        Meta class for Slide\n        '
        verbose_name = _('Slide')
        verbose_name_plural = _('Slides')
        ordering = ['sort_order']