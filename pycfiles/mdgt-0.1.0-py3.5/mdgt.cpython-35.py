# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mdgt\mdgt.py
# Compiled at: 2016-10-17 15:09:43
# Size of source mod 2**32: 3187 bytes
"""
mdgt
A Microdata-Parsing Microservice

Command-line usage:
    python mdgt.py --help
"""
from pathlib import Path
from pkg_resources import resource_filename
import json
from .provider import Provider
from .webserve import serve as webserve

def jsonPrint(dataDict):
    """Outputs parsed information as json to stdout."""
    print(json.dumps(dataDict))


def consolePrint(dataDict):
    """Outputs parsed information in a console-friendly format to stdout."""
    for k in dataDict.keys():
        v = dataDict[k]
        if type(v) is list:
            buf = ''
            outStr = '{}: '.format(k)
            for i in range(len(k) + 2):
                buf = '{} '.format(buf)

            for e in v:
                print('{}{}'.format(outStr, e))
                outStr = buf

        else:
            print('{}: {}'.format(k, v))


def listProvs():
    """Outputs a list of all available providers to stdout."""
    print('Available providers')
    cwd_path = Path('providers')
    provs = list(cwd_path.glob('*.json'))
    print('In CWD/providers:')
    for prov in provs:
        print('- {}'.format(prov.stem))

    pkg_path = Path(resource_filename(__name__, 'providers'))
    provs = list(pkg_path.glob('*.json'))
    print('In package root:')
    for prov in provs:
        print('- {}'.format(prov.stem))