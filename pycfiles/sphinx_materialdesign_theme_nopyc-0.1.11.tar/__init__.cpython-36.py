# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Liam\PycharmProjects\materialthemenopyc\sphinx_materialdesign_theme\sphinx_materialdesign_theme\__init__.py
# Compiled at: 2019-04-28 15:36:52
# Size of source mod 2**32: 263 bytes
from os import path
__version__ = '0.1.11'
__version_full__ = __version__
package_dir = path.dirname(path.abspath(__file__))

def get_path():
    return package_dir


def setup(app):
    app.add_html_theme('sphinx_materialdesign_theme', package_dir)