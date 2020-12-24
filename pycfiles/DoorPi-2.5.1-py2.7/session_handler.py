# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/doorpi/status/webserver_lib/session_handler.py
# Compiled at: 2016-08-01 11:57:45
import logging
logger = logging.getLogger(__name__)
logger.debug('%s loaded', __name__)
import time
from doorpi.action.base import SingleAction
import doorpi
CONF_AREA_PREFIX = 'AREA_'

class SessionHandler:
    _Sessions = {}

    @property
    def config(self):
        return doorpi.DoorPi().config

    @property
    def session_ids(self):
        return self._Sessions.keys()

    @property
    def sessions(self):
        return self._Sessions

    def __init__(self):
        doorpi.DoorPi().event_handler.register_event('WebServerCreateNewSession', __name__)
        doorpi.DoorPi().event_handler.register_event('WebServerAuthUnknownUser', __name__)
        doorpi.DoorPi().event_handler.register_event('WebServerAuthWrongPassword', __name__)

    def destroy(self):
        doorpi.DoorPi().event_handler.unregister_source(__name__, True)

    __del__ = destroy

    def get_session(self, session_id):
        if session_id in self._Sessions:
            logger.trace('session %s found: %s', session_id, self._Sessions[session_id])
            return self._Sessions[session_id]
        else:
            logger.trace('no session with session id %s found', session_id)
            return
            return

    __call__ = get_session

    def exists_session(self, session_id):
        return session_id in self._Sessions

    def build_security_object(self, username, password, remote_client=''):
        if not len(self.config.get_keys('User')):
            self.config.set_value(section='User', key='door', value='pi', password=True)
            self.config.set_value(section='Group', key='administrator', value='door')
            self.config.set_value(section='WritePermission', key='administrator', value='installer')
            self.config.set_value(section='AREA_installer', key='.*', value='')
        groups_with_write_permissions = self.config.get_keys('WritePermission')
        groups_with_read_permissions = self.config.get_keys('ReadPermission')
        groups = self.config.get_keys('Group')
        users = self.config.get_keys('User')
        if username not in users:
            doorpi.DoorPi().event_handler('WebServerAuthUnknownUser', __name__, {'username': username, 
               'remote_client': remote_client})
            return None
        else:
            real_password = self.config.get('User', username, password=True)
            if real_password != password:
                doorpi.DoorPi().event_handler('WebServerAuthWrongPassword', __name__, {'username': username, 
                   'password': password, 
                   'remote_client': remote_client})
                return None
            web_session = dict(username=username, remote_client=remote_client, session_starttime=time.time(), readpermissions=[], writepermissions=[], groups=[])
            for group in groups:
                users_in_group = self.config.get_list('Group', group)
                if username in users_in_group:
                    web_session['groups'].append(group)

            for group in groups_with_read_permissions:
                if group in web_session['groups']:
                    modules = self.config.get_list('ReadPermission', group)
                    for modul in modules:
                        web_session['readpermissions'].extend(self.config.get_keys(CONF_AREA_PREFIX + modul))

            for group in groups_with_write_permissions:
                if group in web_session['groups']:
                    modules = self.config.get_list('WritePermission', group)
                    for modul in modules:
                        web_session['writepermissions'].extend(self.config.get_keys(CONF_AREA_PREFIX + modul))
                        web_session['readpermissions'].extend(self.config.get_keys(CONF_AREA_PREFIX + modul))

            web_session['readpermissions'] = list(set(web_session['readpermissions']))
            web_session['readpermissions'].sort()
            web_session['writepermissions'] = list(set(web_session['writepermissions']))
            web_session['writepermissions'].sort()
            doorpi.DoorPi().event_handler('WebServerCreateNewSession', __name__, {'session': web_session})
            self._Sessions[web_session['username']] = web_session
            return web_session