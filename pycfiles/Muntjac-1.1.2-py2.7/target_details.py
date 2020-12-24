# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/event/dd/target_details.py
# Compiled at: 2013-04-04 15:36:37
"""wraps drop target related information about DragAndDropEvent."""

class ITargetDetails(object):
    """ITargetDetails wraps drop target related information about
    L{DragAndDropEvent}.

    When a ITargetDetails object is used in L{DropHandler} it is often
    preferable to cast the ITargetDetails to an implementation provided by
    DropTarget like L{TreeTargetDetails}. They often provide a better typed,
    drop target specific API.
    """

    def getData(self, key):
        """Gets target data associated with the given string key

        @return: The data associated with the key
        """
        raise NotImplementedError

    def getTarget(self):
        """@return: the drop target on which the L{DragAndDropEvent}
        happened."""
        raise NotImplementedError