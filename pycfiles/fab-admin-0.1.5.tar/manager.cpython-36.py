# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\opt\private\cw1427\fab-admin\fab_admin\addon\sse\manager.py
# Compiled at: 2020-02-10 10:00:48
# Size of source mod 2**32: 871 bytes
import logging
from flask_appbuilder.basemanager import BaseManager
from .views import SSEView
log = logging.getLogger(__name__)

class SSEManager(BaseManager):
    sse_view = SSEView

    def __init__(self, appbuilder):
        super(SSEManager, self).__init__(appbuilder)
        self.appbuilder.get_app.config.setdefault('SSE_KEY', 'sse')

    def register_views(self):
        """
            This method is called by AppBuilder when initializing, use it to add you views
        """
        self.appbuilder.add_view_no_menu(SSEView, 'SSEView')

    def pre_process(self):
        pass

    def post_process(self):
        pass