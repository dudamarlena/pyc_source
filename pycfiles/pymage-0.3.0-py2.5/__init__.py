# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pymage/__init__.py
# Compiled at: 2007-09-07 22:23:35
"""
Various utilities to simplify Pygame_ development.

:Author: Ross Light
:Copyright: Copyright (C) 2006-2007 Ross Light
:Contact: rlight2@gmail.com
:License:
    pymage is free software; you can redistribute it and/or modify it under the
    terms of the `GNU Lesser General Public License`_ as published by the `Free
    Software Foundation`_; either version 3 of the License, or (at your option)
    any later version.
    
    pymage is distributed in the hope that it will be useful, but **WITHOUT ANY
    WARRANTY**; without even the implied warranty of **MERCHANTABILITY** or
    **FITNESS FOR A PARTICULAR PURPOSE**.  See the `GNU Lesser General Public
    License`_ for more details.
    
    You should have received a copy of the `GNU Lesser General Public License`_
    along with this library.  If not, see http://www.gnu.org/licenses/.

.. _Pygame: http://www.pygame.org/
.. _GNU Lesser General Public License: http://www.gnu.org/licenses/lgpl.html
.. _Free Software Foundation: http://fsf.org/
"""
__author__ = 'Ross Light'
__date__ = 'July 20, 2006'
__all__ = ['config',
 'joystick',
 'resman',
 'sound',
 'sprites',
 'states',
 'timer',
 'ui',
 'vector',
 'vfs']
__docformat__ = 'reStructuredText'
__version__ = '0.3.0'
from pymage import config
from pymage import joystick
from pymage import resman
from pymage import sound
from pymage import sprites
from pymage import states
from pymage import timer
from pymage import ui
from pymage import vector
from pymage import vfs