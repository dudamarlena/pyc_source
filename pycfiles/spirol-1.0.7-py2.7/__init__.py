# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spirol/__init__.py
# Compiled at: 2015-01-09 08:50:14
from __future__ import print_function
from spirol.core import spirol_core as spirol
from spirol.errors import InputFormatError, UnknownImplementation, InvalidDirection, NotSupportedError, NonSpirolInterface
from spirol.utils import SpirolType, SpirolDirection, SpirolCorner, TOP_LEFT, TOP_RIGHT, BOTTOM_RIGHT, BOTTOM_LEFT
__author__ = 'Francis Horsman'
__url__ = 'https://bitbucket.org/sys-git/spirol'
__email__ = 'francis.horsman@gmail.com'
__short_description__ = 'A pure-python non-repeating outside-in spiral iterator-generator for 2D arrays'
__long_description__ = __short_description__ + '.\nSpirals can be constructed clockwise or counter-clockwise and start from any corner.'
from .version import get_versions
__version__ = get_versions()['version']
del get_versions
if __name__ == '__main__':
    print(__long_description__)