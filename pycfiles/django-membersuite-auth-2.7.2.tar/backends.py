# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rerb/src/aashe/django-membersuite-auth/django_membersuite_auth/backends.py
# Compiled at: 2019-01-16 12:27:58
from django.conf import settings
from django.contrib.auth.models import User
from membersuite_api_client.client import ConciergeClient
from membersuite_api_client.security.services import LoginToPortalError, get_user_for_membersuite_entity
from .models import MemberSuitePortalUser
from .services import MemberSuitePortalUserService

class MemberSuiteBackend(object):

    def authenticate(self, username=None, password=None):
        """Returns the appropriate django.contrib.auth.models.User if
        successful; otherwise returns None.

        If login succeeds and there's no MemberSuitePortalUser that
        matches on membersuite_id or user;

            1) one is created, and;

            2) a User object might be created too.

        Plus, the is_member attribute on MemberSuitePortalUser is set
        when login succeeds.

        Plus, when a MemberSuitePortalUser is created, the related
        User object gets its names and email updated from MemberSuite.

        Finally, "MAINTENANCE_MODE" is supported, during which all but
        staff logins will fail.

        """
        try:
            self.connect()
            user_service = self.get_user_service()
            authenticated_portal_user = user_service.login(username=username, password=password)
        except LoginToPortalError:
            return

        try:
            membersuite_portal_user = MemberSuitePortalUser.objects.get(membersuite_id=authenticated_portal_user.membersuite_id)
        except MemberSuitePortalUser.DoesNotExist:
            if getattr(settings, 'MAINTENANCE_MODE', False):
                return
            user, user_created = get_user_for_membersuite_entity(membersuite_entity=authenticated_portal_user)
            try:
                membersuite_portal_user = MemberSuitePortalUser.objects.get(user=user)
            except MemberSuitePortalUser.DoesNotExist:
                membersuite_portal_user = MemberSuitePortalUser(user=user, membersuite_id=authenticated_portal_user.membersuite_id)
                if not user_created:
                    user.email = authenticated_portal_user.email_address
                    user.first_name = authenticated_portal_user.first_name
                    user.last_name = authenticated_portal_user.last_name
                user.set_unusable_password()
                user.save()
            else:
                membersuite_portal_user.membersuite_id = authenticated_portal_user.membersuite_id

        membersuite_portal_user.is_member = self.get_is_member(membersuite_portal_user=authenticated_portal_user)
        membersuite_portal_user.save()
        if getattr(settings, 'MAINTENANCE_MODE', None) and not membersuite_portal_user.user.is_staff:
            return
        else:
            return membersuite_portal_user.user

    def connect(self):
        self.client = ConciergeClient(access_key=settings.MS_ACCESS_KEY, secret_key=settings.MS_SECRET_KEY, association_id=settings.MS_ASSOCIATION_ID)

    def get_user_service(self):
        user_service = MemberSuitePortalUserService(client=self.client)
        return user_service

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return

        return

    def get_is_member(self, membersuite_portal_user, client=None):
        client = client if client else self.client
        individual = membersuite_portal_user.get_individual(client=client)
        is_member = individual.is_member(client=client)
        return is_member