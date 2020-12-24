# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dre/work/git/sphinx_iowmd_theme/sphinx_iowmd_theme/__init__.py
# Compiled at: 2020-05-07 06:01:42
# Size of source mod 2**32: 253 bytes
from os import path
__version__ = '0.0.6'
__version_full__ = __version__
package_dir = path.dirname(path.abspath(__file__))

def get_path():
    return package_dir


def setup(app):
    app.add_html_theme('sphinx_iowmd_theme', package_dir)