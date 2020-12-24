# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/omphalos/render_appointment.py
# Compiled at: 2012-10-12 07:02:39
from render_object import *

def render_participants(entity, ctx):
    """
        [{'entityName': 'participant',
          'firstName': 'Adam',
          'lastname': 'Williams',
          'objectId': 11920,
          'participantEntityName': 'Contact',
          'participantObjectId': 10160,
          'role': 'REQ-PARTICIPANT'}]
    """
    result = []
    tm = ctx.type_manager
    for participant in entity.participants:
        kind = tm.get_type(participant.participant_id)
        if kind == 'Contact':
            contact = ctx.run_command('contact::get', id=participant.participant_id)
            if contact is not None:
                first_name = as_string(contact.first_name)
                last_name = as_string(contact.last_name)
            else:
                first_name = ''
                last_name = ''
            result.append({'entityName': 'participant', 'objectId': participant.object_id, 
               'firstName': first_name, 
               'lastName': last_name, 
               'comment': as_string(participant.comment), 
               'rsvp': as_integer(participant.rsvp), 
               'participantEntityName': 'Contact', 
               'participantObjectId': participant.participant_id, 
               'status': as_string(participant.participant_status), 
               'role': as_string(participant.participant_role)})
            contact = None
        elif kind == 'Team':
            team = ctx.run_command('team::get', id=participant.participant_id)
            if team is not None:
                name = team.name
            result.append({'entityName': 'participant', 'objectId': participant.object_id, 
               'name': as_string(name), 
               'comment': as_string(participant.comment), 
               'participantEntityName': 'Team', 
               'rsvp': as_integer(participant.rsvp), 
               'status': 'NEEDS-ACTION', 
               'participantObjectId': participant.participant_id, 
               'role': as_string(participant.participant_role)})
            team = None
        else:
            result.append({'entityName': 'participant', 'objectId': participant.object_id, 
               'participantEntityName': kind, 
               'comment': as_string(participant.comment), 
               'rsvp': as_integer(participant.rsvp), 
               'status': as_string(participant.participant_status), 
               'participantObjectId': participant.participant_id, 
               'role': participant.participant_role})

    return result


def render_conflicts(entity, ctx):
    """ {'appointmentObjectId': '496315',
         'conflictingEntityName': 'Resource',
         'conflictingObjectId': 470730,
         'entityName': 'appointmentConflict',
         'status': 'ACCEPTED'} """
    result = []
    tm = ctx.type_manager
    x = ctx.run_command('schedular::get-conflicts', appointment=entity)
    if x is not None:
        for appointment in x:
            for conflict in x[appointment]:
                if conflict.__entityName__ == 'participant':
                    conflict_id = conflict.participant_id
                    conflict_type = tm.get_type(conflict_id)
                    conflict_status = conflict.participant_status
                else:
                    conflict_id = 0
                    conflict_type = 'Resource'
                    conflict_status = ''
                result.append({'entityName': 'appointmentConflict', 'conflictingEntityName': conflict_type, 
                   'conflictingObjectId': conflict_id, 
                   'status': conflict_status, 
                   'appointmentObjectId': appointment.object_id})

    return result


def render_resource(entity, detail, ctx):
    """
        [{'category': 'Rooms',
          'email': '',
          'emailSubject': '',
          'entityName': 'Resource',
          'name': 'Grand Rapids South Conference Room',
          'notificationTime': 0,
          'objectId': 465950},
         {'category': 'IT Equipment',
          'email': 'cisstaff@morrison-ind.com',
          'emailSubject': 'OGoResource: Conference Phone',
          'entityName': 'Resource',
          'name': 'Conference Phone',
          'notificationTime': 0,
          'objectId': 465990}]
    """
    return render_object({'entityName': 'Resource', 'objectId': entity.object_id, 
       'category': as_string(entity.category), 
       'email': as_string(entity.email), 
       'emailSubject': as_string(entity.subject), 
       'name': as_string(entity.name), 
       'notificationTime': as_integer(entity.notification)}, entity, detail, ctx)


def render_appointment(entity, detail, ctx):
    """
        '_NOTES': [],
        '_OBJECTLINKS': [],
        '_PARTICIPANTS': [{'entityName': 'participant',
                           'firstName': 'Adam',
                           'lastname': 'Williams',
                           'objectId': 11920,
                           'participantEntityName': 'Contact',
                           'participantObjectId': 10160,
                           'role': 'REQ-PARTICIPANT'}],
         '_PROPERTIES': [],
         '_RESOURCES': [{'category': 'Rooms',
                         'email': '',
                         'emailSubject': '',
                         'entityName': 'Resource',
                         'name': 'Grand Rapids South Conference Room',
                         'notificationTime': 0,
                         'objectId': 465950},
                        {'category': 'IT Equipment',
                         'email': 'cisstaff@morrison-ind.com',
                         'emailSubject': 'OGoResource: Conference Phone',
                         'entityName': 'Resource',
                         'name': 'Conference Phone',
                         'notificationTime': 0,
                         'objectId': 465990}],
         'appointmentType': 'tradeshow',
         'comment': '',
         'end': <DateTime '20061220T17:00:00' at b79f7cac>,
         'entityName': 'Appointment',
         'keywords': '',
         'notification': 120,
         'location': 'Test',
         'objectId': 11900,
         'ownerObjectId': 10160,
         'readAccessTeamObjectId': 11530,
         'start': <DateTime '20061220T14:00:00' at b79f7d8c>,
         'title': 'Test',
         'version': 1,
         'postDuration': 50,
         'priorDuration': 15,
         'isConflictDisabled': 0,
         'writeAccessObjectIds': ['11530']
        """
    a = {'entityName': 'Appointment', 
       'objectId': entity.object_id, 
       'title': as_string(entity.title), 
       'appointmentType': as_string(entity.kind), 
       'comment': as_string(entity.comment), 
       'end': as_datetime(entity.end), 
       'keywords': as_string(entity.keywords), 
       'notification': as_integer(entity.notification), 
       'location': as_string(entity.location), 
       'ownerObjectId': as_integer(entity.owner_id), 
       'readAccessTeamObjectId': as_integer(entity.access_id), 
       'start': as_datetime(entity.start), 
       'version': as_integer(entity.version), 
       'isConflictDisabled': as_integer(entity.conflict_disable), 
       'writeAccessObjectIds': as_string(entity.write_ids), 
       'offsetTimeZone': as_string(ctx.get_timezone().zone), 
       'startOffset': as_integer(ctx.get_offset_from(entity.start)), 
       'endOffset': as_integer(ctx.get_offset_from(entity.end))}
    if detail & 8:
        a['_PARTICIPANTS'] = render_participants(entity, ctx)
        resources = ctx.run_command('resource::get', appointment=entity)
        a['_RESOURCES'] = []
        if resources is not None:
            for resource in resources:
                a['_RESOURCES'].append(render_resource(resource, 0, ctx))

    if detail & 64:
        a['_CONFLICTS'] = render_conflicts(entity, ctx)
    flags = []
    if entity.owner_id == ctx.account_id:
        flags.append('SELF')
    rights = ctx.access_manager.access_rights(entity)
    a['FLAGS'] = flags
    return render_object(a, entity, detail, ctx)