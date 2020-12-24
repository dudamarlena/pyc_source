# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/confecho.py
# Compiled at: 2019-04-05 17:19:18
# Size of source mod 2**32: 205 bytes
import pkg_resources, sys
from supervisor.compat import as_string

def main(out=sys.stdout):
    config = pkg_resources.resource_string(__name__, 'skel/sample.conf')
    out.write(as_string(config))