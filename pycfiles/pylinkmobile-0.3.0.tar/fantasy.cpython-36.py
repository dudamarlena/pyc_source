# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/fantasy.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 3510 bytes
from pylinkirc import conf, utils, world
from pylinkirc.log import log

def handle_fantasy(irc, source, command, args):
    """Fantasy command handler."""
    if not irc.connected.is_set():
        return
    channel = args['target']
    orig_text = args['text']
    if irc.is_channel(channel) and not irc.is_internal_client(source):
        for botname, sbot in world.services.copy().items():
            if botname not in world.services:
                pass
            else:
                respondtonick = conf.conf.get(botname, {}).get('respond_to_nick', conf.conf['pylink'].get('respond_to_nick', conf.conf['pylink'].get('respondtonick')))
                log.debug('(%s) fantasy: checking bot %s', irc.name, botname)
                servuid = sbot.uids.get(irc.name)
                if servuid in irc.channels[channel].users:
                    prefixes = [
                     conf.conf.get(botname, {}).get('prefix', conf.conf['pylink'].get('prefixes', {}).get(botname))]
                    nick = irc.to_lower(irc.users[servuid].nick)
                    nick_prefixes = [nick + ',', nick + ':', '@' + nick]
                    if respondtonick:
                        prefixes += nick_prefixes
                    if not any(prefixes):
                        continue
                    lowered_text = irc.to_lower(orig_text)
                    for prefix in filter(None, prefixes):
                        if lowered_text.startswith(prefix):
                            text = orig_text[len(prefix):]
                            if text.startswith(' '):
                                if prefix not in nick_prefixes:
                                    log.debug('(%s) fantasy: skipping trigger with text prefix followed by space', irc.name)
                                    continue
                            sbot.call_cmd(irc, source, text, called_in=channel)
                            continue


utils.add_hook(handle_fantasy, 'PRIVMSG')