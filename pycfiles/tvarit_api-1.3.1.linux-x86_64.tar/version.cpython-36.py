# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/narendra/.pyenv/versions/aws/lib/python3.6/site-packages/tvarit_api/version.py
# Compiled at: 2019-07-17 12:15:45
# Size of source mod 2**32: 967 bytes
__all__ = ['get_version']
import os
from subprocess import check_output

def get_version():
    version = None
    if os.path.isfile('PKG-INFO'):
        with open('PKG-INFO') as (f):
            lines = f.readlines()
            for line in lines:
                if line.startswith('Version: '):
                    version = line.strip()[9:]

    else:
        try:
            tag = check_output([
             'git', 'describe', '--tags', '--abbrev=0', '--match=[0-9]*'])
            return tag.decode('utf-8').strip('\n')
        except Exception:
            pass

        if not version:
            raise RuntimeError('The version number cannot be extracted from git tag in this source distribution; please either download the source from PyPI, or check out from GitHub and make sure that the git CLI is available.')
        return version


if __name__ == '__main__':
    print(get_version())