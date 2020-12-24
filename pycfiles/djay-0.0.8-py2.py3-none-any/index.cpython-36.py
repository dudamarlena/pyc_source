# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/pkginfo/pkginfo/index.py
# Compiled at: 2019-07-30 18:47:11
# Size of source mod 2**32: 518 bytes
from .distribution import Distribution

class Index(dict):

    def __setitem__(self, key, value):
        if not isinstance(value, Distribution):
            raise ValueError('Not a distribution: %r.' % value)
        if key != '%s-%s' % (value.name, value.version):
            raise ValueError('Key must match <name>-<version>.')
        super(Index, self).__setitem__(key, value)

    def add(self, distribution):
        key = '%s-%s' % (distribution.name, distribution.version)
        self[key] = distribution