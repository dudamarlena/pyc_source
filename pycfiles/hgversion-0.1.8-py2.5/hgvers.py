# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hgversion/hgvers.py
# Compiled at: 2008-07-03 16:36:03
import re
repo = None
version = None
try:
    import hgversion as hgv
except ImportError:
    pass
else:
    repo = hgv.repository

if repo is None:
    try:
        f = open('PKG-INFO')
    except IOError:
        pass
    else:
        regex = re.compile('^Version:\\s+(\\S+)')
        for line in f:
            mo = regex.match(line)
            if mo is not None:
                version = mo.group(1)
                break

else:
    version = hgv.version()
if __name__ == '__main__':
    print version