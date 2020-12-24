# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/themes/SimpleBlue_theme.py
# Compiled at: 2016-06-25 14:51:38
# Size of source mod 2**32: 1430 bytes
THEME = {}
lead_color = 'SteelBlue'
standard_text_color = 'black'
THEME['document'] = {'format': 'html5', 
 'width': 800, 
 'height': 600}
THEME['text'] = {'size': 20, 
 'font': 'CMR', 
 'color': standard_text_color, 
 'align': '', 
 'x': 'center', 
 'y': 'auto', 
 'width': None, 
 'usetex': True, 
 'va': ''}
THEME['title'] = {'size': 28, 
 'font': 'CMR', 
 'color': lead_color, 
 'x': {'shift': 0.5, 'unit': 'cm'}, 
 'y': {'shift': 1.2, 'unit': 'cm'}, 
 'reserved_y': '1.5cm', 
 'align': '', 
 'va': 'baseline'}
THEME['maketitle'] = {'title_color': THEME['title']['color'], 
 'author_size': THEME['text']['size'], 
 'date_color': standard_text_color, 
 'subtitle_color': standard_text_color}
THEME['link'] = {'fill': THEME['title']['color']}
THEME['itemize'] = {'x': 'center', 
 'y': 'auto', 
 'item_style': 'bullet', 
 'item_spacing': '+1cm', 
 'item_indent': '0cm', 
 'item_color': THEME['title']['color'], 
 'text_color': THEME['text']['color'], 
 'width': None}