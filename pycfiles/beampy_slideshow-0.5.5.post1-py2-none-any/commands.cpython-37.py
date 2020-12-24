# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/commands.py
# Compiled at: 2019-05-31 13:34:19
# Size of source mod 2**32: 906 bytes
"""
@author: hugo

Here we define commands used to create elements in beampy

"""
from beampy.modules.core import *
from beampy.document import document, section, subsection, subsubsection
from beampy.modules.text import *
from beampy.modules.title import *
from beampy.modules.figure import *
from beampy.modules.animatesvg import *
from beampy.modules.video import *
from beampy.modules.tikz import *
from beampy.modules.code import *
from beampy.modules.svg import *
from beampy.modules.box import *
from beampy.modules.toc import tableofcontents
import beampy.modules.iframe as iframe
from beampy.modules.biblio import cite
import beampy.modules.arrow as arrow
import beampy.modules.itemize as itemize
from beampy.modules.maketitle import *