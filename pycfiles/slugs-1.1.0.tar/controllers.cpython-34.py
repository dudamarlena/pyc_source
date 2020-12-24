# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/peter/slugs/slugs/controllers.py
# Compiled at: 2018-03-12 11:15:11
# Size of source mod 2**32: 6243 bytes
import cherrypy, threading

def synchronize(f):

    def decorator(self, *args, **kwargs):
        with self._lock:
            return f(self, *args, **kwargs)

    return decorator


class MainController(object):

    def __init__(self):
        self._lock = threading.RLock()
        self._users = UsersController()
        self._groups = GroupsController()

    @synchronize
    def update(self, data=None):
        self._users.update(data)
        self._groups.update(data)

    @synchronize
    def _cp_dispatch(self, vpath):
        length = len(vpath)
        controller = self
        if length >= 1:
            arg = vpath.pop(0)
            if arg == 'users':
                controller = self._users
            else:
                if arg == 'groups':
                    controller = self._groups
                else:
                    raise cherrypy.HTTPError(404, 'Collection not found.')
        if length >= 2:
            if controller == self._users:
                cherrypy.request.params['user'] = vpath.pop(0)
            else:
                cherrypy.request.params['group'] = vpath.pop(0)
        if length >= 3:
            arg = vpath.pop(0)
            if controller == self._users:
                if arg != 'groups':
                    raise cherrypy.HTTPError(404, 'User attribute not found.')
                else:
                    cherrypy.request.params['groups'] = True
            else:
                if arg != 'users':
                    raise cherrypy.HTTPError(404, 'Group attribute not found.')
                else:
                    cherrypy.request.params['users'] = True
        if length >= 4:
            if controller == self._users:
                cherrypy.request.params['group'] = vpath.pop(0)
            else:
                cherrypy.request.params['user'] = vpath.pop(0)
        if length >= 5:
            raise cherrypy.HTTPError(404, 'Resource not found.')
        return controller

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @synchronize
    def index(self):
        return {'users': self._users.list(), 
         'groups': self._groups.list()}


class UsersController(object):

    def __init__(self, user_group_mapping=None):
        self.mapping = {}
        self.update(user_group_mapping)

    def update(self, user_group_mapping=None):
        mapping = {}
        if user_group_mapping:
            for user_group in user_group_mapping:
                user_groups = mapping.get(user_group[0], [])
                user_groups.append(user_group[1])
                mapping.update([(user_group[0], user_groups)])

            for user in mapping.keys():
                user_groups = mapping.get(user)
                mapping.update([(user, list(set(user_groups)))])

        self.mapping = mapping

    def list(self):
        return list(self.mapping.keys())

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, user=None, groups=False, group=None):
        if user is not None:
            if user in self.mapping.keys():
                if groups:
                    user_groups = self.mapping.get(user)
                    if group is not None:
                        if group in user_groups:
                            return
                        raise cherrypy.HTTPError(404, 'Group not found.')
                    else:
                        return {'groups': user_groups}
                else:
                    return
            else:
                raise cherrypy.HTTPError(404, 'User not found.')
        else:
            return {'users': list(self.mapping.keys())}


class GroupsController(object):

    def __init__(self, user_group_mapping=None):
        self.mapping = {}
        self.update(user_group_mapping)

    def update(self, user_group_mapping=None):
        mapping = {}
        if user_group_mapping:
            for user_group in user_group_mapping:
                user_groups = mapping.get(user_group[1], [])
                user_groups.append(user_group[0])
                mapping.update([(user_group[1], user_groups)])

            for group in mapping.keys():
                group_users = mapping.get(group)
                mapping.update([(group, list(set(group_users)))])

        self.mapping = mapping

    def list(self):
        return list(self.mapping.keys())

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, group=None, users=False, user=None):
        if group:
            if group in self.mapping.keys():
                if users:
                    group_users = self.mapping.get(group)
                    if user:
                        if user in group_users:
                            return
                        raise cherrypy.HTTPError(404, 'User not found.')
                    else:
                        return {'users': group_users}
                else:
                    return
            else:
                raise cherrypy.HTTPError(404, 'Group not found.')
        else:
            return {'groups': list(self.mapping.keys())}