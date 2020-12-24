# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/rss/actionfeed.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from datetime import datetime
from xml.sax.saxutils import escape
from coils.net import RSSFeed

class ActionFeed(RSSFeed, PathObject):

    def __init__(self, parent, name, **params):
        PathObject.__init__(self, parent, **params)
        RSSFeed.__init__(self, parent, name, **params)
        self.metadata = {'feedUrl': self.get_path(), 'channelUrl': self.get_path(), 
           'channelTitle': 'Tasks', 
           'channelDescription': 'Tasks Feed Description'}

    def actions_query(self, limit=150):
        db = self.context.db_session()
        return []

    def get_items(self):
        query = getattr(self, ('{0}_query').format(self.name[:-4]))()
        for action in query.all():
            if action.task.project is None:
                project_name = 'n/a'
            else:
                project_name = action.task.project.name
            yield {'description': self.transcode_text(action.comment), 'title': 'title', 
               'date': action.date, 
               'author': action.actor_id, 
               'link': None, 
               'guid': 'xyz', 
               'object_id': action.object_id}

        return

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        try:
            object_id = int(name)
        except:
            self.no_such_path()
        else:
            entity = self.context.get_entity(object_id)
            if entity:
                if entity.__entityName__ == 'Team':
                    return TeamFeeds(self, name, entity=entity, request=self.request, context=self.context, parameters=self.parameters)

        self.no_such_path()