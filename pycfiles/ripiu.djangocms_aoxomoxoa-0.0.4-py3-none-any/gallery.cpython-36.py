# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geobaldi/src/ripiu/public/github/djangocms_aoxomoxoa/ripiu/djangocms_aoxomoxoa/models/options/gallery.py
# Compiled at: 2018-04-03 09:24:46
# Size of source mod 2**32: 4454 bytes
from colorfield.fields import ColorField
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class GalleryOptions(models.Model):
    __doc__ = '\n    Gallery options.\n    Valid for:\n      * Carousel\n      * Compact theme\n      * Default theme\n      * Grid theme\n      * Slider\n      * Tiles - Columns\n      * Tiles - Grid\n      * Tiles - Justified\n      * Tiles - Nested\n    '
    gallery_background_color = ColorField((_('background color')),
      blank=True,
      default='',
      help_text=(_('set custom background color. If not set it will be taken from css.')))
    gallery_min_width = models.PositiveSmallIntegerField((_('minimum width')),
      blank=False,
      help_text=(_('Gallery minimum width when resizing.')))

    class Meta:
        abstract = True


class TilesCarouselGalleryOptions(GalleryOptions):
    __doc__ = '\n    Gallery options.\n    Valid for:\n      * Carousel\n      * Tiles - Columns\n      * Tiles - Justified\n      * Tiles - Nested\n    '
    gallery_width = models.CharField((_('width')),
      max_length=8, default='100%',
      blank=False,
      help_text=(_('Gallery width.')))

    class Meta:
        abstract = True


TilesCarouselGalleryOptions._meta.get_field('gallery_min_width').default = 150

class SliderGalleryOptions(GalleryOptions):
    __doc__ = '\n    Gallery options.\n    Valid for:\n      * Compact theme\n      * Default theme\n      * Grid theme\n      * Slider\n    '
    PRELOAD_ALL = 'all'
    PRELOAD_MINIMAL = 'minimal'
    PRELOAD_VISIBLE = 'visible'
    PRELOAD_CHOICES = (
     (
      PRELOAD_ALL, _('load all the images first time')),
     (
      PRELOAD_MINIMAL, _('only image nabours will be loaded each time')),
     (
      PRELOAD_VISIBLE, _('visible thumbs images will be loaded each time')))
    gallery_skin = models.CharField((_('gallery skin')),
      max_length=255, blank=False,
      choices=(settings.RIPIU_AOXOMOXOA_UNITE_SKINS))
    gallery_width = models.PositiveSmallIntegerField((_('width')),
      default=900,
      blank=False,
      help_text=(_('Gallery width.')))
    gallery_autoplay = models.BooleanField((_('gallery autoplay')),
      default=False, help_text=(_('Begin slideshow autoplay on start.')))
    gallery_carousel = models.BooleanField((_('carousel')),
      default=True, help_text=(_('Next button on last image goes to first image.')))
    gallery_control_keyboard = models.BooleanField((_('keyboard')),
      default=True, help_text=(_('Enable / disable keyboard controls.')))
    gallery_control_thumbs_mousewheel = models.BooleanField((_('mousewheel')),
      default=False, help_text=(_('Enable / disable the mousewheel.')))
    gallery_debug_errors = models.BooleanField((_('debug errors')),
      default=True, help_text=(_('show error message when there is some error on the gallery area.')))
    gallery_height = models.PositiveSmallIntegerField((_('height')),
      default=500,
      blank=False,
      help_text=(_('Gallery height.')))
    gallery_images_preload_type = models.CharField((_('preload type')),
      max_length=8, default=PRELOAD_MINIMAL,
      blank=False,
      choices=PRELOAD_CHOICES,
      help_text=(_('Preload type of the images.')))
    gallery_min_height = models.PositiveSmallIntegerField((_('minimum height')),
      default=300,
      blank=False,
      help_text=(_('Gallery minimal height when resizing.')))
    gallery_pause_on_mouseover = models.BooleanField((_('pause on mouseover')),
      default=False, help_text=(_('Pause on mouseover when playing slideshow.')))
    gallery_play_interval = models.PositiveSmallIntegerField((_('play interval')),
      default=3000,
      blank=False,
      help_text=(_('Play interval of the slideshow.')))
    gallery_preserve_ratio = models.BooleanField((_('carousel')),
      default=True, help_text=(_('Preserve aspect ratio on window resize.')))

    class Meta:
        abstract = True


SliderGalleryOptions._meta.get_field('gallery_min_width').default = 400