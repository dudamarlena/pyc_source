# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/dotcloud/ui/parser.py
# Compiled at: 2012-09-19 14:56:08
import argparse, sys
from .version import VERSION
from ..packages.bytesconverter import human2bytes

class Parser(argparse.ArgumentParser):

    def error(self, message):
        print >> sys.stderr, ('error: {0}').format(message)
        self.print_help()
        sys.exit(1)


class ScaleOperation(object):

    def __init__(self, kv):
        if kv.startswith('=') or kv.count('=') != 1:
            raise argparse.ArgumentTypeError(('Invalid action "{0}"').format(kv))
        (k, v) = kv.split('=')
        if not v:
            raise argparse.ArgumentTypeError(('Invalid value for "{0}"').format(k))
        if ':' in k:
            (self.name, self.action) = k.split(':', 1)
        else:
            self.name, self.action = k, 'instances'
        if self.action not in ('instances', 'memory'):
            raise argparse.ArgumentTypeError(('Invalid action for "{0}": Action must be either "instances" or "memory"').format(self.action))
        if self.action == 'instances':
            try:
                self.original_value = int(v)
                self.value = int(v)
            except ValueError:
                raise argparse.ArgumentTypeError(('Invalid value for "{0}": Instance count must be a number').format(kv))

        elif self.action == 'memory':
            self.original_value = v
            v = v.upper()
            if v.endswith('B'):
                v = v[:-1]
            if v.isdigit():
                self.value = int(v)
            else:
                try:
                    self.value = human2bytes(v)
                except Exception:
                    raise argparse.ArgumentTypeError(('Invalid value for "{0}"').format(kv))


def validate_env(kv):
    if kv.find('=') in (-1, 0):
        raise argparse.ArgumentTypeError(('"{0}" is an invalid environment variable expresion. Environment variables are set like "foo=bar".').format(kv))
    return kv


