# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/create_route.py
# Compiled at: 2012-10-12 07:02:39
import shutil, StringIO
from uuid import uuid4
from coils.core import *
from coils.core.logic import CreateCommand
from keymap import COILS_ROUTE_KEYMAP
from utility import filename_for_route_markup

def default_markup(rid, name):
    action_uuid = str(uuid4())
    markup = StringIO.StringIO()
    markup.write('<?xml version="1.0" encoding="UTF-8"?>')
    markup.write(('<package targetNamespace="{0}">').format(name))
    markup.write(('<process id="{0}" persistent="false" name="{1}">').format(rid, name))
    markup.write(('<event activity="{0}" exclusive="false"/>').format(name))
    markup.write('<context atomic="true">')
    markup.write('</context>')
    markup.write(('<action name="{0}" id="{1}" extensionAttributes="{0}/{1}">').format(name, action_uuid))
    markup.write('<input property="InputMessage" formatter="StandardRaw"/>')
    markup.write('<output><source property="InputMessage"/></output>')
    markup.write('<attributes>')
    markup.write('<extension name="activityName">eventAction</extension>')
    markup.write('<extension name="isSavedInContext">true</extension>')
    markup.write('<extension name="description"/>')
    markup.write('</attributes>')
    markup.write('</action>')
    markup.write('</process>')
    markup.write('</package>')
    output = markup.getvalue()
    markup.close()
    return output


class CreateRoute(CreateCommand):
    __domain__ = 'route'
    __operation__ = 'new'

    def __init__(self):
        CreateCommand.__init__(self)

    def prepare(self, ctx, **params):
        self.keymap = COILS_ROUTE_KEYMAP
        self.entity = Route
        CreateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        CreateCommand.parse_parameters(self, **params)
        if 'markup' in params:
            self.values['markup'] = params['markup']
        elif 'filename' in params:
            handle = open(params['filename'], 'rb')
            self.values['markup'] = handle.read()
            handle.close()
        elif 'handle' in params:
            handle = params['handle']
            handle.seek(0)
            self.values['markup'] = handle.read()

    def save_route_markup(self):
        handle = BLOBManager.Create(filename_for_route_markup(self.obj), encoding='binary')
        handle.write(self.obj.get_markup())
        BLOBManager.Close(handle)

    def run(self, **params):
        CreateCommand.run(self, **params)
        if 'markup' in self.values:
            self.log.debug(('New route has {0} bytes of markup.').format(len(self.values['markup'])))
            self.obj.set_markup(self.values['markup'])
        else:
            self.log.warn('No markup specified for route')
            self.obj.set_markup(default_markup(self.obj.object_id, self.obj.name))
        self.save_route_markup()
        self.save()