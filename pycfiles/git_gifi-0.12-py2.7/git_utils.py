# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gifi/utils/git_utils.py
# Compiled at: 2017-06-05 05:18:54
from gifi.command import CommandException
from git import Repo, InvalidGitRepositoryError

def get_current_branch(repo):
    current_branch = repo.git.rev_parse('--abbrev-ref', 'HEAD')
    return current_branch


def check_repo_is_clean(repo):
    if repo.is_dirty():
        raise CommandException('Please commit all untracked files.')


def get_repo(repo=None):
    """

    :rtype : git.Repo
    """
    if repo is None:
        try:
            repo = Repo('.')
        except InvalidGitRepositoryError:
            raise CommandException('To run this command you need to be in git source code directory.')

    return repo


def get_remote_url(remote, repo=None):
    repo = get_repo(repo)
    config_reader = repo.config_reader()
    remote_url = config_reader.get_value('remote "%s"' % remote, 'url')
    config_reader.release()
    return remote_url


def get_from_last_commit_message(repo, item_header):
    item_header = item_header + ':'
    commit_message_lines = repo.head.commit.message.split('\n')
    lines_with_item = [ e for e in commit_message_lines if e.lower().startswith(item_header.lower()) ]
    items = map(lambda e: e[len(item_header):].split(','), lines_with_item)
    items = [ item.strip() for sub_list in items for item in sub_list ]
    return items