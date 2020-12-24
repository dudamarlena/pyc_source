# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/commands/status.py
# Compiled at: 2015-05-27 11:10:17
from __future__ import absolute_import
import json
from catalyze import cli, client, project, output
from catalyze.helpers import environments, services

@cli.command(short_help='Quick status readout')
def status():
    """Check the status of the environment and every service in it."""
    settings = project.read_settings()
    session = client.acquire_session(settings)
    env = environments.retrieve(session, settings['environmentId'])
    output.write('environment state: ' + env['state'])
    codes = []
    noncodes = []
    for service in services.list(session, settings['environmentId']):
        if service['type'] != 'utility':
            if service['type'] == 'code':
                codes.append('\t%s (size = %s, build status = %s, deploy status = %s)' % (service['label'], service['size'], service['build_status'], service['deploy_status']))
            else:
                noncodes.append('\t%s (size = %s, image = %s, status = %s)' % (service['label'], service['size'], service['name'], service['deploy_status']))

    for item in codes + noncodes:
        output.write(item)