# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/botlib/main.py
# Compiled at: 2008-08-09 12:39:34
"""The main function for the command line script."""
__metaclass__ = type
__all__ = [
 'main']
import os, sys, email, random, sqlite3, logging
from email.utils import parseaddr
from botlib import botlog
from botlib.configuration import config
from botlib.database import Database
from botlib.i18n import _
from botlib.options import parseargs
from botlib.reply import do_reply
log = logging.getLogger('replybot')
PROGRAM = sys.argv[0]

def main():
    (parser, options, arguments, keywords) = parseargs()
    config.parser = parser
    config.options = options
    config.arguments = arguments
    config.keywords = keywords
    if options.configuration is None:
        bindir = os.path.dirname(PROGRAM)
        files = [
         os.path.join(bindir, 'replybot.cfg'),
         os.path.join(os.path.dirname(bindir), 'etc', 'replybot.cfg'),
         '/etc/replybot.cfg']
        for filename in files:
            if os.path.exists(filename):
                config.load(filename, options.selector)
                break
        else:
            raise RuntimeError('No configuration file found; use -C')
    else:
        config.load(options.configuration, options.selector)
    botlog.initialize()
    config.db = database = Database(config.database_url)
    if options.purge_cache:
        database.do_purges(options.purge_cache)
        return 0
    if options.add_whitelist or options.whitelist_file:
        database.do_whitelist(options.add_whitelist, options.whitelist_file)
        return 0
    if config.reply_url is None:
        parser.error(_('--reply-url is required'))
    msg = email.message_from_file(sys.stdin)
    try:
        database.process_message(msg)
    except:
        log.exception('process_message() failed')
        raise

    return