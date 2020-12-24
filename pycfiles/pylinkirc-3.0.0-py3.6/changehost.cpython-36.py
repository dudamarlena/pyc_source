# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/changehost.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 5132 bytes
"""
Changehost plugin - automatically changes the hostname of matching users.
"""
import string
from pylinkirc import conf, utils, world
from pylinkirc.coremods import permissions
from pylinkirc.log import log
allowed_chars = string.ascii_letters + '-./:' + string.digits

def _changehost(irc, target):
    changehost_conf = conf.conf.get('changehost')
    if target not in irc.users:
        return
    if irc.is_internal_client(target):
        log.debug('(%s) Skipping changehost on internal client %s', irc.name, target)
        return
    if irc.name not in changehost_conf.get('enabled_nets'):
        if not irc.serverdata.get('changehost_enable'):
            return
    match_ip = irc.get_service_option('changehost', 'match_ip', default=False)
    match_realhosts = irc.get_service_option('changehost', 'match_realhosts', default=False)
    changehost_hosts = irc.get_service_options('changehost', 'hosts', dict)
    if not changehost_hosts:
        return
    args = irc.users[target].get_fields()
    if not changehost_conf.get('force_host_expansion'):
        del args['host']
    log.debug('(%s) Changehost args: %s', irc.name, args)
    for host_glob, host_template in changehost_hosts.items():
        log.debug('(%s) Changehost: checking mask %s', irc.name, host_glob)
        if irc.match_host(host_glob, target, ip=match_ip, realhost=match_realhosts):
            log.debug('(%s) Changehost matched mask %s', irc.name, host_glob)
            template = string.Template(host_template)
            try:
                new_host = template.substitute(args)
            except KeyError as e:
                log.warning('(%s) Bad expansion %s in template %s' % (irc.name, e, host_template))
                continue

            for char in new_host:
                if char not in allowed_chars:
                    new_host = new_host.replace(char, '-')

            if new_host != irc.users[target].host:
                irc.update_client(target, 'HOST', new_host)
            break


def handle_uid(irc, sender, command, args):
    """
    Changehost listener for new connections.
    """
    target = args['uid']
    _changehost(irc, target)


utils.add_hook(handle_uid, 'UID')

def handle_chghost(irc, sender, command, args):
    """
    Handles incoming CHGHOST requests for optional host-change enforcement.
    """
    changehost_conf = conf.conf.get('changehost', {})
    target = args['target']
    if not irc.is_internal_client(sender):
        if not irc.is_internal_server(sender):
            if irc.name in changehost_conf.get('enforced_nets', []) or irc.serverdata.get('changehost_enforce'):
                log.debug('(%s) Enforce for network is on, re-checking host for target %s/%s', irc.name, target, irc.get_friendly_name(target))
                for ex in irc.get_service_options('changehost', 'enforce_exceptions', list):
                    if irc.match_host(ex, target):
                        log.debug('(%s) Skipping host change for target %s; they are exempted by mask %s', irc.name, target, ex)
                        return

                userobj = irc.users.get(target)
                if userobj:
                    _changehost(irc, target)


utils.add_hook(handle_chghost, 'CHGHOST')

def handle_svslogin(irc, sender, command, args):
    """
    Handles services account changes for changehost.
    """
    _changehost(irc, sender)


utils.add_hook(handle_svslogin, 'CLIENT_SERVICES_LOGIN')

@utils.add_cmd
def applyhosts(irc, sender, args):
    """[<network>]

    Applies all configured hosts for users on the given network, or the current network if none is specified."""
    permissions.check_permissions(irc, sender, ['changehost.applyhosts'])
    try:
        network = world.networkobjects[args[0]]
    except IndexError:
        network = irc
    except KeyError:
        irc.error("Unknown network '%s'." % network)
        return

    for user in network.users.copy():
        _changehost(network, user)

    irc.reply('Done.')