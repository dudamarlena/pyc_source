# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/universalcore/unicore.distribute/unicore/distribute/scripts.py
# Compiled at: 2016-05-07 05:25:40
import os, argparse
from elasticgit.storage import StorageManager
from pyramid.paster import bootstrap
from pyramid.request import Request
from unicore.distribute.utils import get_repositories
from unicore.webhooks.events import WebhookEvent

class PollRepositories(object):
    notify = None

    def run(self, repo_dir, ini_file, base_url):
        request = Request.blank('/', base_url=base_url)
        env = bootstrap(ini_file, request=request)
        self.notify = env['registry'].notify
        for repo in get_repositories(repo_dir):
            self.pull_repo(env, repo)

        env['closer']()

    def pull_repo(self, env, repo):
        sm = StorageManager(repo)
        branch = repo.active_branch
        tracking_branch = branch.tracking_branch()
        if tracking_branch:
            remote_name = tracking_branch.remote_name
        else:
            remote_name = repo.remotes[0].name
        original_commit = branch.commit
        sm.pull(branch_name=branch.name, remote_name=remote_name)
        last_commit = branch.commit
        if original_commit.hexsha != last_commit.hexsha:
            name = os.path.basename(repo.working_dir)
            request = env['request']
            self.notify(WebhookEvent(owner=None, event_type='repo.push', payload={'repo': name, 
               'url': request.route_url('repositoryresource', name=name)}))
        return


def get_parser():
    parser = argparse.ArgumentParser(description='unicore.distribute command line tools.')
    subparser = parser.add_subparsers(help='Commands')
    command = subparser.add_parser('poll-repositories', help='poll repositories')
    command.add_argument('-d', '--repo-dir', dest='repo_dir', help='The directory with repositories.', default='./repos')
    command.add_argument('-i', '--ini-file', dest='ini_file', help="The project's ini file.", default='development.ini')
    command.add_argument('-u', '--base-url', dest='base_url', help="This server's public URL (for webhooks)", default='http://localhost/')
    command.set_defaults(dispatcher=PollRepositories)
    return parser


def run(parser):
    args = parser.parse_args()
    data = vars(args)
    dispatcher_class = data.pop('dispatcher')
    dispatcher = dispatcher_class()
    dispatcher.run(**data)


def main():
    parser = get_parser()
    run(parser)