# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apps/command/update.py
# Compiled at: 2010-06-15 14:56:04
import apps.command.base

class update(apps.command.base.Command):
    help = 'Check the remote dependencies and update them.'
    post_commands = ['generate']

    def run(self):
        self.update_deps()