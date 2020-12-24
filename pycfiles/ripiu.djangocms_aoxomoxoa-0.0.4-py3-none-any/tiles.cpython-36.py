# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geobaldi/src/ripiu/public/github/djangocms_aoxomoxoa/ripiu/djangocms_aoxomoxoa/models/options/tiles.py
# Compiled at: 2018-04-03 09:24:46
# Size of source mod 2**32: 4015 bytes
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .constants import ALIGN_CENTER, ALIGN_CHOICES

class TilesOptions(models.Model):
    __doc__ = '\n    Tiles options\n    Valid for:\n      * Tiles - Columns\n      * Tiles - Justified\n      * Tiles - Nested\n    '
    tiles_enable_transition = models.BooleanField((_('enable transition')),
      default=True, help_text=(_('enable transition on screen width change.')))

    class Meta:
        abstract = True


class ColumnLayoutTileOptions(models.Model):
    __doc__ = '\n    Tiles options\n    Valid for:\n      * Tiles - Columns\n      * Tiles - Nested\n    '
    tiles_space_between_cols = models.PositiveSmallIntegerField((_('space between images')),
      default=3,
      blank=False)
    tiles_space_between_cols_mobile = models.PositiveSmallIntegerField((_('space between images (mobile)')),
      default=3,
      blank=False,
      help_text=(_('Space between cols for mobile type.')))
    tiles_min_columns = models.PositiveSmallIntegerField((_('min columns')),
      default=2,
      blank=False,
      help_text=(_('Maximum number of columns, for mobile size.')))

    class Meta:
        abstract = True


class InitialHeightTilesOptions(models.Model):
    __doc__ = '\n    Tiles options\n    Valid for:\n      * Tiles - Columns\n      * Tiles - Justified\n    '
    tiles_set_initial_height = models.BooleanField((_('set initial height')),
      default=True, help_text=(_('Columns type related only.')))

    class Meta:
        abstract = True


class ColumnsTilesOptions(ColumnLayoutTileOptions, InitialHeightTilesOptions, TilesOptions):
    __doc__ = '\n    Tiles options for Tiles - Columns\n    '
    tiles_align = models.CharField((_('align')),
      max_length=6, default=ALIGN_CENTER,
      blank=False,
      choices=ALIGN_CHOICES,
      help_text=(_('Alignment of the tiles in the space.')))
    tiles_col_width = models.PositiveSmallIntegerField((_('column width')),
      default=250,
      blank=False,
      help_text=(_('Column width. Exact or base according the settings.')))
    tiles_exact_width = models.BooleanField((_('exact width')),
      default=False, help_text=(_('Exact width of column. Disables the min and max columns.')))
    tiles_include_padding = models.BooleanField((_('include padding')),
      default=True, help_text=(_('Include padding at the sides of the columns, equal to current space between cols.')))
    tiles_max_columns = models.PositiveSmallIntegerField((_('maximum columns')),
      default=0,
      blank=False,
      help_text=(_('Maximum number of columns (0 for unlimited).')))

    class Meta:
        abstract = True


class NestedTilesOptions(ColumnLayoutTileOptions, TilesOptions):
    __doc__ = '\n    Tiles options for Tiles - Nested\n    '
    tiles_nested_optimal_tile_width = models.PositiveSmallIntegerField((_('optimal_tile_width')),
      default=250,
      blank=False)

    class Meta:
        abstract = True


class JustifiedTilesOptions(InitialHeightTilesOptions, TilesOptions):
    __doc__ = '\n    Tiles options for Tiles - Justified\n    '
    tiles_justified_row_height = models.PositiveSmallIntegerField((_('row height')),
      default=150,
      blank=False,
      help_text=(_('Base row height of the justified type.')))
    tiles_justified_space_between = models.PositiveSmallIntegerField((_('space between')),
      default=3,
      blank=False,
      help_text=(_('Space between the tiles justified type.')))

    class Meta:
        abstract = True