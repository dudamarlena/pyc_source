# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/pyami/scriptbase.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1427 bytes
import os, sys
from boto.utils import ShellCommand, get_ts
import boto, boto.utils

class ScriptBase(object):

    def __init__(self, config_file=None):
        self.instance_id = boto.config.get('Instance', 'instance-id', 'default')
        self.name = self.__class__.__name__
        self.ts = get_ts()
        if config_file:
            boto.config.read(config_file)

    def notify(self, subject, body=''):
        boto.utils.notify(subject, body)

    def mkdir(self, path):
        if not os.path.isdir(path):
            try:
                os.mkdir(path)
            except:
                boto.log.error('Error creating directory: %s' % path)

    def umount(self, path):
        if os.path.ismount(path):
            self.run('umount %s' % path)

    def run(self, command, notify=True, exit_on_error=False, cwd=None):
        self.last_command = ShellCommand(command, cwd=cwd)
        if self.last_command.status != 0:
            boto.log.error('Error running command: "%s". Output: "%s"' % (command, self.last_command.output))
            if notify:
                self.notify('Error encountered', 'Error running the following command:\n\t%s\n\nCommand output:\n\t%s' % (
                 command, self.last_command.output))
            if exit_on_error:
                sys.exit(-1)
        return self.last_command.status

    def main(self):
        pass