# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/icalendar/parse_vtodo.py
# Compiled at: 2012-10-12 07:02:39
import datetime, re, hashlib, base64, vobject
from dateutil.tz import gettz

def hash_for_data(value_):
    hash_ = hashlib.sha512()
    hash_.update(value_)
    return hash_.hexdigest()


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
            log.warn(('Multiple contacts found for e-mail address {0}').format(email))
        else:
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
    pass


def parse_vtodo(event, ctx, log, starts=[], duration=None, **params):
    utc_tz = gettz('UTC')
    values = {}
    for line in event.lines():
        if line.name == 'UID':
            values['uid'] = line.value
        elif line.name == 'STATUS':
            if line.value == 'NEEDS-ACTION':
                values['status'] = '00_created'
            elif line.value == 'IN-PROCESS':
                values['status'] = '20_processing'
            elif line.value == 'CANCELLED':
                values['status'] = '02_rejected'
            elif line.value == 'COMPLETED':
                values['status'] = '25_done'
        elif line.name == 'ATTENDEE':
            pass
        elif line.name == 'SUMMARY':
            values['title'] = line.value
        elif line.name == 'DESCRIPTION':
            values['comment'] = line.value
        elif line.name == 'PERCENT-COMPLETE':
            if line.value.isdigit():
                values['complete'] = int(int(line.value) / 10 * 10)
        elif line.name == 'PRIORITY':
            if line.value == 'LOW':
                values['priority'] = 5
            elif line.value == 'MEDIUM':
                values['priority'] = 3
            elif line.value == 'HIGH':
                values['priority'] = 1
            elif line.value.isdigit():
                tmp = int(line.value)
                if tmp == 0 or tmp == 5:
                    values['priority'] = 3
                elif tmp < 5:
                    values['priority'] = 1
                elif tmp > 6:
                    values['priority'] = 5
                else:
                    raise CoilsException(('Illegal numeric PRIORTY value "{0}" in VTODO').format(line.value))
            else:
                raise CoilsException(('Illegal PRIORTY value "{0}" in VTODO').format(line.value))
        elif line.name == 'ATTACH':
            if line.params.get('VALUE', ['NOTBINARY'])[0] == 'BINARY' and line.params.get('ENCODING', ['NOTBASE64'])[0] == 'BASE64':
                if '_ATTACHMENTS' not in values:
                    values['_ATTACHMENTS'] = []
                for attr in ('X-EVOLUTION-CALDAV-ATTACHMENT-NAME', 'X-ORACLE-FILENAME',
                             'X-COILS-FILENAME'):
                    if attr in line.params:
                        name_ = line.params[attr][0]
                        break
                else:
                    name_ = None

                data_ = base64.decodestring(line.value)
                hash_ = hash_for_data(data_)
                size_ = len(data_)
                mime_ = line.params.get('FMTTYPE', ['application/octet-stream'])[0]
                values['_ATTACHMENTS'].append({'entityName': 'Attachment', 'sha512checksum': hash_, 
                   'data': data_, 
                   'name': name_, 
                   'mimetype': mime_, 
                   'size': size_})
            else:
                raise CoilsException('Unable to parse CalDAV ATTACH; not a binary attachment.')
        elif line.name == 'CATEGORIES':
            value = None
            if isinstance(line.value, list):
                if value:
                    value = line.value[0].strip()
                else:
                    value = ''
            elif isinstance(line.value, basestring):
                value = line.value.strip()
            if value:
                value = value.replace('\\,', ',')
                value = value.split(',')
                value = (',').join([ x.strip() for x in value ])
                values['category'] = value
        elif line.name == 'ORGANIZER':
            pass
        elif line.name == 'CLASS':
            if line.value == 'PUBLIC':
                values['sensitivity'] = 0
            elif line.value == 'PRIVATE':
                values['sensitivity'] = 2
            elif line.value == 'CONFIDENTIAL':
                values['sensitivity'] = 3
        elif line.name == 'DUE':
            if isinstance(line.value, datetime.date):
                values['end'] = line.value
            elif isinstance(line.value, datetime.datetime):
                values['end'] = line.value.locallize(utc_tz)
            else:
                raise CoilsException(('Illegal data type "{0}" in VTODO DUE').format(type(line.value)))
        elif line.name == 'DTSTART':
            if isinstance(line.value, datetime.date):
                values['start'] = line.value
            elif isinstance(line.value, datetime.datetime):
                values['start'] = line.value.locallize(utc_tz)
            else:
                raise CoilsException(('Illegal data type "{0}" in VTODO DTSTART').format(type(line.value)))
        elif line.name == 'X-COILS-OBJECT-ID':
            values['object_id'] = int(line.value)
        elif line.name == 'X-COILS-PROJECT':
            pass
        elif line.name == 'X-COILS-KIND':
            values['kind'] = line.value

    return [values]