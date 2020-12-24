# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bcsaller/Projects/chimera/build/lib.linux-i686-2.5/chimera/__init__.py
# Compiled at: 2007-02-08 13:55:30
__doc__ = "\nchimera\n~~~~~~~~~~~~~~~~~~~~\nSimple Image Generation\n\nChimera is a higher level graphics abstraction than is commonly\navailable for Python. Taking advantage of the power of the Pango\nlibrary (http://www.pango.org/) we are able to render beautiful\nsubpixel rendered, anti-aliased text in the fonts of your choice.\n\nChimera doesn't expose all the funtionality of its underlying\nsystems. In particular its not about drawing, pixel manipulation or\nother low level operations on a surface. Chimera attempts to deal with\nhandling all its operations in a uniform, simple way so that you can\nfocus on the output you want to generate, now how to generate it.\n\n"
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