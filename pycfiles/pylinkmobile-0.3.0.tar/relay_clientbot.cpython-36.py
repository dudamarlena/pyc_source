# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/relay_clientbot.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 13594 bytes
import shlex, string, time
from pylinkirc import conf, utils, world
from pylinkirc.log import log
default_styles = {'MESSAGE':'\x02[$netname]\x02 <$mode_prefix$colored_sender> $text', 
 'KICK':'\x02[$netname]\x02 - $colored_sender$sender_identhost has kicked $target_nick from $channel ($text)', 
 'PART':'\x02[$netname]\x02 - $colored_sender$sender_identhost has left $channel ($text)', 
 'JOIN':'\x02[$netname]\x02 - $colored_sender$sender_identhost has joined $channel', 
 'NICK':'\x02[$netname]\x02 - $colored_sender$sender_identhost is now known as $newnick', 
 'QUIT':'\x02[$netname]\x02 - $colored_sender$sender_identhost has quit ($text)', 
 'ACTION':'\x02[$netname]\x02 * $mode_prefix$colored_sender $text', 
 'NOTICE':'\x02[$netname]\x02 - Notice from $mode_prefix$colored_sender: $text', 
 'SQUIT':'\x02[$netname]\x02 - Netsplit lost users: $colored_nicks', 
 'SJOIN':'\x02[$netname]\x02 - Netjoin gained users: $colored_nicks', 
 'MODE':'\x02[$netname]\x02 - $colored_sender$sender_identhost sets mode $modes on $channel', 
 'PM':'PM from $sender on $netname: $text', 
 'PNOTICE':'<$sender> $text'}

def color_text(s):
    """
    Returns a colorized version of the given text based on a simple hash algorithm.
    """
    if not s:
        return s
    else:
        colors = ('03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13',
                  '15')
        hash_output = hash(s.encode())
        num = hash_output % len(colors)
        return '\x03%s%s\x03' % (colors[num], s)


def cb_relay_core(irc, source, command, args):
    """
    This function takes Clientbot events and formats them as text to the target channel / user.
    """
    real_command = command.split('_')[(-1)]
    relay = world.plugins.get('relay')
    private = False
    if irc.pseudoclient and relay:
        try:
            sourcename = irc.get_friendly_name(source)
        except KeyError:
            sourcename = args['userdata'].nick

        relay_conf = conf.conf.get('relay') or {}
        startup_delay = relay_conf.get('clientbot_startup_delay', 20)
        target = args.get('target')
        if isinstance(target, str):
            target = target.lstrip(''.join(irc.prefixmodes.values()))
        if real_command == 'MESSAGE':
            if not args.get('is_notice') and args['text'].startswith('\x01ACTION '):
                if args['text'].endswith('\x01'):
                    args['text'] = args['text'][8:-1]
                    real_command = 'ACTION'
                if not irc.is_channel(target):
                    if relay_conf.get('allow_clientbot_pms'):
                        real_command = 'PNOTICE' if args.get('is_notice') else 'PM'
                        private = True
                    elif args['text'].startswith('\x01'):
                        return
                    if args.get('is_notice'):
                        real_command = 'NOTICE'
        else:
            if time.time() - irc.start_ts < startup_delay:
                log.debug('(%s) relay_cb_core: Not relaying %s because of startup delay of %s.', irc.name, real_command, startup_delay)
                return
            text_template = irc.get_service_options('relay', 'clientbot_styles', dict).get(real_command, default_styles.get(real_command, ''))
            text_template = string.Template(text_template)
            if text_template:
                if irc.get_service_bot(source):
                    log.debug('(%s) relay_cb_core: Overriding network origin to local (source=%s)', irc.name, source)
                    sourcenet = irc.name
                    realsource = source
                else:
                    log.debug('(%s) relay_cb_core: Trying to find original sender (user) for %s', irc.name, source)
                    try:
                        origuser = relay.get_orig_user(irc, source) or args['userdata'].remote
                    except (AttributeError, KeyError):
                        log.debug('(%s) relay_cb_core: Trying to find original sender (server) for %s. serverdata=%s', irc.name, source, args.get('serverdata'))
                        try:
                            localsid = args.get('serverdata') or irc.servers[source]
                            origuser = (localsid.remote, world.networkobjects[localsid.remote].uplink)
                        except (AttributeError, KeyError):
                            return

                    log.debug('(%s) relay_cb_core: Original sender found as %s', irc.name, origuser)
                    sourcenet, realsource = origuser
                try:
                    netname = conf.conf['servers'][sourcenet]['netname']
                except KeyError:
                    netname = sourcenet

                stripped_target = target = args.get('channel') or args.get('target')
                if isinstance(target, str):
                    stripped_target = target.lstrip(''.join(irc.prefixmodes.values()))
                if target is None or not (irc.is_channel(stripped_target) or private):
                    userdata = args.get('userdata') or irc.users.get(source)
                    if not userdata:
                        userdata = irc.pseudoclient
                    targets = [channel for channel in userdata.channels if relay.get_relay(irc, channel)]
                else:
                    targets = [
                     target]
                    args['channel'] = stripped_target
                log.debug('(%s) relay_cb_core: Relaying event %s to channels: %s', irc.name, real_command, targets)
                identhost = ''
                if source in irc.users:
                    try:
                        identhost = irc.get_hostmask(source).split('!')[(-1)]
                    except KeyError:
                        identhost = '%s@%s' % (args['userdata'].ident, args['userdata'].host)

                    identhost = ' (%s)' % identhost
                if args.get('target') in irc.users:
                    args['target_nick'] = irc.get_friendly_name(args['target'])
                if args.get('modes'):
                    args['modes'] = irc.join_modes(args['modes'])
                mode_prefix = ''
                if 'channel' in args:
                    args['local_channel'] = args['channel']
                    log.debug('(%s) relay_clientbot: coersing $channel from %s to %s', irc.name, args['local_channel'], args['channel'])
                    sourceirc = world.networkobjects.get(sourcenet)
                    log.debug('(%s) relay_clientbot: Checking prefix modes for %s on %s (relaying to %s)', irc.name, realsource, sourcenet, args['channel'])
                    if sourceirc:
                        args['channel'] = remotechan = relay.get_remote_channel(irc, sourceirc, args['channel'])
                        if source in irc.users:
                            if remotechan in sourceirc.channels:
                                if realsource in sourceirc.channels[remotechan].users:
                                    prefixmodes = sourceirc.channels[remotechan].get_prefix_modes(realsource)
                                    log.debug('(%s) relay_clientbot: got prefix modes %s for %s on %s@%s', irc.name, prefixmodes, realsource, remotechan, sourcenet)
                                    if prefixmodes:
                                        mode_prefix = sourceirc.prefixmodes.get(sourceirc.cmodes.get(prefixmodes[0]))
                args.update({'netname':netname, 
                 'sender':sourcename,  'sender_identhost':identhost,  'colored_sender':color_text(sourcename), 
                 'colored_netname':color_text(netname),  'mode_prefix':mode_prefix})
                for target in targets:
                    cargs = args.copy()
                    nicklist = args.get('nicks')
                    if nicklist:
                        if isinstance(nicklist, dict):
                            nicklist = nicklist.get(target, [])
                        if not nicklist:
                            pass
                        else:
                            colored_nicks = [color_text(nick) for nick in nicklist]
                            cargs['nicks'] = ', '.join(nicklist)
                            cargs['colored_nicks'] = ', '.join(colored_nicks)
                    text = text_template.safe_substitute(cargs)
                    irc.msg(target, text, loopback=False, notice=private)


