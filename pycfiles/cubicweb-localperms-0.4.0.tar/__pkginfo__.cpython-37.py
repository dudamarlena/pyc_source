# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dlaxalde/src/cw/cubes/localperms/cubicweb_localperms/__pkginfo__.py
# Compiled at: 2019-03-13 06:09:11
# Size of source mod 2**32: 606 bytes
"""cubicweb-localperms application packaging information"""
modname = 'localperms'
distname = 'cubicweb-localperms'
numversion = (0, 3, 3)
version = '.'.join((str(num) for num in numversion))
license = 'LGPL'
author = 'LOGILAB S.A. (Paris, FRANCE)'
author_email = 'contact@logilab.fr'
description = 'allow definition of local permissions'
web = 'http://www.cubicweb.org/project/%s' % distname
classifiers = [
 'Environment :: Web Environment',
 'Framework :: CubicWeb',
 'Programming Language :: Python']
__depends__ = {'cubicweb': '>= 3.24.0'}
__recommends__ = {}