# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/simon/Workspace/flask-init/flask_init/commands.py
# Compiled at: 2017-07-26 10:53:37
# Size of source mod 2**32: 1037 bytes
import os, click, flask_init
from flask_init.helper import creator
simple_module_name = 'templates/simple'
single_module_name = 'templates/single_module'

@click.command()
@click.argument('project-name')
@click.option('--simple', is_flag=True)
@click.option('--single-module', is_flag=True)
@click.option('--package', is_flag=True)
@click.option('--blueprints', is_flag=True)
def cli(project_name, simple, single_module, package, blueprints):
    """
    Easy way to create Flask Web application. You can use below option with flask init::
        
        --simple-module
        --single-module
    """
    project_path = None
    if project_name:
        if simple or single_module or package or blueprints:
            project_path = os.path.join(os.getcwd(), project_name)
            if not os.path.isdir(project_path):
                os.mkdir(project_path)
    else:
        if single_module:
            creator(single_module_name, project_path)
        else:
            creator(simple_module_name, project_path)