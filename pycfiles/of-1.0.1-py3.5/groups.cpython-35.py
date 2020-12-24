# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/of/common/security/groups.py
# Compiled at: 2016-09-15 19:50:18
# Size of source mod 2**32: 5046 bytes
"""
The groups module contains functionality for checking group level rights.

Created on Mar 6, 2015

@author: Nicklas Boerjesson
"""
from decorator import getfullargspec
__author__ = 'nibo'
_groups = None

def init_groups(_database_access):
    """
    Initiate the global groups object, load all groups from the provided database

    :param _database_access: A database access object
    :return: The global group object

    """
    global _groups
    _groups = Groups(_database_access)


def has_right(_right, _user):
    """

    Global convenience function, see Groups.has_right

    :param _right:

    """
    if _groups:
        _groups.has_right(_right, _user)


def user_in_any_of_groups(_user, _groups):
    """
    Check if a user belongs to any of the groups
    :param _user: A user instance
    :param _groups: A list of groups to check
    :return: True if in any of the groups
    """
    _user_groups = _user['groups']
    for _group in _groups:
        if _group in _user_groups:
            return True

    return False


def aop_has_right(_rights):
    """

    A decorator to supply the has_right functionality. Takes a function pointer.
    It is necessary to make it able to get the data in runtime.
    TODO: That is quite ugly.

    :param _rights_function: A a list with rights or a pointer to a function that returns the right to check for
    :return: returns a decorator function.

    """

    def wrapper(func):

        def wrapped_f(*args, **kwargs):
            if '_user' in kwargs:
                _user = kwargs['_user']
            else:
                _argument_specifications = getfullargspec(func)
                try:
                    user_idx = _argument_specifications.args.index('_user')
                except:
                    raise Exception('Has right aspect for "' + func.__name__ + '": No _user parameter in function, internal error.')

                if user_idx > len(args) - 1:
                    raise Exception('Has right aspect for "' + func.__name__ + '": The _user parameter isn\'t supplied.')
                _user = args[user_idx]
            if isinstance(_rights, list):
                has_right(_rights, _user)
            elif callable(_rights):
                has_right(_rights(), _user)
            return func(*args, **kwargs)

        return wrapped_f

    return wrapper


class RightCheckError(Exception):
    __doc__ = 'Exception class for Rights errors'


class Groups:
    __doc__ = '\n    The Groups class is the central location for group management in MBE and holds the group cache.\n\n    '
    _groups = {}

    def __init__(self, _database_access):
        """
        The class initiates by loading all groups from the database.

        :param _database_access: A database access object instance

        """
        self._groups = {}
        self._database_access = _database_access
        self.reload_all()

    def reload_all(self):
        """
        Reload all groups from database
        """
        self._groups.clear()
        _cursor = self._database_access.find({'collection': 'node', 'conditions': {'schemaRef': 'ref://of.node.group'}})
        for _curr_group in _cursor:
            self._groups[_curr_group['_id']] = _curr_group

    def has_right(self, _right, _user):
        """
        Check if a certain user, through group membership, holds a certain right.
        Raises a RightCheckError if npt

        :param _right: The right in question
        :param _user: A user object

        """
        if type(_right) is list:
            for _curr_group in _user['groups']:
                for _curr_right in _right:
                    if _curr_right in self._groups[_curr_group]['rights']:
                        return _curr_group

        else:
            for _curr_group in _user['groups']:
                if _right in self._groups[_curr_group]['rights']:
                    return _curr_group

        _error = 'The user "' + _user['name'] + '" doesn\'t have the ' + str(_right) + ' right.'
        self._database_access.logging.log_security('right', _error, _user['_id'], None)
        raise RightCheckError('The user "' + _user['name'] + '" doesn\'t have the ' + str(_right) + ' right.')

    def __iter__(self):
        """Access function for making the class iterable."""
        return self._groups

    def __getitem__(self, item):
        """Access function for making the class iterable."""
        return self._groups[item]