def get_parser(name='dotcloud'):
    common_parser = Parser(prog=name, add_help=False)
    common_parser.add_argument('--application', '-A', help='Specify the application')
    connect_options_parser = Parser(prog=name, add_help=False)
    rsync_or_dvcs = connect_options_parser.add_mutually_exclusive_group()
    rsync_or_dvcs.add_argument('--rsync', action='store_true', help='Always use rsync to push (default)')
    rsync_or_dvcs.add_argument('--git', action='store_true', help='Always use git to push')
    rsync_or_dvcs.add_argument('--hg', action='store_true', help='Always use mercurial to push')
    connect_options_parser.add_argument('--branch', '-b', metavar='NAME', help='Always use this branch when pushing via DVCS. (If not set, each push will use the active branch by default)')
    parser = Parser(prog=name, description='dotcloud CLI', parents=[
     common_parser])
    parser.add_argument('--version', '-v', action='version', version=('dotcloud/{0}').format(VERSION))
    subcmd = parser.add_subparsers(dest='cmd')
    subcmd.add_parser('setup', help='Setup the client authentication')
    subcmd.add_parser('check', help='Check the installation and authentication')
    subcmd.add_parser('list', help='List all applications')
    connect = subcmd.add_parser('connect', help='Connect a local directory to an existing application', parents=[
     connect_options_parser])
    connect.add_argument('application', help='Specify the application')
    subcmd.add_parser('disconnect', help='Disconnect the current directory from its application')
    create = subcmd.add_parser('create', help='Create a new application', parents=[
     connect_options_parser])
    create.add_argument('--flavor', '-f', default='sandbox', help='Choose a flavor for your application. Defaults to sandbox.')
    create.add_argument('application', help='Specify the application')
    destroy = subcmd.add_parser('destroy', help='Destroy an existing app', parents=[
     common_parser])
    destroy.add_argument('service', nargs='?', help='Specify the service')
    subcmd.add_parser('app', help='Display the application name connected to the current directory')
    activity = subcmd.add_parser('activity', help='Display your recent activity', parents=[
     common_parser])
    activity.add_argument('--all', '-a', action='store_true', help='Print out your activities among all your applications rather than the currently connected or selected one. (This is the default behavior when not connected to any application.)')
    info = subcmd.add_parser('info', help='Get information about the application or service', parents=[
     common_parser])
    info.add_argument('service', nargs='?', help='Specify the service')
    url = subcmd.add_parser('url', help='Display the URL(s) for the application', parents=[
     common_parser])
    url.add_argument('service', nargs='?', help='Specify the service')
    status = subcmd.add_parser('status', help='Probe the status of a service', parents=[
     common_parser])
    status.add_argument('service', help='Specify the service')
    open_ = subcmd.add_parser('open', help='Open the application in the browser', parents=[
     common_parser])
    open_.add_argument('service', nargs='?', help='Specify the service')
    run = subcmd.add_parser('run', help='Open a shell or run a command inside a service instance', parents=[
     common_parser])
    run.add_argument('service_or_instance', help='Open a shell or run the command on the first instance of a given service (ex: www) or a specific one (ex: www.1)')
    run.add_argument('command', nargs='?', help="The command to execute on the service's instance. If not specified, open a shell.")
    run.add_argument('args', nargs=argparse.REMAINDER, metavar='...', help='Any arguments to the command')
    push = subcmd.add_parser('push', help='Push the code', parents=[common_parser])
    push.add_argument('path', nargs='?', default=None, help='Path to the directory to push (by default "./")')
    push.add_argument('--clean', action='store_true', help='Do a full build (rather than incremental)')
    rsync_or_dvcs = push.add_mutually_exclusive_group()
    rsync_or_dvcs.add_argument('--rsync', action='store_true', help='Use rsync to push (default)')
    rsync_or_dvcs.add_argument('--git', action='store_true', help='Use git to push')
    rsync_or_dvcs.add_argument('--hg', action='store_true', help='Use mercurial to push')
    branch_or_commit = push.add_mutually_exclusive_group()
    branch_or_commit.add_argument('--branch', '-b', metavar='NAME', help='Specify the branch to push when pushing via DVCS (by default, use the active one)')
    branch_or_commit.add_argument('--commit', '-c', metavar='HASH', help='Specify the commit hash to push when pushing via DVCS (by default, use the latest one)')
    deploy = subcmd.add_parser('deploy', help='Deploy a specific version', parents=[
     common_parser])
    deploy.add_argument('revision', help='Revision to deploy (Symbolic revisions "latest" and "previous" are supported)')
    deploy.add_argument('--clean', action='store_true', help='If a build is needed, do a full build (rather than incremental)')
    subcmd.add_parser('dlist', help='List recent deployments', parents=[common_parser])
    dlogs = subcmd.add_parser('dlogs', help='Review past deployments or watch one in-flight', parents=[
     common_parser])
    dlogs.add_argument('deployment_id', help='Which recorded deployment to view (discoverable with the command, "dotcloud dlist") or "latest".')
    dlogs.add_argument('service_or_instance', nargs='?', help='Filter logs by a given service (ex: www) or a specific instance (ex: www.0). ')
    dlogs.add_argument('--no-follow', '-N', action='store_true', help='Do not follow real-time logs')
    dlogs.add_argument('--lines', '-n', type=int, metavar='N', help='Tail only N logs (before following real-time logs by default)')
    logs = subcmd.add_parser('logs', help='View your application logs or watch logs live', parents=[
     common_parser])
    logs.add_argument('service_or_instance', nargs='*', help='Display only logs of a given service (ex: www) or a specific instance (ex: www.1)')
    logs.add_argument('--no-follow', '-N', action='store_true', help='Do not follow real-time logs')
    logs.add_argument('--lines', '-n', type=int, metavar='N', help='Tail only N logs (before following real-time logs by default)')
    var = subcmd.add_parser('env', help='Manipulate application environment variables', parents=[
     common_parser]).add_subparsers(dest='subcmd')
    var.add_parser('list', help='List the application environment variables', parents=[
     common_parser])
    var_set = var.add_parser('set', help='Set application environment variables', parents=[
     common_parser])
    var_set.add_argument('variables', help='Application environment variables to set', metavar='key=value', nargs='+', type=validate_env)
    var_unset = var.add_parser('unset', help='Unset (remove) application environment variables', parents=[
     common_parser])
    var_unset.add_argument('variables', help='Application environment variables to unset', metavar='var', nargs='+')
    scale = subcmd.add_parser('scale', help='Scale services', description='Manage horizontal (instances) or vertical (memory) scaling of services', parents=[
     common_parser])
    scale.add_argument('services', nargs='+', metavar='service:action=value', help='Scaling action to perform e.g. www:instances=2 or www:memory=1gb', type=ScaleOperation)
    restart = subcmd.add_parser('restart', help='Restart a service instance', parents=[
     common_parser])
    restart.add_argument('instance', help='Restart the first instance of a given service (ex: www) or a specific one (ex: www.1)')
    domain = subcmd.add_parser('domain', help='Manage domains for the service', parents=[
     common_parser]).add_subparsers(dest='subcmd')
    domain.add_parser('list', help='List the domains', parents=[common_parser])
    domain_add = domain.add_parser('add', help='Add a new domain', parents=[common_parser])
    domain_add.add_argument('service', help='Service to set domain for')
    domain_add.add_argument('domain', help='New domain name')
    domain_rm = domain.add_parser('rm', help='Remove a domain', parents=[common_parser])
    domain_rm.add_argument('service', help='Service to remove the domain from')
    domain_rm.add_argument('domain', help='Domain name to remove')
    revisions = subcmd.add_parser('revisions', help='Display all the knowns revision of the application', parents=[
     common_parser])
    return parser