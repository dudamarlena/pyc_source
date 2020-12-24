# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/botlib/options.py
# Compiled at: 2008-08-09 12:39:34
"""Parse command line options."""
from __future__ import with_statement
__metaclass__ = type
__all__ = [
 'parseargs']
from optparse import OptionParser
from botlib import version
from botlib.i18n import _

def parseargs():
    parser = OptionParser(version='The Python Replybot v%s' % version.__version__, usage=_('%prog [options] [key val [key val ...]]\n\nSend an automatic reply to a message posted to an email address.\n\nThis script sends a reply to a message taken from standard input.  The reply\ntext is fetched from a url specified in a configuration file and cached for a\ncertain amount of time to reduce network traffic.\n\nThe reply text uses $variable expansions as described here:\n\nhttp://www.python.org/doc/current/lib/node40.html\n\nSubstitution variables are taken from the RFC 2822 headers of the original\nmessage (coerced to lower case) and the optional case-sensitive key/value\npairs provided on the command line.'))
    parser.add_option('-C', '--configuration', metavar='FILE', help=_('The configuration file to use, otherwise search for the file in this order:\nreplybot.cfg in the directory containing the replybot script, replybot.cfg in\na sibling etc directory to the directory where this script lives\n(i.e. ../etc/replybot.cfg), the system file /etc/replybot.cfg.  If no\nconfiguration file is found and this option is not given, an error occurs.\nSee the file replybot.cfg.sample in the source distribution for details.'))
    parser.add_option('-s', '--selector', action='store', default='DEFAULT', metavar='SECTION', help='SECTION chooses and override section in the configuration file.  Without this,\nonly the DEFAULT section values will be used.')
    parser.add_option('-p', '--purge-cache', default=[], metavar='CHOICES', action='append', choices=('notices',
                                                                                                      'replies',
                                                                                                      'whitelist',
                                                                                                      'all'), help=_("This option purges certain information in the replybot's database.  You can\nhave multiple purge options on the command line.  After a purge, replybot\nexits.  Here are the options: `notices' purges the cache of reply messages;\n`replies' purges the last reply dates for all recipients; `whitelist' purges\nall whitelist flags; `all' combines all the previous purge options."))
    parser.add_option('-w', '--add-whitelist', default=[], metavar='PATTERN', action='append', help=_('Add a pattern to the whitelist; the pattern can either be an explicit address,\nor it can be a regular expression.  Put a ^ at the front of PATTERN to\nindicate a regular expression.  Whitelisted addresses will never get an\nautoreply.  Multiple -w options can be provided, or use -W to provide a file\nof patterns to whitelist.  After processing this option, replybot exits.'))
    parser.add_option('-W', '--whitelist-file', action='store', metavar='FILE', default=None, help=_('Add all the patterns in the file to the whitelist.  Whitelisted addresses will\nnever get an autoreply.  Patterns in this file must appear one-per line, and\ncan be in either form accepted by email.Utils.parseaddr(), or prepend the line\nwith a ^ to indicate a regular expression.  After processing this option,\nreplybot exits.'))
    parser.add_option('-d', '--debug', default=False, action='store_true', help=_('Put replybot in debug mode.  Everything works except that autoreply emails are\nnever actually sent.'))
    parser.add_option('-t', '--testing', default=False, action='store_true', help=_("Put replybot in testing mode.  This enables some extra functionality, such as\npositive replies being sent to messages with an `X-Ack: Yes' header."))
    (options, arguments) = parser.parse_args()
    if len(arguments) % 2:
        parser.error(_('Odd number of key/value pairs'))
    keywords = dict(zip(arguments[::2], arguments[1::2]))
    return (parser, options, arguments, keywords)