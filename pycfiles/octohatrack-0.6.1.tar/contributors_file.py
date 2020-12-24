# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: octohatrack/contributors_file.py
# Compiled at: 2016-05-01 22:01:57
import base64, re, hashlib
from .helpers import progress, progress_advance, get_user_data, get_data

def get_contributors_file(repo_name):
    progress('Collecting CONTRIBUTORS file')
    response = get_data('/repos/%s/contents/CONTRIBUTORS' % repo_name)
    if response is None:
        print 'No CONTRIBUTORS file'
        return []
    else:
        if 'message' in response.keys():
            print 'No CONTRIBUTORS file'
        results = []
        content = base64.b64decode(response['content']).decode('utf-8', 'ignore')
        for line in content.splitlines():
            progress_advance()
            name, avatar, user_name = None, None, None
            if not line.startswith('#'):
                if line.strip() is not '':
                    if '<' in line:
                        name, alias = line.strip('>').split('<')
                        if ':' in alias:
                            service, user_name = alias.split(':@')
                            if service == 'twitter':
                                avatar = get_twitter_avatar(user_name)
                                user_name += ' (twitter)'
                            if service == 'github':
                                avatar = get_gh_avatar(user_name)
                        elif '@' in alias:
                            user_name = alias
                            avatar = get_gravatar(user_name)
                        else:
                            log.debug('Invalid contributor line type: %s. Returning plain' % line)
                            avatar = 'unknown'
                        results.append({'name': name.strip(), 'avatar': avatar, 'user_name': user_name})

        return results


def get_gh_avatar(user_name):
    u = get_data('/users/%s' % user_name)
    return u['avatar_url']


def get_gravatar(email):
    return 'http://TODO.com/%s' % email


def get_twitter_avatar(user_name):
    return 'https://twitter.com/%s/profile_image?size=original' % user_name