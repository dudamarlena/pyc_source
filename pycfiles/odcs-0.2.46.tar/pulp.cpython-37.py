# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/pulp.py
# Compiled at: 2019-03-25 05:56:58
# Size of source mod 2**32: 8108 bytes
import copy, json, requests
from odcs.server.mergerepo import MergeRepo
from odcs.server.utils import retry

class Pulp(object):
    __doc__ = 'Interface to Pulp'

    def __init__(self, server_url, username, password, compose):
        self.username = username
        self.password = password
        self.server_url = server_url
        self.compose = compose
        self.rest_api_root = '{0}/pulp/api/v2/'.format(self.server_url.rstrip('/'))

    @retry(wait_on=(requests.exceptions.RequestException))
    def _rest_post(self, endpoint, post_data):
        query_data = json.dumps(post_data)
        r = requests.post(('{0}{1}'.format(self.rest_api_root, endpoint.lstrip('/'))),
          query_data,
          auth=(
         self.username, self.password))
        r.raise_for_status()
        return r.json()

    def _try_arch_merge(self, content_set_repos):
        """
        Tries replacing arch string (e.g. "x86_64" or "ppc64le") in each "url"
        in content_set_repos with "$basearch" and if this results in the same
        repository URL for each repo in the content_set_repos and also
        the sigkeys are the same, returns the single repo with $basearch.
        If not, returns an empty dict.

        The "arches" value of returned repo is set to union of merged "arches".

        For example, for following input:
            [{"url": "http://localhost/x86_64/os", "arches": ["x86_64"]},
             {"url": "http://localhost/ppc64le/os", "arches": ["ppc64le"]}]
        This method returns:
            {"url": "http://localhost/$basearch/os",
             "arches": ["x86_64", "ppc64le"]}
        """
        if len(content_set_repos) < 2:
            return {}
        first_repo = None
        for repo in content_set_repos:
            if len(repo['arches']) != 1:
                raise ValueError('Content set repository %s does not have exactly 1 arch: %r.' % (
                 repo['url'], repo['arches']))
            url = repo['url'].replace(list(repo['arches'])[0], '$basearch')
            if first_repo is None:
                first_repo = copy.deepcopy(repo)
                first_repo['url'] = url
                continue
            if not first_repo['url'] != url:
                if first_repo['sigkeys'] != repo['sigkeys']:
                    return {}
                first_repo['arches'] = first_repo['arches'].union(repo['arches'])

        return first_repo

    def _merge_repos(self, content_set, content_set_repos):
        """
        Merges the repositories of the same arch from `content_set_repos`
        and returns the new repository dict pointing to the newly created
        merged repository.

        In case there is just single (or none) repository in
        `content_set_repos`, returns empty dict.
        """
        if len(content_set_repos) < 2:
            return {}
        per_arch_repos = {}
        for repo in content_set_repos:
            if len(repo['arches']) != 1:
                raise ValueError('Content set repository %s does not have exactly 1 arch: %r.' % (
                 repo['url'], repo['arches']))
            arch = list(repo['arches'])[0]
            if arch not in per_arch_repos:
                per_arch_repos[arch] = []
            per_arch_repos[arch].append(repo)

        merge_repo = MergeRepo(self.compose)
        for arch, repos in per_arch_repos.items():
            urls = [repo['url'] for repo in repos]
            merge_repo.run(arch, urls, content_set)

        return {'url':'%s/%s/$basearch' % (self.compose.result_repo_url, content_set), 
         'arches':set(per_arch_repos.keys()), 
         'sigkeys':content_set_repos[0]['sigkeys']}

    def get_repos_from_content_sets(self, content_sets, include_unpublished_repos=False):
        """
        Returns dictionary with URLs of all shipped repositories defined by
        the content_sets.
        The key in the returned dict is the content_set name and the value
        is the URL to repository with RPMs.

        :param list content_sets: Content sets to look for.
        :rtype: dict
        :return: Dictionary in following format:
            {
                content_set_1: {
                    "url": repo_url,
                    "arches": set([repo_arch1, repo_arch2]),
                    'sigkeys': ['sigkey1', 'sigkey2', ...]
                },
                ...
            }
        """
        query_data = {'criteria': {'filters':{'notes.content_set': {'$in': content_sets}}, 
                      'fields':[
                       'notes']}}
        if not include_unpublished_repos:
            query_data['criteria']['filters']['notes.include_in_download_service'] = 'True'
        repos = self._rest_post('repositories/search/', query_data)
        per_content_set_repos = {}
        for repo in repos:
            notes = repo['notes']
            url = '%s/%s' % (self.server_url.rstrip('/'),
             notes['relative_url'])
            arch = notes['arch']
            sigkeys = sorted(notes['signatures'].split(','))
            if url.startswith('https://'):
                url = 'http://' + url[len('https://'):]
            if notes['content_set'] not in per_content_set_repos:
                per_content_set_repos[notes['content_set']] = []
            per_content_set_repos[notes['content_set']].append({'url':url, 
             'arches':set([arch]), 
             'sigkeys':sigkeys})

        ret = {}
        for cs, repos in per_content_set_repos.items():
            merged_repos = self._try_arch_merge(repos)
            if not merged_repos:
                merged_repos = self._merge_repos(cs, repos)
            if merged_repos:
                ret[cs] = merged_repos
            else:
                ret[cs] = repos[(-1)]

        return ret