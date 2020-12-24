# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/logout.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import print_function, unicode_literals
import logging
from rbtools.commands import Command

class Logout(Command):
    """Logs out of a Review Board server.

    The session cookie will be removed into from the .rbtools-cookies
    file. The next RBTools command you run will then prompt for credentials.
    """
    name = b'logout'
    author = b'The Review Board Project'
    option_list = [
     Command.server_options]

    def main(self):
        """Run the command."""
        server_url = self.get_server_url(None, None)
        api_client, api_root = self.get_api(server_url)
        session = api_root.get_session(expand=b'user')
        if session.authenticated:
            api_client.logout()
            logging.info(b'You are now logged out of Review Board at %s', api_client.domain)
        else:
            logging.info(b'You are already logged out of Review Board at %s', api_client.domain)
        return