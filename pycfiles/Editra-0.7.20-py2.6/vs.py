# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/pygments/styles/vs.py
# Compiled at: 2011-04-22 17:53:22
"""
    pygments.styles.vs
    ~~~~~~~~~~~~~~~~~~

    Simple style with MS Visual Studio colors.

    :copyright: Copyright 2006-2010 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Operator, Generic

class VisualStudioStyle(Style):
    background_color = '#ffffff'
    default_style = ''
    styles = {Comment: '#008000', 
       Comment.Preproc: '#0000ff', 
       Keyword: '#0000ff', 
       Operator.Word: '#0000ff', 
       Keyword.Type: '#2b91af', 
       Name.Class: '#2b91af', 
       String: '#a31515', 
       Generic.Heading: 'bold', 
       Generic.Subheading: 'bold', 
       Generic.Emph: 'italic', 
       Generic.Strong: 'bold', 
       Generic.Prompt: 'bold', 
       Error: 'border:#FF0000'}