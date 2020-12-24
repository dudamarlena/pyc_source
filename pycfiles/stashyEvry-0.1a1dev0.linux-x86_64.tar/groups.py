# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/e210990/bin/python26/lib/python2.6/site-packages/stashy/admin/groups.py
# Compiled at: 2014-06-25 10:41:27
from ..helpers import ResourceBase, FilteredIterableResource
from ..errors import ok_or_error, response_or_error
from ..compat import update_doc

class Groups(ResourceBase, FilteredIterableResource):

    @response_or_error
    def add(self, group):
        """
        Add a group, returns a dictionary containing the group name
        """
        return self._client.post(self.url(), {}, params=dict(name=group))

    @ok_or_error
    def delete(self, group):
        """
        Delete a group.
        """
        return self._client.delete(self.url(), params=dict(name=group))

    @ok_or_error
    def add_user(self, group, user):
        """
        Add a user to a group.
        """
        return self._client.post(self.url('/add-user'), dict(context=group, itemName=user))

    @ok_or_error
    def remove_user(self, group, user):
        """
        Remove a user to a group.
        """
        return self._client.post(self.url('/remove-user'), dict(context=group, itemName=user))

    def more_members(self, group, filter=None):
        """
        Retrieves a list of users that are members of a specified group.

        filter: return only users with usernames, display names or email addresses containing this string
        """
        params = dict(context=group)
        if filter:
            params['filter'] = filter
        return self.paginate('/more-members', params)

    def more_non_members(self, group, filter=None):
        """
        Retrieves a list of users that are not members of a specified group.

        filter: return only users with usernames, display names or email addresses containing this string
        """
        params = dict(context=group)
        if filter:
            params['filter'] = filter
        return self.paginate('/more-non-members', params)


update_doc(Groups.all, '\nReturns an iterator that will walk all the groups, paginating as necessary.\n\nfilter: if specified only group names containing the supplied string will be returned\n')