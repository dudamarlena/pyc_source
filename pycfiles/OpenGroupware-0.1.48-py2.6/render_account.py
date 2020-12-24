# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/omphalos/render_account.py
# Compiled at: 2012-10-12 07:02:39
from render_object import *
from render_contact import *
from render_timezone import *

def build_calendar_panel(defaults, ctx):
    ids = []
    for account in defaults.get('scheduler_panel_accounts', []):
        ids.append(int(account))

    for contact in defaults.get('scheduler_panel_persons', []):
        ids.append(int(contact))

    for team in defaults.get('scheduler_panel_teams', []):
        ids.append(int(team))

    if 'scheduler_panel_resourceNames' in defaults:
        resources = ctx.run_command('resource::get', names=defaults['scheduler_panel_resourceNames'])
        if resources is not None:
            for resource in resources:
                ids.append(resource.object_id)

    return ids


def render_account(entity, defaults, detail, ctx, favorite_ids=[]):
    if detail & 256:
        a = render_contact(entity, detail, ctx, favorite_ids=favorite_ids)
    else:
        a = {'objectId': entity.object_id, 'entityName': 'Account', 
           'version': entity.version, 
           'login': entity.login}
        if detail & 2:
            a['_OBJECTLINKS'] = render_object_links(entity, ctx)
        if detail & 16:
            a['_PROPERTIES'] = render_object_properties(entity, ctx)
    if 'timezone' in defaults:
        tz = render_timezone(defaults['timezone'], ctx)
        is_tz_set = 1
    else:
        tz = render_timezone('GMT', ctx)
        is_tz_set = 0
    if defaults.has_key('scheduler_ccForNotificationMails'):
        cc = defaults['scheduler_ccForNotificationMails']
    else:
        cc = None
    a['_DEFAULTS'] = {'entityName': 'defaults', 'accountObjectId': entity.object_id, 'calendarPanelObjectIds': build_calendar_panel(defaults, ctx), 
       'appointmentReadAccessTeam': 0, 
       'appointmentWriteAccess': [], 'notificationCC': as_string(cc), 
       'secondsFromGMT': as_integer(tz['offsetFromGMT']), 
       'isDST': as_integer(tz['isCurrentlyDST']), 
       'timeZone': as_string(tz['abbreviation']), 
       'timeZoneName': as_string(tz['description']), 
       'isTimeZoneSet': as_integer(is_tz_set)}
    return a