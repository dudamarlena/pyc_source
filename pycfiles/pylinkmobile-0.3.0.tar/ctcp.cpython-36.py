# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/ctcp.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 3189 bytes
import datetime, random
from pylinkirc import utils
from pylinkirc.log import log

def handle_ctcp(irc, source, command, args):
    """
    CTCP event handler.
    """
    text = args['text']
    if not (text.startswith('\x01') and text.endswith('\x01')):
        return
    target = args['target']
    if not irc.get_service_bot(target):
        return
    else:
        text = text.strip('\x01')
        try:
            ctcp_command, data = text.split(' ', 1)
        except ValueError:
            ctcp_command = text
            data = ''

        ctcp_command = ctcp_command.upper()
        log.debug('(%s) ctcp: got CTCP command %r, data %r', irc.name, ctcp_command, data)
        if ctcp_command in SUPPORTED_COMMANDS:
            log.info('(%s) Received CTCP %s from %s to %s', irc.name, ctcp_command, irc.get_hostmask(source), irc.get_friendly_name(target))
            result = SUPPORTED_COMMANDS[ctcp_command](irc, source, ctcp_command, data)
            if result:
                if source in irc.users:
                    irc.msg(source, ('\x01%s %s\x01' % (ctcp_command, result)), notice=True,
                      source=target)
            return False
        log.info('(%s) Received unknown CTCP %s from %s to %s', irc.name, ctcp_command, irc.get_hostmask(source), irc.get_friendly_name(target))
        return False


utils.add_hook(handle_ctcp, 'PRIVMSG', priority=200)

def handle_ctcpversion(irc, source, ctcp, data):
    """
    Handles CTCP version requests.
    """
    return irc.version()


def handle_ctcpeaster(irc, source, ctcp, data):
    """
    Secret easter egg.
    """
    responses = [
     'Legends say the cord monster was born only %s years ago...' % (datetime.datetime.now().year - 2014),
     'Hiss%s' % ('...' * random.randint(1, 5)),
     'His%s%s' % ('s' * random.randint(1, 4), '...' * random.randint(1, 5)),
     "It's Easter already? Where are the eggs?",
     'Maybe later.',
     'Janus? Never heard of it.',
     irc.version(),
     "Let me out of here, I'll give you cookies!",
     'About as likely as pigs flying.',
     'Request timed out.',
     'No actual pie here, sorry.',
     'Hey, no loitering!',
     'Hey, can you keep a secret? \x031,1 %s' % ' ' * random.randint(1, 20)]
    return random.choice(responses)


SUPPORTED_COMMANDS = {'VERSION':handle_ctcpversion, 
 'PING':lambda irc, source, ctcp, data: data, 
 'ABOUT':handle_ctcpeaster, 
 'EASTER':handle_ctcpeaster}