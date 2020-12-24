# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\utils\make_github_issue.py
# Compiled at: 2019-06-23 18:44:39
# Size of source mod 2**32: 1917 bytes
import json, logging, os
from urllib.parse import urlencode
import requests
logger = logging.getLogger('MAKE_GITHUB_ISSUE')
USERNAME = os.getenv('GITHUB_USERNAME')
PASSWORD = os.getenv('GITHUB_PASSWORD')
REPO_OWNER = 'dipu-bd'
REPO_NAME = 'lightnovel-crawler'

def post_issue(title, body=None, labels=None):
    """Create an issue on github.com using the given parameters."""
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)
    issue = {'title':title, 
     'body':body, 
     'labels':labels}
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        logger.info('Successfully created Issue {0:s}'.format(title))
    else:
        logger.info('Could not create Issue {0:s}'.format(title))
        logger.debug('Response:\n%s\n' % r.content)
        raise Exception('Failed to create issue')


def find_issues(labels=None):
    """Returns list of issues by query"""
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    session = requests.Session()
    data = {'labels': labels}
    r = session.get(url + '?' + urlencode(data))
    if 200 <= r.status_code <= 300:
        logger.info('Successfully retrieved issues')
        return r.json()
    logger.info('Failed to get issues: %s' % url)
    logger.debug('Response:\n%s\n' % r.content)
    return []