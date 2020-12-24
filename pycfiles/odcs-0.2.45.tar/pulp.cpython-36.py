# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/pulp.py
# Compiled at: 2017-10-30 03:09:30
# Size of source mod 2**32: 3207 bytes
import json, requests

class Pulp(object):
    __doc__ = 'Interface to Pulp'

    def __init__(self, server_url, username, password):
        self.username = username
        self.password = password
        self.server_url = server_url
        self.rest_api_root = '{0}/pulp/api/v2/'.format(self.server_url.rstrip('/'))

    def _rest_post(self, endpoint, post_data):
        query_data = json.dumps(post_data)
        r = requests.post(('{0}{1}'.format(self.rest_api_root, endpoint.lstrip('/'))),
          query_data,
          auth=(
         self.username, self.password))
        r.raise_for_status()
        return r.json()

    def get_repo_urls_from_content_sets(self, content_sets, arch):
        """
        Returns dictionary with URLs of all shipped repositories defining
        the content set for given arch.
        The key in the returned dict is the content_set name and the value
        is the URL to repository with RPMs.

        :param list content_sets: Content sets to look for.
        :param str arch: Architecture of returned repositories.
        :rtype: dict
        :return: Dictionary with {content_set:repo_url}.
        """
        query_data = {'criteria': {'filters':{'notes.content_set':{'$in': content_sets}, 
                       'notes.arch':arch, 
                       'notes.include_in_download_service':'True'}, 
                      'fields':[
                       'notes.relative_url', 'notes.content_set']}}
        repos = self._rest_post('repositories/search/', query_data)
        ret = {}
        for repo in repos:
            url = '%s/%s' % (self.server_url.rstrip('/'),
             repo['notes']['relative_url'])
            if url.startswith('https://'):
                url = 'http://' + url[len('https://'):]
            ret[repo['notes']['content_set']] = url

        return ret