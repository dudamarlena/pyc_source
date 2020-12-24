# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/bots.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 9607 bytes
"""
bots.py: Spawn virtual users/bots on a PyLink server and make them interact
with things.
"""
from pylinkirc import utils
from pylinkirc.coremods import permissions
from pylinkirc.log import log

@utils.add_cmd
def spawnclient(irc, source, args):
    """<nick> <ident> <host>

    Spawns the specified client on the PyLink server.
    Note: this doesn't check the validity of any fields you give it!"""
    if not irc.has_cap('can-spawn-clients'):
        irc.error('This network does not support client spawning.')
        return
    permissions.check_permissions(irc, source, ['bots.spawnclient'])
    try:
        nick, ident, host = args[:3]
    except ValueError:
        irc.error('Not enough arguments. Needs 3: nick, user, host.')
        return
    else:
        irc.spawn_client(nick, ident, host, manipulatable=True)
        irc.reply('Done.')


@utils.add_cmd
def quit(irc, source, args):
    """<target> [<reason>]

    Quits the PyLink client with nick <target>, if one exists."""
    permissions.check_permissions(irc, source, ['bots.quit'])
    try:
        nick = args[0]
    except IndexError:
        irc.error('Not enough arguments. Needs 1-2: nick, reason (optional).')
        return
    else:
        u = irc.nick_to_uid(nick, filterfunc=(irc.is_internal_client))
        if u is None:
            irc.error('Unknown user %r' % nick)
            return
        if irc.pseudoclient.uid == u:
            irc.error('Cannot quit the main PyLink client!')
            return
        quitmsg = ' '.join(args[1:]) or 'Client Quit'
        if not irc.is_manipulatable_client(u):
            irc.error('Cannot force quit a protected PyLink services client.')
            return
        irc.quit(u, quitmsg)
        irc.reply('Done.')
        irc.call_hooks([u, 'PYLINK_BOTSPLUGIN_QUIT', {'text':quitmsg,  'parse_as':'QUIT'}])


def joinclient(irc, source, args):
    """[<target>] <channel1>[,<channel2>,<channel3>,...]

    Joins <target>, the nick of a PyLink client, to a comma-separated list of channels.
    If <target> is not given, it defaults to the main PyLink client.

    For the channel arguments, prefixes can also be specified to join the given client with
    (e.g. @#channel will join the client with op, while ~@#channel will join it with +qo.
    """
    permissions.check_permissions(irc, source, ['bots.join', 'bots.joinclient'])
    try:
        u = irc.nick_to_uid((args[0]), filterfunc=(irc.is_internal_client))
        if u is None:
            raise IndexError
        clist = args[1]
    except IndexError:
        u = irc.pseudoclient.uid
        try:
            clist = args[0]
        except IndexError:
            irc.error('Not enough arguments. Needs 1-2: nick (optional), comma separated list of channels.')
            return

    clist = clist.split(',')
    if not clist:
        irc.error('No valid channels given.')
        return
    if not (irc.is_manipulatable_client(u) or irc.get_service_bot(u)):
        irc.error('Cannot force join a protected PyLink services client.')
        return
    prefix_to_mode = {v:k for k, v in irc.prefixmodes.items()}
    for channel in clist:
        real_channel = channel.lstrip(''.join(prefix_to_mode))
        prefixes = channel[:len(channel) - len(real_channel)]
        joinmodes = ''.join(prefix_to_mode[prefix] for prefix in prefixes)
        if not irc.is_channel(real_channel):
            irc.error('Invalid channel name %r.' % real_channel)
            return
        if prefixes:
            irc.sjoin(irc.sid, real_channel, [(joinmodes, u)])
        else:
            irc.join(u, real_channel)
        try:
            modes = irc.channels[real_channel].modes
        except KeyError:
            modes = []

        irc.call_hooks([u, 'PYLINK_BOTSPLUGIN_JOIN',
         {'channel':real_channel,  'users':[u],  'modes':modes, 
          'parse_as':'JOIN'}])

    irc.reply('Done.')


utils.add_cmd(joinclient, name='join')

