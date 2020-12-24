# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/streaming/browser/views.py
# Compiled at: 2009-09-14 10:15:09
from atreal.richfile.streaming.interfaces import IStreamable
from atreal.richfile.qualifier.common import RFView
from atreal.richfile.streaming import RichFileStreamingMessageFactory as _

class RFStreamingView(RFView):
    """
    """
    __module__ = __name__
    plugin_interface = IStreamable
    kss_id = 'streaming'
    viewlet_name = 'atreal.richfile.streaming.flowplayer'
    update_message = _('The streaming has been updated.')
    active_message = _('Streaming activated.')
    unactive_message = _('Streaming un-activated.')