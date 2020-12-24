# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/berrymq/adapter/wxpython.py
# Compiled at: 2009-11-07 07:20:53
import wx, wx.lib.newevent, berrymq
(BerryMQEvent, EVT_BERRYMQ_MSG) = wx.lib.newevent.NewEvent()

class wxPythonAdapter(object):
    __module__ = __name__

    def __init__(self, window, id_filter):
        self.window = window
        berrymq.regist_method(id_filter, self.listener)
        print 'wxPythonAdapter, %s' % id_filter

    def listener(self, message):
        print message.id
        event = BerryMQEvent(id=message.id, args=message.args, kwargs=message.kwargs)
        wx.PostEvent(self.window, event)