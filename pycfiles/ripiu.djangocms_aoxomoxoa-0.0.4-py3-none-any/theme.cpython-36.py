# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geobaldi/src/ripiu/public/github/djangocms_aoxomoxoa/ripiu/djangocms_aoxomoxoa/models/options/theme.py
# Compiled at: 2018-04-03 09:24:46
# Size of source mod 2**32: 6530 bytes
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .constants import ALIGN_LEFT, ALIGN_CENTER, ALIGN_CHOICES, POSITION_RIGHT, POSITION_BOTTOM, POSITION_CHOICES

class CompactGridDefaultThemeOptions(models.Model):
    __doc__ = '\n    Theme options.\n    Valid for:\n      * Default template\n      * Grid Theme\n      * Compact Theme\n    '
    theme_hide_panel_under_width = models.PositiveSmallIntegerField((_('hide panel under width')),
      default=480,
      blank=True,
      null=True,
      help_text=(_("Hide panel under certain browser width, if null, don't hide.")))

    class Meta:
        abstract = True


class CompactGridThemeOptions(CompactGridDefaultThemeOptions):
    __doc__ = '\n    Theme options.\n    Valid for:\n      * Grid Theme\n      * Compact Theme\n    '
    PANEL_POSITION_CHOICES = POSITION_CHOICES
    theme_panel_position = models.CharField((_('panel position')),
      max_length=6, blank=False,
      choices=PANEL_POSITION_CHOICES,
      help_text=(_('Thumbs panel position.')))

    class Meta:
        abstract = True


class TilesCarouselThemeOptions(models.Model):
    __doc__ = '\n    Theme options.\n    Valid for:\n      * Carousel\n      * Tiles - Columns\n      * Tiles - Grid\n      * Tiles - Justified\n      * Tiles - Nested\n    '
    theme_gallery_padding = models.PositiveSmallIntegerField((_('gallery padding')),
      default=0,
      blank=False,
      help_text=(_('The horizontal padding of the gallery from the sides.')))

    class Meta:
        abstract = True


class TilesGridThemeOptions(TilesCarouselThemeOptions):
    __doc__ = '\n    Theme options.\n    Valid for:\n      * Tiles - Columns\n      * Tiles - Grid\n      * Tiles - Justified\n      * Tiles - Nested\n    '
    theme_auto_open = models.PositiveSmallIntegerField((_('auto open')),
      default=None,
      blank=True,
      null=True,
      help_text=(_('Auto open lightbox at start. If some number gived, like 0.')))

    class Meta:
        abstract = True


class TilesThemeOptions(TilesGridThemeOptions):
    __doc__ = '\n    Theme options.\n    Valid for:\n      * Tiles - Justified\n      * Tiles - Nested\n      * Tiles - Columns\n    '
    theme_enable_preloader = models.BooleanField((_('enable preloader')),
      default=True, help_text=(_('Enable preloader circle.')))
    theme_preloading_height = models.PositiveSmallIntegerField((_('preloading height')),
      default=200,
      blank=False,
      help_text=(_('The height of the preloading div, it is shown before the gallery.')))
    theme_preloader_vertpos = models.PositiveSmallIntegerField((_('preloader vertical position')),
      default=100,
      blank=False,
      help_text=(_('The vertical position of the preloader.')))

    class Meta:
        abstract = True


class TilesColumnsThemeOptions(TilesThemeOptions):
    __doc__ = '\n    Theme options for Tiles - Columns\n    '
    ORDER_NORMAL = 'normal'
    ORDER_SHUFFLE = 'shuffle'
    ORDER_KEEP = 'keep'
    ORDER_CHOICES = (
     (
      ORDER_NORMAL, _('Normal')),
     (
      ORDER_SHUFFLE, _('Shuffle')),
     (
      ORDER_KEEP, _('Keep order')))
    theme_appearance_order = models.CharField((_('appearance order')),
      max_length=8, default=ORDER_NORMAL,
      blank=False,
      choices=ORDER_CHOICES,
      help_text=(_('The appearance order of the tiles.')))

    class Meta:
        abstract = True


class CarouselThemeOptions(TilesCarouselThemeOptions):
    __doc__ = '\n    Theme options for Carousel\n    '
    theme_carousel_align = models.CharField((_('align')),
      max_length=6, default=ALIGN_CENTER,
      blank=False,
      choices=ALIGN_CHOICES,
      help_text=(_('The align of the carousel.')))
    theme_carousel_offset = models.PositiveSmallIntegerField((_('offset')),
      default=0,
      blank=False,
      help_text=(_('The offset of the carousel from the align sides.')))

    class Meta:
        abstract = True


class CompactThemeOptions(CompactGridThemeOptions):
    __doc__ = '\n    Theme options for Compact Theme\n    '

    class Meta:
        abstract = True


CompactThemeOptions._meta.get_field('theme_panel_position').default = POSITION_BOTTOM

class GridThemeOptions(CompactGridThemeOptions):
    __doc__ = '\n    Theme options for Grid Theme\n    '

    class Meta:
        abstract = True


GridThemeOptions._meta.get_field('theme_panel_position').default = POSITION_RIGHT

class DefaultThemeOptions(CompactGridDefaultThemeOptions):
    __doc__ = '\n    Theme options for Default Theme\n    '
    TEXT_TYPE_TITLE = 'title'
    TEXT_TYPE_DESCRIPTION = 'description'
    TEXT_TYPE_CHOICES = (
     (
      TEXT_TYPE_TITLE, _('Title')),
     (
      TEXT_TYPE_DESCRIPTION, _('Description')))
    theme_enable_fullscreen_button = models.BooleanField((_('enable fullscreen button')),
      default=True, help_text=(_('Show, hide the theme fullscreen button. The position in the theme is constant.')))
    theme_enable_hidepanel_button = models.BooleanField((_('enable hidepanel button')),
      default=True, help_text=(_('Show, hide the hidepanel button.')))
    theme_enable_play_button = models.BooleanField((_('enable play button')),
      default=True, help_text=(_('Show, hide the theme play button. The position in the theme is constant.')))
    theme_enable_text_panel = models.BooleanField((_('enable text panel')),
      default=True, help_text=(_('Enable the panel text panel.')))
    theme_text_align = models.CharField((_('text align')),
      max_length=6, default=ALIGN_LEFT,
      blank=False,
      choices=ALIGN_CHOICES,
      help_text=(_('The align of the text in the textpanel.')))
    theme_text_padding_left = models.PositiveSmallIntegerField((_('text padding left')),
      default=20,
      blank=False,
      help_text=(_('Left padding of the text in the textpanel.')))
    theme_text_padding_right = models.PositiveSmallIntegerField((_('text padding right')),
      default=5,
      blank=False,
      help_text=(_('Right padding of the text in the textpanel.')))
    theme_text_type = models.CharField((_('text align')),
      max_length=6, default=TEXT_TYPE_TITLE,
      blank=False,
      choices=TEXT_TYPE_CHOICES,
      help_text=(_('text that will be shown on the text panel, title or description.')))

    class Meta:
        abstract = True