# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/default_reviewer.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import six
from djblets.util.decorators import augment_method_from
from djblets.webapi.decorators import webapi_login_required, webapi_response_errors, webapi_request_fields
from djblets.webapi.errors import DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED
from reviewboard.reviews.forms import DefaultReviewerForm
from reviewboard.reviews.models import DefaultReviewer, Group
from reviewboard.scmtools.models import Repository
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_login_required, webapi_check_local_site

class DefaultReviewerResource(WebAPIResource):
    """Provides information on default reviewers for review requests.

    Review Board will apply any default reviewers that match the repository
    and any file path in an uploaded diff for new and updated review requests.
    A default reviewer entry can list multiple users and groups.

    This is useful when different groups own different parts of a codebase.
    Adding DefaultReviewer entries ensures that the right people will always
    see the review request and discussions.

    Default reviewers take a regular expression for the file path matching,
    making it flexible.

    As a tip, specifying ``.*`` for the regular expression would have this
    default reviewer applied to every review request on the matched
    repositories.
    """
    added_in = b'1.6.16'
    name = b'default_reviewer'
    model = DefaultReviewer
    fields = {b'id': {b'type': int, 
               b'description': b'The numeric ID of the default reviewer.'}, 
       b'name': {b'type': six.text_type, 
                 b'description': b'The descriptive name of the entry.'}, 
       b'file_regex': {b'type': six.text_type, 
                       b'description': b'The regular expression that is used to match files uploaded in a diff.'}, 
       b'repositories': {b'type': six.text_type, 
                         b'description': b'A comma-separated list of repository IDs that this default reviewer will match against.'}, 
       b'users': {b'type': six.text_type, 
                  b'description': b'A comma-separated list of usernames that this default reviewer applies to matched review requests.'}, 
       b'groups': {b'type': six.text_type, 
                   b'description': b'A comma-separated list of group names that this default reviewer applies to matched review requests.'}}
    uri_object_key = b'default_reviewer_id'
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    def serialize_repositories_field(self, default_reviewer, **kwargs):
        return default_reviewer.repository.all()

    def serialize_users_field(self, default_reviewer, **kwargs):
        return default_reviewer.people.all()

    @webapi_check_login_required
    def get_queryset(self, request, is_list=False, local_site=None, *args, **kwargs):
        """Returns a queryset for DefaultReviewer models.

        By default, this returns all default reviewers.

        If the queryset is being used for a list of default reviewer
        resources, then it can be further filtered by one or more of the
        arguments listed in get_list.
        """
        queryset = self.model.objects.filter(local_site=local_site)
        if is_list:
            if b'repositories' in request.GET:
                for repo_id in request.GET.get(b'repositories').split(b','):
                    try:
                        queryset = queryset.filter(repository=repo_id)
                    except ValueError:
                        pass

            if b'users' in request.GET:
                for username in request.GET.get(b'users').split(b','):
                    queryset = queryset.filter(people__username=username)

            if b'groups' in request.GET:
                for name in request.GET.get(b'groups').split(b','):
                    queryset = queryset.filter(groups__name=name)

        return queryset

    def has_access_permissions(self, request, default_reviewer, *args, **kwargs):
        return default_reviewer.is_accessible_by(request.user)

    def has_modify_permissions(self, request, default_reviewer, *args, **kwargs):
        return default_reviewer.is_mutable_by(request.user)

    def has_delete_permissions(self, request, default_reviewer, *args, **kwargs):
        return default_reviewer.is_mutable_by(request.user)

    @webapi_check_local_site
    @webapi_request_fields(optional={b'groups': {b'type': six.text_type, 
                   b'description': b'A comma-separated list of group names that each resulting default reviewer must apply to review requests.'}, 
       b'repositories': {b'type': six.text_type, 
                         b'description': b'A comma-separated list of IDs of repositories that each resulting default reviewer must match against.'}, 
       b'users': {b'type': six.text_type, 
                  b'description': b'A comma-separated list of usernames that each resulting default reviewer must apply to review requests.'}})
    @augment_method_from(WebAPIResource)
    def get_list(self, request, *args, **kwargs):
        """Retrieves the list of default reviewers on the server.

        By default, this lists all default reviewers. This list can be
        further filtered down through the query arguments.
        """
        pass

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Retrieves information on a particular default reviewer."""
        pass

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(required={b'name': {b'type': six.text_type, 
                 b'description': b'The name of the default reviewer entry.'}, 
       b'file_regex': {b'type': six.text_type, 
                       b'description': b'The regular expression used to match file paths in newly uploaded diffs.'}}, optional={b'repositories': {b'type': six.text_type, 
                         b'description': b'A comma-separated list of repository IDs.'}, 
       b'groups': {b'type': six.text_type, 
                   b'description': b'A comma-separated list of group names.'}, 
       b'users': {b'type': six.text_type, 
                  b'description': b'A comma-separated list of usernames.'}})
    def create(self, request, local_site=None, *args, **kwargs):
        """Creates a new default reviewer entry.

        Note that by default, a default reviewer will apply to review
        requests on all repositories, unless one or more repositories are
        provided in the default reviewer's list.
        """
        if not self.model.objects.can_create(request.user, local_site):
            return self.get_no_access_error(request)
        else:
            code, data = self._create_or_update(request, local_site, **kwargs)
            if code == 200:
                return (201, data)
            return (code, data)

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(optional={b'name': {b'type': six.text_type, 
                 b'description': b'The name of the default reviewer entry.'}, 
       b'file_regex': {b'type': six.text_type, 
                       b'description': b'The regular expression used to match file paths in newly uploaded diffs.'}, 
       b'repositories': {b'type': six.text_type, 
                         b'description': b'A comma-separated list of repository IDs.'}, 
       b'groups': {b'type': six.text_type, 
                   b'description': b'A comma-separated list of group names.'}, 
       b'users': {b'type': six.text_type, 
                  b'description': b'A comma-separated list of usernames.'}})
    def update(self, request, local_site=None, *args, **kwargs):
        """Updates an existing default reviewer entry.

        If the list of repositories is updated with a blank entry, then
        the default reviewer will apply to review requests on all repositories.
        """
        try:
            default_reviewer = self.get_object(request, local_site=local_site, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_modify_permissions(request, default_reviewer):
            return self.get_no_access_error(request)
        return self._create_or_update(request, local_site, default_reviewer, **kwargs)

    def _create_or_update(self, request, local_site, default_reviewer=None, **kwargs):
        invalid_fields = {}
        form_data = {}
        if b'groups' in kwargs:
            group_names = [ name for name in (name.strip() for name in kwargs[b'groups'].split(b',')) if name
                          ]
            group_ids = [ group[b'pk'] for group in Group.objects.filter(name__in=group_names, local_site=local_site).values(b'pk')
                        ]
            if len(group_ids) != len(group_names):
                invalid_fields[b'groups'] = [b'One or more groups were not found']
            form_data[b'groups'] = group_ids
        if b'repositories' in kwargs:
            repo_ids = []
            try:
                repo_ids = [ int(repo_id) for repo_id in (repo_id.strip() for repo_id in kwargs[b'repositories'].split(b',')) if repo_id
                           ]
            except ValueError:
                invalid_fields[b'repositories'] = [b'One or more repository IDs were not in a valid format.']

            if repo_ids:
                found_count = Repository.objects.filter(pk__in=repo_ids, local_site=local_site).count()
                if len(repo_ids) != found_count:
                    invalid_fields[b'repositories'] = [b'One or more repositories were not found']
            form_data[b'repository'] = repo_ids
        if b'users' in kwargs:
            usernames = [ name for name in (name.strip() for name in kwargs[b'users'].split(b',')) if name
                        ]
            user_ids = [ user[b'pk'] for user in User.objects.filter(username__in=usernames).values(b'pk')
                       ]
            if len(user_ids) != len(usernames):
                invalid_fields[b'users'] = [b'One or more users were not found']
            form_data[b'people'] = user_ids
        if invalid_fields:
            return (INVALID_FORM_DATA,
             {b'fields': invalid_fields})
        for field in ('name', 'file_regex'):
            if field in kwargs:
                form_data[field] = kwargs[field]

        form = DefaultReviewerForm(data=form_data, instance=default_reviewer, limit_to_local_site=local_site, request=request)
        if not form.is_valid():
            field_errors = self._get_form_errors(form)
            if b'people' in field_errors:
                field_errors[b'users'] = field_errors.pop(b'people')
            if b'repository' in field_errors:
                field_errors[b'repositories'] = field_errors.pop(b'repository')
            return (
             INVALID_FORM_DATA,
             {b'fields': field_errors})
        default_reviewer = form.save()
        return (
         200,
         {self.item_result_key: default_reviewer})

    @augment_method_from(WebAPIResource)
    def delete(self, *args, **kwargs):
        """Deletes the default reviewer entry.

        This will not remove any reviewers from any review requests.
        It will only prevent these default reviewer rules from being
        applied to any new review requests or updates.
        """
        pass


default_reviewer_resource = DefaultReviewerResource()