# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oebakery/cmd_init.py
# Compiled at: 2010-01-22 10:22:52
import os, subprocess, socket, shutil, optparse, oebakery
from oebakery.cmd_update import UpdateCommand

class InitCommand:

    def __init__(self, argv=[]):
        parser = optparse.OptionParser('Usage: oe init [options]\n\n  Setup OE Bakery development environment in the current directory.')
        (self.options, self.args) = parser.parse_args(argv)
        self.config = oebakery.read_config()

    def run(self):
        topdir = oebakery.set_topdir(os.path.curdir)
        if not os.path.exists('.git'):
            if not oebakery.call('git init'):
                print 'Failed to initialize git'
                return
            if not oebakery.call('git config push.default tracking'):
                print 'Failed to set push.default = tracking'
        oebakery.copy_local_conf_sample(self.config.get('bitbake', 'confdir'))
        self.update_cmd = UpdateCommand(self.config)
        return self.update_cmd.run()