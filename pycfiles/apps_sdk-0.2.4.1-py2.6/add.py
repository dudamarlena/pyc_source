# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apps/command/add.py
# Compiled at: 2010-08-17 19:03:01
import apps.command.base, logging, sys

class add(apps.command.base.Command):
    user_options = [
     ('file=', 'f', 'file to add', None)]
    post_commands = ['generate']
    help = 'Add an external dependency to the project.'

    def run(self):
        if not self.options.has_key('file'):
            logging.error('ERROR: Nothing to add. Specify a file to add using the --file flag.')
            sys.exit(1)
        self.add(self.options['file'].rsplit('/', 1)[(-1)], self.options['file'])