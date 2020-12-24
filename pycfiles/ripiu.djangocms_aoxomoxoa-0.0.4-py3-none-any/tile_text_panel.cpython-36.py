# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geobaldi/src/ripiu/public/github/djangocms_aoxomoxoa/ripiu/djangocms_aoxomoxoa/models/options/tile_text_panel.py
# Compiled at: 2018-04-03 09:24:46
# Size of source mod 2**32: 6452 bytes
from colorfield.fields import ColorField
from djangocms_attributes_field.fields import AttributesField
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from .constants import APPEAR_SLIDE, ALIGN_CHOICES, APPEAR_CHOICES

class TileTextPanelOptions(models.Model):
    __doc__ = '\n    Tile text panel options.\n    Valid for:\n      * Carousel\n      * Tiles - Columns\n      * Tiles - Grid\n      * Tiles - Justified\n      * Tiles - Nested\n    '
    TEXTPANEL_POSITION_INSIDE_BOTTOM = 'inside_bottom'
    TEXTPANEL_POSITION_INSIDE_TOP = 'inside_top'
    TEXTPANEL_POSITION_INSIDE_CENTER = 'inside_center'
    TEXTPANEL_POSITION_TOP = 'top'
    TEXTPANEL_POSITION_BOTTOM = 'bottom'
    TEXTPANEL_POSITION_CHOICES = (
     (
      TEXTPANEL_POSITION_INSIDE_BOTTOM, _('Inside bottom')),
     (
      TEXTPANEL_POSITION_INSIDE_TOP, _('Inside top')),
     (
      TEXTPANEL_POSITION_INSIDE_CENTER, _('Inside center')),
     (
      TEXTPANEL_POSITION_TOP, _('Top')),
     (
      TEXTPANEL_POSITION_BOTTOM, _('Bottom')))
    SOURCE_TITLE = 'title'
    SOURCE_DESC = 'desc'
    SOURCE_DESC_TITLE = 'desc_title'
    SOURCE_CHOICES = (
     (
      SOURCE_TITLE, _('Title')),
     (
      SOURCE_DESC, _('Description')),
     (
      SOURCE_DESC_TITLE, _('Description or title')))
    tile_enable_textpanel = models.BooleanField((_('enable')),
      default=False)
    tile_textpanel_always_on = models.BooleanField((_('always on')),
      default=False)
    tile_textpanel_appear_type = models.CharField((_('appear type')),
      max_length=5, default=APPEAR_SLIDE,
      blank=False,
      choices=APPEAR_CHOICES,
      help_text=(_('Appear type of the textpanel on mouseover.')))
    tile_textpanel_bg_color = ColorField((_('background color')),
      blank=False,
      default='#000000')
    tile_textpanel_bg_css = AttributesField(verbose_name=(_('background CSS')),
      blank=True,
      default={},
      help_text=(_('Textpanel background CSS.')))
    tile_textpanel_bg_opacity = models.PositiveSmallIntegerField((_('background opacity (%)')),
      blank=False,
      default=40,
      validators=[
     MaxValueValidator(100)])
    tile_textpanel_css_description = AttributesField(verbose_name=(_('description CSS')),
      blank=True,
      default={},
      help_text=(_('Description additional CSS.')))
    tile_textpanel_css_title = AttributesField(verbose_name=(_('description CSS')),
      blank=True,
      default={},
      help_text=(_('Title additional CSS.')))
    tile_textpanel_desc_bold = models.NullBooleanField((_('Bold description')),
      default=None)
    tile_textpanel_desc_color = ColorField((_('description color')),
      blank=True,
      default='',
      help_text=(_('Textpanel description text color. If blank take from css.')))
    tile_textpanel_desc_font_family = models.CharField((_('description font family')),
      max_length=255, default='',
      blank=True,
      help_text=(_('A CSS font family for the description.')))
    tile_textpanel_desc_font_size = models.PositiveSmallIntegerField((_('description font size (px)')),
      default=None,
      blank=True,
      null=True,
      help_text=(_('Textpanel description font size. If blank take from css.')))
    tile_textpanel_desc_text_align = models.CharField((_('description text alignment')),
      max_length=6, default='',
      blank=True,
      choices=ALIGN_CHOICES,
      help_text=(_('Textpanel description text alignment. If blank take from CSS.')))
    tile_textpanel_offset = models.PositiveSmallIntegerField((_('vertical offset')),
      default=0,
      blank=False)
    tile_textpanel_padding_bottom = models.PositiveSmallIntegerField((_('bottom padding')),
      default=8,
      blank=False)
    tile_textpanel_padding_left = models.PositiveSmallIntegerField((_('left padding')),
      default=11,
      blank=False,
      help_text=(_('Cut some space for text from left.')))
    tile_textpanel_padding_right = models.PositiveSmallIntegerField((_('right padding')),
      default=11,
      blank=False,
      help_text=(_('Cut some space for text from right.')))
    tile_textpanel_padding_top = models.PositiveSmallIntegerField((_('top padding')),
      default=8,
      blank=False)
    tile_textpanel_position = models.CharField((_('text panel position')),
      max_length=13, default=TEXTPANEL_POSITION_BOTTOM,
      blank=False,
      choices=TEXTPANEL_POSITION_CHOICES,
      help_text=(_('The position of the textpanel.')))
    tile_textpanel_source = models.CharField((_('text panel source')),
      max_length=10, default=SOURCE_TITLE,
      blank=False,
      choices=SOURCE_CHOICES,
      help_text=(_('Source of the textpanel.')))
    tile_textpanel_title_bold = models.NullBooleanField((_('bold title')),
      default=None)
    tile_textpanel_title_color = ColorField((_('title color')),
      blank=True,
      default='',
      help_text=(_('Textpanel title color. If blank take from CSS.')))
    tile_textpanel_title_font_family = models.CharField((_('title font family')),
      max_length=255, default='',
      blank=True,
      help_text=(_('A CSS font family for the title.')))
    tile_textpanel_title_font_size = models.PositiveSmallIntegerField((_('title font size (px)')),
      default=None,
      blank=True,
      null=True,
      help_text=(_('Textpanel title font size. If blank take from CSS.')))
    tile_textpanel_title_text_align = models.CharField((_('title text alignment')),
      max_length=6, default='',
      blank=True,
      choices=ALIGN_CHOICES,
      help_text=(_('Textpanel title text alignment. If blank take from CSS.')))

    class Meta:
        abstract = True