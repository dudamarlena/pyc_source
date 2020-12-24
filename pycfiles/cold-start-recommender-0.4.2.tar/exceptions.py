# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mal/Dropbox/Python/cold-start-recommender/csrec/exceptions.py
# Compiled at: 2016-01-31 07:03:12
__author__ = 'elegans.io Ltd'
__email__ = 'info@elegans.io'

class DatabaseOperationException(Exception):
    """
    Exception used to report generic database error
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class IntegrityViolationException(Exception):
    """
    Exception used for integrity violations, e.g. item already in database
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class GetException(Exception):
    """
    Exception used to report problems getting data from db
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InsertException(Exception):
    """
    Exception used to report problems inserting data on db
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SerializeException(Exception):
    """
    Exception used to report problems during data serialization
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RestoreException(Exception):
    """
    Exception used to report problems restoring data on db from a serialized archive
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MergeEntitiesException(Exception):
    """
    Exception used to report problems merging data on db, e.g. user reconciliation
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DeleteException(Exception):
    """
    Exception used to report problems removing data from db
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InitializationException(Exception):
    """
    Exception used to report problems during DAL initialization initialization
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class BadParametersException(Exception):
    """
    Exception used to report that initialization has failed because of unsupported or wrong parameters
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)