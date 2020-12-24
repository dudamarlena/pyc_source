# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/LeslieZhu/.pyenv/versions/2.7.15/Python.framework/Versions/2.7/lib/python2.7/site-packages/orgnote/__init__.py
# Compiled at: 2019-11-27 20:06:24
"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""
from __future__ import absolute_import
__version__ = '0.5.7'

def main():
    import orgnote.__main__
    orgnote.__main__.main()