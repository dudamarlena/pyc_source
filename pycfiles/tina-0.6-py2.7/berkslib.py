# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tina/berkslib.py
# Compiled at: 2013-04-10 10:01:21
import re
from urlparse import urlparse
import subprocess, json
from tag import Tag

def get_name_from_url(repo_url):
    match = re.match('.*/(.+?)\\.git.*', repo_url)
    if not match:
        raise Exception("Error: git URL is malformed: '%s'" % repo_url)
    return match.group(1)


def repos_from_berks():
    data = _get_json_from_berks_run()
    repos = {}
    for repo in data['cookbooks']:
        url = None
        if 'location' in repo.keys():
            url = _get_url_from_string(repo['location'])
        repos[repo['name']] = url

    return repos


def _get_json_from_berks_run():
    print 'Running Berkshelf...'
    proc = subprocess.Popen(['berks', 'install', '--path', '.tina',
     '--format=json'], stdout=subprocess.PIPE)
    berks_output, errors = proc.communicate()
    return json.loads(berks_output)


def _get_url_from_string(line):
    regex = re.compile('.*[\'"]([a-zA-Z]*://.*?)[\'"]')
    match = regex.match(line)
    if not match:
        return None
    else:
        word = match.group(1)
        return word.replace('"', '')


def normalize_urls_to_git(url):
    if url == None:
        return
    else:
        if re.match('git@.*:.*', url):
            return url
        parts = urlparse(url)
        if not parts.hostname or not parts.path:
            raise SyntaxError("URL is malformed: '%s'" % url)
        norm = 'git@' + parts.hostname
        norm += ':' + parts.path.lstrip('/')
        if not norm.endswith('.git'):
            norm += '.git'
        return norm