# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apps/command/update.py
# Compiled at: 2010-06-15 14:56:04
import apps.command.base

class update(apps.command.base.Command):
    help = 'Check the remote dependencies and update them.'
    post_commands = ['generate']

    def run(self):
        self.update_deps()