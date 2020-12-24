# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/rapport/plugins/github.py
# Compiled at: 2013-05-22 10:22:35
"""
Github plugin.
"""
import collections, json, re, requests, rapport.plugin, rapport.util

class GithubPlugin(rapport.plugin.Plugin):

    def __init__(self, *args, **kwargs):
        super(GithubPlugin, self).__init__(*args, **kwargs)

    def _get_json(self, url):
        response = requests.get(url, auth=(self.login, self.password))
        link_url = None
        if 'link' in response.headers:
            link_url = response.headers['link']
            if link_url.startswith('<'):
                link_url = re.match('<([^>]+)>; rel="next"', link_url).groups()[0]
        return (
         json.loads(response.text), link_url)

    def collect(self, timeframe):
        url = ('https://api.github.com/users/{0}/events').format(self.login)
        d = collections.defaultdict(list)
        while True:
            events_json, url = self._get_json(url)
            for event in events_json:
                created_at = rapport.util.datetime_from_iso8601(event['created_at'])
                if timeframe.contains(created_at):
                    d['events'].append(event)
                    if event['type'] == 'CommitCommentEvent':
                        d['commit_comment_events'].append(event)
                    elif event['type'] == 'CreateEvent':
                        d['create_events'].append(event)
                    elif event['type'] == 'DeleteEvent':
                        d['delete_events'].append(event)
                    elif event['type'] == 'ForkEvent':
                        d['fork_events'].append(event)
                    elif event['type'] == 'GistEvent':
                        d['gist_events'].append(event)
                    elif event['type'] == 'GollumEvent':
                        d['gollum_events'].append(event)
                    elif event['type'] == 'IssuesEvent':
                        d['issues_events'].append(event)
                    elif event['type'] == 'IssueCommentEvent':
                        d['issues_comment_events'].append(event)
                    elif event['type'] == 'PullRequestEvent':
                        d['pull_request_events'].append(event)
                    elif event['type'] == 'PullRequestReviewCommentEvent':
                        d['pull_request_review_comment_events'].append(event)
                    elif event['type'] == 'PushEvent':
                        d['push_events'].append(event)
                    elif event['type'] == 'TeamAddEvent':
                        d['team_add_events'].append(event)
                elif d['events']:
                    url = None
                    break

            if url is None:
                break

        return self._results(d)


rapport.plugin.register('github', GithubPlugin)