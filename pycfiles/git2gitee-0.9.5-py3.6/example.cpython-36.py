# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/git2gitee/example.py
# Compiled at: 2020-05-03 09:05:19
# Size of source mod 2**32: 461 bytes
"""
example
"""
import os
from git2gitee.login import GiteeLogin, Cross
if __name__ == '__main__':
    username = 'mikele'
    password = os.getenv('GITEE_PWD')
    print(password)
    gitee = GiteeLogin(username, password)
    if gitee.login():
        print('登陆成功')
    cross = Cross('toyourheart163/git2gitee', username, gitee.token, gitee.sess, gitee.headers)
    cross.import_to_gitee()