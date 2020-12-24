# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/accountsmanager/accountshandler.py
# Compiled at: 2020-05-10 06:49:25
# Size of source mod 2**32: 4511 bytes
"""Exposes a RESTful interface ."""
import empower_core.apimanager.apimanager as apimanager

class AccountsHandler(apimanager.APIHandler):
    __doc__ = 'All the accounts defined in the controller.'
    URLS = [
     '/api/v1/accounts/?',
     '/api/v1/accounts/([a-zA-Z0-9:.]*)/?']

    @apimanager.validate(max_args=1)
    def get(self, *args, **kwargs):
        """List the accounts.

        Args:

            [0]: the username

        Example URLs:

            GET /api/v1/accounts

            [
                {
                    "email": "admin@empower.it",
                    "name": "admin",
                    "username": "root"
                },
                {
                    "email": "foo@empower.it",
                    "name": "Foo",
                    "username": "foo"
                },
                {
                    "email": "bar@empower.it",
                    "name": "Bar",
                    "username": "bar"
                }
            ]

            GET /api/v1/accounts/root

            {
                "email": "admin@empower.it",
                "name": "admin",
                "username": "root"
            }
        """
        if not args:
            return self.service.accounts
        return self.service.accounts[args[0]]

    @apimanager.validate(returncode=201)
    def post(self, *args, **kwargs):
        """Create a new account.

        Request:

            version: protocol version (1.0)
            username: username (mandatory)
            password: password (mandatory)
            name: name (mandatory)
            email: email (mandatory)

        Example URLs:

            POST /api/v1/accounts

            {
              "version" : 1.0,
              "username" : "foo",
              "password" : "foo",
              "name" : "foo",
              "email" : "foo@empower.io"
            }
        """
        self.service.create(username=(kwargs['username']), password=(kwargs['password']),
          name=(kwargs['name']),
          email=(kwargs['email']))

    @apimanager.validate(returncode=204, min_args=1, max_args=1)
    def put(self, *args, **kwargs):
        """Update an account.

        Args:

            [0]: the username

        Request:

            version: protocol version (1.0)
            name: name (mandatory)
            email: email (mandatory)
            password: password (optional)
            new_password: new_password (optional)
            new_password_confirm: new_password_confirm (optional)

        Example URLs:

            PUT /api/v1/accounts/test

            {
              "version" : 1.0,
              "name" : "foo",
              "email" : "foo@empowr.io",
              "new_password" : "new",
              "new_password_confirm" : "new",
            }

            PUT /api/v1/accounts/test

            {
              "version" : 1.0,
              "name" : "foo",
              "email" : "foo@empowr.io",
            }
        """
        username = args[0]
        password = None
        name = kwargs['name'] if 'name' in kwargs else None
        email = kwargs['email'] if 'email' in kwargs else None
        if 'new_password' in kwargs:
            if 'new_password_confirm' in kwargs:
                if kwargs['new_password'] != kwargs['new_password_confirm']:
                    raise ValueError('Passwords do not match')
                password = kwargs['new_password']
        self.service.update(username=username, password=password, name=name, email=email)

    @apimanager.validate(returncode=204, min_args=1, max_args=1)
    def delete(self, *args, **kwargs):
        """Delete an account.

        Args:

            [0]: the username

        Example URLs:

            DELETE /api/v1/accounts/foo
        """
        self.service.remove(args[0])