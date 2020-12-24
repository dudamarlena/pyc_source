# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/rss_feed.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from datetime import datetime
from xml.sax.saxutils import escape
from coils.net import RSSFeed

class TasksRSSFeed(RSSFeed):

    def __init__(self, parent, name, **params):
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


class ProjectTaskActionsRSSFeed(RSSFeed):

    def __init__(self, parent, name, project, **params):
        RSSFeed.__init__(self, parent, name, **params)
        self.project = project
        if self.project is None:
            self.metadata = {'channelTitle': ("Actions for user {0}'s projects").format(self.context.login), 'channelDescription': ''}
        else:
            self.metadata = {'channelTitle': ('Task actions for project {0}').format(self.project.name), 'channelDescription': ''}
        return

    def format_comment(self, action):
        if self.project is None:
            return ('{0}\n-----\n<STRONG>Project Name:</STRONG> {1}\n').format(escape(action.comment), action.task.project.name)
        else:
            return escape(action.comment)
            return

    def get_items(self):
        if self.project is None:
            results = self.context.run_command('project::get-task-actions')
        else:
            results = self.context.run_command('project::get-task-actions', id=self.project.object_id)
        for action in results:
            yield {'description': self.format_comment(action), 'title': ('{0} ({1} by {2})').format(action.task.name, action.action[3:], action.actor.login), 
               'date': action.date, 
               'author': ('{0} ({1}, {2})').format(action.actor.get_company_value_text('email1'), action.actor.last_name, action.actor.first_name), 
               'link': None, 
               'guid': ('OGo-TaskAction-{0}-todo').format(action.object_id), 
               'object_id': action.task.object_id}

        return


class ProjectDocumentChangesRSSFeed(RSSFeed):

    def __init__(self, parent, project_d, **params):
        RSSFeed.__init__(self, parent, **params)
        self.metadata = {'feedUrl': None, 'channelUrl': None, 
           'channelTitle': None, 
           'channelDescription': None}
        return

    def get_items(self):
        pass