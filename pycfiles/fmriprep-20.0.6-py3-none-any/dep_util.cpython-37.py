# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/setuptools/setuptools/dep_util.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 949 bytes
from distutils.dep_util import newer_group

def newer_pairwise_group(sources_groups, targets):
    """Walk both arguments in parallel, testing if each source group is newer
    than its corresponding target. Returns a pair of lists (sources_groups,
    targets) where sources is newer than target, according to the semantics
    of 'newer_group()'.
    """
    if len(sources_groups) != len(targets):
        raise ValueError("'sources_group' and 'targets' must be the same length")
    n_sources = []
    n_targets = []
    for i in range(len(sources_groups)):
        if newer_group(sources_groups[i], targets[i]):
            n_sources.append(sources_groups[i])
            n_targets.append(targets[i])

    return (
     n_sources, n_targets)