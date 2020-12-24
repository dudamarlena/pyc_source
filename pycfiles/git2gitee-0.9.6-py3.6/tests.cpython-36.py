# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/git2gitee/tests.py
# Compiled at: 2020-05-03 09:09:35
# Size of source mod 2**32: 317 bytes
"""
test
"""
import os
from git2gitee.login import GiteeLogin

def test_login():
    """test login to gitee"""
    username = 'mikele'
    password = os.getenv('GITEE_PWD')
    gitee = GiteeLogin(username, password)
    if gitee.login():
        print('登陆成功')


if __name__ == '__main__':
    test_login()