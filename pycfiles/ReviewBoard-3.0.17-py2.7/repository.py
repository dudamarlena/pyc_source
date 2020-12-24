# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/repository.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Q
from django.utils import six
from djblets.util.decorators import augment_method_from
from djblets.webapi.decorators import webapi_login_required, webapi_response_errors, webapi_request_fields
from djblets.webapi.errors import DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED
from reviewboard.scmtools.forms import RepositoryForm
from reviewboard.scmtools.models import Repository, Tool
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_login_required, webapi_check_local_site
from reviewboard.webapi.errors import BAD_HOST_KEY, MISSING_REPOSITORY, MISSING_USER_KEY, REPO_AUTHENTICATION_ERROR, REPO_INFO_ERROR, REPOSITORY_ALREADY_EXISTS, SERVER_CONFIG_ERROR, UNVERIFIED_HOST_CERT, UNVERIFIED_HOST_KEY
from reviewboard.webapi.mixins import UpdateFormMixin
from reviewboard.webapi.resources import resources

class RepositoryResource(UpdateFormMixin, WebAPIResource):
    """Provides information on a registered repository.

    Review Board has a list of known repositories, which can be modified
    through the site's administration interface. These repositories contain
    the information needed for Review Board to access the files referenced
    in diffs.
    """
    model = Repository
    form_class = RepositoryForm
    name_plural = b'repositories'
    fields = {b'id': {b'type': int, 
               b'description': b'The numeric ID of the repository.'}, 
       b'name': {b'type': six.text_type, 
                 b'description': b'The name of the repository.'}, 
       b'path': {b'type': six.text_type, 
                 b'description': b'The main path to the repository, which is used for communicating with the repository and accessing files.'}, 
       b'mirror_path': {b'type': six.text_type, 
                        b'description': b'An alternate path to the repository, for lookup purposes.', 
                        b'added_in': b'1.7.19'}, 
       b'visible': {b'type': bool, 
                    b'description': b'Whether or not this repository is visible (admin only).', 
                    b'added_in': b'2.0'}, 
       b'tool': {b'type': six.text_type, 
                 b'description': b'The name of the internal repository communication class used to talk to the repository. This is generally the type of the repository.'}, 
       b'bug_tracker': {b'type': six.text_type, 
                        b'description': b'The URL to a bug in the bug tracker for this repository, with ``%s`` in place of the bug ID.', 
                        b'added_in': b'2.5'}}
    uri_object_key = b'repository_id'
    item_child_resources = [
     resources.diff_file_attachment,
     resources.repository_branches,
     resources.repository_commits,
     resources.repository_info]
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')

    @webapi_check_login_required
    def get_queryset(self, request, is_list=False, local_site_name=None, show_invisible=False, *args, **kwargs):
        """Returns a queryset for Repository models."""
        local_site = self._get_local_site(local_site_name)
        if is_list:
            queryset = self.model.objects.accessible(request.user, visible_only=not show_invisible, local_site=local_site)
            q = Q()
            if b'name' in request.GET:
                q = q & Q(name__in=request.GET.get(b'name').split(b','))
            if b'path' in request.GET:
                paths = request.GET[b'path'].split(b',')
                q = q & (Q(path__in=paths) | Q(mirror_path__in=paths))
            if b'name-or-path' in request.GET:
                name_or_paths = request.GET[b'name-or-path'].split(b',')
                q = q & (Q(name__in=name_or_paths) | Q(path__in=name_or_paths) | Q(mirror_path__in=name_or_paths))
            if b'tool' in request.GET:
                q = q & Q(tool__name__in=request.GET[b'tool'].split(b','))
            if b'hosting-service' in request.GET:
                q = q & Q(hosting_account__service_name__in=request.GET[b'hosting-service'].split(b','))
            if b'username' in request.GET:
                usernames = request.GET[b'username'].split(b',')
                q = q & (Q(username__in=usernames) | Q(hosting_account__username__in=usernames))
            return queryset.filter(q).distinct()
        else:
            return self.model.objects.filter(local_site=local_site)

    def parse_tool_field(self, value, **kwargs):
        """Parse the tool field in a request.

        Args:
            value (unicode):
                The name of the tool, as provided in the request.

            **kwargs (dict):
                Additional keyword arguments passed to the method.

        Returns:
            unicode:
            The resulting SCMTool ID to use for the form.

        Raises:
            django.core.exceptions.ValidationError:
                The tool could not be found.
        """
        try:
            return Tool.objects.filter(name=value)[0].scmtool_id
        except IndexError:
            raise ValidationError(b'This is not a valid SCMTool')

    def serialize_tool_field(self, obj, **kwargs):
        return obj.tool.name

    def has_access_permissions(self, request, repository, *args, **kwargs):
        return repository.is_accessible_by(request.user)

    def has_modify_permissions(self, request, repository, *args, **kwargs):
        return repository.is_mutable_by(request.user)

    def has_delete_permissions(self, request, repository, *args, **kwargs):
        return repository.is_mutable_by(request.user)

    @webapi_check_login_required
    @webapi_check_local_site
    @webapi_request_fields(optional=dict({b'name': {b'type': str, 
                 b'description': b'Filter repositories by one or more comma-separated names.', 
                 b'added_in': b'1.7.21'}, 
       b'path': {b'type': str, 
                 b'description': b'Filter repositories by one or more comma-separated paths or mirror paths.', 
                 b'added_in': b'1.7.21'}, 
       b'name-or-path': {b'type': str, 
                         b'description': b'Filter repositories by one or more comma-separated names, paths, or mirror paths.', 
                         b'added_in': b'1.7.21'}, 
       b'tool': {b'type': str, 
                 b'description': b'Filter repositories by one or more comma-separated tool names.', 
                 b'added_in': b'1.7.21'}, 
       b'hosting-service': {b'type': str, 
                            b'description': b'Filter repositories by one or more comma-separated hosting service IDs.', 
                            b'added_in': b'1.7.21'}, 
       b'username': {b'type': str, 
                     b'description': b'Filter repositories by one or more comma-separated usernames.', 
                     b'added_in': b'1.7.21'}, 
       b'show-invisible': {b'type': bool, 
                           b'description': b'Whether to list only visible repositories or all repositories.', 
                           b'added_in': b'2.0'}}, **WebAPIResource.get_list.optional_fields), required=WebAPIResource.get_list.required_fields, allow_unknown=True)
    def get_list(self, request, *args, **kwargs):
        """Retrieves the list of repositories on the server.

        This will only list visible repositories. Any repository that the
        administrator has hidden will be excluded from the list.
        """
        show_invisible = request.GET.get(b'show-invisible', False)
        return super(RepositoryResource, self).get_list(request, show_invisible=show_invisible, *args, **kwargs)

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Retrieves information on a particular repository.

        This will only return basic information on the repository.
        Authentication information, hosting details, and repository-specific
        information are not provided.
        """
        pass

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(BAD_HOST_KEY, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED, REPO_AUTHENTICATION_ERROR, REPO_INFO_ERROR, REPOSITORY_ALREADY_EXISTS, SERVER_CONFIG_ERROR, UNVERIFIED_HOST_CERT, UNVERIFIED_HOST_KEY)
    @webapi_request_fields(required={b'name': {b'type': six.text_type, 
                 b'description': b'The human-readable name of the repository.', 
                 b'added_in': b'1.6'}, 
       b'path': {b'type': six.text_type, 
                 b'description': b'The path to the repository.', 
                 b'added_in': b'1.6'}, 
       b'tool': {b'type': six.text_type, 
                 b'description': b'The name of the SCMTool to use. Valid names can be found in the Administration UI.', 
                 b'added_in': b'1.6'}}, optional={b'bug_tracker': {b'type': six.text_type, 
                        b'description': b'The URL to a bug in the bug tracker for this repository, with ``%s`` in place of the bug ID.', 
                        b'added_in': b'1.6'}, 
       b'encoding': {b'type': six.text_type, 
                     b'description': b'The encoding used for files in the repository. This is an advanced setting and should only be used if you absolutely need it.', 
                     b'added_in': b'1.6'}, 
       b'mirror_path': {b'type': six.text_type, 
                        b'description': b'An alternate path to the repository.', 
                        b'added_in': b'1.6'}, 
       b'password': {b'type': six.text_type, 
                     b'description': b'The password used to access the repository.', 
                     b'added_in': b'1.6'}, 
       b'public': {b'type': bool, 
                   b'description': b'Whether or not review requests on the repository will be publicly accessible by users on the site. The default is true.', 
                   b'added_in': b'1.6'}, 
       b'raw_file_url': {b'type': six.text_type, 
                         b'description': b"A URL mask used to check out a particular file using HTTP. This is needed for repository types that can't access files natively. Use ``<revision>`` and ``<filename>`` in the URL in place of the revision and filename parts of the path.", 
                         b'added_in': b'1.6'}, 
       b'trust_host': {b'type': bool, 
                       b'description': b'Whether or not any unknown host key or certificate should be accepted. The default is false, in which case this will error out if encountering an unknown host key or certificate.', 
                       b'added_in': b'1.6'}, 
       b'username': {b'type': six.text_type, 
                     b'description': b'The username used to access the repository.', 
                     b'added_in': b'1.6'}, 
       b'visible': {b'type': bool, 
                    b'description': b'Whether the repository is visible.', 
                    b'added_in': b'2.0'}})
    def create(self, request, local_site, parsed_request_fields, *args, **kwargs):
        """Creates a repository.

        This will create a new repository that can immediately be used for
        review requests.

        The ``tool`` is a registered SCMTool name. This must be known
        beforehand, and can be looked up in the Review Board administration UI.

        Before saving the new repository, the repository will be checked for
        access. On success, the repository will be created and this will
        return :http:`201`.

        In the event of an access problem (authentication problems,
        bad/unknown SSH key, or unknown certificate), an error will be
        returned and the repository information won't be updated. Pass
        ``trust_host=1`` to approve bad/unknown SSH keys or certificates.
        """
        if not Repository.objects.can_create(request.user, local_site):
            return self.get_no_access_error(request)
        return self._create_or_update(form_data=parsed_request_fields, request=request, local_site=local_site)

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED, INVALID_FORM_DATA, SERVER_CONFIG_ERROR, BAD_HOST_KEY, UNVERIFIED_HOST_KEY, UNVERIFIED_HOST_CERT, REPO_AUTHENTICATION_ERROR, REPO_INFO_ERROR)
    @webapi_request_fields(optional={b'archive_name': {b'type': bool, 
                         b'description': b"Whether or not the (non-user-visible) name of the repository should be changed so that it (probably) won't conflict with any future repository names. Starting in 3.0.12, performing a DELETE will archive the repository, and is the preferred method.", 
                         b'added_in': b'1.6.2', 
                         b'deprecated_in': b'3.0.12'}, 
       b'bug_tracker': {b'type': six.text_type, 
                        b'description': b'The URL to a bug in the bug tracker for this repository, with ``%s`` in place of the bug ID.', 
                        b'added_in': b'1.6'}, 
       b'encoding': {b'type': six.text_type, 
                     b'description': b'The encoding used for files in the repository. This is an advanced setting and should only be used if you absolutely need it.', 
                     b'added_in': b'1.6'}, 
       b'mirror_path': {b'type': six.text_type, 
                        b'description': b'An alternate path to the repository.', 
                        b'added_in': b'1.6'}, 
       b'name': {b'type': six.text_type, 
                 b'description': b'The human-readable name of the repository.', 
                 b'added_in': b'1.6'}, 
       b'password': {b'type': six.text_type, 
                     b'description': b'The password used to access the repository.', 
                     b'added_in': b'1.6'}, 
       b'path': {b'type': six.text_type, 
                 b'description': b'The path to the repository.', 
                 b'added_in': b'1.6'}, 
       b'public': {b'type': bool, 
                   b'description': b'Whether or not review requests on the repository will be publicly accessible by users on the site. The default is true.', 
                   b'added_in': b'1.6'}, 
       b'raw_file_url': {b'type': six.text_type, 
                         b'description': b"A URL mask used to check out a particular file using HTTP. This is needed for repository types that can't access files natively. Use ``<revision>`` and ``<filename>`` in the URL in place of the revision and filename parts of the path.", 
                         b'added_in': b'1.6'}, 
       b'trust_host': {b'type': bool, 
                       b'description': b'Whether or not any unknown host key or certificate should be accepted. The default is false, in which case this will error out if encountering an unknown host key or certificate.', 
                       b'added_in': b'1.6'}, 
       b'username': {b'type': six.text_type, 
                     b'description': b'The username used to access the repository.', 
                     b'added_in': b'1.6'}, 
       b'visible': {b'type': bool, 
                    b'description': b'Whether the repository is visible.', 
                    b'added_in': b'2.0'}})
    def update(self, request, local_site, parsed_request_fields, archive_name=None, *args, **kwargs):
        """Updates a repository.

        This will update the information on a repository. If the path,
        username, or password has changed, Review Board will try again to
        verify access to the repository.

        In the event of an access problem (authentication problems,
        bad/unknown SSH key, or unknown certificate), an error will be
        returned and the repository information won't be updated. Pass
        ``trust_host=1`` to approve bad/unknown SSH keys or certificates.
        """
        try:
            repository = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_modify_permissions(request, repository):
            return self.get_no_access_error(request)
        form_data = parsed_request_fields.copy()
        form_data[b'tool'] = repository.tool.name
        return self._create_or_update(repository=repository, form_data=form_data, request=request, local_site=local_site, archive=archive_name)

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    def delete(self, request, *args, **kwargs):
        """Deletes a repository.

        Repositories associated with review requests won't be fully deleted
        from the database. Instead, they'll be archived, removing them from
        any lists of repositories but freeing up their name for use in a
        future repository.

        .. versionchanged::
            3.0.12
            Previous releases simply marked a repository as invisible when
            deleting. Starting in 3.0.12, the repository is archived instead.
        """
        try:
            repository = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_delete_permissions(request, repository):
            return self.get_no_access_error(request)
        if repository.review_requests.exists():
            repository.archive()
        else:
            repository.delete()
        return (204, {})

    def _create_or_update(self, form_data, request, local_site, repository=None, archive=False):
        """Create or update a repository.

        Args:
            form_data (dict):
                The repository data to pass to the form.

            request (django.http.HttpRequest):
                The HTTP request from the client.

            local_site (reviewboard.site.models.LocalSite):
                The Local Site being operated on.

            repository (reviewboard.scmtools.models.Repository):
                An existing repository instance to update, if responding to
                a HTTP PUT request.

            archive (bool, optional):
                Whether to archive the repository after updating it.

        Returns:
            tuple or django.http.HttpResponse:
            The response to send back to the client.
        """
        if form_data.get(b'bug_tracker'):
            form_data[b'bug_tracker_type'] = RepositoryForm.CUSTOM_BUG_TRACKER_ID
        return self.handle_form_request(data=form_data, request=request, instance=repository, form_kwargs={b'limit_to_local_site': local_site, 
           b'request': request}, archive=archive)

    def save_form(self, archive, **kwargs):
        """Save the form.

        This will save the repository instance and then optionally archive
        the repository.

        Args:
            archive (bool):
                Whether to archive the repository.

            **kwargs (dict):
                Additional keyword arguments to pass to the parent method.

        Returns:
            reviewboard.scmtools.models.Repository:
            The saved repository.
        """
        repository = super(RepositoryResource, self).save_form(**kwargs)
        if archive:
            repository.archive()
        return repository

    def build_form_error_response(self, form=None, **kwargs):
        """Build an error response based on the form.

        Args:
            form (reviewboard.scmtools.forms.RepositoryForm, optional):
                The repository form.

            **kwargs (dict):
                Keyword arguments passed to this method.

        Returns:
            tuple or django.http.HttpResponse:
            The error response.
        """
        if form is not None:
            if form.get_repository_already_exists():
                return REPOSITORY_ALREADY_EXISTS
            if form.form_validation_error is not None:
                code = getattr(form.form_validation_error, b'code', None)
                params = getattr(form.form_validation_error, b'params') or {}
                e = params.get(b'exception')
                if code == b'repository_not_found':
                    return MISSING_REPOSITORY
                if code == b'repo_auth_failed':
                    return (REPO_AUTHENTICATION_ERROR,
                     {b'reason': six.text_type(e)})
                if code == b'cert_unverified':
                    cert = e.certificate
                    return (
                     UNVERIFIED_HOST_CERT,
                     {b'certificate': {b'failures': cert.failures, 
                                         b'fingerprint': cert.fingerprint, 
                                         b'hostname': cert.hostname, 
                                         b'issuer': cert.issuer, 
                                         b'valid': {b'from': cert.valid_from, 
                                                    b'until': cert.valid_until}}})
                if code == b'host_key_invalid':
                    return (BAD_HOST_KEY,
                     {b'hostname': e.hostname, 
                        b'expected_key': e.raw_expected_key.get_base64(), 
                        b'key': e.raw_key.get_base64()})
                if code == b'host_key_unverified':
                    return (UNVERIFIED_HOST_KEY,
                     {b'hostname': e.hostname, 
                        b'key': e.raw_key.get_base64()})
                if code in ('accept_cert_failed', 'add_host_key_failed', 'replace_host_key_failed'):
                    return (SERVER_CONFIG_ERROR,
                     {b'reason': six.text_type(e)})
                if code == b'missing_ssh_key':
                    return MISSING_USER_KEY
                if code in ('unexpected_scm_failure', 'unexpected_ssh_failure', 'unexpected_failure'):
                    return (REPO_INFO_ERROR,
                     {b'error': six.text_type(e)})
        return super(RepositoryResource, self).build_form_error_response(form=form, **kwargs)


repository_resource = RepositoryResource()