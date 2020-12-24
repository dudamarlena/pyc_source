# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/mx-theme/mxtheme/__init__.py
# Compiled at: 2019-11-06 16:19:36
# Size of source mod 2**32: 276 bytes
from os import path
from .card import CardDirective
__version__ = '0.3.11'
__version_full__ = __version__
package_dir = path.dirname(path.abspath(__file__))

def get_path():
    return package_dir


def setup(app):
    app.add_html_theme('mxtheme', package_dir)