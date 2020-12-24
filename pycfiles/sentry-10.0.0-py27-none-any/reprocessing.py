# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/reprocessing.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import uuid
REPROCESSING_OPTION = 'sentry:processing-rev'

def get_reprocessing_revision(project, cached=True):
    """Returns the current revision of the projects reprocessing config set."""
    from sentry.models import ProjectOption, Project
    if cached:
        return ProjectOption.objects.get_value(project, REPROCESSING_OPTION)
    try:
        if isinstance(project, Project):
            project = project.id
        return ProjectOption.objects.get(project=project, key=REPROCESSING_OPTION).value
    except ProjectOption.DoesNotExist:
        pass


def bump_reprocessing_revision(project):
    """Bumps the reprocessing revision."""
    from sentry.models import ProjectOption
    rev = uuid.uuid4().hex
    ProjectOption.objects.set_value(project, REPROCESSING_OPTION, rev)
    return rev


def report_processing_issue(event_data, scope, object=None, type=None, data=None):
    """Reports a processing issue for a given scope and object.  Per
    scope/object combination only one issue can be recorded where the last
    one reported wins.
    """
    if object is None:
        object = '*'
    if type is None:
        from sentry.models import EventError
        type = EventError.INVALID_DATA
    uid = '%s:%s' % (scope, object)
    event_data.setdefault('processing_issues', {})[uid] = {'scope': scope, 
       'object': object, 
       'type': type, 
       'data': data}
    return


def resolve_processing_issue(project, scope, object=None, type=None):
    """Given a project, scope and object (and optionally a type) this marks
    affected processing issues are resolved and kicks off a task to move
    events back to reprocessing.
    """
    if object is None:
        object = '*'
    from sentry.models import ProcessingIssue
    ProcessingIssue.objects.resolve_processing_issue(project=project, scope=scope, object=object, type=type)
    return


def trigger_reprocessing(project):
    from sentry.tasks.reprocessing import reprocess_events
    reprocess_events.delay(project_id=project.id)