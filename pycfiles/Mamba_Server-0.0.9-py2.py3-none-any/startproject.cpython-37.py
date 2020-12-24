# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/argos/Workspace/mamba-framework/mamba-server/mamba_server/commands/startproject.py
# Compiled at: 2020-05-13 09:04:25
# Size of source mod 2**32: 978 bytes
import os
from mamba_server.commands import MambaCommand

class Command(MambaCommand):

    @staticmethod
    def syntax():
        return '<project_name>'

    @staticmethod
    def short_desc():
        return 'Create new project'

    @staticmethod
    def run(args, opts, mamba_dir):
        project_name = args[0]
        os.mkdir(project_name)
        with open(os.path.join(project_name, 'mamba.cfg'), 'w') as (fp):
            pass
        os.mkdir(os.path.join(project_name, 'components'))
        with open(os.path.join(project_name, 'components', '__init__.py'), 'w') as (fp):
            pass
        os.mkdir(os.path.join(project_name, 'components', 'drivers'))
        os.mkdir(os.path.join(project_name, 'components', 'gui'))
        print('New Mamba project created in: {}'.format(project_name))
        print('You can create your first component with:')
        print('    cd %s' % project_name)
        print('    mamba gencomponent example')