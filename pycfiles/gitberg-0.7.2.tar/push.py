# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/push.py
# Compiled at: 2019-01-01 15:58:55
"""
Syncs a local git book repo to a remote git repo (by default, github)
"""
import base64, datetime, logging, re
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import git, github3, requests, semver
from . import config
from .parameters import GITHUB_ORG, ORG_HOMEPAGE
logger = logging.getLogger(__name__)

class GithubRepo:

    def __init__(self, book):
        self.org_name = GITHUB_ORG
        self.org_homepage = ORG_HOMEPAGE
        self.book = book
        self._repo_token = None
        self._github_token = None
        if not config.data:
            config.ConfigFile()
        self.create_api_handler()
        return

    @property
    def repo_id(self):
        return ('{}/{}').format(self.org_name, self.book.meta._repo)

    def push(self):
        self.book.local_repo.git.remote('origin').push(self.book.local_repo.git.refs.master, tags=True)

    def create_and_push(self):
        self.create_repo()
        origin = self.add_remote_origin_to_local_repo()
        origin.push(self.book.local_repo.git.refs.master)

    def update(self, message):
        self.book.local_repo.update(message)
        self.push()

    def tag(self, version, message=''):
        if version == 'bump' or not version:
            old_version = self.book.meta._version
            if old_version:
                version = old_version
            else:
                version = '0.0.1'
        while version in self.book.local_repo.git.tags:
            version = semver.bump_patch(version)

        self.book.meta.metadata['_version'] = version
        self.book.save_meta()
        self.update(('tag: {}. {}').format(version, message))
        ref = self.book.local_repo.tag(version)
        self.push()
        logger.info('tagged and pushed ' + str(ref))

    def create_api_handler(self):
        """ Creates an api handler and sets it on self """
        try:
            self.github = github3.login(username=config.data['gh_user'], password=config.data['gh_password'])
        except KeyError as e:
            raise config.NotConfigured(e)

        logger.info(('ratelimit remaining: {}').format(self.github.ratelimit_remaining))
        if hasattr(self.github, 'set_user_agent'):
            self.github.set_user_agent(('{}: {}').format(self.org_name, self.org_homepage))
        try:
            self.org = self.github.organization(self.org_name)
        except github3.GitHubError:
            logger.error('Possibly the github ratelimit has been exceeded')
            logger.info('ratelimit: ' + str(self.github.ratelimit_remaining))

    def format_desc(self):
        if hasattr(self.book, 'meta'):
            title = re.sub('[\\r\\n \\t]+', ' ', self.book.meta.title)
            author = (' by {}').format(self.book.meta.authors_short())
        else:
            title = self.book.repo_name
            author = ''
        return ('{0}{1} is a Project Gutenberg book, now on Github.').format(title, author)

    def create_repo(self):
        try:
            self.repo = self.org.create_repository(self.book.repo_name, description=self.format_desc(), homepage=self.org_homepage, private=False, has_issues=True, has_wiki=False)
        except github3.GitHubError as e:
            logger.warning(('repo already created?: {}').format(e))
            self.repo = self.github.repository(self.org_name, self.book.repo_name)

    def update_repo(self):
        try:
            self.repo = self.github.repository(self.org_name, self.book.repo_name)
            self.repo.edit(self.book.repo_name, description=self.format_desc(), homepage=self.org_homepage, private=False, has_issues=True, has_wiki=False, has_downloads=True)
        except github3.GitHubError as e:
            logger.warning(("couldn't edit repo: {}").format(e))

    def add_remote_origin_to_local_repo(self):
        try:
            origin = self.book.local_repo.git.create_remote('origin', self.repo.ssh_url)
        except git.exc.GitCommandError:
            logger.warning('We may have already added a remote origin to this repo')
            return self.book.local_repo.git.remote('origin')

        return origin

    def github_token(self):
        if self._github_token is not None:
            return self._github_token
        else:
            token = github3.authorize(config.data['gh_user'], config.data['gh_password'], scopes=('read:org',
                                                                                                  'user:email',
                                                                                                  'repo_deployment',
                                                                                                  'repo:status',
                                                                                                  'write:repo_hook'), note=token_note)
            self._github_token = token.token
            return self._github_token

    def repo_token(self):
        if self._repo_token is not None:
            return self._repo_token
        else:
            token_note = ('automatic releases for {} {}').format(self.repo_id, datetime.datetime.utcnow().isoformat())
            token = github3.authorize(config.data['gh_user'], config.data['gh_password'], scopes='public_repo', note=token_note)
            self._repo_token = token.token
            return self._repo_token