# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geobaldi/src/ripiu/public/github/djangocms_aoxomoxoa/ripiu/djangocms_aoxomoxoa/models/options/lightbox.py
# Compiled at: 2018-04-03 09:24:46
# Size of source mod 2**32: 5194 bytes
from colorfield.fields import ColorField
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _

class LightboxOptions(models.Model):
    __doc__ = '\n    Lightbox options\n    Valid for:\n      * Carousel\n      * Tiles - Columns\n      * Tiles - Grid\n      * Tiles - Justified\n      * Tiles - Nested\n    '
    TYPE_COMPACT = 'compact'
    TYPE_WIDE = 'wide'
    TYPE_CHOICES = (
     (
      TYPE_COMPACT, _('Compact')),
     (
      TYPE_WIDE, _('Wide')))
    ARROWS_POSITION_SIDES = 'sides'
    ARROWS_POSITION_INSIDE = 'inside'
    ARROWS_POSITION_CHOICES = (
     (
      ARROWS_POSITION_SIDES, _('Sides')),
     (
      ARROWS_POSITION_INSIDE, _('Inside')))
    lightbox_type = models.CharField((_('lightbox type')),
      max_length=7, default=TYPE_WIDE,
      blank=False,
      choices=TYPE_CHOICES)
    lightbox_hide_arrows_onvideoplay = models.BooleanField((_('hide arrows during video play')),
      default=True, help_text=(_('Hide the arrows when a video starts playing and show them when it stops.')))
    lightbox_arrows_position = models.CharField((_('lightbox type')),
      max_length=6, default=ARROWS_POSITION_SIDES,
      blank=False,
      choices=ARROWS_POSITION_CHOICES,
      help_text=(_('Position of the arrows, used on compact type.')))
    lightbox_arrows_offset = models.PositiveSmallIntegerField((_('arrows offset')),
      default=10,
      blank=False,
      help_text=(_('The horizontal offset of the arrows.')))
    lightbox_arrows_inside_offset = models.PositiveSmallIntegerField((_('arrows inside offset')),
      default=10,
      blank=False,
      help_text=(_('The offset from the image border if the arrows are placed inside.')))
    lightbox_arrows_inside_alwayson = models.BooleanField((_('arrows always on')),
      default=False, help_text=(_('Show the arrows on mouseover, or always on.')))
    lightbox_overlay_color = ColorField((_('overlay color')),
      blank=True,
      default='',
      help_text=(_('The color of the overlay. If null - will take from CSS.')))
    lightbox_overlay_opacity = models.PositiveSmallIntegerField((_('overlay opacity (%)')),
      blank=False,
      default=100,
      validators=[
     MaxValueValidator(100)],
      help_text=(_('The opacity of the overlay. for compact type 60%.')))
    lightbox_top_panel_opacity = models.PositiveSmallIntegerField((_('top panel opacity (%)')),
      blank=True,
      null=True,
      default=None,
      validators=[
     MaxValueValidator(100)],
      help_text=(_('The opacity of the top panel.')))
    lightbox_close_on_emptyspace = models.BooleanField((_('close on empty space')),
      default=False)
    lightbox_show_numbers = models.BooleanField((_('show numbers')),
      default=True, help_text=(_('Show numbers on the right side.')))
    lightbox_numbers_size = models.PositiveSmallIntegerField((_('numbers size')),
      default=None,
      blank=True,
      null=True,
      help_text=(_('The size of the numbers string.')))
    lightbox_numbers_color = ColorField((_('numbers color')),
      blank=True,
      default='')
    lightbox_numbers_padding_top = models.PositiveSmallIntegerField((_('numbers top padding')),
      default=None,
      blank=True,
      null=True,
      help_text=(_('The top padding of the numbers (used in compact mode).')))
    lightbox_numbers_padding_right = models.PositiveSmallIntegerField((_('numbers right padding')),
      default=None,
      blank=True,
      null=True,
      help_text=(_('The right padding of the numbers (used in compact mode).')))
    lightbox_slider_image_border = models.BooleanField((_('slider image border')),
      default=True, help_text=(_('Enable border around the image (for compact type only).')))
    lightbox_slider_image_border_width = models.PositiveSmallIntegerField((_('image border width')),
      default=10,
      blank=False,
      help_text=(_('Image border width.')))
    lightbox_slider_image_border_color = ColorField((_('image border color')),
      blank=False,
      default='#FFFFFF')
    lightbox_slider_image_border_radius = models.PositiveSmallIntegerField((_('image border radius')),
      default=0,
      blank=False)
    lightbox_slider_image_shadow = models.BooleanField((_('slider image shadow')),
      default=True)
    lightbox_slider_control_swipe = models.BooleanField((_('slider control swipe')),
      default=True, help_text=(_('Enable swiping control.')))
    lightbox_slider_control_zoom = models.BooleanField((_('slider control zoom')),
      default=True, help_text=(_('Enable zooming control.')))

    class Meta:
        abstract = True