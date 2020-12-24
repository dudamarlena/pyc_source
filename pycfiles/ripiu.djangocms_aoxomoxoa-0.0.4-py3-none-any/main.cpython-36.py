# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/geobaldi/src/ripiu/public/github/djangocms_aoxomoxoa/ripiu/djangocms_aoxomoxoa/models/options/main.py
# Compiled at: 2018-04-03 09:24:46
# Size of source mod 2**32: 1233 bytes
from django.db import models
from django.utils.translation import ugettext_lazy as _

class MainOptions(models.Model):
    __doc__ = '\n    Main options.\n    Valid for:\n      * Carousel\n      * Tiles - Grid\n    '
    tile_height = models.PositiveSmallIntegerField((_('tile height')),
      default=150,
      blank=False)
    tile_width = models.PositiveSmallIntegerField((_('tile height')),
      default=180,
      blank=False)

    class Meta:
        abstract = True


class TilesGridMainOptions(MainOptions):
    __doc__ = '\n    Main options for Tiles - Grid\n    '
    grid_padding = models.PositiveSmallIntegerField((_('tile height')),
      default=10,
      blank=False)
    grid_space_between_cols = models.PositiveSmallIntegerField((_('space between columns')),
      default=20,
      blank=False)
    grid_space_between_rows = models.PositiveSmallIntegerField((_('space between rows')),
      default=20,
      blank=False)

    class Meta:
        abstract = True