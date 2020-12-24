# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/acl/adapters/base.py
# Compiled at: 2009-04-27 10:32:00
"""
Base defitions for PyACL source adapters.

"""
from acl.core import ACE
from acl.exc import SourceError, ExistingGroupError, NonExistingGroupError, UserPresentError, UserNotPresentError

class ACLCollection(object):
    """
    Source adapter for ACL collections.
    
    """

    def __init__(self, fallback_decision=ACE.decisions['deny']):
        self.fallback_decision = fallback_decision

    def get_acl(self, aco):
        """
        Return the ACL assigned to the ``aco`` ACO.
        
        :param aco: The Access Control Object in question.
        :return: The ACL assigned to ``aco``.
        
        """
        raise NotImplementedError

    def filter_acl(self, aco, aro, include_parents=False):
        """
        Return those ACEs in the ACL for``aco`` which are assigned to ``aro``.
        
        """
        raise NotImplementedError

    def add_ace(self, aco, ace):
        raise NotImplementedError

    def replace_ace(self, aco, old_ace, new_ace):
        raise NotImplementedError

    def remove_ace(self, aco, ace):
        raise NotImplementedError


class GroupsAdapter(object):
    """
    Base class for :term:`group source adapters <group source adapter>`.
    
    Please note that these abstract methods may only raise one exception:
    :class:`SourceError`, which is raised if there was a problem while dealing 
    with the source. They may not raise other exceptions because they should not
    validate anything but the source (not even the parameters they get).
    
    .. attribute:: writable = True
    
        :type: bool
        
        Whether the adapter can write to the source.
        
        If the source type handled by your adapter doesn't support write
        access, or if your adapter itself doesn't support writting to the
        source (yet), then you should set this value to ``False`` in the class
        itself; it will get overriden if the ``writable`` parameter in 
        :meth:`the contructor <GroupsAdapter.__init__>` is set, unless you 
        explicitly disable that parameter::
        
            # (...)
            class MyFakeAdapter(GroupsAdapter):
                def __init__():
                    super(MyFakeAdapter, self).__init__(writable=False)
            # (...)
        
        .. note::
        
            If it's ``False``, then you don't have to define the methods that
            modify the source because they won't be used:
            
            * :meth:`_include_users`
            * :meth:`_exclude_users`
            * :meth:`_create_group`
            * :meth:`_rename_group`
            * :meth:`_delete_group`
    
    """

    def __init__(self, writable=True):
        """
        Run common setup for group source adapters.
        
        :param writable: Whether the source is writable.
        :type writable: bool
        
        """
        self.writable = writable

    def get_all_groups(self):
        """
        Return all the groups found in the source.
        
        :return: All the groups found in the source.
        :rtype: dict
        :raise SourceError: If there was a problem with the source.
        
        """
        return self._get_all_groups()

    def get_group_users(self, group):
        """
        Return the users that belong to ``group``.
        
        :param group: The name of the group to be fetched.
        :type group: basestring
        :return: The users of the ``group``.
        :rtype: tuple
        :raise NonExistingGroupError: If the requested group doesn't exist.
        :raise SourceError: If there was a problem with the source.
        
        """
        self._check_group_existence(group)
        return self._get_group_users(group)

    def set_group_users(self, group, users):
        """
        Set ``users`` as the only users of the ``group``.
        
        :raise NonExistingGroupError: If the group doesn't exist.
        :raise SourceError: If there was a problem with the source.
        
        """
        old_users = self.get_group_users(group)
        users = set(users)
        added = set(i for i in users if i not in old_users)
        removed = set(i for i in old_users if i not in users)
        self.exclude_users(group, removed)
        self.include_users(group, added)

    def find_groups(self, user):
        """
        Return the groups to which ``user`` belongs.
        
        :param user: The identifier for user in question.
        :type user: basestring
        :return: The groups to which ``user`` belongs.
        :rtype: tuple
        :raise SourceError: If there was a problem with the source.
        
        """
        return self._find_groups(user)

    def include_user(self, group, user):
        """
        Include ``user`` in ``group``.
        
        This is the individual (non-bulk) edition of :meth:`include_users`.
        
        :param group: The ``group`` to contain the ``user``.
        :type group: unicode
        :param user: The new ``user`` of the ``group``.
        :type user: tuple
        :raise NonExistingGroupError: If the ``group`` doesn't exist.
        :raise UserPresentError: If the ``user`` is already included.
        :raise SourceError: If there was a problem with the source.
        
        """
        self.include_users(group, (user,))

    def include_users(self, group, users):
        """
        Include ``users`` in ``group``.
        
        This is the bulk edition of :meth:`include_users`.
        
        :param group: The ``group`` to contain the ``users``.
        :type group: unicode
        :param users: The new ``users`` of the ``group``.
        :type users: tuple
        :raise NonExistingGroupError: If the ``group`` doesn't exist.
        :raise UserPresentError: If at least one of the users is already
            present.
        :raise SourceError: If there was a problem with the source.
        
        """
        self._check_group_existence(group)
        for i in users:
            self._confirm_user_not_present(group, i)

        self._check_writable()
        users = set(users)
        self._include_users(group, users)

    def exclude_user(self, group, user):
        """
        Exclude ``user`` from ``group``.
        
        This is the individual (non-bulk) edition of :meth:`exclude_users`.
        
        :param group: The ``group`` that contains the ``user``.
        :type group: unicode
        :param user: The ``user`` to be removed from ``group``.
        :type user: tuple
        :raise NonExistingGroupError: If the ``group`` doesn't exist.
        :raise UserNotPresentError: If the user is not included in the group.
        :raise SourceError: If there was a problem with the source.
        
        """
        self.exclude_users(group, (user,))

    def exclude_users(self, group, users):
        """
        Exclude ``users`` from ``group``.
        
        This is the bulk edition of :meth:`exclude_user`.
        
        :param group: The ``group`` that contains the ``users``.
        :type group: unicode
        :param users: The ``users`` to be removed from ``group``.
        :type users: tuple
        :raise NonExistingGroupError: If the ``group`` doesn't exist.
        :raise UserNotPresentError: If at least one of the users is not
            included in the group.
        :raise SourceError: If there was a problem with the source.
        
        """
        self._check_group_existence(group)
        for i in users:
            self._confirm_user_is_present(group, i)

        self._check_writable()
        users = set(users)
        self._exclude_users(group, users)

    def create_group(self, group):
        """
        Add ``group`` to the source.
        
        :param group: The group name.
        :type group: unicode
        :raise ExistingGroupError: If the group name is already in use.
        :raise SourceError: If there was a problem with the source.
        
        """
        self._check_group_not_existence(group)
        self._check_writable()
        self._create_group(group)

    def rename_group(self, group, new_group):
        """
        Rename ``group`` to ``new_group``.
        
        :param group: The current name of the group.
        :type group: unicode
        :param new_group: The new name of the group.
        :type new_group: unicode
        :raise NonExistingGroupError: If the group doesn't exist.
        :raise SourceError: If there was a problem with the source.
        
        """
        self._check_group_existence(group)
        self._check_writable()
        self._rename_group(group, new_group)

    def delete_group(self, group):
        """
        Delete ``group``.
        
        It removes the ``group`` from the source.
        
        :param group: The name of the group to be deleted.
        :type group: unicode
        :raise NonExistingGroupError: If the group in question doesn't 
            exist.
        :raise SourceError: If there was a problem with the source.
        
        """
        self._check_group_existence(group)
        self._check_writable()
        self._delete_group(group)

    def _check_writable(self):
        """
        Raise an exception if the source is not writable.
        
        :raise SourceError: If the source is not writable.
        
        """
        if not self.writable:
            raise SourceError('The source is not writable')

    def _check_group_existence(self, group):
        """
        Raise an exception if ``group`` is not defined in the source.
        
        :param group: The name of the group to look for.
        :type group: unicode
        :raise NonExistingGroupError: If the group is not defined.
        :raise SourceError: If there was a problem with the source.
        
        """
        if not self._group_exists(group):
            msg = 'group "%s" is not defined in the source' % group
            raise NonExistingGroupError(msg)

    def _check_group_not_existence(self, group):
        """
        Raise an exception if ``group`` is defined in the source.
        
        :param group: The name of the group to look for.
        :type group: unicode
        :raise ExistingGroupError: If the group is defined.
        :raise SourceError: If there was a problem with the source.
        
        """
        if self._group_exists(group):
            msg = 'group "%s" is already defined in the source' % group
            raise ExistingGroupError(msg)

    def _confirm_user_is_present(self, group, user):
        """
        Raise an exception if ``group`` doesn't contain ``user``.
        
        :param group: The name of the group that may contain the user.
        :type group: unicode
        :param user: The name of the user to look for.
        :type user: unicode
        :raise NonExistingGroupError: If the group doesn't exist.
        :raise UserNotPresentError: If the user is not included.
        :raise SourceError: If there was a problem with the source.
        
        """
        self._check_group_existence(group)
        if not self._user_is_included(group, user):
            msg = 'User "%s" is not included in group "%s"' % (user, group)
            raise UserNotPresentError(msg)

    def _confirm_user_not_present(self, group, user):
        """
        Raise an exception if ``group`` already contains ``user``.
        
        :param group: The name of the group that may contain the user.
        :type group: unicode
        :param user: The name of the user to look for.
        :type user: unicode
        :raise NonExistingGroupError: If the group doesn't exist.
        :raise UserPresentError: If the user is already included.
        :raise SourceError: If there was a problem with the source.
        
        """
        self._check_group_existence(group)
        if self._user_is_included(group, user):
            msg = 'User "%s" is already included in group "%s"' % (user, group)
            raise UserPresentError(msg)

    def _get_all_groups(self):
        """
        Return all the groups found in the source.
        
        :return: All the groups found in the source.
        :rtype: dict
        :raise SourceError: If there was a problem with the source while
            retrieving the groups.
        
        """
        raise NotImplementedError()

    def _get_group_users(self, group):
        """
        Return the users of the group called ``group``.
        
        :param group: The name of the group to be fetched.
        :type group: unicode
        :return: The users of the group.
        :rtype: set
        :raise SourceError: If there was a problem with the source while 
            retrieving the group.
        
        .. attention::
            When implementing this method, don't check whether the
            group really exists; that's already done when this method is
            called.
        
        """
        raise NotImplementedError()

    def _find_groups(self, user):
        """
        Return the groups ``user`` belongs to.
        
        :param user: The identifier for the user in question.
        :type user: basestring
        :return: The groups to which ``user`` belongs.
        :rtype: tuple
        :raise SourceError: If there was a problem with the source while
            retrieving the groups.
        
        """
        raise NotImplementedError()

    def _include_users(self, group, users):
        """
        Add ``users`` to the ``group``, in the source.
        
        :param group: The group to contain the users.
        :type group: unicode
        :param users: The new users of the group.
        :type users: tuple
        :raise SourceError: If the users could not be added to the group.

        .. attention:: 
            When implementing this method, don't check whether the
            group really exists or the users are already included; that's 
            already done when this method is called.
        
        """
        raise NotImplementedError()

    def _exclude_users(self, group, users):
        """
        Remove ``users`` from the ``group``, in the source.
        
        :param group: The group that contains the users.
        :type group: unicode
        :param users: The users to be removed from group.
        :type users: tuple
        :raise SourceError: If the users could not be removed from the group.
        
        .. attention:: 
            When implementing this method, don't check whether the
            group really exists or the users are already included; that's 
            already done when this method is called.
        
        """
        raise NotImplementedError()

    def _user_is_included(self, group, user):
        """
        Check whether ``user`` is included in ``group``.
        
        :param group: The name of the user to look for.
        :type group: unicode
        :param group: The name of the group that may include the user.
        :type group: unicode
        :return: Whether the user is included in group or not.
        :rtype: bool
        :raise SourceError: If there was a problem with the source.
        
        .. attention:: 
            When implementing this method, don't check whether the
            group really exists; that's already done when this method is
            called.
        
        """
        raise NotImplementedError()

    def _create_group(self, group):
        """
        Add ``group`` to the source.
        
        :param group: The group name.
        :type group: unicode
        :raise SourceError: If the group could not be added.
        
        .. attention:: 
            When implementing this method, don't check whether the
            group already exists; that's already done when this method is
            called.
        
        """
        raise NotImplementedError()

    def _rename_group(self, group, new_group):
        """
        Edit ``group``'s properties.
        
        :param group: The current name of the group.
        :type group: unicode
        :param new_group: The new name of the group.
        :type new_group: unicode
        :raise SourceError: If the group could not be edited.
        
        .. attention:: 
            When implementing this method, don't check whether the
            group really exists; that's already done when this method is
            called.
        
        """
        raise NotImplementedError()

    def _delete_group(self, group):
        """
        Delete ``group``.
        
        It removes the ``group`` from the source.
        
        :param group: The name of the group to be deleted.
        :type group: unicode
        :raise SourceError: If the group could not be deleted.
        
        .. attention:: 
            When implementing this method, don't check whether the
            group really exists; that's already done when this method is
            called.
        
        """
        raise NotImplementedError()

    def _group_exists(self, group):
        """
        Check whether ``group`` is defined in the source.
        
        :param group: The name of the group to check.
        :type group: unicode
        :return: Whether the group is the defined in the source or not.
        :rtype: bool
        :raise SourceError: If there was a problem with the source.
        
        """
        raise NotImplementedError()