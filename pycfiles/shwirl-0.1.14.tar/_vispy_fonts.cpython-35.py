# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/util/fonts/_vispy_fonts.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 752 bytes
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