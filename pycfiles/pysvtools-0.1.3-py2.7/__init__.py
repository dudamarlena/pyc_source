# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/pysvtools/__init__.py
# Compiled at: 2015-11-10 10:04:57
"""
pySVtools: VCF toolkit for SV analysis

Copyright (c) 2013-2014 Leiden University Medical Center <sasc@lumc.nl>
Copyright (c) 2013-2015 Wai Yi Leung <w.y.leung@lumc.nl>

Licensed under the MIT license, see the LICENSE file.
"""
RELEASE = False
__version_info__ = ('0', '1', '3')
__version__ = ('.').join(__version_info__)
__author__ = 'LUMC, Wai Yi Leung'
__contact__ = 'w.y.leung@lumc.nl'
__homepage__ = 'https://github.com/wyleung/pySVtools'
usage = __doc__.split('\n\n\n')

def docSplit(func):
    return func.__doc__.split('\n\n')[0]


def version(name):
    return '%s version %s\n\nAuthor   : %s <%s>\nHomepage : %s' % (name,
     __version__, __author__, __contact__, __homepage__)