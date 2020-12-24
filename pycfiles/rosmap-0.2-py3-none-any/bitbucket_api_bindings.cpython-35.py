# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/github_repository_cloner/api_bindings/bitbucket_api_bindings.py
# Compiled at: 2019-02-01 12:17:40
# Size of source mod 2**32: 4087 bytes
import time, urllib3, json, sys, logging

class BitbucketApiBindings:
    __doc__ = '\n    Wraps Bitbucket API functions.\n    '

    def __init__(self, rate_limit: int):
        self._BitbucketApiBindings__rate_limit = rate_limit

    def form_bitbucket_request(self, url: str) -> urllib3.response:
        """
        Creates new bitbucket request and returns the response.
        :param url: The url to call.
        :return: The response resulting from the request.
        """
        time.sleep(3600 / self._BitbucketApiBindings__rate_limit)
        http = urllib3.PoolManager()
        return http.request('GET', url)

    def get_repo_substring(self, url, provider):
        """
        Gets the repo-substring (i.e. url: https://bitbucket.org/osrf/gazebo -> returns: osrf/gazebo
        :param url: URL to get the substring from.
        :param provider: Part to cut off from the front.
        :return: the substring formatted as {<user>|<organization>}/{repository_name}
        """
        project_string = url.split(provider)[1]
        project_string = project_string.split('.git')[0]
        return project_string

    def get_stargazer_count(self, repo_url):
        """
        Gets the "stargazer" count for github. Used watchers since stargazers do not exist in Bitbucket.
        :param repo_url: URL to the repository.
        :return: the amount of watchers on the repository, -1 if request failed.
        """
        project_string = self.get_repo_substring(repo_url, 'https://bitbucket.org/')
        response = self.form_bitbucket_request('https://api.bitbucket.org/2.0/repositories/' + project_string + '/watchers')
        if response.status == 200:
            data = response.data
            decoded = json.loads(data.decode(sys.stdout.encoding))
            return decoded['size']
        return -1

    def get_next_url(self, result):
        """
        Gets the URL for the next page.
        :param result: URL for the next page.
        :return: The next url, or empty string, if no next string is available.
        """
        if 'next' in result:
            return result['next']
        else:
            return ''

    def get_issues_api_string(self, repo_url):
        """
        Returns API url to call for issues associated with the repository.
        :param repo_url: Repository URL to get issues from.
        :return: API URL for retrieving an issue list.
        """
        project_string = self.get_repo_substring(repo_url, 'https://bitbucket.org/')
        return 'https://api.bitbucket.org/2.0/repositories/' + project_string + '/issues'

    def get_pull_requests_api_string(self, repo_uri):
        """
        Returns API URL to call for (open) pull requests associated with the repository.
        :param repo_uri: Repository URL to get pull requests from.
        :return: API URL for retrieving pull request list.
        """
        project_string = self.get_repo_substring(repo_uri, 'https://bitbucket.org/')
        return 'https://api.bitbucket.org/2.0/repositories/' + project_string + '/pullrequests?state=OPEN'

    def get_values(self, api_url) -> iter:
        """
        Gets the values field from an Bitbucket API result (used for e.g. pull requests, issues, etc..)
        :param api_url: API url to call. (see *_api_string)
        :return: Yield returns the values from the Bitbucket API.
        """
        next_url = api_url
        while next_url != '':
            response = self.form_bitbucket_request(next_url)
            if response.status != 200:
                logging.info('[Bitbucket API Connector]: Could not reach ' + next_url + ', request returned ' + str(response.status))
                next_url = ''
            else:
                result = json.loads(response.data.decode(sys.stdout.encoding))
                if 'values' in result:
                    for value in result['values']:
                        yield value

                next_url = self.get_next_url(result)