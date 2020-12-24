# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/repo/github_tool.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 5255 bytes
import requests
from github import Github
from foxylib.tools.collections.collections_tool import IterTool

class GithubTool:

    class Config:
        TOKEN = 'token'
        OWNER = 'owner'
        REPOSITORY = 'repo'
        BRANCH = 'branch'
        TAG = 'tag'

    @classmethod
    def j_config2token(cls, j_config):
        return j_config[cls.Config.TOKEN]

    @classmethod
    def j_config2owner(cls, j_config):
        return j_config[cls.Config.OWNER]

    @classmethod
    def j_config2repository(cls, j_config):
        return j_config[cls.Config.REPOSITORY]

    @classmethod
    def j_config2branch(cls, j_config):
        return j_config[cls.Config.BRANCH]

    @classmethod
    def j_config2tag(cls, j_config):
        return j_config[cls.Config.TAG]

    @classmethod
    def j_config2github(cls, j_config):
        token = cls.j_config2token(j_config)
        assert token
        return Github(token)

    @classmethod
    def j_config2repo(cls, j_config):
        github = cls.j_config2github(j_config)
        owner = cls.j_config2owner(j_config)
        repository = cls.j_config2repository(j_config)
        return github.get_repo('/'.join([owner, repository]))

    @classmethod
    def release(cls, j_config):
        tag = cls.j_config2tag(j_config)
        assert tag
        branch = cls.j_config2branch(j_config)
        assert branch
        repo = cls.j_config2repo(j_config)
        j_response = repo.create_git_release(tag, tag, '', target_commitish=branch)
        return j_response

    @classmethod
    def repo2j_pr_list(cls, token, repo, j_payload):
        url = (repo.pulls_url.format)(**{'/number': ''})
        headers = {'Content-Type':'application/json', 
         'Authorization':'token {}'.format(token), 
         'Accept':'*/*', 
         'Cache-Control':'no-cache', 
         'Host':'api.github.com', 
         'Accept-Encoding':'gzip, deflate', 
         'Content-Length':'64', 
         'Connection':'keep-alive', 
         'cache-control':'no-cache'}
        response = requests.request('GET', url, json=j_payload, headers=headers)
        return response.json()

    @classmethod
    def j_pr2pull(cls, repo, j_pr):
        return repo.get_pull(j_pr['number'])

    @classmethod
    def pull2is_approved(cls, pull):
        reviews = pull.get_reviews()
        is_empty = IterTool.iter2is_empty(filter(lambda review: review.state == 'APPROVED', reviews))
        return not is_empty