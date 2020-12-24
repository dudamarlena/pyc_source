# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/commands/worker.py
# Compiled at: 2015-03-18 13:43:44
from __future__ import absolute_import
import click
from catalyze import cli, client, project, output
from catalyze.helpers import services

@cli.command(short_help='Start a background worker')
@click.argument('target', default='worker')
def worker(target):
    """Starts a Procfile target as a worker. Worker containers are intended to be short-lived, one-off tasks."""
    settings = project.read_settings()
    session = client.acquire_session(settings)
    output.write('Initiating a background worker for Service: %s (procfile target = "%s")' % (settings['serviceId'], target))
    services.initiate_worker(session, settings['environmentId'], settings['serviceId'], target)
    output.write('Worker started.')