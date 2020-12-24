# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/review_group.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import six
from djblets.util.decorators import augment_method_from
from djblets.webapi.decorators import webapi_login_required, webapi_response_errors, webapi_request_fields
from djblets.webapi.errors import DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED
from reviewboard.reviews.models import Group
from reviewboard.webapi.base import ImportExtraDataError, WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.errors import GROUP_ALREADY_EXISTS, INVALID_USER
from reviewboard.webapi.resources import resources

class ReviewGroupResource(WebAPIResource):
    """Provides information on review groups.

    Review groups are groups of users that can be listed as an intended
    reviewer on a review request.
    """
    model = Group
    fields = {b'id': {b'type': int, 
               b'description': b'The numeric ID of the review group.'}, 
       b'name': {b'type': six.text_type, 
                 b'description': b'The short name of the group, used in the reviewer list and the Dashboard.'}, 
       b'display_name': {b'type': six.text_type, 
                         b'description': b'The human-readable name of the group, sometimes used as a short description.'}, 
       b'invite_only': {b'type': bool, 
                        b'description': b'Whether or not the group is invite-only. An invite-only group is only accessible by members of the group.', 
                        b'added_in': b'1.6'}, 
       b'mailing_list': {b'type': six.text_type, 
                         b'description': b'The e-mail address that all posts on a review group are sent to.'}, 
       b'url': {b'type': six.text_type, 
                b'description': b"The URL to the user's page on the site. This is deprecated and will be removed in a future version.", 
                b'deprecated_in': b'2.0'}, 
       b'absolute_url': {b'type': six.text_type, 
                         b'description': b"The absolute URL to the user's page on the site.", 
                         b'added_in': b'2.0'}, 
       b'visible': {b'type': bool, 
                    b'description': b'Whether or not the group is visible to users who are not members. This does not prevent users from accessing the group if they know it, though.', 
                    b'added_in': b'1.6'}, 
       b'extra_data': {b'type': dict, 
                       b'description': b'Extra data as part of the review group. This can be set by the API or extensions.', 
                       b'added_in': b'2.0'}}
    item_child_resources = [
     resources.review_group_user]
    uri_object_key = b'group_name'
    uri_object_key_regex = b'[A-Za-z0-9_-]+'
    model_object_key = b'name'
    mimetype_list_resource_name = b'review-groups'
    mimetype_item_resource_name = b'review-group'
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def has_delete_permissions(self, request, group, *args, **kwargs):
        return group.is_mutable_by(request.user)

    def has_modify_permissions(self, request, group):
        return group.is_mutable_by(request.user)

    def get_queryset(self, request, is_list=False, local_site_name=None, *args, **kwargs):
        search_q = request.GET.get(b'q', None)
        local_site = self._get_local_site(local_site_name)
        if is_list:
            query = self.model.objects.accessible(request.user, local_site=local_site)
        else:
            query = self.model.objects.filter(local_site=local_site)
        if search_q:
            q = Q(name__istartswith=search_q)
            if request.GET.get(b'displayname', None):
                q = q | Q(display_name__istartswith=search_q)
            query = query.filter(q)
        return query

    def serialize_url_field(self, group, **kwargs):
        return group.get_absolute_url()

    def serialize_absolute_url_field(self, obj, request, **kwargs):
        return request.build_absolute_uri(obj.get_absolute_url())

    def has_access_permissions(self, request, group, *args, **kwargs):
        return group.is_accessible_by(request.user)

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Retrieve information on a review group.

        Some basic information on the review group is provided, including
        the name, description, and mailing list (if any) that e-mails to
        the group are sent to.

        The group links to the list of users that are members of the group.
        """
        pass

    @webapi_check_local_site
    @webapi_request_fields(optional={b'q': {b'type': six.text_type, 
              b'description': b'The string that the group name (or the  display name when using ``displayname``) must start with in order to be included in the list. This is case-insensitive.'}, 
       b'displayname': {b'type': bool, 
                        b'description': b'Specifies whether ``q`` should also match the beginning of the display name.'}}, allow_unknown=True)
    @augment_method_from(WebAPIResource)
    def get_list(self, *args, **kwargs):
        """Retrieves the list of review groups on the site.

        The list of review groups can be filtered down using the ``q`` and
        ``displayname`` parameters.

        Setting ``q`` to a value will by default limit the results to
        group names starting with that value. This is a case-insensitive
        comparison.

        If ``displayname`` is set to ``1``, the display names will also be
        checked along with the username. ``displayname`` is ignored if ``q``
        is not set.

        For example, accessing ``/api/groups/?q=dev&displayname=1`` will list
        any groups with a name or display name starting with ``dev``.
        """
        pass

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(GROUP_ALREADY_EXISTS, INVALID_FORM_DATA, INVALID_USER, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(required={b'name': {b'type': six.text_type, 
                 b'description': b'The name of the group.', 
                 b'added_in': b'1.6.14'}, 
       b'display_name': {b'type': six.text_type, 
                         b'description': b'The human-readable name of the group.', 
                         b'added_in': b'1.6.14'}}, optional={b'mailing_list': {b'type': six.text_type, 
                         b'description': b'The e-mail address that all posts on a review group are sent to.', 
                         b'added_in': b'1.6.14'}, 
       b'visible': {b'type': bool, 
                    b'description': b'Whether or not the group is visible to users who are not members. The default is true.', 
                    b'added_in': b'1.6.14'}, 
       b'invite_only': {b'type': bool, 
                        b'description': b'Whether or not the group is invite-only. The default is false.', 
                        b'added_in': b'1.6.14'}}, allow_unknown=True)
    def create(self, request, name, display_name, mailing_list=None, visible=True, invite_only=False, local_site_name=None, extra_fields={}, *args, **kargs):
        """Creates a new review group.

        This will create a brand new review group with the given name
        and display name. The group will be public by default, unless
        specified otherwise.

        Extra data can be stored later lookup. See
        :ref:`webapi2.0-extra-data` for more information.
        """
        local_site = self._get_local_site(local_site_name)
        if not self.model.objects.can_create(request.user, local_site):
            return self.get_no_access_error(request)
        group, is_new = self.model.objects.get_or_create(name=name, local_site=local_site, defaults={b'display_name': display_name, 
           b'mailing_list': mailing_list or b'', 
           b'visible': bool(visible), 
           b'invite_only': bool(invite_only)})
        if not is_new:
            return GROUP_ALREADY_EXISTS
        if extra_fields:
            try:
                self.import_extra_data(group, group.extra_data, extra_fields)
            except ImportExtraDataError as e:
                return e.error_payload

            group.save(update_fields=[b'extra_data'])
        return (201,
         {self.item_result_key: group})

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, INVALID_FORM_DATA, GROUP_ALREADY_EXISTS, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(optional={b'name': {b'type': six.text_type, 
                 b'description': b'The new name for the group.', 
                 b'added_in': b'1.6.14'}, 
       b'display_name': {b'type': six.text_type, 
                         b'description': b'The human-readable name of the group.', 
                         b'added_in': b'1.6.14'}, 
       b'mailing_list': {b'type': six.text_type, 
                         b'description': b'The e-mail address that all posts on a review group are sent to.', 
                         b'added_in': b'1.6.14'}, 
       b'visible': {b'type': bool, 
                    b'description': b'Whether or not the group is visible to users who are not members.', 
                    b'added_in': b'1.6.14'}, 
       b'invite_only': {b'type': bool, 
                        b'description': b'Whether or not the group is invite-only.', 
                        b'added_in': b'1.6.14'}}, allow_unknown=True)
    def update(self, request, name=None, extra_fields={}, *args, **kwargs):
        """Updates an existing review group.

        All the fields of a review group can be modified, including the
        name, so long as it doesn't conflict with another review group.

        Extra data can be stored later lookup. See
        :ref:`webapi2.0-extra-data` for more information.
        """
        try:
            group = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_modify_permissions(request, group):
            return self.get_no_access_error(request)
        else:
            if name is not None and name != group.name:
                local_site = self._get_local_site(kwargs.get(b'local_site_name'))
                if self.model.objects.filter(name=name, local_site=local_site).exists():
                    return GROUP_ALREADY_EXISTS
                group.name = name
            for field in ('display_name', 'mailing_list', 'visible', 'invite_only'):
                val = kwargs.get(field, None)
                if val is not None:
                    setattr(group, field, val)

            try:
                self.import_extra_data(group, group.extra_data, extra_fields)
            except ImportExtraDataError as e:
                return e.error_payload

            group.save()
            return (
             200,
             {self.item_result_key: group})

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    def delete(self, request, *args, **kwargs):
        """Deletes a review group.

        This will disassociate the group from all review requests previously
        targetting the group, and permanently delete the group.

        It is best to only delete empty, unused groups, and to instead
        change a group to not be visible if it's on longer needed.
        """
        try:
            group = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_delete_permissions(request, group):
            return self.get_no_access_error(request)
        group.delete()
        return (
         204, {})


review_group_resource = ReviewGroupResource()