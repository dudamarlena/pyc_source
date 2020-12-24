# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/ed_thread.py
# Compiled at: 2011-04-10 13:31:51
"""
Implements and provides the interface for dispatching asynchronous jobs through
the Editra Threadpool.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: ed_thread.py 67397 2011-04-05 20:46:23Z CJP $'
__revision__ = '$Revision: 67397 $'
import wx, ebmlib

class EdThreadPool(ebmlib.ThreadPool):
    """Singleton ThreadPool"""
    __metaclass__ = ebmlib.Singleton

    def __init__(self):
        super(EdThreadPool, self).__init__(5)