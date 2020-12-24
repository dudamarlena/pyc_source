# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geobaldi/src/ripiu/public/github/djangocms_aoxomoxoa/ripiu/djangocms_aoxomoxoa/models/options/slider.py
# Compiled at: 2018-04-03 09:24:46
# Size of source mod 2**32: 23743 bytes
from colorfield.fields import ColorField
from djangocms_attributes_field.fields import AttributesField
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from .constants import ALIGN_LEFT, VALIGN_TOP, ALIGN_RIGHT, ALIGN_CENTER, APPEAR_SLIDE, ALIGN_CHOICES, VALIGN_BOTTOM, VALIGN_MIDDLE, APPEAR_CHOICES, EASING_CHOICES, VALIGN_CHOICES, EASE_INOUT_QUAD

class SliderOptions(models.Model):
    __doc__ = '\n    Slider options\n    Valid for:\n      * Compact theme\n      * Default theme\n      * Grid theme\n      * Slider\n    '
    COLOR_WHITE = 'white'
    COLOR_BLACK = 'black'
    LOADER_COLOR_CHOICES = (
     (
      COLOR_WHITE, _('White')),
     (
      COLOR_BLACK, _('Black')))
    BUTTON_TYPE_SQUARE = 'square'
    BUTTON_TYPE_ROUND = 'round'
    BUTTON_TYPE_CHOICES = (
     (
      BUTTON_TYPE_SQUARE, _('Square')),
     (
      BUTTON_TYPE_ROUND, _('Round')))
    LOADER_TYPE_1 = 1
    LOADER_TYPE_2 = 2
    LOADER_TYPE_3 = 3
    LOADER_TYPE_4 = 4
    LOADER_TYPE_5 = 5
    LOADER_TYPE_6 = 6
    LOADER_TYPE_7 = 7
    LOADER_TYPE_CHOICES = (
     (
      LOADER_TYPE_1, _('Shape 1')),
     (
      LOADER_TYPE_2, _('Shape 2')),
     (
      LOADER_TYPE_3, _('Shape 3')),
     (
      LOADER_TYPE_4, _('Shape 4')),
     (
      LOADER_TYPE_5, _('Shape 5')),
     (
      LOADER_TYPE_6, _('Shape 6')),
     (
      LOADER_TYPE_7, _('Shape 7')))
    PROGRESSPIE_TYPE_STROKE = False
    PROGRESSPIE_TYPE_FILL = True
    PROGRESSPIE_TYPE_CHOICES = (
     (
      PROGRESSPIE_TYPE_STROKE, _('Stroke')),
     (
      PROGRESSPIE_TYPE_FILL, _('Fill')))
    INDICATOR_TYPE_PIE = 'pie'
    INDICATOR_TYPE_PIE2 = 'pie2'
    INDICATOR_TYPE_BAR = 'bar'
    INDICATOR_TYPE_CHOICES = (
     (
      INDICATOR_TYPE_PIE, _('Pie')),
     (
      INDICATOR_TYPE_PIE2, _('Pie 2')),
     (
      INDICATOR_TYPE_BAR, _('Bar')))
    SCALE_MODE_FIT = 'fit'
    SCALE_MODE_DOWN = 'down'
    SCALE_MODE_FILL = 'fill'
    SCALE_MODE_FITVERT = 'fitvert'
    SCALE_MODE_CHOICES = (
     (
      SCALE_MODE_FIT, _('scale down and up the image to always fit the slider')),
     (
      SCALE_MODE_DOWN, _("scale down only, smaller images will be shown, don't enlarge images (scale up)")),
     (
      SCALE_MODE_FILL, _('fill the entire slider space by scaling, cropping and centering the image')),
     (
      SCALE_MODE_FITVERT, _('make the image always fill the vertical slider area')))
    slider_arrows_skin = models.CharField((_('arrows skin')),
      max_length=255, blank=True,
      default='',
      choices=(settings.RIPIU_AOXOMOXOA_UNITE_SKINS),
      help_text=(_('Skin of the slider arrows, if blank inherit from gallery skin.')))
    slider_arrow_left_align_hor = models.CharField((_('left arrow alignment')),
      max_length=6, default=ALIGN_LEFT,
      blank=False,
      choices=ALIGN_CHOICES,
      help_text=(_('Left arrow horizonal alignment.')))
    slider_arrow_left_align_vert = models.CharField((_('left arrow vertical alignment')),
      max_length=6, default=VALIGN_MIDDLE,
      blank=False,
      choices=VALIGN_CHOICES)
    slider_arrow_right_align_vert = models.CharField((_('right arrow vertical alignment')),
      max_length=6, default=VALIGN_MIDDLE,
      blank=False,
      choices=VALIGN_CHOICES)
    slider_arrow_left_offset_hor = models.PositiveSmallIntegerField((_('left arrow horizontal offset')),
      default=20,
      blank=False)
    slider_arrow_left_offset_vert = models.PositiveSmallIntegerField((_('left arrow vertical offset')),
      default=0,
      blank=False)
    slider_arrow_right_align_hor = models.CharField((_('Right arrow alignment')),
      max_length=6, default=ALIGN_RIGHT,
      blank=False,
      choices=ALIGN_CHOICES,
      help_text=(_('Right arrow horizonal alignment.')))
    slider_arrow_right_align_vert = models.CharField((_('light arrow vertical alignment')),
      max_length=6, default=VALIGN_MIDDLE,
      blank=False,
      choices=VALIGN_CHOICES)
    slider_arrow_right_offset_hor = models.PositiveSmallIntegerField((_('right arrow horizontal offset')),
      default=20,
      blank=False)
    slider_arrow_right_offset_vert = models.PositiveSmallIntegerField((_('right arrow vertical offset')),
      default=0,
      blank=False)
    slider_bullets_align_hor = models.CharField((_('bullets alignment')),
      max_length=6, default=ALIGN_CENTER,
      blank=False,
      choices=ALIGN_CHOICES,
      help_text=(_('Bullets horizontal alignment.')))
    slider_bullets_align_vert = models.CharField((_('bullets vertical alignment')),
      max_length=6, default=VALIGN_BOTTOM,
      blank=False,
      choices=VALIGN_CHOICES)
    slider_bullets_offset_hor = models.PositiveSmallIntegerField((_('bullets horizontal offset')),
      default=0,
      blank=False)
    slider_bullets_offset_vert = models.PositiveSmallIntegerField((_('bullets vertical offset')),
      default=10,
      blank=False)
    slider_bullets_skin = models.CharField((_('bullets skin')),
      max_length=255, blank=True,
      default='',
      choices=(settings.RIPIU_AOXOMOXOA_UNITE_SKINS),
      help_text=(_('Skin of the bullets, if blank inherit from gallery skin.')))
    slider_bullets_space_between = models.SmallIntegerField((_('space between bullets')),
      default=None,
      blank=True,
      null=True,
      help_text=(_('Set the space between bullets. If blank then will be set default space from the skins.')))
    slider_controls_always_on = models.BooleanField((_('controls always on')),
      default=True, help_text=(_('Controls are always on, false - show only on mouseover.')))
    slider_controls_appear_duration = models.PositiveSmallIntegerField((_('controls appear duration')),
      default=300,
      blank=False,
      help_text=(_('The duration of appearing controls.')))
    slider_controls_appear_ontap = models.BooleanField((_('controls appear on tap')),
      default=True, help_text=(_('Appear controls on tap event on touch devices.')))
    slider_control_swipe = models.BooleanField((_('enable swiping control')),
      default=True)
    slider_control_zoom = models.BooleanField((_('enable zooming control')),
      default=True)
    slider_enable_arrows = models.BooleanField((_('enable arrows')),
      default=True)
    slider_enable_bullets = models.BooleanField((_('enable bullets')),
      default=False)
    slider_enable_fullscreen_button = models.BooleanField((_('enable fullscreen button')),
      default=True)
    slider_enable_play_button = models.BooleanField((_('enable play button')),
      default=True)
    slider_enable_progress_indicator = models.BooleanField((_('enable progress indicator')),
      default=True)
    slider_enable_text_panel = models.BooleanField((_('enable text panel')),
      default=False)
    slider_enable_zoom_panel = models.BooleanField((_('enable zoom panel')),
      default=True, help_text=(_('Enable the zoom buttons, works together with zoom control.')))
    slider_fullscreen_button_align_hor = models.CharField((_('fullscreen button alignment')),
      max_length=6, default=ALIGN_LEFT,
      blank=False,
      choices=ALIGN_CHOICES,
      help_text=(_('Fullscreen button horizonatal alignment.')))
    slider_fullscreen_button_align_vert = models.CharField((_('fullscreen button vertical alignment')),
      max_length=6, default=VALIGN_TOP,
      blank=False,
      choices=VALIGN_CHOICES)
    slider_fullscreen_button_offset_hor = models.PositiveSmallIntegerField((_('fullscreen button horizontal offset')),
      default=11,
      blank=False)
    slider_fullscreen_button_offset_vert = models.PositiveSmallIntegerField((_('fullscreen button vertical offset')),
      default=9,
      blank=False)
    slider_fullscreen_button_skin = models.CharField((_('fullscreen button skin')),
      max_length=255, blank=True,
      default='',
      choices=(settings.RIPIU_AOXOMOXOA_UNITE_SKINS),
      help_text=(_('Skin of the slider fullscreen button, if empty inherit from gallery skin.')))
    slider_item_padding_bottom = models.PositiveSmallIntegerField((_('slider item bottom padding')),
      default=0,
      blank=False)
    slider_item_padding_left = models.PositiveSmallIntegerField((_('slider item left padding')),
      default=0,
      blank=False)
    slider_item_padding_right = models.PositiveSmallIntegerField((_('slider item right padding')),
      default=0,
      blank=False)
    slider_item_padding_top = models.PositiveSmallIntegerField((_('slider item top padding')),
      default=0,
      blank=False)
    slider_loader_color = models.CharField((_('loader color')),
      max_length=6, default=COLOR_WHITE,
      blank=False,
      choices=LOADER_COLOR_CHOICES)
    slider_loader_type = models.PositiveSmallIntegerField((_('shape of the loader')),
      default=LOADER_TYPE_1,
      blank=False,
      choices=LOADER_TYPE_CHOICES)
    slider_play_button_align_hor = models.CharField((_('play button alignment')),
      max_length=6, default=ALIGN_LEFT,
      blank=False,
      choices=ALIGN_CHOICES,
      help_text=(_('Play button horizonatal alignment.')))
    slider_play_button_align_vert = models.CharField((_('play button vertical alignment')),
      max_length=6, default=VALIGN_TOP,
      blank=False,
      choices=VALIGN_CHOICES)
    slider_play_button_offset_hor = models.PositiveSmallIntegerField((_('play button horizontal offset')),
      default=40,
      blank=False)
    slider_play_button_offset_vert = models.PositiveSmallIntegerField((_('play button vertical offset')),
      default=8,
      blank=False)
    slider_play_button_skin = models.CharField((_('play button skin')),
      max_length=255, blank=True,
      default='',
      choices=(settings.RIPIU_AOXOMOXOA_UNITE_SKINS),
      help_text=(_('Skin of the slider play button, if empty inherit from gallery skin.')))
    slider_progressbar_color = ColorField((_('progress bar color')),
      blank=False,
      default='#FFFFFF')
    slider_progressbar_line_width = models.PositiveSmallIntegerField((_('progress bar line width')),
      default=5,
      blank=False)
    slider_progressbar_opacity = models.PositiveSmallIntegerField((_('progress bar opacity (%)')),
      blank=False,
      default=60,
      validators=[
     MaxValueValidator(100)],
      help_text=(_('The opacity of the progress bar.')))
    slider_progresspie_color1 = ColorField((_('progress pie first color')),
      blank=False,
      default='#B5B5B5')
    slider_progresspie_color2 = ColorField((_('progress pie second color')),
      blank=False,
      default='#E5E5E5')
    slider_progresspie_height = models.PositiveSmallIntegerField((_('progress pie height')),
      default=30,
      blank=False)
    slider_progresspie_stroke_width = models.PositiveSmallIntegerField((_('progress pie stroke width')),
      default=6,
      blank=False)
    slider_progresspie_type_fill = models.BooleanField((_('progress pie type')),
      default=PROGRESSPIE_TYPE_STROKE,
      choices=PROGRESSPIE_TYPE_CHOICES)
    slider_progresspie_width = models.PositiveSmallIntegerField((_('progress pie width')),
      default=30,
      blank=False)
    slider_progress_indicator_align_hor = models.CharField((_('progress indicator alignment')),
      max_length=6, default=ALIGN_LEFT,
      blank=False,
      choices=ALIGN_CHOICES,
      help_text=(_('Progress indicator horizonatal alignment.')))
    slider_progress_indicator_align_vert = models.CharField((_('progress indicator vertical alignment')),
      max_length=6, default=VALIGN_TOP,
      blank=False,
      choices=VALIGN_CHOICES)
    slider_progress_indicator_offset_hor = models.PositiveSmallIntegerField((_('progress indicator horizontal offset ')),
      default=16,
      blank=False)
    slider_progress_indicator_offset_vert = models.PositiveSmallIntegerField((_('progress indicator vertical offset ')),
      default=36,
      blank=False)
    slider_progress_indicator_type = models.CharField((_('progress indicator type')),
      max_length=4, default=INDICATOR_TYPE_PIE,
      blank=False,
      choices=INDICATOR_TYPE_CHOICES,
      help_text=(_('if pie not supported, it will switch to bar automatically.')))
    slider_scale_mode = models.CharField((_('scale mode')),
      max_length=4, default=SCALE_MODE_FILL,
      blank=False,
      choices=SCALE_MODE_CHOICES)
    slider_scale_mode_fullscreen = models.CharField((_('fullscreen scale mode')),
      max_length=4, default=SCALE_MODE_DOWN,
      blank=False,
      choices=SCALE_MODE_CHOICES)
    slider_scale_mode_media = models.CharField((_('scale mode on media items')),
      max_length=4, default=SCALE_MODE_FILL,
      blank=False,
      choices=SCALE_MODE_CHOICES)
    slider_textpanel_always_on = models.BooleanField((_('text panel always on')),
      default=True, help_text=(_('Text panel are always on or show only on mouseover.')))
    slider_textpanel_bg_color = ColorField((_('text panel background color')),
      blank=False,
      default='#000000')
    slider_textpanel_bg_css = AttributesField(verbose_name=(_('text panel background CSS')),
      blank=True,
      default={})
    slider_textpanel_bg_opacity = models.PositiveSmallIntegerField((_('text panel background opacity (%)')),
      blank=False,
      default=40,
      validators=[
     MaxValueValidator(100)])
    slider_textpanel_css_description = AttributesField(verbose_name=(_('text panel description CSS')),
      blank=True,
      default={},
      help_text=(_('Textpanel additional CSS of the description.')))
    slider_textpanel_css_title = AttributesField(verbose_name=(_('text panel title CSS')),
      blank=True,
      default={},
      help_text=(_('Textpanel additional CSS of the title.')))
    slider_textpanel_desc_bold = models.NullBooleanField((_('Bold description')),
      default=None)
    slider_textpanel_desc_color = ColorField((_('text panel description text color')),
      blank=True,
      default='')
    slider_textpanel_desc_font_family = models.CharField((_('description font family')),
      max_length=255, default='',
      blank=True,
      help_text=(_('A CSS font family for the description.')))
    slider_textpanel_desc_font_size = models.PositiveSmallIntegerField((_('description font size (px)')),
      default=None,
      blank=True,
      null=True,
      help_text=(_('Textpanel description font size. If blank take from css.')))
    slider_textpanel_desc_text_align = models.CharField((_('description text alignment')),
      max_length=6, default='',
      blank=True,
      choices=ALIGN_CHOICES,
      help_text=(_('Textpanel description text alignment. If blank take from CSS.')))
    slider_textpanel_enable_bg = models.BooleanField((_('enable background')),
      default=True, help_text=(_('Enable the textpanel background.')))
    slider_textpanel_enable_description = models.BooleanField((_('enable description')),
      default=True, help_text=(_('Enable the description text.')))
    slider_textpanel_enable_title = models.BooleanField((_('enable title')),
      default=True, help_text=(_('Enable the title text.')))
    slider_textpanel_fade_duration = models.PositiveSmallIntegerField((_('text panel fade duration ')),
      default=200,
      blank=False)
    slider_textpanel_height = models.PositiveSmallIntegerField((_('text panel height ')),
      default=None,
      blank=True,
      null=True,
      help_text=(_('If blank it will be set dynamically.')))
    slider_textpanel_padding_bottom = models.PositiveSmallIntegerField((_('text panel bottom padding')),
      default=10,
      blank=False)
    slider_textpanel_padding_left = models.PositiveSmallIntegerField((_('text panel left padding')),
      default=11,
      blank=False)
    slider_textpanel_padding_right = models.PositiveSmallIntegerField((_('text panel right padding')),
      default=10,
      blank=False)
    slider_textpanel_padding_title_description = models.PositiveSmallIntegerField((_('text panel title padding')),
      default=5,
      blank=False,
      help_text=(_('the space between the title and the description.')))
    slider_textpanel_padding_top = models.PositiveSmallIntegerField((_('text panel top padding')),
      default=10,
      blank=False)
    slider_textpanel_text_valign = models.CharField((_('text panel vertical alignment')),
      max_length=6, default=VALIGN_MIDDLE,
      blank=False,
      choices=VALIGN_CHOICES)
    slider_textpanel_title_bold = models.NullBooleanField((_('Bold title')),
      default=None)
    slider_textpanel_title_color = ColorField((_('text panel title text color')),
      blank=True,
      default='')
    slider_textpanel_title_font_family = models.CharField((_('title font family')),
      max_length=255, default='',
      blank=True,
      help_text=(_('A CSS font family for the title.')))
    slider_textpanel_title_font_size = models.PositiveSmallIntegerField((_('title font size (px)')),
      default=None,
      blank=True,
      null=True,
      help_text=(_('Textpanel title font size. If blank take from css.')))
    slider_textpanel_title_text_align = models.CharField((_('description text alignment')),
      max_length=6, default='',
      blank=True,
      choices=ALIGN_CHOICES,
      help_text=(_('Textpanel title text alignment. If blank take from CSS.')))
    slider_transition = models.CharField((_('transition')),
      max_length=5, default=APPEAR_SLIDE,
      blank=False,
      choices=APPEAR_CHOICES,
      help_text=(_('The transition of the slide change.')))
    slider_transition_easing = models.CharField((_('transition easing')),
      max_length=17, default=EASE_INOUT_QUAD,
      blank=False,
      choices=EASING_CHOICES,
      help_text=(_('Transition easing function of slide change.')))
    slider_transition_speed = models.PositiveSmallIntegerField((_('transition speed')),
      default=300,
      blank=False,
      help_text=(_('Transition duration of slide change.')))
    slider_videoplay_button_type = models.CharField((_('videoplay button type')),
      max_length=6, default=BUTTON_TYPE_SQUARE,
      blank=False,
      choices=BUTTON_TYPE_CHOICES)
    slider_zoompanel_align_hor = models.CharField((_('zoom panel alignment')),
      max_length=6, default=ALIGN_RIGHT,
      blank=False,
      choices=ALIGN_CHOICES,
      help_text=(_('Zoom panel horizonatal alignment.')))
    slider_zoompanel_align_vert = models.CharField((_('zoom panel vertical alignment')),
      max_length=6, default=VALIGN_TOP,
      blank=False,
      choices=VALIGN_CHOICES)
    slider_zoompanel_offset_hor = models.PositiveSmallIntegerField((_('zoom panel horizontal offset')),
      default=12,
      blank=False)
    slider_zoompanel_offset_vert = models.PositiveSmallIntegerField((_('zoom panel vertical offset')),
      default=10,
      blank=False)
    slider_zoompanel_skin = models.CharField((_('zoom panel skin')),
      max_length=255, blank=True,
      default='',
      choices=(settings.RIPIU_AOXOMOXOA_UNITE_SKINS),
      help_text=(_('Skin of the slider zoom panel, if empty inherit from gallery skin.')))
    slider_zoom_max_ratio = models.PositiveSmallIntegerField((_('maximum zoom ratio')),
      default=6,
      blank=False)

    class Meta:
        abstract = True