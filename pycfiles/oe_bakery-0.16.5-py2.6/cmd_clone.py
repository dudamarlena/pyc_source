# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oebakery/cmd_clone.py
# Compiled at: 2010-01-25 03:42:28
import optparse, sys, os, oebakery
from oebakery.cmd_update import UpdateCommand

class CloneCommand:

    def __init__(self, argv):
        parser = optparse.OptionParser('Usage: oe clone [options]* <repository> [directory]\n\n  Clone OE Bakery development environment into a new directory.\n\nArguments:\n  file        bakery configuration file (remote URL or local file)\n  directory   directory to clone into (default is current directory)')
        (options, args) = parser.parse_args(argv)
        if len(args) < 1:
            parser.error('too few arguments')
        if len(args) > 2:
            parser.error('too many arguments')
        self.repository = args[0]
        if len(args) == 2:
            self.directory = args[1]
        else:
            self.directory = os.path.basename(self.repository)
            if self.directory[-4:] == '.git':
                self.directory = self.directory[:-4]
        self.options = options

    def run(self):
        if not oebakery.call('git clone %s %s' % (self.repository,
         self.directory)):
            return
        topdir = oebakery.set_topdir(self.directory)
        oebakery.chdir(self.directory)
        if not oebakery.call('git config push.default tracking'):
            print 'Failed to set push.default = tracking'
        config = oebakery.read_config()
        oebakery.copy_local_conf_sample(config.get('bitbake', 'confdir'))
        self.update_cmd = UpdateCommand(config)
        return self.update_cmd.run()