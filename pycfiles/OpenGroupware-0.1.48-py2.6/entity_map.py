# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/foundation/entity_map.py
# Compiled at: 2012-10-12 07:02:39
ENTITYMAP = {'Contact': {'get-command': 'contact::get', 'data-command': 'object::get-as-ics', 
               'mime-type': 'text/x-vcard'}, 
   'Appointment': {'get-command': 'appointment::get', 'data-command': 'object::get-as-ics', 
                   'mime-type': 'text/calendar'}, 
   'Route': {'get-command': 'route::get', 'data-command': 'route::get-text', 
             'mime-type': 'text/xml'}, 
   'Message': {'get-command': 'message::get', 'data-command': 'message::get-text', 
               'mime-type': 'text/plain'}, 
   'Team': {'get-command': 'team::get', 'data-command': 'team::get-as-ics', 
            'mime-type': 'text/x-vcard'}, 
   'Document': {'get-command': 'document::get', 'data-command': 'document::get-handle', 
                'mime-type': 'application/octet-stream'}, 
   'note': {'get-command': 'note::get', 'data-command': 'object::get-as-ics', 
            'mime-type': 'text/calendar'}, 
   'Process': {'get-command': 'process::get', 'data-command': 'object::get-as-ics', 
               'mime-type': 'text/calendar'}, 
   'Task': {'get-command': 'task::get', 'data-command': 'task::get-as-ics', 
            'mime-type': 'text/calendar'}}