# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/owyl/blackboard.py
# Compiled at: 2009-01-15 23:41:43
"""blackboard -- basic blackboard behaviors for Owyl

Copyright 2008 David Eyk. All rights reserved.

$Author: david.eyk $

$Rev: 30 $

$Date: 2009-01-08 07:39:11 -0600 (Thu, 08 Jan 2009) $
"""
__author__ = '$Author: david.eyk $'[9:-2]
__revision__ = '$Rev: 30 $'[6:-2]
__date__ = '$Date: 2009-01-08 07:39:11 -0600 (Thu, 08 Jan 2009) $'[7:-2]
from collections import defaultdict
import core
__all__ = [
 'checkBB', 'setBB']

class Blackboard(defaultdict):
    """A dict that defaults values to None.
    """

    def __init__(self, **kwargs):
        default = lambda : None
        super(Blackboard, self).__init__(default, **kwargs)


@core.task
def checkBB(**kwargs):
    """Check a value on the blackboard.

    @keyword blackboard: The blackboard object.

    @keyword key: The name of a key on the blackboard.
    @type key: A hashable object

    @keyword check: A function that takes the value on the blackboard
                    and returns a boolean.
    """
    bb = kwargs['blackboard']
    key = kwargs['key']
    check = kwargs.get('check', lambda x: x is not None)
    value = bb[key]
    result = check(value) and True or False
    yield result


@core.task
def setBB(**kwargs):
    """Set a value on the blackboard.

    @keyword blackboard: The blackboard object.

    @keyword key: The name of a key on the blackboard.
    @type key: A hashable object

    @keyword value: The value to set on the key.
    """
    bb = kwargs['blackboard']
    key = kwargs['key']
    value = kwargs['value']
    bb[key] = value
    yield True