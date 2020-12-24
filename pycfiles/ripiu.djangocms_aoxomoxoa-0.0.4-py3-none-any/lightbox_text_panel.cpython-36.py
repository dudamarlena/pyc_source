# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geobaldi/src/ripiu/public/github/djangocms_aoxomoxoa/ripiu/djangocms_aoxomoxoa/models/options/lightbox_text_panel.py
# Compiled at: 2018-04-03 09:24:46
# Size of source mod 2**32: 4596 bytes
from colorfield.fields import ColorField
from djangocms_attributes_field.fields import AttributesField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .constants import ALIGN_CHOICES

class LightboxTextPanelOptions(models.Model):
    __doc__ = '\n    Lightbox text panel options\n    Valid for:\n      * Carousel\n      * Tiles - Columns\n      * Tiles - Grid\n      * Tiles - Justified\n      * Tiles - Nested\n    '
    lightbox_show_textpanel = models.BooleanField((_('show text panel')),
      default=True, help_text=(_('Show the text panel.')))
    lightbox_textpanel_css_description = AttributesField(verbose_name=(_('description CSS')),
      blank=True,
      default={},
      help_text=(_('Textpanel additional CSS of the description.')))
    lightbox_textpanel_css_title = AttributesField(verbose_name=(_('title CSS')),
      blank=True,
      default={},
      help_text=(_('Textpanel additional CSS of the title.')))
    lightbox_textpanel_desc_bold = models.NullBooleanField((_('Bold description')),
      default=None)
    lightbox_textpanel_desc_color = ColorField((_('description color')),
      blank=True,
      default='',
      help_text=(_('Textpanel description text color. If blank take from CSS.')))
    lightbox_textpanel_desc_font_family = models.CharField((_('description font family')),
      max_length=255, default='',
      blank=True,
      help_text=(_('A CSS font family for the description.')))
    lightbox_textpanel_desc_font_size = models.PositiveSmallIntegerField((_('description font size (px)')),
      default=None,
      blank=True,
      null=True,
      help_text=(_('Textpanel description font size. If blank take from css.')))
    lightbox_textpanel_desc_text_align = models.CharField((_('description text alignment')),
      max_length=6, default='',
      blank=True,
      choices=ALIGN_CHOICES,
      help_text=(_('Textpanel description text alignment. If blank take from CSS.')))
    lightbox_textpanel_enable_description = models.BooleanField((_('enable description')),
      default=False, help_text=(_('Enable the description text.')))
    lightbox_textpanel_enable_title = models.BooleanField((_('enable title')),
      default=True, help_text=(_('Enable the title text.')))
    lightbox_textpanel_padding_bottom = models.PositiveSmallIntegerField((_('bottom padding')),
      default=5,
      blank=False,
      help_text=(_('Textpanel bottom padding.')))
    lightbox_textpanel_padding_left = models.PositiveSmallIntegerField((_('left padding')),
      default=11,
      blank=False,
      help_text=(_('Cut some space for text from left.')))
    lightbox_textpanel_padding_right = models.PositiveSmallIntegerField((_('right padding')),
      default=11,
      blank=False,
      help_text=(_('Cut some space for text from right.')))
    lightbox_textpanel_padding_top = models.PositiveSmallIntegerField((_('top padding')),
      default=5,
      blank=False,
      help_text=(_('Textpanel top padding.')))
    lightbox_textpanel_title_bold = models.NullBooleanField((_('Bold description')),
      default=None)
    lightbox_textpanel_title_color = ColorField((_('title color')),
      blank=True,
      default='',
      help_text=(_('Textpanel title color. If blank take from CSS.')))
    lightbox_textpanel_title_font_family = models.CharField((_('description font family')),
      max_length=255, default='',
      blank=True,
      help_text=(_('A CSS font family for the title.')))
    lightbox_textpanel_title_font_size = models.PositiveSmallIntegerField((_('description font size (px)')),
      default=None,
      blank=True,
      null=True,
      help_text=(_('Textpanel title font size. If blank take from css.')))
    lightbox_textpanel_title_text_align = models.CharField((_('description text alignment')),
      max_length=6, default='',
      blank=True,
      choices=ALIGN_CHOICES,
      help_text=(_('Textpanel title text alignment. If blank take from CSS.')))
    lightbox_textpanel_width = models.PositiveSmallIntegerField((_('width')),
      default=550,
      blank=False,
      help_text=(_('the width of the text panel. wide type only.')))

    class Meta:
        abstract = True