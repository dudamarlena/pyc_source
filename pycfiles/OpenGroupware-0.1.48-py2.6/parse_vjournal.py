# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/icalendar/parse_vjournal.py
# Compiled at: 2012-10-12 07:02:39
import datetime, re, vobject
from dateutil.tz import gettz

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


def parse_vjournal(memo, ctx, log, **params):
    utc_tz = gettz('UTC')
    values = {}
    for line in memo.lines():
        if line.name == 'UID':
            keys = line.value.split('/')
            if keys[0] == 'coils:':
                if keys[(len(keys) - 1)].isdigit():
                    values['object_id'] = int(keys[(len(keys) - 1)])
        elif line.name == 'STATUS':
            pass
        elif line.name == 'ATTENDEE':
            pass
        elif line.name == 'SUMMARY':
            values['title'] = line.value
        elif line.name == 'DESCRIPTION':
            values['content'] = line.value
        elif line.name == 'CATEGORIES':
            values['category'] = (',').join(line.value)
        elif line.name == 'ORGANIZER':
            pass
        elif line.name == 'X-COILS-PROJECT-ID':
            if len(line.value) == 0 or line.value == '-':
                values['project_id'] = None
            elif line.value.isdigit():
                values['project_id'] = int(line.value)
        elif line.name == 'X-COILS-COMPANY-ID':
            if len(line.value) == 0 or line.value == '-':
                values['company_id'] = None
            elif line.value.isdigit():
                values['company_id'] = int(line.value)
        elif line.name == 'X-COILS-APPOINTMENT-ID':
            if len(line.value) == 0 or line.value == '-':
                values['date_id'] = None
            elif line.value.isdigit():
                values['appointment_id'] = int(line.value)

    if 'object_id' not in values:
        pass
    return [
     values]