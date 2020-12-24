# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/repositories.py
# Compiled at: 2018-07-31 04:26:56
from __future__ import unicode_literals
import logging, os, appdirs
from reviewbot.config import config
from reviewbot.utils.filesystem import make_tempdir
from reviewbot.utils.process import execute
repositories = {}

class Repository(object):
    """A repository."""

    def sync(self):
        """Sync the latest state of the repository."""
        pass


class GitRepository(Repository):
    """A git repository."""

    def __init__(self, name, clone_path):
        """Initialize the repository.

        Args:
            name (unicode):
                The configured name of the repository.

            clone_path (unicode):
                The path of the git remote to clone.
        """
        self.name = name
        self.clone_path = clone_path
        self.repo_path = os.path.join(appdirs.site_data_dir(b'reviewbot'), b'repositories', name)

    def sync(self):
        """Sync the latest state of the repository."""
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
            logging.info(b'Cloning repository %s to %s', self.clone_path, self.repo_path)
            execute([b'git', b'clone', b'--bare', self.clone_path,
             self.repo_path])
        else:
            logging.info(b'Fetching into existing repository %s', self.repo_path)
            execute([b'git', b'--git-dir=%s' % self.repo_path, b'fetch',
             b'origin', b'+refs/heads/*:refs/heads/*', b'--prune'])

    def checkout(self, commit_id):
        """Check out the given commit.

        Args:
            commit_id (unicode):
                The ID of the commit to check out.

        Returns:
            unicode:
            The name of a directory with the given checkout.
        """
        workdir = make_tempdir()
        branchname = b'br-%s' % commit_id
        logging.info(b'Creating temporary branch for clone in repo %s', self.repo_path)
        execute([b'git', b'--git-dir=%s' % self.repo_path, b'branch', branchname,
         commit_id])
        logging.info(b'Creating working tree for commit ID %s in %s', commit_id, workdir)
        execute([b'git', b'clone', b'--local', b'--depth', b'1',
         b'--branch', branchname, self.repo_path, workdir])
        logging.info(b'Removing temporary branch for clone in repo %s', self.repo_path)
        execute([b'git', b'--git-dir=%s' % self.repo_path, b'branch', b'-d',
         branchname])
        return workdir


class HgRepository(Repository):
    """A hg repository."""

    def __init__(self, name, clone_path):
        """Initialize the repository.

        Args:
            name (unicode):
                The configured name of the repository.

            clone_path (unicode):
                The path of the hg repository to clone.
        """
        self.name = name
        self.clone_path = clone_path
        self.repo_path = os.path.join(appdirs.site_data_dir(b'reviewbot'), b'repositories', name)

    def sync(self):
        """Sync the latest state of the repository."""
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
            logging.info(b'Cloning repository %s to %s', self.clone_path, self.repo_path)
            execute([b'hg', b'clone', b'-U', self.clone_path,
             self.repo_path])
        else:
            logging.info(b'Pulling into existing repository %s', self.repo_path)
            execute([b'hg', b'-R', self.repo_path, b'pull'])

    def checkout(self, commit_id):
        """Check out the given commit.

        Args:
            commit_id (unicode):
                The ID of the commit to check out.

        Returns:
            unicode:
            The name of a directory with the given checkout.
        """
        workdir = make_tempdir()
        logging.info(b'Creating working tree for commit ID %s in %s', commit_id, workdir)
        execute([b'hg', b'-R', self.repo_path, b'archive', b'-r', commit_id,
         b'-t', b'files', workdir])
        return workdir


def init_repositories():
    """Set up configured repositories."""
    global repositories
    for repository in config[b'repositories']:
        repo_name = repository[b'name']
        repo_type = repository.get(b'type')
        if repo_type == b'git':
            repositories[repo_name] = GitRepository(repo_name, repository[b'clone_path'])
        elif repo_type == b'hg':
            repositories[repo_name] = HgRepository(repo_name, repository[b'clone_path'])
        else:
            logging.error(b'Unknown type "%s" for configured repository %s', repo_type, repo_name)