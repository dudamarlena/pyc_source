# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fatfrog/Documents/backmap/.eggs/setuptools_scm-2.0.0-py3.6.egg/setuptools_scm/discover.py
# Compiled at: 2018-04-13 13:17:12
# Size of source mod 2**32: 416 bytes
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