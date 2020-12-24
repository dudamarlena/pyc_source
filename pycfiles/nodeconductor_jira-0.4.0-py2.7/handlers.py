# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_jira/handlers.py
# Compiled at: 2016-09-16 10:02:59
from .executors import ProjectImportExecutor
from .log import event_logger
from .models import Issue

def import_project_issues(sender, instance, **kwargs):
    ProjectImportExecutor.execute(instance, updated_fields=None)
    return


def log_issue_save(sender, instance, created=False, **kwargs):
    if created or instance.state == Issue.States.CREATING:
        pass
    elif instance.tracker.previous('state') == Issue.States.CREATING and instance.state == Issue.States.OK:
        event_logger.jira_issue.info('Issue {issue_key} has been created.', event_type='issue_creation_succeeded', event_context={'issue': instance})
    else:
        event_logger.jira_issue.info('Issue {issue_key} has been updated.', event_type='issue_update_succeeded', event_context={'issue': instance})


def log_issue_delete(sender, instance, **kwargs):
    event_logger.jira_issue.info('Issue {issue_key} has been deleted.', event_type='issue_deletion_succeeded', event_context={'issue': instance})


def log_comment_save(sender, instance, created=False, **kwargs):
    if created:
        event_logger.jira_comment.info('Comment for issue {issue_key} has been created.', event_type='comment_creation_succeeded', event_context={'comment': instance})
    else:
        event_logger.jira_comment.info('Comment for issue {issue_key} has been updated.', event_type='comment_update_succeeded', event_context={'comment': instance})


def log_comment_delete(sender, instance, **kwargs):
    event_logger.jira_comment.info('Comment for issue {issue_key} has been deleted.', event_type='comment_deletion_succeeded', event_context={'comment': instance})