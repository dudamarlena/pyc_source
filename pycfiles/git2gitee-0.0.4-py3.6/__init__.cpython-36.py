# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/git2gitee/__init__.py
# Compiled at: 2020-05-01 06:12:06
# Size of source mod 2**32: 997 bytes
"""
从github导入仓库到gitee
解决github下载速度慢的问题
"""
import sys
from argparse import ArgumentParser
from git2gitee.cross import Cross
from git2gitee.config import token
__author__ = 'wei40680@gmail.com'
__version__ = '0.0.4'
my_gitee = 'https://gitee.com/mikele'

def cmd():
    ap = ArgumentParser(description='fork github repo to gitee. then clone to local.')
    ap.add_argument(dest='repo', metavar='repo')
    ap.add_argument('-u', '--username', action='store', default='mikele', help='gitee username')
    ap.add_argument('-s', '--seconds', action='store', default=180)
    ap.add_argument('-t', '--token', action='store', help='gitee api token', default=token)
    ap.add_argument('-c', '--clone', action='store_true')
    args = ap.parse_args()
    gee = Cross((args.token), (args.repo), (args.username), timeout=(args.seconds))
    gee.import_to_gitee()
    if args.clone:
        gee.clone()
        gee.rename_config_repo_url()


if __name__ == '__main__':
    cmd()