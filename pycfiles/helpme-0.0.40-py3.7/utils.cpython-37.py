# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpme/main/github/utils.py
# Compiled at: 2019-12-18 16:21:27
# Size of source mod 2**32: 2073 bytes
"""

Copyright (C) 2017-2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
from helpme.logger import bot
import sys, requests, json, urllib, webbrowser

def create_issue(title, body, repo, token):
    """create a Github issue, given a title, body, repo, and token.

       Parameters
       ==========
       title: the issue title
       body: the issue body
       repo: the full name of the repo
       token: the user's personal Github token

    """
    owner, name = repo.split('/')
    url = 'https://api.github.com/repos/%s/%s/issues' % (owner, name)
    data = {'title':title, 
     'body':body}
    headers = {'Authorization':'token %s' % token, 
     'Accept':'application/vnd.github.symmetra-preview+json'}
    response = requests.post(url, data=(json.dumps(data)), headers=headers)
    if response.status_code in (201, 202):
        url = response.json()['html_url']
        bot.info(url)
        return url
    if response.status_code == 404:
        bot.error('Cannot create issue. Does your token have scope repo?')
        sys.exit(1)
    else:
        bot.error('Cannot create issue %s' % title)
        bot.error(response.content)
        sys.exit(1)


def open_issue(title, body, repo):
    """open a GitHub issue given a title, body, and repository. Does not
       rely on the GitHub API, but instead opens a browser URL.

       Parameters
       ==========
       title: the issue title
       body: the issue body
       repo: the full name of the repo
    """
    owner, name = repo.split('/')
    title = title.replace(' ', '+')
    body = urllib.parse.quote(body)
    url = 'https://github.com/%s/%s/issues/new?labels=bug&title=%s&body=%s' % (
     owner,
     name,
     title,
     body)
    bot.info('Browser opening to:')
    bot.info(url)
    webbrowser.open_new(url)