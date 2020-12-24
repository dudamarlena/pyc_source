# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/csft/_meta.py
# Compiled at: 2018-01-15 11:14:49
# Size of source mod 2**32: 692 bytes
__author__ = 'Yan QiDong'
__email__ = 'yanqd0@outlook.com'
__url__ = 'https://github.com/yanqd0/csft'
__copyright__ = 'Copyright (C) 2017 ' + __author__
__license__ = 'MIT License'

def _get_version(default='x.x.x.dev'):
    try:
        from pkg_resources import DistributionNotFound, get_distribution
    except ImportError:
        return default
    else:
        try:
            return get_distribution(__package__).version
        except DistributionNotFound:
            return default
        except ValueError:
            return default
        except TypeError:
            return default


__version__ = _get_version()