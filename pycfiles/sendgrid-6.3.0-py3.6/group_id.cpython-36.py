# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/helpers/mail/group_id.py
# Compiled at: 2020-04-29 15:57:11
# Size of source mod 2**32: 1048 bytes


class GroupId(object):
    __doc__ = 'The unsubscribe group ID to associate with this email.'

    def __init__(self, group_id=None):
        """Create a GroupId object

        :param group_id: The unsubscribe group to associate with this email.
        :type group_id: integer, optional
        """
        self._group_id = None
        if group_id is not None:
            self.group_id = group_id

    @property
    def group_id(self):
        """The unsubscribe group to associate with this email.

        :rtype: integer
        """
        return self._group_id

    @group_id.setter
    def group_id(self, value):
        """The unsubscribe group to associate with this email.

        :param value: The unsubscribe group to associate with this email.
        :type value: integer
        """
        self._group_id = value

    def get(self):
        """
        Get a JSON-ready representation of this GroupId.

        :returns: This GroupId, ready for use in a request body.
        :rtype: integer
        """
        return self.group_id