# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kmclaughlin/git/LABHR/octohatrack/octohatrack/contributors_file.py
# Compiled at: 2016-05-04 05:16:43
# Size of source mod 2**32: 1597 bytes
import base64, re, hashlib
from .helpers import *

def get_contributors_file(repo_name):
    progress('Collecting CONTRIBUTORS file')
    response = get_data('/repos/%s/contents/CONTRIBUTORS' % repo_name)
    if response is None:
        print('No CONTRIBUTORS file')
        return []
    if 'message' in response.keys():
        print('No CONTRIBUTORS file')
    results = []
    content = base64.b64decode(response['content']).decode('utf-8', 'ignore')
    for line in content.splitlines():
        progress_advance()
        if not line.startswith('#'):
            if line.strip() is not '' and '<' in line:
                name, alias = line.strip('>').split('<')
                if ':' in alias:
                    service, user_name = alias.split(':@')
                    if service == 'twitter':
                        user_name += ' (twitter)'
                else:
                    if '@' in alias:
                        user_name = alias
                    else:
                        log.debug('Invalid contributor line type: %s. Returning plain' % line)
                    results.append({'name': name.strip(), 'user_name': user_name})

    progress_complete()
    return results