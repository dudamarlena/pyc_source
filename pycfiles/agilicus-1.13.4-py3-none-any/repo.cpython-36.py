# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/agiletoolkit/repo.py
# Compiled at: 2019-07-05 03:51:03
# Size of source mod 2**32: 3189 bytes
import os, re
from dataclasses import dataclass
from urllib.parse import urlparse
from .manager import Manager
from .api import GithubApi, GithubException
from .slack import SlackIntegration
from . import utils

@dataclass
class Branches:
    dev: str = 'master'
    sandbox: str = 'deploy'


class RepoManager(Manager):

    def init(self):
        self.info = utils.gitrepo(self.path)
        SlackIntegration.add(self)

    def software_version(self):
        """Software version

        Requires the Makefile entry

        version:
            ....
        """
        return utils.version()

    def version(self):
        """Software version of the current repository
        """
        branches = self.branches()
        if self.info['branch'] == branches.sandbox:
            try:
                return self.software_version()
            except Exception as exc:
                raise utils.CommandError('Could not obtain repo version, do you have a makefile with version entry?\n%s' % exc)

        else:
            branch = self.info['branch'].lower()
            branch = re.sub('[^a-z0-9_-]+', '-', branch)
            return f"{branch}-{self.info['head']['id'][:8]}"

    def validate_version(self, prefix='v'):
        """Validate version by checking if it is a valid semantic version
        and its value is higher than latest github tag
        """
        version = self.software_version()
        repo = self.github_repo()
        repo.releases.validate_tag(version, prefix)
        return version

    def skip_build(self):
        """Check if build should be skipped
        """
        skip_msg = self.config.get('skip', '[ci skip]')
        return os.environ.get('CODEBUILD_BUILD_SUCCEEDING') == '0' or self.info['current_tag'] or skip_msg in self.info['head']['message']

    def can_release(self, target=None):
        if self.skip_build() or self.info['pr']:
            return False
        else:
            branch = self.info['branch']
            branches = self.branches()
            if branch not in (branches.dev, branches.sandbox):
                return False
            if target:
                if branch != getattr(branches, target):
                    return False
            if not target:
                target = 'sandbox' if branch == branches.sandbox else 'dev'
            if target == 'sandbox':
                try:
                    self.validate_version()
                except GithubException:
                    return False

            return True

    def github(self):
        return GithubApi()

    def branches(self):
        return self.get('branches', Branches)

    def target_from_branch(self):
        branches = self.branches()
        if self.info['branch'] == branches.dev:
            return 'dev'
        else:
            return 'sandbox'

    def github_repo(self) -> str:
        url = self.info['remotes'][0]['url']
        if url.startswith('git@'):
            url = url.split(':')
            assert url[0] == 'git@github.com'
            path = url[1]
        else:
            path = urlparse(url).path[1:]
        bits = path.split('.')
        bits.pop()
        return self.github().repo('.'.join(bits))