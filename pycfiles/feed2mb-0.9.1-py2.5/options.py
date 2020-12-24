# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/feed2mb/options.py
# Compiled at: 2010-09-01 16:07:39
from optparse import OptionParser
import sys

class Options(object):

    def __init__(self):
        self.parser = OptionParser()
        self.parser.add_option('-c', '--config', dest='config_filename', help='name of the file to read the settings', metavar='FILE')
        self.parser.add_option('-l', '--log', dest='log_filename', default=False, help='name of the file to log the updates (otherwise, will be echoed in the terminal)', metavar='LOGFILE')
        self.parser.add_option('-p', '--print_sample_config', action='store_true', dest='sample_config', default=False, help='print a sample config file and exit')
        self.parser.add_option('-v', '--version', action='store_true', dest='show_version', default=False, help='Show the feed2mb version')

    def parse(self):
        (options, args) = self.parser.parse_args()
        if not options.config_filename and not options.sample_config and not options.show_version:
            self.parser.print_help()
            sys.exit()
        return options