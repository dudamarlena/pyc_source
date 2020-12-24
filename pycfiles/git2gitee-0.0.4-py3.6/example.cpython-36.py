# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/git2gitee/example.py
# Compiled at: 2020-05-01 05:28:34
# Size of source mod 2**32: 238 bytes
"""
example
"""
from git2gitee.cross import Cross
from git2gitee.config import token
if __name__ == '__main__':
    gee = Cross(token, 'toyourheart163/seeing')
    gee.import_to_gitee()
    gee.clone()
    gee.rename_config_repo_url()