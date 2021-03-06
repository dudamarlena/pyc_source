# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bcsaller/Projects/chimera/build/lib.linux-i686-2.5/chimera/__init__.py
# Compiled at: 2007-02-08 13:55:30
"""
chimera
~~~~~~~~~~~~~~~~~~~~
Simple Image Generation

Chimera is a higher level graphics abstraction than is commonly
available for Python. Taking advantage of the power of the Pango
library (http://www.pango.org/) we are able to render beautiful
subpixel rendered, anti-aliased text in the fonts of your choice.

Chimera doesn't expose all the funtionality of its underlying
systems. In particular its not about drawing, pixel manipulation or
other low level operations on a surface. Chimera attempts to deal with
handling all its operations in a uniform, simple way so that you can
focus on the output you want to generate, now how to generate it.

"""
__author__ = 'Benjamin Saller <bcsaller@objectrealms.net>'
__docformat__ = 'restructuredtext'
__copyright__ = 'Copyright Benjamin Saller, 2005.'
__license__ = 'The GNU Public License V2+'
from chimera import pangocairo
from chimera import fontconfig
from chimera import chimera_svg
from chimera import utils
from chimera import *
pangocairo.cairo_operator_map = utils.twoway(pangocairo.cairo_operators)