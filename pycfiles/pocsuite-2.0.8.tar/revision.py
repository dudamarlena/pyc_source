# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/core/revision.py
# Compiled at: 2018-11-28 03:20:09
"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
import os, re
from subprocess import Popen as execute
from subprocess import PIPE

def getRevisionNumber():
    """
    Returns abbreviated commit hash number as retrieved with "git rev-parse --short HEAD"
    """
    retVal = None
    filePath = None
    _ = os.path.dirname(__file__)
    while True:
        filePath = os.path.join(_, '.git', 'HEAD')
        if os.path.exists(filePath):
            break
        else:
            filePath = None
            if _ == os.path.dirname(_):
                break
            else:
                _ = os.path.dirname(_)

    while True:
        if filePath and os.path.isfile(filePath):
            with open(filePath, 'r') as (f):
                content = f.read()
                filePath = None
                if content.startswith('ref: '):
                    filePath = os.path.join(_, '.git', content.replace('ref: ', '')).strip()
                else:
                    match = re.match('(?i)[0-9a-f]{32}', content)
                    retVal = match.group(0) if match else None
                    break
        else:
            break

    if not retVal:
        process = execute('git rev-parse --verify HEAD', shell=True, stdout=PIPE, stderr=PIPE)
        stdout, _ = process.communicate()
        match = re.search('(?i)[0-9a-f]{32}', stdout or '')
        retVal = match.group(0) if match else None
    if retVal:
        return retVal[:7]
    else:
        return