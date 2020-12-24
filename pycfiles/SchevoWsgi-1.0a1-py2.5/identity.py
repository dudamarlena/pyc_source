# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevowsgi/identity.py
# Compiled at: 2008-01-19 12:48:17
"""Schevo identity middleware.

For copyright, license, and warranty, see bottom of file.
"""

def schevo_authfunc(db_name='schevo.db', extent_name='SchevoIdUser', name_field='name', password_field='password'):
    """Return an authentication function for use as the ``authfunc``
    when using `paste.auth` middleware."""

    def authfunc(username, password, environ):
        print environ
        db = environ[db_name]
        print '   db', db
        extent = db.extent(extent_name)
        print '   extent', extent
        criteria = {name_field: username, password_field: password}
        print '   criteria', criteria
        user = extent.findone(**criteria)
        print '   user', user
        return user is not None

    return authfunc


class RemoteUserDereferencer(object):
    """If a username exists in the WSGI environ, dereference it to an
    entity."""

    def __init__(self, app, remote_user_name='REMOTE_USER', dereferenced_name='REMOTE_USER.entity', db_name='schevo.db', extent_name='SchevoIdUser', name_field='name'):
        self._app = app
        self._remote_user_name = remote_user_name
        self._dereferenced_name = dereferenced_name
        self._db_name = db_name
        self._extent_name = extent_name
        self._name_field = name_field

    def __call__(self, environ, start_response):
        db = environ[self._db_name]
        name = environ.get(self._remote_user_name, None)
        if name is not None:
            extent = db.extent(self._extent_name)
            criteria = {self._name_field: name}
            user = extent.findone(**criteria)
            environ[self._dereferenced_name] = user
        return self._app(environ, start_response)