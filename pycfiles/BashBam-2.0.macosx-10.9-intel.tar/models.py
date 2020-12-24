# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/amay/.virtualenvs/bam/lib/python2.7/site-packages/bashbam/models.py
# Compiled at: 2014-02-23 18:21:13


class Script:
    name = None
    path = None
    origin = None

    def __unicode__(self):
        return self.name

    def __init__(self=None, name=None, path=None, origin=None):
        self.name = name
        self.path = path
        self.origin = origin


class Gist:
    id = None
    name = None
    raw_url = None

    def __unicode__(self):
        if name:
            return name
        return id

    def __init__(self, id, raw_url=None, name=None):
        self.id = id
        self.raw_url = raw_url
        self.name = name