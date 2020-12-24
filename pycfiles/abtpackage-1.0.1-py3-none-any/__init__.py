# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bryanbriney/git/abtools/abtools/__init__.py
# Compiled at: 2016-04-27 21:05:35
import os
if not os.environ.get('READTHEDOCS', None):
    from ._compare import run as compare
    from ._correct import run as correct
    from ._finder import run as finder
    from ._phylogeny import run as phylogeny
    from pkg_resources import get_distribution, DistributionNotFound
    import os.path
    try:
        _dist = get_distribution('abtools')
        dist_loc = os.path.normcase(_dist.location)
        here = os.path.normcase(__file__)
        if not here.startswith(os.path.join(dist_loc, 'abtools')):
            raise DistributionNotFound
    except DistributionNotFound:
        __version__ = 'Please install AbTools before checking the version'
    else:
        __version__ = _dist.version