@utils.add_cmd
def nick(irc, source, args):
    """[<target>] <newnick>

    Changes the nick of <target>, a PyLink client, to <newnick>. If <target> is not given, it defaults to the main PyLink client."""
    permissions.check_permissions(irc, source, ['bots.nick'])
    try:
        nick = args[0]
        newnick = args[1]
    except IndexError:
        try:
            nick = irc.pseudoclient.nick
            newnick = args[0]
        except IndexError:
            irc.error('Not enough arguments. Needs 1-2: nick (optional), newnick.')
            return

    u = irc.nick_to_uid(nick, filterfunc=(irc.is_internal_client))
    if newnick in ('0', u):
        newnick = u
    else:
        if not irc.is_nick(newnick):
            irc.error('Invalid nickname %r.' % newnick)
            return
    if not (irc.is_manipulatable_client(u) or irc.get_service_bot(u)):
        irc.error('Cannot force nick changes for a protected PyLink services client.')
        return
    irc.nick(u, newnick)
    irc.reply('Done.')
    irc.call_hooks([u, 'PYLINK_BOTSPLUGIN_NICK', {'newnick':newnick,  'oldnick':nick,  'parse_as':'NICK'}])


@utils.add_cmd
def part(irc, source, args):
    """[<target>] <channel1>,[<channel2>],... [<reason>]

    Parts <target>, the nick of a PyLink client, from a comma-separated list of channels. If <target> is not given, it defaults to the main PyLink client."""
    permissions.check_permissions(irc, source, ['bots.part'])
    try:
        nick = args[0]
        clist = args[1]
        reason = ' '.join(args[2:])
        u = irc.nick_to_uid(nick, filterfunc=(irc.is_internal_client))
        if u is None:
            raise IndexError
    except IndexError:
        u = irc.pseudoclient.uid
        try:
            clist = args[0]
        except IndexError:
            irc.error('Not enough arguments. Needs 1-2: nick (optional), comma separated list of channels.')
            return

        reason = ' '.join(args[1:])

    clist = clist.split(',')
    if not clist:
        irc.error('No valid channels given.')
        return
    if not (irc.is_manipulatable_client(u) or irc.get_service_bot(u)):
        irc.error('Cannot force part a protected PyLink services client.')
        return
    for channel in clist:
        if not irc.is_channel(channel):
            irc.error('Invalid channel name %r.' % channel)
            return
        irc.part(u, channel, reason)

    irc.reply('Done.')
    irc.call_hooks([u, 'PYLINK_BOTSPLUGIN_PART', {'channels':clist,  'text':reason,  'parse_as':'PART'}])


def msg(irc, source, args):
    """[<source>] <target> <text>

    Sends message <text> from <source>, where <source> is the nick of a PyLink client. If <source> is not given, it defaults to the main PyLink client."""
    permissions.check_permissions(irc, source, ['bots.msg'])
    try:
        msgsource = args[0]
        target = args[1]
        text = ' '.join(args[2:])
        sourceuid = irc.nick_to_uid(msgsource, filterfunc=(irc.is_internal_client))
        if sourceuid is None or not text:
            raise IndexError
    except IndexError:
        try:
            sourceuid = irc.pseudoclient.uid
            target = args[0]
            text = ' '.join(args[1:])
        except IndexError:
            irc.error('Not enough arguments. Needs 2-3: source nick (optional), target, text.')
            return

    if not text:
        irc.error('No text given.')
        return
    else:
        try:
            int_u = int(target)
        except:
            int_u = None

        if int_u:
            if int_u in irc.users:
                real_target = int_u
        if target in irc.users:
            real_target = target
        else:
            if not irc.is_channel(target):
                potential_targets = irc.nick_to_uid(target, multi=True)
                if not potential_targets:
                    irc.error('Unknown user %r.' % target)
                    return
                if len(potential_targets) > 1:
                    irc.error('Multiple users with the nick %r found: please select the right UID: %s' % (target, str(potential_targets)))
                    return
                real_target = potential_targets[0]
            else:
                real_target = target
    irc.message(sourceuid, real_target, text)
    irc.reply('Done.')
    irc.call_hooks([sourceuid, 'PYLINK_BOTSPLUGIN_MSG', {'target':real_target,  'text':text,  'parse_as':'PRIVMSG'}])


utils.add_cmd(msg, aliases=('say', ))