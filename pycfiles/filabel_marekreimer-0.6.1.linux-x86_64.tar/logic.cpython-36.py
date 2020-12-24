# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/filabel/logic.py
# Compiled at: 2018-12-31 13:00:08
# Size of source mod 2**32: 12195 bytes
import enum, fnmatch, itertools, requests, aiohttp, asyncio

class GitHub:
    __doc__ = '\n    This class can communicate with the GitHub API\n    just give it a token and go.\n    '
    API = 'https://api.github.com'

    def __init__(self, token):
        """
        :param token: GitHub token
        """
        self.token = token
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'filabel'}
        self.session.auth = self._token_auth

    def user(self):
        """
        Get current user authenticated by token
        """
        return self._paginated_json_get(f"{self.API}/user")

    def _token_auth(self, req):
        """
        This alters all our outgoing requests
        """
        req.headers['Authorization'] = 'token ' + self.token
        return req

    def _paginated_json_get(self, url, params=None):
        r = self.session.get(url, params=params)
        r.raise_for_status()
        json = r.json()
        if 'next' in r.links:
            if 'url' in r.links['next']:
                json += self._paginated_json_get(r.links['next']['url'], params)
        return json

    def pull_requests(self, owner, repo, state='open', base=None):
        """
        Get all Pull Requests of a repo

        :param owner: GtiHub user or org
        :param repo: repo name
        :param state: open, closed, all
        :param base: optional branch the PRs are open for
        """
        params = {'state': state}
        if base is not None:
            params['base'] = base
        url = f"{self.API}/repos/{owner}/{repo}/pulls"
        return self._paginated_json_get(url, params)

    def pr_files(self, owner, repo, number):
        """
        Get files of one Pull Request

        :param owner: GtiHub user or org
        :param repo: repo name
        :param number: PR number/id
        """
        url = f"{self.API}/repos/{owner}/{repo}/pulls/{number}/files"
        return self._paginated_json_get(url)

    def pr_filenames(self, owner, repo, number):
        """
        Get filenames of one Pull Request. A generator.

        :param owner: GtiHub user or org
        :param repo: repo name
        :param number: PR number/id
        """
        return (f['filename'] for f in self.pr_files(owner, repo, number))

    def reset_labels(self, owner, repo, number, labels):
        """
        Set's labels for Pull Request. Replaces all existing lables.

        :param owner: GtiHub user or org
        :param repo: repo name
        :param lables: all lables this PR will have
        """
        url = f"{self.API}/repos/{owner}/{repo}/issues/{number}"
        r = self.session.patch(url, json={'labels': labels})
        r.raise_for_status()
        return r.json()['labels']


class AsyncGitHub(GitHub):
    __doc__ = "\n    This is a subclass of :class: `.GitHub`.\n    It overwrites it's behaviour to support asynchronnous communication.\n    "
    API = 'https://api.github.com'

    def __init__(self, token):
        super().__init__(token)
        self.create_session()

    def create_session(self):
        """
        Create asynchronnous session: `aiohttp.ClientSession`
        """
        self.session = aiohttp.ClientSession(skip_auto_headers=[
         'User-Agent'],
          headers={'User-Agent':'filabel', 
         'Authorization':'token ' + self.token})

    async def user(self):
        """
        Get current user authenticated by token
        """
        return self._paginated_json_get(f"{self.API}/user")

    async def _paginated_json_get(self, url, params=None):
        async with self.session.get(url, params=params) as r:
            json = await r.json()
            r.raise_for_status()
        if 'next' in r.links:
            if 'url' in r.links['next']:
                loop = asyncio.get_event_loop()
                t = loop.create_task(self._paginated_json_get(r.links['next']['url'], params))
                await t
                json += t.result()
        return json

    async def pr_files(self, owner, repo, number):
        """
        Get files of one Pull Request

        :param owner: GtiHub user or org
        :param repo: repo name
        :param number: PR number/id
        """
        url = f"{self.API}/repos/{owner}/{repo}/pulls/{number}/files"
        loop = asyncio.get_event_loop()
        t = loop.create_task(self._paginated_json_get(url))
        await t
        return t.result()

    async def pr_filenames(self, owner, repo, number):
        """
        Get filenames of one Pull Request. A generator.

        :param owner: GtiHub user or org
        :param repo: repo name
        :param number: PR number/id
        """
        loop = asyncio.get_event_loop()
        t = loop.create_task(self.pr_files(owner, repo, number))
        await t
        return (f['filename'] for f in t.result())

    async def reset_labels(self, owner, repo, number, labels):
        """
        Set's labels for Pull Request. Replaces all existing lables.

        :param owner: GtiHub user or org
        :param repo: repo name
        :param lables: all lables this PR will have
        """
        url = f"{self.API}/repos/{owner}/{repo}/issues/{number}"
        async with self.session.patch(url, json={'labels': labels}) as r:
            json = await r.json()
            r.raise_for_status()
        return json['labels']


class Change(enum.Enum):
    __doc__ = '\n    Enumeration of possible label changes\n    '
    ADD = 1
    DELETE = 2
    NONE = 3


class Report:
    __doc__ = '\n    Simple container for reporting repo-pr label changes\n    '

    def __init__(self, repo):
        self.repo = repo
        self.ok = True
        self.prs = {}


