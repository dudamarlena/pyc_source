# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/bots/test/post_github.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 3267 bytes
import json, logging, os, platform, sys
from datetime import datetime
from urllib.parse import urlencode
import requests
from ...assets.user_agents import user_agents
logger = logging.getLogger('MAKE_GITHUB_ISSUE')
USERNAME = os.getenv('GITHUB_USERNAME')
TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = 'dipu-bd'
REPO_NAME = 'lightnovel-crawler'
headers = {'User-Agent':user_agents[0], 
 'Authorization':'token %s' % TOKEN, 
 'Accept':'application/vnd.github.golden-comet-preview+json'}

def find_issues(labels=None):
    """Returns list of issues by query"""
    url = 'https://api.github.com/repos/%s/%s/issues' % (REPO_OWNER, REPO_NAME)
    session = requests.Session()
    data = {'labels': labels}
    r = session.get((url + '?' + urlencode(data)), headers=headers)
    if r.ok:
        logger.info('Successfully retrieved issues')
        return r.json()
    else:
        logger.info('Failed to get issues: %s' % url)
        logger.debug('Response:\n%s\n' % r.content)
        return []


def post_issue(title, body=None, labels=None):
    """Create an issue on github.com using the given parameters."""
    url = 'https://api.github.com/repos/%s/%s/import/issues' % (REPO_OWNER, REPO_NAME)
    session = requests.Session()
    payload = json.dumps({'issue': {'title':title, 
               'body':body, 
               'labels':labels}})
    r = session.post(url, data=payload, headers=headers)
    if r.ok:
        logger.info('Successfully created Issue %s' % title)
    else:
        logger.info('Could not create Issue %s' % title)
        logger.debug('Response:\n%s\n' % r.content)
        raise Exception('Failed to create issue')


def post_on_github(self, message):
    if sys.version_info.minor != 6:
        print('Not Python 3.6... skipping.')
        return
    issues = find_issues('bot-report')
    if len(issues):
        time = int(issues[0]['title'].split('~')[(-1)].strip())
        diff = datetime.utcnow().timestamp() - time
        if diff < 604800:
            print('Detected an open issue younger than a week... skipping.')
            return
    title = '[Test Bot][Python %d.%d][%s] Report ~ %s' % (
     sys.version_info.major,
     sys.version_info.minor,
     platform.system(),
     datetime.utcnow().strftime('%s'))
    post_issue(title, message, ['bot-report'])