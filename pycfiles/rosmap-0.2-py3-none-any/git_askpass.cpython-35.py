# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/repository_cloners/git_askpass.py
# Compiled at: 2019-03-15 11:16:31
# Size of source mod 2**32: 362 bytes
from sys import argv
from os import environ
if __name__ == '__main__':
    if argv[1] == "Username for 'https://github.com': ":
        print(environ['GIT_USERNAME'])
        exit()
    if argv[1] == "Password for 'https://" + environ['GIT_USERNAME'] + "@github.com': ":
        print(environ['GIT_PASSWORD'])
        exit()
    exit(1)