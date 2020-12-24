# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/simon/Workspace/flask-init/flask_init/helper.py
# Compiled at: 2017-07-26 08:00:30
# Size of source mod 2**32: 1038 bytes
import os, click, flask_init
from jinja2 import Environment, PackageLoader

def creator(project_type, project_path):
    click.echo(project_type)
    click.echo(project_path)
    module_path = os.path.join(os.path.dirname(flask_init.__file__), project_type)
    environment = Environment(loader=(PackageLoader('flask_init', project_type)))
    for temp in environment.list_templates():
        template = environment.get_template(temp)
        parsed_template = template.render()
        file_name = template.name.split('-tpl')[0]
        distination_file = os.path.join(project_path, file_name)
        os.makedirs((os.path.dirname(distination_file)), exist_ok=True)
        with open(distination_file, 'w') as (f):
            f.write(parsed_template + '\n')