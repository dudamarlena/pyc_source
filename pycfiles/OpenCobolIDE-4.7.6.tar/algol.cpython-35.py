# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/styles/algol.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 2263 bytes
"""
    pygments.styles.algol
    ~~~~~~~~~~~~~~~~~~~~~

    Algol publication style.

    This style renders source code for publication of algorithms in
    scientific papers and academic texts, where its format is frequently used.

    It is based on the style of the revised Algol-60 language report[1].

    o  No colours, only black, white and shades of grey are used.
    o  Keywords are rendered in lowercase underline boldface.
    o  Builtins are rendered in lowercase boldface italic.
    o  Docstrings and pragmas are rendered in dark grey boldface.
    o  Library identifiers are rendered in dark grey boldface italic.
    o  Comments are rendered in grey italic.

    To render keywords without underlining, refer to the `Algol_Nu` style.

    For lowercase conversion of keywords and builtins in languages where
    these are not or might not be lowercase, a supporting lexer is required.
    The Algol and Modula-2 lexers automatically convert to lowercase whenever
    this style is selected.

    [1] `Revised Report on the Algorithmic Language Algol-60 <http://www.masswerk.at/algol60/report.htm>`

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Operator

class AlgolStyle(Style):
    background_color = '#ffffff'
    default_style = ''
    styles = {Comment: 'italic #888', 
     Comment.Preproc: 'bold noitalic #888', 
     Comment.Special: 'bold noitalic #888', 
     Keyword: 'underline bold', 
     Keyword.Declaration: 'italic', 
     Name.Builtin: 'bold italic', 
     Name.Builtin.Pseudo: 'bold italic', 
     Name.Namespace: 'bold italic #666', 
     Name.Class: 'bold italic #666', 
     Name.Function: 'bold italic #666', 
     Name.Variable: 'bold italic #666', 
     Name.Constant: 'bold italic #666', 
     Operator.Word: 'bold', 
     String: 'italic #666', 
     Error: 'border:#FF0000'}