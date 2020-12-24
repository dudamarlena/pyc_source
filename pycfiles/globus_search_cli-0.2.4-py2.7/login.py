# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus_search_cli/commands/login.py
# Compiled at: 2019-12-03 15:45:33
import platform, click
from globus_search_cli.config import SEARCH_AT_EXPIRES_OPTNAME, SEARCH_AT_OPTNAME, SEARCH_RT_OPTNAME, internal_auth_client, lookup_option, write_option
from globus_search_cli.printing import safeprint
SEARCH_ALL_SCOPE = 'urn:globus:auth:scope:search.api.globus.org:all'
_SHARED_EPILOG = '\nLogout of the Globus Search CLI with\n  globus-search logout\n'
_LOGIN_EPILOG = '\nYou have successfully logged in to the Globus Search CLI\n' + _SHARED_EPILOG
_LOGGED_IN_RESPONSE = 'You are already logged in!\n\nYou may force a new login with\n  globus-search login --force\n' + _SHARED_EPILOG

def _check_logged_in():
    search_rt = lookup_option(SEARCH_RT_OPTNAME)
    if search_rt is None:
        return False
    else:
        native_client = internal_auth_client()
        res = native_client.oauth2_validate_token(search_rt)
        return res['active']


def _revoke_current_tokens(native_client):
    for token_opt in (SEARCH_RT_OPTNAME, SEARCH_AT_OPTNAME):
        token = lookup_option(token_opt)
        if token:
            native_client.oauth2_revoke_token(token)


def _store_config(token_response):
    tkn = token_response.by_resource_server
    search_at = tkn['search.api.globus.org']['access_token']
    search_rt = tkn['search.api.globus.org']['refresh_token']
    search_at_expires = tkn['search.api.globus.org']['expires_at_seconds']
    write_option(SEARCH_RT_OPTNAME, search_rt)
    write_option(SEARCH_AT_OPTNAME, search_at)
    write_option(SEARCH_AT_EXPIRES_OPTNAME, search_at_expires)
    safeprint(_LOGIN_EPILOG)


def _do_login_flow():
    native_client = internal_auth_client()
    label = platform.node() or None
    native_client.oauth2_start_flow(requested_scopes=SEARCH_ALL_SCOPE, refresh_tokens=True, prefill_named_grant=label)
    linkprompt = 'Please log into Globus here'
    safeprint(('{0}:\n{1}\n{2}\n{1}\n').format(linkprompt, '-' * len(linkprompt), native_client.oauth2_get_authorize_url()))
    auth_code = click.prompt('Enter the resulting Authorization Code here').strip()
    tkn = native_client.oauth2_exchange_code_for_tokens(auth_code)
    _revoke_current_tokens(native_client)
    _store_config(tkn)
    return


@click.command('login', short_help='Log into Globus to get credentials for the Globus Search CLI', help="Get credentials for the Globus Search CLI. Necessary before any 'globus-search' commands which require authentication will work")
@click.option('--force', is_flag=True, help='Do a fresh login, ignoring any existing credentials')
def login_command(force):
    if not force and _check_logged_in():
        safeprint(_LOGGED_IN_RESPONSE)
        return
    _do_login_flow()