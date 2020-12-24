# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/djbaldey/src/sphinx-rosix-theme/rosixdocs/__init__.py
# Compiled at: 2015-07-17 03:04:13
import os
VERSION = (0, 1, 3)

def get_version(*args, **kwargs):
    return '%d.%d.%d' % VERSION


def get_docs_version(*args, **kwargs):
    return '%d.%d' % VERSION[:2]


__version__ = get_version()

def get_themes_path():
    """ Returns path to included themes. """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'themes'))