# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/package/Package.py
# Compiled at: 2013-12-08 21:45:16


class Package:
    name = None
    deps = None
    repo = None
    patch = None

    def getRevision(self):
        from .repoutils import getRevision
        return getRevision(self.repo)


class Repository:
    """package repository"""
    checkout_command = None
    update_command = None
    url = None


__id__ = '$Id$'