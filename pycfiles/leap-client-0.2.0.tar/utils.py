# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cal/leap/leap_client/pkg/utils.py
# Compiled at: 2013-02-14 19:31:03
"""
utils to help in the setup process
"""
import os, re, sys

def get_reqs_from_files(reqfiles):
    for reqfile in reqfiles:
        if os.path.isfile(reqfile):
            return open(reqfile, 'r').read().split('\n')


def parse_requirements(reqfiles=['requirements.txt',
 'requirements.pip',
 'pkg/requirements.pip']):
    requirements = []
    for line in get_reqs_from_files(reqfiles):
        if re.match('\\s*-e\\s+', line):
            requirements.append(re.sub('\\s*-e\\s+.*#egg=(.*)$', '\\1', line))
        elif re.match('\\s*https?:', line):
            requirements.append(re.sub('\\s*https?:.*#egg=(.*)$', '\\1', line))
        elif re.match('\\s*-f\\s+', line):
            pass
        elif line == 'argparse' and sys.version_info >= (2, 7):
            pass
        elif line != '':
            requirements.append(line)

    return requirements