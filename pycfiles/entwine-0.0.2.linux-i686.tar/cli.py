# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/entwine/cli.py
# Compiled at: 2008-03-13 16:09:49
"""

cli.py
======

Desc: Command-line tool for querying twine.com

Author: Rob Cakebread <cakebread a t gmail.com>

License : New BSD (See COPYING)

"""
__docformat__ = 'restructuredtext'
__revision__ = '$Revision: 180 $'[11:-1].strip()
import sys, optparse, logging, urllib2
from entwine.entwinelib import get_profile, parse_profile
from entwine.utils import get_rcfile_path
from entwine.__init__ import __version__ as VERSION

class Entwine(object):
    """
    Main class for entwine
    """

    def __init__(self):
        self.options = None
        self.logger = logging.getLogger('entwine')
        return

    def set_log_level(self):
        """
        Set log level according to command-line options

        @returns: logger object
        """
        if self.options.debug:
            self.logger.setLevel(logging.DEBUG)
        elif self.options.quiet:
            self.logger.setLevel(logging.ERROR)
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        return self.logger

    def run(self):
        """
        Perform actions based on CLI options
        
        @returns: status code
        """
        opt_parser = setup_opt_parser()
        (self.options, remaining_args) = opt_parser.parse_args()
        self.set_log_level()
        if len(sys.argv) == 1 or len(remaining_args) > 2:
            opt_parser.print_help()
            return 2
        if self.options.profile:
            self.profile(self.options.profile, self.options.raw)
            return
        elif self.options.version:
            self.entwine_version()
        else:
            opt_parser.print_help()

    def profile(self, username, raw):
        """Print a user's profile to stdout"""
        if raw:
            try:
                print get_profile(username).read()
            except urllib2.HTTPError, errmsg:
                self.handle_error(errmsg)

        else:
            try:
                parse_profile(get_profile(username))
            except urllib2.HTTPError, errmsg:
                self.handle_error(errmsg)

    def handle_error(self, errmsg):
        self.logger.error(errmsg)
        if 'Wrong userid or password' in str(errmsg):
            print 'Make sure your username and password are correct in %s' % get_rcfile_path()
        else:
            self.logger.error('Profile not found.')

    def entwine_version(self):
        """
        Show entwine's version

        @returns: 0
        """
        self.logger.info('entwine version %s (rev. %s)' % (
         VERSION, __revision__))
        return 0


def setup_opt_parser():
    """
    Setup the optparser

    @returns: opt_parser.OptionParser
    
    """
    usage = 'usage: %prog [options]'
    opt_parser = optparse.OptionParser(usage=usage)
    opt_parser.add_option('--version', action='store_true', dest='entwine_version', default=False, help='Show entwine version and exit.')
    opt_parser.add_option('--debug', action='store_true', dest='debug', default=False, help='Show debugging information.')
    opt_parser.add_option('-q', '--quiet', action='store_true', dest='quiet', default=False, help='Show less output.')
    opt_parser.add_option('-p', '--profile', action='store', dest='profile', metavar='username', default=False, help="Show user's information.")
    opt_parser.add_option('--raw', action='store_true', dest='raw', default=False, help='Show output in raw RDF.')
    return opt_parser


def main():
    """
    Let's do it.
    """
    my_entwine = Entwine()
    my_entwine.run()


if __name__ == '__main__':
    sys.exit(main())