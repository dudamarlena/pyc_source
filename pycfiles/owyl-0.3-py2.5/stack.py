# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/owyl/stack.py
# Compiled at: 2009-01-15 23:41:43
"""stack -- stack implementation for owyl

Copyright 2008 David Eyk. All rights reserved.

$Author: david.eyk $

$Rev: 27 $

$Date: 2009-01-07 13:46:38 -0600 (Wed, 07 Jan 2009) $
"""
__author__ = '$Author: david.eyk $'[9:-2]
__revision__ = '$Rev: 27 $'[6:-2]
__date__ = '$Date: 2009-01-07 13:46:38 -0600 (Wed, 07 Jan 2009) $'[7:-2]
__all__ = ('EmptyError Stack').split()
EmptyError = IndexError

class Stack(list):
    """A list with a push method.
    """
    push = list.append