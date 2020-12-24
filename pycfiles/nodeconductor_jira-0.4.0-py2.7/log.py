# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_jira/log.py
# Compiled at: 2016-09-16 10:02:59
from nodeconductor.logging.loggers import EventLogger, event_logger
from .models import Issue, Comment

class IssueEventLogger(EventLogger):
    issue = Issue

    class Meta:
        event_types = ('issue_deletion_succeeded', 'issue_update_succeeded', 'issue_creation_succeeded')
        event_groups = {'jira': event_types}


class CommentEventLogger(EventLogger):
    comment = Comment

    class Meta:
        event_types = ('comment_deletion_succeeded', 'comment_update_succeeded', 'comment_creation_succeeded')
        event_groups = {'jira': event_types}


event_logger.register('jira_issue', IssueEventLogger)
event_logger.register('jira_comment', CommentEventLogger)