# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/reports/queries.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import six
from djblets.db.query import get_object_or_none
from reviewboard.accounts.models import Profile
from reviewboard.extensions.base import get_extension_manager
from reviewboard.reviews.models import Group
_reviewbot_user_id = None
_did_reviewbot_check = False

def get_reviewbot_user_id():
    """Return the primary key/ID of the Review Bot user, if any.

    If Review Bot is installed, it's likely that data about it isn't helpful.
    This is particularly true in the case of reports like the "time to first
    feedback", since Review Bot will give feedback within a few seconds of
    posting.

    Returns:
        int:
        The primary key/ID of the Review Bot user, or ``None`` if Review Bot
        is not installed.
    """
    global _did_reviewbot_check
    global _reviewbot_user_id
    if not _did_reviewbot_check:
        manager = get_extension_manager()
        extension = manager.get_enabled_extension(b'reviewbotext.extension.ReviewBotExtension')
        if extension is not None:
            _reviewbot_user_id = extension.settings[b'user']
        _did_reviewbot_check = True
    return _reviewbot_user_id


class UserQuery(object):
    """An object which encapsulates querying for a list of users."""

    def __init__(self, name=None, user=None, local_site=None, usernames=None, group_names=None):
        """Initialize the query.

        Args:
            name (unicode):
                A name to use when saving the query.

            user (django.contrib.auth.models.User):
                The user making the query.

            local_site (reviewboard.site.models.LocalSite):
                An optional local site to limit the query to.

            usernames (list):
                A list of usernames to search for.

            group_names (list):
                A list of group names to search. Users who are members of these
                groups will be added to the results.
        """
        self._local_site = None
        self._local_site_pk = None
        self._original_name = name
        self.name = name
        self.user = user
        self.local_site = local_site
        self.usernames = usernames or []
        self.group_names = group_names or []
        return

    @property
    def local_site(self):
        """Return the local site.

        Returns:
            reviewboard.site.models.LocalSite:
            The local site for this query, or None.
        """
        return self._local_site

    @local_site.setter
    def local_site(self, local_site):
        """Set the local site.

        Args:
            local_site (reviewboard.site.models.LocalSite):
                The site for this query, or None.
        """
        self._local_site = local_site
        self._local_site_pk = self._get_local_site_pk(local_site)

    def get_objects(self):
        """Return a queryset for the current query.

        Returns:
            django.db.models.query.QuerySet:
            A queryset for the selected users.
        """
        groups = Group.objects.filter(local_site=self.local_site, name__in=self.group_names).values_list(b'pk', flat=True)
        return User.objects.filter(Q(is_active=True) & (Q(username__in=self.usernames) | Q(review_groups__in=groups))).exclude(pk=get_reviewbot_user_id())

    def to_json(self):
        """Return a data structure suitable for serializing to the JSON API.

        Returns:
            dict:
            Data to serialize to JSON.
        """
        return {b'id': self.name, 
           b'name': self.name, 
           b'usernames': self.usernames, 
           b'group_names': self.group_names}

    def to_profile(self):
        """Return a data structure suitable for serializing to the profile.

        Returns:
            dict:
            Data to serialize into the user profile.
        """
        return {b'name': self.name, 
           b'local_site_pk': self._local_site_pk, 
           b'usernames': self.usernames, 
           b'group_names': self.group_names}

    def save(self):
        """Save this query to the user profile.

        Raises:
            ValueError:
                The query did not have required fields to save.
        """
        if self.user is None:
            raise ValueError(b'UserQuery cannot be saved without a "user" field.')
        if not isinstance(self.name, six.text_type):
            raise ValueError(b'UserQuery cannot be saved without a "name" field.')
        profile = Profile.objects.get_or_create(user=self.user)[0]
        if profile.extra_data is None:
            profile.extra_data = {b'saved_user_queries': []}
        else:
            saved_queries = profile.extra_data.setdefault(b'saved_user_queries', [])
        for i, query in enumerate(saved_queries):
            if query[b'name'] == self._original_name and query[b'local_site_pk'] == self._local_site_pk:
                saved_queries[i] = self.to_profile()
                break
        else:
            saved_queries.append(self.to_profile())

        profile.save(update_fields=[b'extra_data'])
        return

    def delete(self):
        """Delete this query from the user profile.

        Raises:
            ValueError:
                This query did not include required fields.

            KeyError:
                This query does not exist in the user profile.
        """
        if self.user is None:
            raise ValueError(b'UserQuery cannot be deleted without a "user" field.')
        if not isinstance(self.name, six.text_type):
            raise ValueError(b'UserQuery cannot be deleted without a "name" field.')
        profile = Profile.objects.get_or_create(user=self.user)[0]
        saved_queries = profile.extra_data.get(b'saved_user_queries', [])
        for i, query in enumerate(saved_queries):
            if query[b'name'] == self.name and query[b'local_site_pk'] == self._local_site_pk:
                del saved_queries[i]
                profile.save(update_fields=[b'extra_data'])
                break
        else:
            raise KeyError(b'UserQuery with name "%s" was not found for user %s' % (
             self.name, self.user.username))

        return

    @staticmethod
    def from_profile(user, local_site, name):
        """Return a new UserQuery matching the given name.

        Returns:
            UserQuery:
            The matching query.

        Raises:
            KeyError:
                The query does not exist in the user profile.
        """
        profile = get_object_or_none(Profile, user=user)
        extra_data = profile and profile.extra_data or {}
        saved_user_queries = extra_data.get(b'saved_user_queries', [])
        local_site_pk = UserQuery._get_local_site_pk(local_site)
        for query in saved_user_queries:
            if query[b'name'] == name and query[b'local_site_pk'] == local_site_pk:
                return UserQuery(name=name, user=user, local_site=local_site, usernames=query[b'usernames'], group_names=query[b'group_names'])
        else:
            raise KeyError(b'UserQuery with name "%s" was not found for user %s' % (
             name, user.username))

    @staticmethod
    def find(user, local_site):
        """Return all UserQueries from the given user's profile.

        Returns:
            list:
            A list of UserQuery objects for the given local site.
        """
        try:
            profile = user.get_profile()
        except Profile.DoesNotExist:
            return []

        if profile.extra_data is None or b'saved_user_queries' not in profile.extra_data:
            return []
        local_site_pk = UserQuery._get_local_site_pk(local_site)
        return [ UserQuery(name=query[b'name'], user=user, local_site=local_site, usernames=query[b'usernames'], group_names=query[b'group_names']) for query in profile.extra_data[b'saved_user_queries'] if query[b'local_site_pk'] == local_site_pk
               ]

    @staticmethod
    def _get_local_site_pk(local_site):
        """Return the pk of the given local site, or None.

        Args:
            local_site (reviewboard.site.models.LocalSite):
                A local site, or None.

        Returns:
            int:
            The primary key of the local site, or None.
        """
        if local_site:
            return local_site.pk
        else:
            return
            return