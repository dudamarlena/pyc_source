# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/icalendar/parse_vevent.py
# Compiled at: 2012-10-12 07:02:39
import datetime, re, uuid, vobject
from dateutil.tz import gettz
from copy import deepcopy
from datetime import date, datetime, timedelta

def take_integer_value(values, key, name, vevent, default=None):
    key = key.replace('-', '_')
    if hasattr(vevent.key):
        try:
            values[name] = int(getattr(vevent, key).value)
        except:
            values[name] = default


def take_string_value(values, key, name, vevent, default=None):
    key = key.replace('-', '_')
    if hasattr(vevent.key):
        try:
            values[name] = str(getattr(vevent, key).value)
        except:
            values[name] = default


def find_attendee(ctx, email, log):
    if len(email.strip()) < 6:
        return
    else:
        contacts = ctx.run_command('contact::get', email=email)
        if len(contacts) == 1:
            contact_id = contacts[0].object_id
            log.debug(('Found contact objectId#{0} for e-mail address {1}').format(contact_id, email))
            return contact_id
        if len(contacts) > 1:
            contact_id = None
            log.warn(('Multiple contacts found for e-mail address {0}').format(email))
            for contact in contacts:
                if contact.is_account == 1:
                    log.warn(('Selected objectId#{0} due to account status.').format(contact.object_id))
                    contact_id = contact.object_id
                    break
            else:
                log.warn('Returning arbitrary matching contact.')
                contact_id = contacts[0].object_id

            return contact_id
        log.warn(('No contact found for e-mail address {0}').format(email))
        teams = ctx.run_command('team::get', email=email)
        if teams:
            if len(teams) > 1:
                log.warn(('Multiple teams found for e-mail address {0}').format(email))
            return teams[0].object_id
        resources = ctx.run_command('resource::get', email=email)
        if resources:
            if len(resources) > 1:
                log.warn(('Multiple resources found for e-mail address {0}').format(email))
            return resources[0].object_id
        return


def parse_attendee(line, ctx, log):
    """
    {u'attendee': [<ATTENDEE{u'X-COILS-PARTICIPANT-ID': [u'27190'],
                             u'CUTYPE': [u'INDIVIDUAL'],
                             u'ROLE': [u'REQ-PARTICIPANT'],
                             u'PARTSTAT': [u'NEEDS-ACTION'],
                             u'RSVP': [u'TRUE']}
                             CN:SVZ:MAILTO=steve@morrison-ind.com>,
    """
    participant = {}
    if 'ROLE' in line.params:
        participant['participant_role'] = line.params['ROLE'][0]
    if 'PARTSTAT' in line.params:
        participant['participant_status'] = line.params['PARTSTAT'][0]
    if 'COMMENT' in line.params:
        participant['comment'] = line.params['COMMENT'][0]
    if 'RSVP' in line.params:
        if line.params['RSVP'][0] in ('YES', 'TRUE', '1', 'yes', 'true'):
            participant['rsvp'] = 1
        else:
            participant['rsvp'] = 0
    if 'X-COILS-PARTICIPANT-ID' in line.params:
        object_id = line.params['X-COILS-PARTICIPANT-ID'][0]
        if object_id.isdigit():
            participant['participant_id'] = int(object_id)
    if 'participant_id' not in participant:
        log.debug(('No particpant id parameter in ATTENDEE attribute with value "{0}"').format(line.value))
        object_ids = re.findall('=OGo([0-9]*)[-:@]+', line.value)
        for object_id in object_ids:
            if object_id.isdigit():
                log.debug(('Found OGo#{0} embedded in ATTENDEE').format(object_id))
                participant['participant_id'] = int(object_ids[0])
                break
        else:
            emails = re.findall('MAILTO[:=]*([A-z@0-9-_+.]*)[;:= ]*', line.value)
            for email in emails:
                log.debug(('** Found email {0} embedded in ATTENDEE').format(email))
                participant_id = find_attendee(ctx, email, log)
                if participant_id is not None:
                    participant['participant_id'] = participant_id
                    break
            else:
                log.debug('Unable to match ATTENDEE to an existing entity.')
    if 'participant_id' not in participant:
        return
    else:
        return participant


