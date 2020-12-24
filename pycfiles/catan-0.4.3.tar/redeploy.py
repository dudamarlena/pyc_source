# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/commands/redeploy.py
# Compiled at: 2015-03-18 13:43:44
from __future__ import absolute_import
from catalyze import cli, client, config, project, output
from catalyze.helpers import services
import click

@cli.command(short_help='Redeploy without pushing')
def redeploy():
    """Redeploy an environment's service manually."""
    settings = project.read_settings()
    session = client.acquire_session(settings)
    service_id = settings['serviceId']
    output.write('Redeploying ' + service_id)
    services.redeploy(session, settings['environmentId'], service_id)
    output.write('Redeploy successful, check status and logs for updates')