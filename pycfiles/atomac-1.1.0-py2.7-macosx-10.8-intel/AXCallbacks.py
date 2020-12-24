# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/AXCallbacks.py
# Compiled at: 2012-08-03 19:46:40


def elemDisappearedCallback(retelem, obj, **kwargs):
    """ Callback for checking if a UI element is no longer onscreen

       kwargs should contains some unique set of identifier (e.g. title /
       value, role)
       Returns:  Boolean
   """
    return not obj.findFirstR(**kwargs)


def returnElemCallback(retelem):
    """ Callback for when a sheet appears

       Returns: element returned by observer callback
   """
    return retelem