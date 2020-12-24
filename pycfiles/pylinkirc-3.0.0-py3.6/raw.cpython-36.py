# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/raw.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 1041 bytes
"""
raw.py: Provides a 'raw' command for sending raw text to IRC.
"""
from pylinkirc import utils
from pylinkirc.coremods import permissions
from pylinkirc.log import log

@utils.add_cmd
def raw(irc, source, args):
    """<text>

    Sends raw text to the IRC server.

    This command is not officially supported on non-Clientbot networks, where it
    requires a separate permission."""
    if irc.protoname == 'clientbot':
        perms = ['raw.raw', 'exec.raw']
    else:
        perms = [
         'raw.raw.unsupported_network']
    permissions.check_permissions(irc, source, perms)
    args = ' '.join(args)
    if not args.strip():
        irc.reply('No text entered!')
        return
    log.debug('(%s) Sending raw text %r to IRC for %s', irc.name, args, irc.get_hostmask(source))
    irc.send(args)
    irc.reply('Done.')