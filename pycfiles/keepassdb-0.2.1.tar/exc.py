# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hans/workspace/keepassdb/keepassdb/exc.py
# Compiled at: 2012-12-27 22:14:37
"""
"""
__authors__ = [
 'Hans Lellelid <hans@xmpl.org>']
__license__ = '\nkeepassdb is free software: you can redistribute it and/or modify it under the terms\nof the GNU General Public License as published by the Free Software Foundation,\neither version 3 of the License, or at your option) any later version.\n\nkeepassdb is distributed in the hope that it will be useful, but WITHOUT ANY\nWARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR\nA PARTICULAR PURPOSE. See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with\nkeepassdb.  If not, see <http://www.gnu.org/licenses/>.\n'

class KPError(Exception):
    """
    KPError is the base exception class to handle exception raised by keepassdb.
    """
    pass


class ReadOnlyDatabase(KPError):
    """
    Error when database was opened read-only.
    """
    pass


class InvalidDatabase(KPError):
    """
    Error raised when database appears to be invalid. :)
    """
    pass


class DatabaseAlreadyLocked(KPError):
    """
    Raised when the database is already locked.
    """
    pass


class UnsupportedDatabaseVersion(KPError):
    """
    Error raised when attempting to open a database version that is newer (e.g. KeePass2).
    """
    pass


class UnsupportedDatabaseEncryption(KPError):
    pass


class AuthenticationError(KPError):
    """
    Exception raised when (encrypted) contents cannot be verified against signature.
    """
    pass


class IncorrectKey(KPError):
    """
    Exception raised when contents cannot be decrypted with specified key.
    """
    pass


class ParseError(KPError):
    """
    Exception raised when unable to parse database structure. 
    """
    pass


class UnboundModelError(KPError):
    """
    Exception raised when referencing a group or entity that hasn't been bound to the database. 
    """
    pass