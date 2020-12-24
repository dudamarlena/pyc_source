# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: troy/bundle_wrapper/../external/bundle/src/bundle/version.py
# Compiled at: 2014-02-24 20:40:00
__author__ = 'Francis Liu'
__copyright__ = 'Copyright 2013, AIMES project'
__license__ = 'MIT'
import os
version = 'latest'
try:
    cwd = os.path.dirname(os.path.abspath(__file__))
    fn = os.path.join(cwd, 'VERSION')
    version = open(fn).read().strip()
except IOError:
    from subprocess import Popen, PIPE, STDOUT
    import re
    VERSION_MATCH = re.compile('\\d+\\.\\d+\\.\\d+(\\w|-)*')
    try:
        p = Popen(['git', 'describe', '--tags', '--always'], stdout=PIPE, stderr=STDOUT)
        out = p.communicate()[0]
        if not p.returncode and out:
            v = VERSION_MATCH.search(out)
            if v:
                version = v.group()
    except OSError:
        pass