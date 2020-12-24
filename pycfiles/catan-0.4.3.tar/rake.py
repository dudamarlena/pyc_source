# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/commands/rake.py
# Compiled at: 2015-03-18 13:43:44
from __future__ import absolute_import
import click
from catalyze import cli, client, project, output
from catalyze.helpers import services

@cli.command(short_help='Execute a rake task')
@click.argument('task_name')
def rake(task_name):
    """Execute a rake task. This is only applicable to ruby-based applications."""
    settings = project.read_settings()
    session = client.acquire_session(settings)
    output.write(('Executing Rake Task: {}').format(task_name))
    resp = services.initiate_rake(session, settings['environmentId'], settings['serviceId'], task_name)
    output.write('Rake task output viewable in the logging server.')