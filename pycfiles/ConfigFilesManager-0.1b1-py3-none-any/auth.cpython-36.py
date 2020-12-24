# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/configfiles/auth.py
# Compiled at: 2018-11-05 09:00:56
# Size of source mod 2**32: 3523 bytes
__doc__ = '\nUtilities for authentication\n'
import getpass
from paramiko.agent import Agent
from paramiko.ssh_exception import AuthenticationException, BadAuthenticationType, ChannelException, SSHException

def interpret_urlish(url: str):
    """
    Interpret the server urlishes (so-called due to their non-conformance with traditional urls)

    Formatted like this:

    [username@]some.server.with.a.dns.name:some/path/yipee

    Returns an array of [username (defaults to logged in user), servername, path]
    """
    if '@' in url:
        if url.index('@') < url.index(':'):
            username, *url = url.split('@')
            url = ''.join(url)
    else:
        username = getpass.getuser()
    servername, *url = url.split(':')
    path = ''.join(url)
    return [
     username, servername, path]


use_public_key = True
use_password = True
use_interactive = True
guessed_username = ''
guessed_password = ''

def interpret_authentication_params(urlish, username, password, no_interactive):
    """
    Interpret parameters passed in to guess authentication parameters. Any can be none.

    If no method works, fall back to interactive auth
    """
    global guessed_password
    global guessed_username
    global use_interactive
    global use_password
    if urlish:
        if not username:
            guessed_username, *_ = interpret_urlish(urlish)
    else:
        if username:
            guessed_username = username
        else:
            guessed_username = getpass.getuser()
        if password:
            use_public_key = False
            guessed_password = password
        else:
            use_password = False
    if no_interactive:
        use_interactive = False


def authenticate_transport(transport):
    """
    Authenticate the transport with the current authentication parameters.

    Raises AuthenticationException if the authentication failed
    """
    global guessed_password
    global use_password
    global use_public_key
    if use_password:
        if not use_public_key:
            try:
                transport.auth_password(guessed_username, guessed_password)
            except (BadAuthenticationType, AuthenticationException):
                use_password = False

            if transport.is_authenticated():
                return
        else:
            if use_public_key or not use_password:
                agent = Agent()
                keys = agent.get_keys()
                if keys:
                    key = keys[0]
                    try:
                        try:
                            transport.auth_publickey(guessed_username, key)
                        except (BadAuthenticationType, AuthenticationException):
                            use_public_key = False

                    finally:
                        agent.close()

                else:
                    use_public_key = False
                    agent.close()
        if transport.is_authenticated():
            return
    else:
        if use_interactive:

            def interactive_handler(title, instruct, prompts):
                return [input(x) if y else getpass.getpass(x) for x, y in prompts]

            try:
                transport.auth_interactive(guessed_username, interactive_handler)
            except BadAuthenticationType:
                guessed_password = getpass.getpass('Password for remote: ')
                transport.auth_password(guessed_username, guessed_password)
                use_password = True
                use_public_key = False

        if transport.is_authenticated():
            return
    raise AuthenticationException('could not authenticate with any of the methods')