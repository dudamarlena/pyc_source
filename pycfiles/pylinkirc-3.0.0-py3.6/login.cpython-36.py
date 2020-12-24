# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/coremods/login.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 5210 bytes
"""
login.py - Implement core login abstraction.
"""
from pylinkirc import conf, utils, world
from pylinkirc.log import log
pwd_context = None
_DEFAULT_CRYPTCONTEXT_SETTINGS = {'schemes': ['pbkdf2_sha256', 'sha512_crypt']}

def _make_cryptcontext():
    global pwd_context
    try:
        from passlib.context import CryptContext
    except ImportError:
        log.warning('Hashed passwords are disabled because passlib is not installed. Please install it (pip3 install passlib) and rehash for this feature to work.')
        return
    else:
        context_settings = conf.conf.get('login', {}).get('cryptcontext_settings') or _DEFAULT_CRYPTCONTEXT_SETTINGS
        if pwd_context is None:
            log.debug('Initialized new CryptContext with settings: %s', context_settings)
            pwd_context = CryptContext(**context_settings)
        else:
            log.debug('Updated CryptContext with settings: %s', context_settings)
            (pwd_context.update)(**context_settings)


_make_cryptcontext()

def _get_account(accountname):
    """
    Returns the login data block for the given account name (case-insensitive), or False if none
    exists.
    """
    accounts = {k.lower():v for k, v in conf.conf['login'].get('accounts', {}).items()}
    try:
        return accounts[accountname.lower()]
    except KeyError:
        return False


def check_login(user, password):
    """Checks whether the given user and password is a valid combination."""
    account = _get_account(user)
    if account:
        passhash = account.get('password')
        if not passhash:
            return False
        if account.get('encrypted', False):
            return verify_hash(password, passhash)
        return password == passhash
    else:
        return False


def verify_hash(password, passhash):
    """Checks whether the password given matches the hash."""
    if password:
        if not pwd_context:
            raise utils.NotAuthorizedError('Cannot log in to an account with a hashed password because passlib is not installed.')
        return pwd_context.verify(password, passhash)
    else:
        return False


def _irc_try_login(irc, source, username, skip_checks=False):
    """Internal function to process logins via IRC."""
    if irc.is_internal_client(source):
        irc.error("Cannot use 'identify' via a command proxy.")
        return
    else:
        if not skip_checks:
            logindata = _get_account(username)
            network_filter = logindata.get('networks')
            require_oper = logindata.get('require_oper', False)
            hosts_filter = logindata.get('hosts', [])
            if network_filter:
                if irc.name not in network_filter:
                    log.warning('(%s) Failed login to %r from %s (wrong network: networks filter says %r but we got %r)', irc.name, username, irc.get_hostmask(source), ', '.join(network_filter), irc.name)
                    raise utils.NotAuthorizedError('Account is not authorized to login on this network.')
            if require_oper and not irc.is_oper(source):
                log.warning('(%s) Failed login to %r from %s (needs oper)', irc.name, username, irc.get_hostmask(source))
                raise utils.NotAuthorizedError('You must be opered.')
            elif hosts_filter:
                if not any(irc.match_host(host, source) for host in hosts_filter):
                    log.warning('(%s) Failed login to %r from %s (hostname mismatch)', irc.name, username, irc.get_hostmask(source))
                    raise utils.NotAuthorizedError('Hostname mismatch.')
        irc.users[source].account = username
        irc.reply('Successfully logged in as %s.' % username)
        log.info('(%s) Successful login to %r by %s', irc.name, username, irc.get_hostmask(source))
        return True


def identify(irc, source, args):
    """<username> <password>

    Logs in to PyLink using the configured administrator account."""
    if irc.is_channel(irc.called_in):
        irc.reply('Error: This command must be sent in private. (Would you really type a password inside a channel?)')
        return
    try:
        username, password = args[0], args[1]
    except IndexError:
        irc.reply('Error: Not enough arguments.')
        return
    else:
        if check_login(username, password):
            _irc_try_login(irc, source, username)
            return
        if username.lower() == conf.conf['login'].get('user', '').lower():
            if password == conf.conf['login'].get('password'):
                realuser = conf.conf['login']['user']
                _irc_try_login(irc, source, realuser, skip_checks=True)
                return
        log.warning('(%s) Failed login to %r from %s', irc.name, username, irc.get_hostmask(source))
        raise utils.NotAuthorizedError('Bad username or password.')


utils.add_cmd(identify, aliases=('login', 'id'))