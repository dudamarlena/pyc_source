# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geobaldi/src/ripiu/public/github/djangocms_aoxomoxoa/ripiu/djangocms_aoxomoxoa/models/options/carousel.py
# Compiled at: 2018-04-03 09:24:46
# Size of source mod 2**32: 2195 bytes
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .constants import EASE_OUT_CUBIC, EASING_CHOICES

class CarouselOptions(models.Model):
    __doc__ = '\n    Carousel options for Carousel\n    '
    DIRECTION_LEFT = 'left'
    DIRECTION_RIGHT = 'right'
    DIRECTION_CHOICES = (
     (
      DIRECTION_LEFT, _('Left')),
     (
      DIRECTION_RIGHT, _('Right')))
    carousel_autoplay = models.BooleanField((_('carousel autoplay')),
      default=True, help_text=(_('Autoplay of the carousel on start.')))
    carousel_autoplay_direction = models.CharField((_('scroll easing')),
      max_length=6, default=DIRECTION_RIGHT,
      blank=False,
      choices=DIRECTION_CHOICES,
      help_text=(_('Autoplay direction.')))
    carousel_autoplay_pause_onhover = models.BooleanField((_('pause on hover')),
      default=True, help_text=(_('Pause the autoplay on mouse over.')))
    carousel_autoplay_timeout = models.PositiveSmallIntegerField((_('autoplay timeout')),
      default=3000,
      blank=False)
    carousel_navigation_numtiles = models.PositiveSmallIntegerField((_('navigation numtiles')),
      default=3,
      blank=False,
      help_text=(_('Number of tiles to scroll when user clicks on next/prev button.')))
    carousel_padding = models.PositiveSmallIntegerField((_('padding')),
      default=8,
      blank=False,
      help_text=(_('Padding at the sides of the carousel.')))
    carousel_scroll_duration = models.PositiveSmallIntegerField((_('scroll duration')),
      default=500,
      blank=False,
      help_text=(_('Duration of scrolling to tile.')))
    carousel_scroll_easing = models.CharField((_('scroll easing')),
      max_length=17, default=EASE_OUT_CUBIC,
      blank=False,
      choices=EASING_CHOICES,
      help_text=(_('Easing of scrolling to tile animation.')))
    carousel_space_between_tiles = models.PositiveSmallIntegerField((_('space between tiles')),
      default=20,
      blank=False)

    class Meta:
        abstract = True