# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/kolekto/db.py
# Compiled at: 2014-06-16 16:12:17
from kolekto.helpers import JsonDbm

class MoviesMetadata(JsonDbm):
    """ A database used to store metadata about movies managed by kolekto.
    """

    def itermovieshash(self):
        """ Iterate over movies hash stored in the database.
        """
        cur = self._db.firstkey()
        while cur is not None:
            yield cur
            cur = self._db.nextkey(cur)

        return

    def itermovies(self):
        """ Iterate over (hash, movie) couple stored in database.
        """
        return self.iteritems()