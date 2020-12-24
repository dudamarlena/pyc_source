# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/juca/mysrc/toxicbuild/sphinx_pdj_theme/__init__.py
# Compiled at: 2019-09-17 09:46:30
# Size of source mod 2**32: 261 bytes
import os
VERSION = '0.1.5'

def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    return cur_dir


def setup(app):
    app.add_html_theme('sphinx_pdj_theme', get_html_theme_path())