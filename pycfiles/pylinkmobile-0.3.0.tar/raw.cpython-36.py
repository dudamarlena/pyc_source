# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylinkirc/plugins/raw.py
# Compiled at: 2020-04-11 03:31:40
# Size of source mod 2**32: 1041 bytes
__doc__ = "\nraw.py: Provides a 'raw' command for sending raw text to IRC.\n"
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