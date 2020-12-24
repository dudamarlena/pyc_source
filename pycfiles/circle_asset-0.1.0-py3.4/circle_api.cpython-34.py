# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/circle_asset/circle_api.py
# Compiled at: 2015-02-28 13:09:08
# Size of source mod 2**32: 1278 bytes
import requests
from urllib.parse import urljoin
from .project import Project

def get_latest_build(project, branch, allow_failures=False):
    filt = 'completed' if allow_failures else 'successful'
    target = '{root}/project/{user}/{project}/tree/{branch}?limit=1&filter={filt}'.format(root=project.api_root, user=project.username, project=project.project, branch=branch, filt=filt)
    if project.token is not None:
        target += '&circle-token={}'.format(project.token)
    data = requests.get(target, headers={'Accept': 'application/json'})
    output = data.json()
    if len(output) == 0:
        raise ValueError('No matching builds.')
    return output[0]['build_num']


def get_artifact_list(project, build):
    target = '{root}/project/{user}/{project}/{build}/artifacts'.format(root=project.api_root, user=project.username, project=project.project, build=build)
    if project.token is not None:
        target += '?circle-token={}'.format(project.token)
    data = requests.get(target, headers={'Accept': 'application/json'})
    output = data.json()
    return {x['pretty_path'][18:]:x['url'] for x in output}