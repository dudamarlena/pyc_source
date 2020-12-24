# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/utils/users.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import unicode_literals
import logging, sys
from six.moves import range
from rbtools.api.errors import AuthorizationError
from rbtools.utils.console import get_input, get_pass

def get_authenticated_session(api_client, api_root, auth_required=False, session=None, num_retries=3):
    """Return an authenticated session.

    None will be returned if the user is not authenticated, unless the
    'auth_required' parameter is True, in which case the user will be prompted
    to login.
    """
    if not session:
        session = api_root.get_session(expand=b'user')
    if not session.authenticated:
        if not auth_required:
            return
        if not sys.stdin.isatty():
            logging.error(b'Authentication is required but input is not a tty.')
            if sys.platform == b'win32':
                logging.info(b'Check that you are not running this script from a Cygwin terminal emulator (or use Cygwin Python to run it).')
            raise AuthorizationError(http_status=None, error_code=None)
        logging.info(b'Please log in to the Review Board server at %s', api_client.domain)
        for i in range(num_retries + 1):
            username = get_input(b'Username: ', require=True)
            password = get_pass(b'Password: ', require=True)
            api_client.login(username, password)
            try:
                session = session.get_self()
                break
            except AuthorizationError:
                sys.stderr.write(b'\n')
                if i == num_retries:
                    raise
                logging.error(b'The username or password was incorrect. Please try again.')

    return session


def get_user(api_client, api_root, auth_required=False):
    """Return the user resource for the current session."""
    session = get_authenticated_session(api_client, api_root, auth_required)
    if session:
        return session.user
    else:
        return


def get_username(api_client, api_root, auth_required=False):
    """Return the username for the current session."""
    user = get_user(api_client, api_root, auth_required)
    if user:
        return user.username
    else:
        return