# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/omphalos/render_task.py
# Compiled at: 2012-10-12 07:02:39
import time
from coils.foundation import OGO_ROLE_HELPDESK
from render_object import *
TASK_ACTIONS = [
 {'state': set(['00_created', '20_processing']), 'rights': set(['w']), 
    'flags': set(['EXECUTOR', 'OWNER', 'CANDIDATE']), 
    'flag': 'DONE'},
 {'state': set(['00_created', '20_processing', '25_done']), 'flags': set(['OWNER']), 
    'rights': set(['w']), 
    'flag': 'ARCHIVE'},
 {'state': set(['25_done', '30_archived']), 'flags': set(['EXECUTOR', 'OWNER', 'CANDIDATE']), 
    'rights': set(['w']), 
    'flag': 'REACTIVATE'},
 {'state': set(['02_rejected']), 'flags': set(['OWNER', 'HELPDESK']), 
    'rights': set(['w']), 
    'flag': 'REACTIVATE'},
 {'state': set(['00_created']), 'rights': set(['w']), 
    'flags': set(['EXECUTOR', 'CANDIDATE']), 
    'flag': 'ACCEPT'},
 {'state': set(['00_created']), 'rights': set(['w']), 
    'flags': set(['EXECUTOR', 'CANDIDATE']), 
    'flag': 'REJECT'},
 {'state': set(['20_processing']), 'rights': set(['w']), 
    'flags': set(['EXECUTOR']), 
    'flag': 'REJECT'}]

def render_task_notations(entity):
    """
        {'comment': 'COMMENT COMMENT COMMENT',
         'actionDate': <DateTime u'20061205T11:58:44' at -484cd194>,
         'objectId': 38330,
         'entityName': 'taskNotation',
         'taskStatus': '00_created',
         'taskObjectId': 38320,
         'action': '00_created',
         'actorObjectId': 10120}
    """
    result = []
    for notation in entity.notes:
        result.append({'entityName': 'taskNotation', 'objectId': as_integer(notation.object_id), 
           'comment': as_string(notation.comment), 
           'taskStatus': as_string(notation.task_status), 
           'taskObjectId': as_integer(notation.task_id), 
           'actionDate': as_datetime(notation.action_date), 
           'action': as_string(notation.action), 
           'actorObjectId': as_integer(notation.actor_id)})

    return result


def render_task(entity, detail, ctx):
    """
    {'comment': 'COMMENT COMMENT COMMENT',
     'sensitivity': 2,
     'percentComplete': 40,
     'keywords': 'ZOGI',
     'category': '',
     'completionDate': '',
     'end': <DateTime '20070125T00:00:00' at 815416c>,
     '_OBJECTLINKS': [{'direction': 'from',
                       'objectId': '15990',
                       'entityName': 'objectLink',
                       'targetEntityName': 'Contact',
                       'targetObjectId': '10000',
                       'label': 'Object Link Label',
                       'type': 'generic'}],
     'objectId': 476660,
     'priority': 2,
     'start': <DateTime '20061231T00:00:00' at 815408c>,
     'version': 2,
     'accountingInfo': 'Accounting Info',
     '_PROPERTIES': [],
     'executantObjectId': 10160,
     'entityName': 'Task',
     'status': '20_processing',
     'creatorObjectId': 10160,
     'ownerObjectId': 54720,
     'associatedContacts': '',
     'associatedCompanies': '',
     'timerDate': '',
     'kilometers': '34',
     'totalWork': 75,
     '_NOTES': [],
     'isTeamJob': 0,
     'parentTaskObjectId': 11409747,
     'kind': '',
     'name': 'Updated ZOGI Task 5',
     'lastModified': '',
     'objectProjectId': '',
     'actualWork': 23,
     'graph': {'12339323': {'12677171': {},
                            '12710721': {},
                            '12710725': {},
                            '12736451': {},
                            '12739574': {},
                            '12751507': {'11409747': {'476660': {}},
                                         '4560420': {}},
                            '12757951': {}}},
     'notify': 1}
    """
    executor_type = ctx.type_manager.get_type(entity.executor_id)
    if executor_type == 'Team':
        is_team_job = 1
    else:
        is_team_job = 0
    task = {'entityName': 'Task', 'objectId': entity.object_id, 'version': as_integer(entity.version), 
       'comment': as_string(entity.comment), 
       'sensitivity': as_integer(entity.sensitivity), 
       'percentComplete': as_integer(entity.complete), 
       'keywords': as_string(entity.keywords), 
       'category': as_string(entity.category), 
       'completionDate': as_datetime(entity.completed), 
       'end': as_datetime(entity.end), 
       'start': as_datetime(entity.start), 
       'priority': as_integer(entity.priority), 
       'accountingInfo': as_string(entity.accounting), 
       'executantObjectId': as_integer(entity.executor_id), 
       'status': as_string(entity.state), 
       'creatorObjectId': as_integer(entity.creator_id), 
       'ownerObjectId': as_integer(entity.owner_id), 
       'associatedContacts': as_string(entity.associated_contacts), 
       'associatedCompanies': as_string(entity.associated_companies), 
       'timerDate': as_datetime(entity.timer), 
       'kilometers': as_integer(entity.travel), 
       'totalWork': as_integer(entity.total), 
       'isTeamJob': is_team_job, 
       'parentTaskObjectId': as_integer(entity.parent_id), 
       'kind': as_string(entity.kind), 
       'name': as_string(entity.name), 
       'objectProjectId': as_integer(entity.project_id), 
       'actualWork': as_integer(entity.actual)}
    if entity.modified:
        task['lastModified'] = int(time.mktime(entity.modified.timetuple()))
    else:
        task['lastModified'] = ''
    if task['priority'] < 1:
        task['priority'] = 1
    elif task['priority'] > 5:
        task['priority'] = 5
    if entity.project_id:
        project = entity.project
        if project:
            task['projectName'] = project.name
            task['projectNumber'] = project.number
    if detail & 128:
        task['graph'] = ctx.run_command('task::get-graph', object=entity)
    if detail & 1:
        task['_NOTES'] = render_task_notations(entity)
    flags = []
    rights = ctx.access_manager.access_rights(entity)
    if ctx.has_role(OGO_ROLE_HELPDESK):
        flags.append('HELPDESK')
    if 'w' in rights:
        flags.append('WRITE')
    else:
        flags.append('READONLY')
    if 'r' in rights:
        flags.append('READ')
    else:
        flags.append('VISIBLE')
    if 'd' in rights:
        flags.append('DELETE')
    if ctx.account_id == entity.owner_id:
        flags.append('OWNER')
    if ctx.account_id == entity.creator_id:
        flags.append('CREATOR')
    if ctx.account_id == entity.executor_id:
        flags.append('EXECUTOR')
    elif entity.executor_id in ctx.context_ids:
        flags.append('CANDIDATE')
    if entity.state in ('00_created', '20_processing'):
        now = ctx.get_utctime()
        if entity.start > now:
            flags.append('UPCOMING')
        elif entity.end < now:
            flags.append('OVERDUE')
    for action in TASK_ACTIONS:
        if action['rights'].intersection(rights) and action['flags'].intersection(flags) and entity.state in action['state']:
            if action['flag'] not in flags:
                flags.append(action['flag'])

    task['FLAGS'] = flags
    return render_object(task, entity, detail, ctx)