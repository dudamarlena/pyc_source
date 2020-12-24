# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/threebean/devel/busmon/busmon/controllers/root.py
# Compiled at: 2012-10-11 12:19:29
__doc__ = 'Main Controller'
from tg import expose
from busmon.lib.base import BaseController
from busmon.controllers.error import ErrorController
from busmon.widgets import TopicsBarChart, MessagesTimeSeries, ColorizedMessagesWidget
__all__ = [
 'RootController']

class RootController(BaseController):
    error = ErrorController()

    @expose('busmon.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(barchart=TopicsBarChart, timeseries=MessagesTimeSeries(id='messages-time-series'), colorized_messages=ColorizedMessagesWidget)

    @expose('')
    def _heartbeat(self):
        """ A nice lightweight url for our proxies to check. """
        return 'I am ok.  Thanks for asking.'