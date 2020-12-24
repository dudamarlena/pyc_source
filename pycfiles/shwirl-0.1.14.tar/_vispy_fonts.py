# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/util/fonts/_vispy_fonts.py
# Compiled at: 2016-11-03 01:40:19
from ..fetching import load_data_file
_vispy_fonts = ('OpenSans', 'Cabin')

def _get_vispy_font_filename(face, bold, italic):
    """Fetch a remote vispy font"""
    name = face + '-'
    name += 'Regular' if not bold and not italic else ''
    name += 'Bold' if bold else ''
    name += 'Italic' if italic else ''
    name += '.ttf'
    return load_data_file('fonts/%s' % name)