# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/ximenez/actions/action.py
# Compiled at: 2007-11-10 08:06:38
"""Define ``Action`` abstract class.

$Id: action.py 8 2007-11-10 13:06:44Z damien.baty $
"""
from ximenez.input import InputAware

class Action(object, InputAware):
    """The purpose of action plug-ins is to... do things.

    ``Action`` is an abstract class which real action plug-ins must
    subclass.
    """
    __module__ = __name__

    def execute(self, sequence):
        """Execute an action on ``sequence`` (whose type of items
        depends on the collector being used).

        This method **must** be implemented.
        """
        raise NotImplementedError