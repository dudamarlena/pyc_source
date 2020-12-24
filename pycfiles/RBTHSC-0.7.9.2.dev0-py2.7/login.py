# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\commands\login.py
# Compiled at: 2017-04-19 05:14:04
from __future__ import print_function, unicode_literals
import logging
from rbtools.commands import Command
from rbtools.utils.users import get_authenticated_session

class Login(Command):
    """Logs into a Review Board server.

    The user will be prompted for a username and password, unless otherwise
    passed on the command line, allowing the user to log in and save a
    session cookie without needing to be in a repository or posting to
    the server.

    If the user is already logged in, this won't do anything.
    """
    name = b'login'
    author = b'The Review Board Project'
    option_list = [
     Command.server_options]

    def main(self):
        """Run the command."""
        server_url = self.get_server_url(None, None)
        api_client, api_root = self.get_api(server_url)
        session = api_root.get_session(expand=b'user')
        was_authenticated = session.authenticated
        if not was_authenticated:
            session = get_authenticated_session(api_client, api_root, auth_required=True, session=session)
        if session.authenticated:
            if not was_authenticated or self.options.username and self.options.password:
                logging.info(b'Successfully logged in to Review Board.')
            else:
                logging.info(b'You are already logged in to Review Board at %s', api_client.domain)
        return