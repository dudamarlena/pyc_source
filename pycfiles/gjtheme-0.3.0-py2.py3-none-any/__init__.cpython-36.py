# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grantj/repos/sphinx-gjtheme/gjtheme/__init__.py
# Compiled at: 2018-02-09 11:44:15
# Size of source mod 2**32: 378 bytes
"""Sphinx GJ Theme

Sphinx GJ Theme is an Apache2 licensed Sphinx theme for projects by Grant
Jenks.

"""
import os

def setup(app):
    app.add_html_theme('gjtheme', os.path.abspath(os.path.dirname(__file__)))


__title__ = 'gjtheme'
__version__ = '0.2.5'
__build__ = 517
__author__ = 'Grant Jenks'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2018 Grant Jenks'