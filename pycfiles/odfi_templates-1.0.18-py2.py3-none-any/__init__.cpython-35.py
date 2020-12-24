# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/leysr/git/main/doc/duckdoc/master/sphinx/odfi_templates\odfi_templates\mariana\__init__.py
# Compiled at: 2017-03-11 11:56:56
# Size of source mod 2**32: 254 bytes
""" Sphinx ODFi Theme
"""
import os
__version__ = '1.0.1'
__version_full__ = __version__

def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return cur_dir