# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/rss/teamfeed.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from datetime import datetime
from xml.sax.saxutils import escape
from actionfeed import ActionFeed

class TeamFeed(PathObject):

    def __init__(self, parent, name, **params):
        PathObject.__init__(self, parent, **params)

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if name == 'actions.rss':
            return ActionFeed(self, name, entity=self.entity, request=self.request, context=self.context, parameters=self.parameters)
        self.no_such_path()