def parse_vevent(event, ctx, log, calendar=None, starts=[], duration=None, timezone=None, all_day=None):
    utc_tz = gettz('UTC')
    values = {'_PROPERTIES': []}
    for line in event.lines():
        if line.name == 'UID':
            if line.value.isdigit():
                values['object_id'] = int(line.value)
            else:
                values['caldav_uid'] = line.value
        elif line.name == 'STATUS':
            pass
        elif line.name == 'X-COILS-CONFLICT-DISABLE':
            if line.value == 'TRUE':
                values['conflict_disable'] = 1
            else:
                values['conflict_disable'] = 0
        elif line.name == 'ATTENDEE':
            if 'participants' not in values:
                values['participants'] = []
            participant = parse_attendee(line, ctx, log)
            if participant is not None:
                values['participants'].append(participant)
        elif line.name == 'TRANSP':
            values['fb_type'] = line.value.upper()
        elif line.name == 'DTSTAMP':
            pass
        elif line.name == 'SUMMARY':
            values['title'] = line.value
        elif line.name == 'LOCATION':
            values['location'] = line.value
        elif line.name == 'X-MICROSOFT-CDO-BUSYSTATUS':
            if 'fb_type' in values:
                pass
            elif line.value == 'FREE':
                values['fb_type'] = 'TRANSPARENT'
            else:
                values['fb_type'] = 'OPAQUE'
        elif line.name == 'X-COILS-READ-ACCESS':
            object_ids = []
            for object_id in line.value.split(','):
                if object_id.isdigit():
                    object_ids.append(int(object_id))

        elif line.name == 'PRIORITY':
            if line.value.isdigit():
                values['priority'] = int(line.value)
        elif line.name == 'X-MICROSOFT-CDO-IMPORTANCE':
            if 'priority' in values:
                pass
            else:
                value = int(line.value)
        elif line.name == 'X-MICROSOFT-CDO-INSTTYPE':
            pass
        elif line.name == 'ORGANIZER':
            pass
        elif line.name == 'CLASS':
            sensitivity = line.value.upper().strip()
            if sensitivity == 'PUBLIC':
                sensitivity = 0
            elif sensitivity == 'PRIVATE':
                sensitivity = 2
            elif sensitivity == 'CONFIDENTIAL':
                sensitivity = 3
            else:
                sensitivity = 0
            values['sensitivity'] = sensitivity
        elif line.name == 'X-COILS-APPOINTMENT-KIND':
            values['kind'] = line.value.lower()
        elif line.name == 'X-COILS-OBJECT-ID':
            try:
                x = int(line.value.strip())
            except:
                pass
            else:
                values['objectId'] = x
        elif line.name == 'DESCRIPTION':
            values['comment'] = line.value
        elif line.name == 'X-COILS-CONFLICT-DISABLE':
            if line.value == 'TRUE':
                values['conflict_disable'] = 1
            else:
                values['conflict_disable'] = 0
        elif line.name == 'X-COILS-POST-DURATION':
            if line.value.isdigit():
                values['post_duration'] = int(line.value)
        elif line.name == 'X-COILS-PRIOR-DURATION':
            if line.value.isdigit():
                values['pre_duration'] = int(line.value)
        elif line.name == 'CATEGORIES':
            values['categories'] = (',').join(line.value)
        elif line.name == 'X-COILS-WRITE-ACCESS':
            pass
        elif line.name in ('X-MICROSOFT-CDO-ALLDAYEVENT', 'X-FUNAMBOL-ALLDAY'):
            pass
        elif line.name == 'ATTACH':
            name = None
            for name_param in 'X-EVOLUTION-CALDAV-ATTACHMENT-NAME':
                if name_param in line.params:
                    name = line.params[name_param][0]
                    break

            if name is None:
                name = ('{0}.data').format(uuid.uuid4())
            if 'BINARY' in line.params.get('VALUE', []):
                if 'BASE64' in line.params.get('ENCODING', []):
                    pass
            else:
                raise CoilsException('Unsupported iCalendar attachment type encountered')
            parameters = {}
            for param in line.params:
                parameters[param] = line.params[param]

            log.debug(('Found attachment with parameters of: {0}').format(parameters))
        elif line.name.startswith('X-'):
            values['_PROPERTIES'].append({'namespace': 'http://www.opengroupware.us/ics', 'attribute': line.name.lower(), 
               'value': line.value})
        elif line.name in ('DTSTART', 'DTEND', 'CREATED', 'LAST-MODIFIED'):
            pass
        else:
            log.debug(('VEVENT attribute "{0}" with value of "{1}" discarded').format(line.name, line.value))

    if 'calendar' is not None:
        values['calendar_name'] = calendar
    if 'object_id' not in values:
        pass
    result = []
    for start in starts:
        appointment = deepcopy(values)
        if isinstance(start, datetime):
            appointment['start'] = start.astimezone(utc_tz)
            appointment['end'] = start.astimezone(utc_tz) + duration
            appointment['timezone'] = timezone
            appointment['isallday'] = 'NO'
        else:
            appointment['start'] = start
            appointment['end'] = start + duration
            appointment['timezone'] = 'UTC'
            appointment['isallday'] = 'YES'
        result.append(appointment)

    return result