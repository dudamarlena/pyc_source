# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/feed2twitter/options.py
# Compiled at: 2008-09-23 11:31:57
from optparse import OptionParser
import sys

class Options(object):
    __module__ = __name__

    def __init__(self):
        self.parser = OptionParser()
        self.parser.add_option('-c', '--config', dest='config_filename', help='name of the file to read the settings', metavar='FILE')
        self.parser.add_option('-p', '--print_sample_config', action='store_true', dest='sample_config', default=False, help='print a sample config file and exit')

    def parse(self):
        (options, args) = self.parser.parse_args()
        if not options.config_filename and not options.sample_config:
            self.parser.print_help()
            sys.exit()
        return options