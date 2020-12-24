# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grantj/repos/sphinx-gjtheme/gjtheme/__init__.py
# Compiled at: 2018-05-09 15:40:41
"""Sphinx GJ Theme

Sphinx GJ Theme is an Apache2 licensed Sphinx theme for projects by Grant
Jenks.

"""
import os

def setup(app):
    app.add_html_theme('gjtheme', os.path.abspath(os.path.dirname(__file__)))


__title__ = 'gjtheme'
__version__ = '0.3.0'
__build__ = 768
__author__ = 'Grant Jenks'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2018 Grant Jenks'