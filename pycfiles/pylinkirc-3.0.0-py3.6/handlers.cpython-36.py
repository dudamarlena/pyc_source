# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/coremods/handlers.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 9992 bytes
"""
handlers.py - Implements miscellaneous IRC command handlers (WHOIS, services login, etc.)
"""
import time
from pylinkirc import conf, utils
from pylinkirc.log import log

def handle_whois(irc, source, command, args):
    """Handle WHOIS queries."""
    target = args['target']
    user = irc.users.get(target)
    f = lambda num, source, text: irc.numeric(irc.sid, num, source, text)
    server = irc.get_server(target)
    if user is None:
        nick = target
        f(401, source, '%s :No such nick/channel' % nick)
    else:
        nick = user.nick
        source_is_oper = ('o', None) in irc.users[source].modes
        source_is_bot = (irc.umodes.get('bot'), None) in irc.users[source].modes
        netname = irc.serverdata.get('netname', irc.name)
        f(311, source, '%s %s %s * :%s' % (nick, user.ident, user.host, user.realname))
        isHideChans = (
         irc.umodes.get('hidechans'), None) in user.modes
        if not isHideChans or isHideChans and source_is_oper:
            public_chans = []
            for chan in user.channels:
                c = irc.channels[chan]
                if (
                 irc.cmodes.get('secret'), None) in c.modes or (
                 irc.cmodes.get('private'), None) in c.modes:
                    if not (source_is_oper or source in c.users):
                        continue
                prefixes = c.get_prefix_modes(target)
                if prefixes:
                    highest = prefixes[0]
                    modechar = irc.cmodes[highest]
                    chan = irc.prefixmodes[modechar] + chan
                public_chans.append(chan)

            if public_chans:
                f(319, source, '%s :%s' % (nick, ' '.join(public_chans)))
        f(312, source, '%s %s :%s' % (nick, irc.servers[server].name,
         irc.servers[server].desc))
        if ('o', None) in user.modes:
            isHideOper = (
             irc.umodes.get('hideoper'), None) in user.modes
            if not isHideOper or isHideOper and source_is_oper or isHideOper and not conf.conf['pylink'].get('whois_use_hideoper', True):
                opertype = user.opertype
                n = 'n' if opertype[0].lower() in 'aeiou' else ''
                opertype = opertype.replace(' (on %s)' % irc.get_full_network_name(), '')
                f(313, source, '%s :is a%s %s' % (nick, n, opertype))
        if source_is_oper:
            f(378, source, '%s :is connecting from %s@%s %s' % (nick, user.ident, user.realhost, user.ip))
            f(379, source, '%s :is using modes %s' % (nick, irc.join_modes((user.modes), sort=True)))
        away_text = user.away
        log.debug('(%s) coremods.handlers.handle_whois: away_text for %s is %r', irc.name, target, away_text)
        if away_text:
            f(301, source, '%s :%s' % (nick, away_text))
        if (irc.umodes.get('bot'), None) in user.modes:
            f(335, source, '%s :is a bot' % nick)
        if irc.get_service_bot(target):
            if conf.conf['pylink'].get('whois_show_startup_time', True):
                f(317, source, '%s 0 %s :seconds idle (placeholder), signon time' % (nick, irc.start_ts))
        if source_is_bot and conf.conf['pylink'].get('whois_show_extensions_to_bots') or not source_is_bot:
            irc.call_hooks([source, 'PYLINK_CUSTOM_WHOIS', {'target':target,  'server':server}])
        else:
            log.debug('(%s) coremods.handlers.handle_whois: skipping custom whois handlers because caller %s is marked as a bot', irc.name, source)
    f(318, source, '%s :End of /WHOIS list' % nick)


utils.add_hook(handle_whois, 'WHOIS')

def handle_mode(irc, source, command, args):
    """Protect against forced deoper attempts."""
    target = args['target']
    modes = args['modes']
    if irc.is_internal_client(target):
        if not irc.is_internal_client(source):
            if ('-o', None) in modes:
                if target == irc.pseudoclient.uid or not irc.is_manipulatable_client(target):
                    irc.mode(irc.sid, target, {('+o', None)})


utils.add_hook(handle_mode, 'MODE')

def handle_operup(irc, source, command, args):
    """Logs successful oper-ups on networks."""
    otype = args.get('text', 'IRC Operator')
    log.debug('(%s) Successful oper-up (opertype %r) from %s', irc.name, otype, irc.get_hostmask(source))
    irc.users[source].opertype = otype


utils.add_hook(handle_operup, 'CLIENT_OPERED')

def handle_services_login(irc, source, command, args):
    """Sets services login status for users."""
    try:
        irc.users[source].services_account = args['text']
    except KeyError:
        log.debug("(%s) Ignoring early account name setting for %s (UID hasn't been sent yet)", irc.name, source)


utils.add_hook(handle_services_login, 'CLIENT_SERVICES_LOGIN')

def handle_version(irc, source, command, args):
    """Handles requests for the PyLink server version."""
    fullversion = irc.version()
    irc.numeric(irc.sid, 351, source, fullversion)


utils.add_hook(handle_version, 'VERSION')

def handle_time(irc, source, command, args):
    """Handles requests for the PyLink server time."""
    timestring = time.ctime()
    irc.numeric(irc.sid, 391, source, '%s :%s' % (irc.hostname(), timestring))


utils.add_hook(handle_time, 'TIME')

def _state_cleanup_core(irc, source, channel):
    """
    Handles PART and KICK on clientbot-like networks (where only the users and channels we see are available)
    by deleting channels when we leave and users when they leave all shared channels.
    """
    if irc.has_cap('visible-state-only'):
        if irc.pseudoclient:
            if source == irc.pseudoclient.uid:
                log.debug('(%s) state_cleanup: removing channel %s since we have left', irc.name, channel)
                del irc._channels[channel]
        if not irc.users[source].channels:
            if not irc.is_internal_client(source):
                log.debug('(%s) state_cleanup: removing external user %s/%s who no longer shares a channel with us', irc.name, source, irc.users[source].nick)
                irc._remove_client(source)
    if channel in irc.channels:
        if not (irc._channels[channel].users or (irc.cmodes.get('permanent'), None) in irc._channels[channel].modes):
            log.debug('(%s) state_cleanup: removing empty channel %s', irc.name, channel)
            del irc._channels[channel]


def _state_cleanup_part(irc, source, command, args):
    for channel in args['channels']:
        _state_cleanup_core(irc, source, channel)


utils.add_hook(_state_cleanup_part, 'PART', priority=(-100))

def _state_cleanup_kick(irc, source, command, args):
    _state_cleanup_core(irc, args['target'], args['channel'])


utils.add_hook(_state_cleanup_kick, 'KICK', priority=(-100))

def _state_cleanup_mode(irc, source, command, args):
    """
    Cleans up and removes empty channels when -P (permanent mode) is removed from them.
    """
    target = args['target']
    if target in irc.channels:
        if 'permanent' in irc.cmodes:
            c = irc.channels[target]
            mode = '-%s' % irc.cmodes['permanent']
            if not c.users:
                if (mode, None) in args['modes']:
                    log.debug('(%s) _state_cleanup_mode: deleting empty channel %s as %s was set', irc.name, target, mode)
                    del irc._channels[target]
                    return False


utils.add_hook(_state_cleanup_mode, 'MODE', priority=10000)