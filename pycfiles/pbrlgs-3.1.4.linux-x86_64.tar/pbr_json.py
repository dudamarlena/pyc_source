# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/pbr_json.py
# Compiled at: 2017-12-04 07:19:32
import json
from pbr import git

def write_pbr_json(cmd, basename, filename):
    if not hasattr(cmd.distribution, 'pbr') or not cmd.distribution.pbr:
        return
    git_dir = git._run_git_functions()
    if not git_dir:
        return
    else:
        values = dict()
        git_version = git.get_git_short_sha(git_dir)
        is_release = git.get_is_release(git_dir)
        if git_version is not None:
            values['git_version'] = git_version
            values['is_release'] = is_release
            cmd.write_file('pbr', filename, json.dumps(values, sort_keys=True))
        return