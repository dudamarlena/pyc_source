# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/git2gitee/__init__.py
# Compiled at: 2020-05-04 06:12:48
# Size of source mod 2**32: 247 bytes
"""
从github导入仓库到gitee
解决github下载速度慢的问题
"""
from git2gitee.login import GiteeLogin
from git2gitee.project import Project
__author__ = 'wei40680@163.com'
__version__ = '0.9.5'
my_gitee = 'https://gitee.com/mikele'