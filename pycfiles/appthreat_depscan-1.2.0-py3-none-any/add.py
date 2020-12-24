# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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