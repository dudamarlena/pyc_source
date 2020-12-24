# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/juca/mysrc/etc-docs/staticworkflow/sphinx_pdj_theme/__init__.py
# Compiled at: 2017-10-21 14:53:30
# Size of source mod 2**32: 192 bytes
import os
VERSION = '0.1'

def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    return cur_dir