# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/onefinestay/sphinx-nameko-theme/sphinx_nameko_theme/__init__.py
# Compiled at: 2015-04-08 09:22:18
"""Sphinx Nameko Theme.

A fork of https://github.com/ignacysokolowski/sphinx-readable-theme for use
in Nameko (https://github.com/onefinestay/nameko)

"""
import os

def get_html_theme_path():
    """Return path to directory containing package theme."""
    return os.path.abspath(os.path.dirname(__file__))