class Filabel:
    __doc__ = '\n    Main login of PR labeler\n    '

    def __init__(self, token, labels, state='open', base=None, delete_old=True):
        """
        :param token: GitHub token
        :param labels: Configuration of labels with globs
        :param state: State of PR to be (re)labeled
        :param base: Base branch of PRs to be (re)labeled
        :param delete_old: If no longer matching labels should be deleted
        """
        self.github = GitHub(token)
        self.labels = labels
        self.state = state
        self.base = base
        self.delete_old = delete_old

    @property
    def defined_labels(self):
        """
        Set of labels defined in configuration
        """
        return set(self.labels.keys())

    def _matching_labels(self, pr_filenames):
        """
        Find matching labels based on given filenames

        :param pr_filenames: list of filenames as strings
        """
        labels = set()
        for filename in pr_filenames:
            for label, patterns in self.labels.items():
                for pattern in patterns:
                    if fnmatch.fnmatch(filename, pattern):
                        labels.add(label)
                        break

        return labels

    def _compute_labels(self, defined, matching, existing):
        """
        Compute added, remained, deleted, and future label sets

        :param defined: Set of defined labels in config
        :param matching: Set of matching labels that should be in PR
        :param existing: Set of labels that are currently in PR
        """
        added = matching - existing
        remained = matching & existing
        deleted = set()
        future = existing
        if self.delete_old:
            deleted = (existing & defined) - matching
            future = existing - defined
        future = future | matching
        return (added, remained, deleted, future)

    def run_pr(self, owner, repo, pr_dict):
        """
        Manage labels for single given PR

        :param owner: Owner of GitHub repository
        :param repo: Name of GitHub repository
        :param pr_dict: PR as dict from GitHub API
        """
        pr_filenames = list(self.github.pr_filenames(owner, repo, pr_dict['number']))
        added, remained, deleted, future = self._compute_labels(self.defined_labels, self._matching_labels(pr_filenames), set(l['name'] for l in pr_dict['labels']))
        new_labels = self.github.reset_labels(owner, repo, pr_dict['number'], list(future))
        new_label_names = set(l['name'] for l in new_labels)
        if future == new_label_names:
            return sorted(itertools.chain([(a, Change.ADD) for a in added], [(r, Change.NONE) for r in remained], [(d, Change.DELETE) for d in deleted]))

    def run_repo(self, reposlug):
        """
        Manage labels for all matching PRs in given repo

        :param reposlug: Reposlug (full name) of GitHub repo (i.e. "owner/name")
        """
        report = Report(reposlug)
        owner, repo = reposlug.split('/')
        try:
            prs = self.github.pull_requests(owner, repo, self.state, self.base)
        except Exception:
            report.ok = False
            return report
        else:
            for pr_dict in prs:
                url = pr_dict.get('html_url', 'unknown')
                report.prs[url] = None
                try:
                    report.prs[url] = self.run_pr(owner, repo, pr_dict)
                except Exception:
                    pass

            return report


class AsyncFilabel(Filabel):
    __doc__ = '\n    This is a subclass of class: `.Filabel`.\n    It overwrites several methods to support asynchronnous communication.\n    '

    def __init__(self, token, labels, state='open', base=None, delete_old=True):
        super().__init__(token, labels, state, base, delete_old)
        self.github = AsyncGitHub(token)
        self.token = token

    async def run_pr(self, owner, repo, pr_dict):
        """
        Manage labels for single given PR asynchronnously

        :param owner: Owner of GitHub repository
        :param repo: Name of GitHub repository
        :param pr_dict: PR as dict from GitHub API
        """
        loop = asyncio.get_event_loop()
        t = loop.create_task(self.github.pr_filenames(owner, repo, pr_dict['number']))
        await t
        pr_filenames = list(t.result())
        added, remained, deleted, future = self._compute_labels(self.defined_labels, self._matching_labels(pr_filenames), set(l['name'] for l in pr_dict['labels']))
        t = loop.create_task(self.github.reset_labels(owner, repo, pr_dict['number'], list(future)))
        await t
        new_labels = t.result()
        new_label_names = set(l['name'] for l in new_labels)
        if future == new_label_names:
            return sorted(itertools.chain([(a, Change.ADD) for a in added], [(r, Change.NONE) for r in remained], [(d, Change.DELETE) for d in deleted]))

    async def run_repo(self, reposlug):
        """
        Manage labels for all matching PRs in given repo asynchronnously

        :param reposlug: Reposlug (full name) of GitHub repo (i.e. "owner/name")
        :type reposlug: str
        """
        report = Report(reposlug)
        owner, repo = reposlug.split('/')
        loop = asyncio.get_event_loop()
        try:
            task = loop.create_task(self.github.pull_requests(owner, repo, self.state, self.base))
            await task
            prs = task.result()
        except Exception:
            report.ok = False
            return report
        else:
            tasks = {}
            for pr_dict in prs:
                url = pr_dict.get('html_url', 'unknown')
                report.prs[url] = None
                cr = asyncio.create_task(self.run_pr(owner, repo, pr_dict))
                tasks[url] = cr

            for url, task in tasks.items():
                try:
                    await task
                    report.prs[url] = task.result()
                except Exception:
                    pass

            return report