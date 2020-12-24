# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/yaco/applyfun/walker_funcs.py
# Compiled at: 2008-06-13 07:08:02
""" Use this module in combination with walker.py.
    Each function you define here and add to the functions dict,
    will be available as an option in the @@applyfun zope3 view.
"""
functions = {}

def list_children(ob, logger=None):
    """
    Example function to demonstrate the use of the httplogger.
    args:
    none
    """
    if logger:
        path = ('/').join(ob.getPhysicalPath())
        if 'menu' not in path:
            logger.log(path)
        else:
            logger.log(path, color='blue')


functions['List children'] = list_children