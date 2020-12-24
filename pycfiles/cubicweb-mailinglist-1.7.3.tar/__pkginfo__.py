# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: cubicweb_localperms/__pkginfo__.py
# Compiled at: 2019-03-13 06:09:11
__doc__ = 'cubicweb-localperms application packaging information'
modname = 'localperms'
distname = 'cubicweb-localperms'
numversion = (0, 3, 3)
version = ('.').join(str(num) for num in numversion)
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