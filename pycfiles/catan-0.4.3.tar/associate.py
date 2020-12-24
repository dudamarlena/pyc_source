# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/commands/associate.py
# Compiled at: 2015-03-18 13:43:44
from __future__ import absolute_import
import click
from catalyze import cli, client, git, project, output
from catalyze.helpers import environments, services

@cli.command(short_help='Associates a local repository with an environment')
@click.argument('env_label')
@click.argument('service_label', required=False, default=None)
@click.option('--remote', default='catalyze', help='The name of the git remote to be created.')
def associate(env_label, service_label, remote):
    """Associates the git repository in the current directory. This means that the service and environment IDs are stored locally, and a git remote is created (default name = "catalyze") so that code can be pushed, built, and deployed."""
    session = client.acquire_session()
    for env in environments.list(session):
        if env['data']['name'] == env_label:
            settings = {'token': session.token, 'user_id': session.user_id, 
               'environmentId': env['environmentId']}
            code_services = [ svc for svc in services.list(session, env['environmentId']) if svc['type'] == 'code' ]
            selected_service = None
            if len(code_services) == 0:
                output.error('No code service found for "%s" environment (%s)' % (env_label, env['environmentId']))
            elif service_label:
                for svc in code_services:
                    if svc['label'] == service_label:
                        selected_service = svc
                        break

                if selected_service is None:
                    output.error("No code service found with label '%s'. Labels found: %s" % (
                     service_label, (', ').join([ svc['label'] for svc in code_services ])))
            elif len(code_services) > 1:
                output.error('Found multiple code services. Must pass one specifically to associate with. Labels found: ' + (', ').join([ svc['label'] for svc in code_services ]))
            else:
                selected_service = code_services[0]
            if remote in git.remote_list():
                git.remote_remove(remote)
            git.remote_add(remote, selected_service['source'])
            settings['serviceId'] = selected_service['id']
            project.save_settings(settings)
            output.write('"%s" remote added.' % (remote,))
            return

    output.error('No environment with label "%s" found.' % (env_label,))
    return


@cli.command()
def disassociate():
    """Remove association with environment"""
    project.clear_settings()
    output.write('Association cleared.')