utils.add_hook(cb_relay_core, 'CLIENTBOT_MESSAGE')
utils.add_hook(cb_relay_core, 'CLIENTBOT_KICK')
utils.add_hook(cb_relay_core, 'CLIENTBOT_PART')
utils.add_hook(cb_relay_core, 'CLIENTBOT_JOIN')
utils.add_hook(cb_relay_core, 'CLIENTBOT_QUIT')
utils.add_hook(cb_relay_core, 'CLIENTBOT_NICK')
utils.add_hook(cb_relay_core, 'CLIENTBOT_SJOIN')
utils.add_hook(cb_relay_core, 'CLIENTBOT_SQUIT')
utils.add_hook(cb_relay_core, 'RELAY_RAW_MODE')

@utils.add_cmd
def rpm(irc, source, args):
    """<target nick/UID> <text>

    Sends PMs to users over Relay, if Clientbot PMs are enabled.
    If the target nick has spaces in it, you may quote the nick as "nick".
    """
    args = shlex.split(' '.join(args))
    try:
        target = args[0]
        text = ' '.join(args[1:])
    except IndexError:
        irc.error('Not enough arguments. Needs 2: target nick and text.')
        return
    else:
        relay = world.plugins.get('relay')
        if irc.has_cap('can-spawn-clients'):
            irc.error('This command is only supported on Clientbot networks. Try /msg %s <text>' % target)
            return
        if relay is None:
            irc.error('PyLink Relay is not loaded.')
            return
        if not text:
            irc.error('No text given.')
            return
        if not conf.conf.get('relay').get('allow_clientbot_pms'):
            irc.error('Private messages with users connected via Clientbot have been administratively disabled.')
            return
        if target in irc.users:
            uids = [
             target]
        else:
            uids = irc.nick_to_uid(target, multi=True, filterfunc=(lambda u: relay.is_relay_client(irc, u)))
        if not uids:
            irc.error('Unknown user %s.' % target)
            return
        if len(uids) > 1:
            targets = ['\x02%s\x02: %s @ %s' % (uid, irc.get_hostmask(uid), irc.users[uid].remote[0]) for uid in uids]
            irc.error('Please select the target you want to PM: %s' % ', '.join(targets))
            return
        assert not irc.is_internal_client(source), 'rpm is not allowed from PyLink bots'
        relay.handle_messages(irc, source, 'RELAY_CLIENTBOT_PRIVMSG', {'target':uids[0],  'text':text})
        irc.reply('Message sent.')