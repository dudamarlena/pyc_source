# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/setuptools_scm/discover.py
# Compiled at: 2020-02-13 15:05:29
import os
from pkg_resources import iter_entry_points
from .utils import trace

def iter_matching_entrypoints(path, entrypoint):
    trace('looking for ep', entrypoint, path)
    for ep in iter_entry_points(entrypoint):
        if os.path.exists(os.path.join(path, ep.name)):
            if os.path.isabs(ep.name):
                trace('ignoring bad ep', ep)
            trace('found ep', ep)
            yield ep