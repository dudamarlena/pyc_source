# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus_search_cli/commands/logout.py
# Compiled at: 2019-12-03 15:45:33
import click, globus_sdk
from globus_search_cli.config import SEARCH_AT_EXPIRES_OPTNAME, SEARCH_AT_OPTNAME, SEARCH_RT_OPTNAME, internal_auth_client, lookup_option, remove_option
from globus_search_cli.printing import safeprint
_RESCIND_HELP = 'Rescinding Consents\n-------------------\nThe logout command only revokes tokens that it can see in its storage.\nIf you are concerned that logout may have failed to revoke a token,\nyou may want to manually rescind the Globus Search CLI consent on the\nManage Consents Page:\n\n    https://auth.globus.org/consents\n'
_LOGOUT_EPILOG = 'You are now successfully logged out of the Globus Search CLI.\nYou may also want to logout of any browser session you have with Globus:\n\n  https://auth.globus.org/v2/web/logout\n\nBefore attempting any further CLI commands, you will have to login again using\n\n  globus-search login\n'

@click.command('logout', short_help='Logout of the Globus Search CLI', help='Logout of the Globus Search CLI. Removes your Globus tokens from local storage, and revokes them so that they cannot be used anymore')
@click.confirmation_option(prompt='Are you sure you want to logout?', help='Automatically say "yes" to all prompts')
def logout_command():
    safeprint('Logging out of Globus Search CLI\n')
    native_client = internal_auth_client()
    print_rescind_help = False
    for token_opt in (SEARCH_RT_OPTNAME, SEARCH_AT_OPTNAME):
        token = lookup_option(token_opt)
        if not token:
            safeprint(('Warning: Found no token named "{}"! Recommend rescinding consent').format(token_opt))
            print_rescind_help = True
            continue
        try:
            native_client.oauth2_revoke_token(token)
        except globus_sdk.NetworkError:
            safeprint('Failed to reach Globus to revoke tokens. Because we cannot revoke these tokens, cancelling logout')
            click.get_current_context().exit(1)

        remove_option(token_opt)

    remove_option(SEARCH_AT_EXPIRES_OPTNAME)
    safeprint(('\n' if print_rescind_help else '') + _LOGOUT_EPILOG)
    if print_rescind_help:
        safeprint(_RESCIND_HELP)