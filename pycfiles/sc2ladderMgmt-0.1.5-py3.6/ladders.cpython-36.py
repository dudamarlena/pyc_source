# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2ladderMgmt\ladders.py
# Compiled at: 2018-07-13 01:01:21
# Size of source mod 2**32: 4073 bytes
"""
PURPOSE: define what a ladder is, how it works
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import json, os
from sc2ladderMgmt import constants as c
ladderCache = {}

class Ladder(object):
    __doc__ = 'represent a given set of settings for a defined Ladder'

    def __init__(self, source=None, **override):
        self.name = ''
        self.ipAddress = c.LOCALHOST
        self.serverPort = c.DEFAULT_PORT
        self.allowNewPlayers = True
        self.maxLocalGamesAllowed = 0
        self.inactiveScan = True
        self.inactivePurge = False
        if isinstance(source, str):
            self.load(source)
        else:
            if isinstance(source, dict):
                self.update(source)
            else:
                if isinstance(source, Ladder):
                    self.update(source.__dict__)
        self.update(override)
        if not self.name:
            raise ValueError("must define 'name' parameter as part of %s source settings" % self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.name)

    @property
    def filename(self):
        """return the absolute path to the object's filename"""
        return os.path.join(c.LADDER_FOLDER, 'ladder_%s.json' % self.name)

    @property
    def attrs(self):
        """provide a copy of this ladder's attributes as a dictionary"""
        return dict(self.__dict__)

    def _validateAttrs(self, keys):
        """prove that all attributes are defined appropriately"""
        badAttrsMsg = ''
        for k in keys:
            if k not in self.attrs:
                badAttrsMsg += "Attribute key '%s' is not a valid attribute" % k

        if badAttrsMsg:
            raise ValueError('Encountered invalid attributes.  ALLOWED: %s%s%s' % (
             list(self.attrs), os.linesep, badAttrsMsg))

    def load(self, ladderName):
        """retrieve the ladder settings from saved disk file"""
        self.name = ladderName
        with open(self.filename, 'rb') as (f):
            data = f.read()
            self.__dict__.update(json.loads(data))

    def save(self):
        """save ladder settings to disk"""
        with open(self.filename, 'wb') as (f):
            data = str.encode(json.dumps((self.attrs), indent=4, sort_keys=True))
            f.write(data)

    def update(self, attrs):
        """update attributes initialized with the proper type"""
        self._validateAttrs(attrs)
        for k, v in attrs.items():
            typecast = type(getattr(self, k))
            if typecast == bool:
                if v == 'False':
                    newval = False
            else:
                newval = typecast(v.lower())
            setattr(self, k, newval)