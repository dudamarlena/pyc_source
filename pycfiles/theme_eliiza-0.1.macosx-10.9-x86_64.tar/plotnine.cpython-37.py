# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/admin/miniconda3/lib/python3.7/site-packages/theme_eliiza/plotnine.py
# Compiled at: 2020-04-16 02:26:39
# Size of source mod 2**32: 2000 bytes
import matplotlib, os
from plotnine.options import get_option
from plotnine.themes import theme
from plotnine.themes.elements import element_line, element_rect, element_text, element_blank
here = os.path.dirname(os.path.realpath(__file__))
font_path = os.path.join(here, 'data', 'Poppins-Regular.ttf')
matplotlib.font_manager.fontManager.addfont(font_path)
eliiza_filepath = os.path.join(here, 'data', 'eliiza.mplstyle')
rc_params = matplotlib.rc_params_from_file(eliiza_filepath)
eliiza_purple = '#9e00e9'
eliiza_teal = '#32acac'
eliiza_navy = '#1e3452'
eliiza_dark_purple = '#4A0F6F'
phi = 1.618

class theme_eliiza(theme):

    def __init__(self, base_size=16):
        half_line = base_size / 2
        theme.__init__(self,
          rect=element_rect(fill=(rc_params['axes.facecolor']), color=(rc_params['axes.facecolor'])),
          line=element_line(color=(rc_params['grid.color'])),
          text=element_text(family='Poppins', size=base_size, color=(rc_params['text.color'])),
          title=element_text(size=(base_size * phi)),
          axis_text=element_text(size=(base_size / phi)),
          axis_title=element_text(size=base_size),
          axis_text_x=element_text(va='top', margin={'t': half_line / 2}),
          axis_title_x=element_text(va='top', margin={'t': half_line}),
          axis_text_y=element_text(angle=0, ha='right', margin={'r': half_line / 2}),
          axis_title_y=element_text(angle=0, va='top', ha='left', margin={'r': half_line}),
          panel_grid_major_x=(element_blank()),
          panel_grid_minor_x=(element_blank()),
          panel_grid_major_y=(element_blank()),
          axis_line=(element_blank()),
          axis_ticks_pad=(half_line * 2),
          aspect_ratio=(get_option('aspect_ratio')))