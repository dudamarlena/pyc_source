# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/networks.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 8215 bytes
"""Networks plugin - allows you to manipulate connections to various configured networks."""
import importlib, threading, types, pylinkirc
from pylinkirc import utils, world
from pylinkirc.coremods import control, permissions
from pylinkirc.log import log
REMOTE_IN_USE = threading.Event()

@utils.add_cmd
def disconnect(irc, source, args):
    """<network>

    Disconnects the network <network>. When all networks are disconnected, PyLink will automatically exit.

    To reconnect a network disconnected using this command, use REHASH to reload the networks list."""
    permissions.check_permissions(irc, source, ['networks.disconnect'])
    try:
        netname = args[0]
        network = world.networkobjects[netname]
    except IndexError:
        irc.error('Not enough arguments (needs 1: network name (case sensitive)).')
        return
    except KeyError:
        irc.error('No such network "%s" (case sensitive).' % netname)
        return
    else:
        if network.has_cap('virtual-server'):
            irc.error('"%s" is a virtual server and cannot be directly disconnected.' % netname)
            return
        log.info('Disconnecting network %r per %s', netname, irc.get_hostmask(source))
        control.remove_network(network)
        irc.reply("Done. If you want to reconnect this network, use the 'rehash' command.")


@utils.add_cmd
def autoconnect(irc, source, args):
    """<network> <seconds>

    Sets the autoconnect time for <network> to <seconds>.
    You can disable autoconnect for a network by setting <seconds> to a negative value."""
    permissions.check_permissions(irc, source, ['networks.autoconnect'])
    try:
        netname = args[0]
        seconds = float(args[1])
        network = world.networkobjects[netname]
    except IndexError:
        irc.error('Not enough arguments (needs 2: network name (case sensitive), autoconnect time (in seconds)).')
        return
    except KeyError:
        irc.error('No such network "%s" (case sensitive).' % netname)
        return
    except ValueError:
        irc.error('Invalid argument "%s" for <seconds>.' % seconds)
        return
    else:
        network.serverdata['autoconnect'] = seconds
        irc.reply('Done.')


remote_parser = utils.IRCParser()
remote_parser.add_argument('--service', type=str, default='pylink')
remote_parser.add_argument('network')
remote_parser.add_argument('command', nargs=(utils.IRCParser.REMAINDER))

@utils.add_cmd
def remote(irc, source, args):
    """[--service <service name>] <network> <command>

    Runs <command> on the remote network <network>. Plugin responses sent using irc.reply() are
    supported and returned here, but others are dropped due to protocol limitations."""
    global REMOTE_IN_USE
    args = remote_parser.parse_args(args)
    if not args.command:
        irc.error('No command given!')
        return
    netname = args.network
    permissions.check_permissions(irc, source, [
     'networks.remote',
     'networks.remote.%s' % netname,
     'networks.remote.%s.%s' % (netname, args.service),
     'networks.remote.%s.%s.%s' % (netname, args.service, args.command[0])])
    if REMOTE_IN_USE.is_set():
        irc.error("The 'remote' command can not be nested.")
        return
    REMOTE_IN_USE.set()
    if netname == irc.name:
        irc.error('Cannot remote-send a command to the local network; use a normal command!')
        REMOTE_IN_USE.clear()
        return
    try:
        remoteirc = world.networkobjects[netname]
    except KeyError:
        irc.error('No such network %r (case sensitive).' % netname)
        REMOTE_IN_USE.clear()
        return
    else:
        if args.service not in world.services:
            irc.error('Unknown service %r.' % args.service)
            REMOTE_IN_USE.clear()
            return
        elif not remoteirc.connected.is_set():
            irc.error('Network %r is not connected.' % netname)
            REMOTE_IN_USE.clear()
            return
        else:
            if not world.services[args.service].uids.get(netname):
                irc.error('The requested service %r is not available on %r.' % (args.service, netname))
                REMOTE_IN_USE.clear()
                return
            try:
                remoteirc.called_in = remoteirc.called_by = remoteirc.pseudoclient.uid
                remoteirc.pseudoclient.account = irc.users[source].account
            except:
                REMOTE_IN_USE.clear()
                raise

        def _remote_reply(placeholder_self, text, **kwargs):
            assert irc.name != placeholder_self.name, 'Refusing to route reply back to the same network, as this would cause a recursive loop'
            log.debug('(%s) networks.remote: re-routing reply %r from network %s', irc.name, text, placeholder_self.name)
            if 'source' in kwargs:
                del kwargs['source']
            (irc.reply)(text, source=irc.pseudoclient.uid, **kwargs)

        old_reply = remoteirc._reply
        with remoteirc._reply_lock:
            try:
                log.debug('(%s) networks.remote: overriding reply() of IRC object %s', irc.name, netname)
                remoteirc._reply = types.MethodType(_remote_reply, remoteirc)
                world.services[args.service].call_cmd(remoteirc, remoteirc.pseudoclient.uid, ' '.join(args.command))
            finally:
                log.debug('(%s) networks.remote: restoring reply() of IRC object %s', irc.name, netname)
                remoteirc._reply = old_reply
                try:
                    remoteirc.pseudoclient.account = ''
                except:
                    log.warning('(%s) networks.remote: failed to restore pseudoclient account for %s; did the remote network disconnect while running this command?', irc.name, netname)

                REMOTE_IN_USE.clear()


@utils.add_cmd
def reloadproto(irc, source, args):
    """<protocol module name>

    Reloads the given protocol module without restart. You will have to manually disconnect and reconnect any network using the module for changes to apply."""
    permissions.check_permissions(irc, source, ['networks.reloadproto'])
    try:
        name = args[0]
    except IndexError:
        irc.error('Not enough arguments (needs 1: protocol module name)')
        return
    else:
        importlib.reload(pylinkirc.classes)
        log.debug('networks.reloadproto: reloading %s', pylinkirc.classes)
        for common_name in pylinkirc.protocols.common_modules:
            module = utils._get_protocol_module(common_name)
            log.debug('networks.reloadproto: reloading %s', module)
            importlib.reload(module)

        proto = utils._get_protocol_module(name)
        log.debug('networks.reloadproto: reloading %s', proto)
        importlib.reload(proto)
        irc.reply('Done. You will have to manually disconnect and reconnect any network using the %r module for changes to apply.' % name)