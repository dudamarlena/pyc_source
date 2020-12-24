# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/error.py
# Compiled at: 2016-10-03 09:39:22


class BaubleError(Exception):

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        if self.msg is None:
            return str(type(self).__name__)
        else:
            return '%s: %s' % (type(self).__name__, self.msg)
            return self.msg


class CommitException(Exception):

    def __init__(self, exc, row):
        self.row = row
        self.exc = exc

    def __str__(self):
        return str(self.exc)


class NoResultException(BaubleError):
    pass


class DatabaseError(BaubleError):
    pass


class EmptyDatabaseError(DatabaseError):
    pass


class MetaTableError(DatabaseError):
    pass


class TimestampError(DatabaseError):
    pass


class RegistryError(DatabaseError):
    pass


class VersionError(DatabaseError):

    def __init__(self, version):
        super(VersionError, self).__init__()
        self.version = version


class SQLAlchemyVersionError(BaubleError):
    pass


class CheckConditionError(BaubleError):
    pass


def check(condition, msg=None):
    """
    Check that condition is true.  If not then raise
    CheckConditionError(msg)
    """
    if not condition:
        raise CheckConditionError(msg)