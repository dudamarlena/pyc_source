# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/shrubbery/__init__.py
# Compiled at: 2007-06-22 17:40:39
"""A simple template engine.

Shrubbery intends to be the world's easiest template language. It
has two major advantages::

1. The user doesn't need to learn a new syntax. Templates are simply
   structural, and contain no code at all. Logic is dictated by the
   data following an implicit -- though intuitive! -- algorithm.

2. Templates don't have to be valid HTML/XHTML. Shrubbery uses the
   wonderful BeautifulSoup module for the heavy lifting, and can
   handle templates with broken HTML.
"""
from template import Template