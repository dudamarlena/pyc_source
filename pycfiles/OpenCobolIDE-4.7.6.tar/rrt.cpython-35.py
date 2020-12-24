# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/styles/rrt.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 852 bytes
"""
    pygments.styles.rrt
    ~~~~~~~~~~~~~~~~~~~

    pygments "rrt" theme, based on Zap and Emacs defaults.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Comment, Name, Keyword, String

class RrtStyle(Style):
    __doc__ = '\n    Minimalistic "rrt" theme, based on Zap and Emacs defaults.\n    '
    background_color = '#000000'
    highlight_color = '#0000ff'
    styles = {Comment: '#00ff00', 
     Name.Function: '#ffff00', 
     Name.Variable: '#eedd82', 
     Name.Constant: '#7fffd4', 
     Keyword: '#ff0000', 
     Comment.Preproc: '#e5e5e5', 
     String: '#87ceeb', 
     Keyword.Type: '#ee82ee'}