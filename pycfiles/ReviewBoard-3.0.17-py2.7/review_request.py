# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/review_request.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
import logging, dateutil.parser
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ValidationError
from django.db.models import Q
from django.utils import six
from django.utils.timezone import get_current_timezone, is_aware, make_aware
from djblets.util.decorators import augment_method_from
from djblets.webapi.decorators import webapi_login_required, webapi_response_errors, webapi_request_fields
from djblets.webapi.errors import DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED
from pytz.exceptions import AmbiguousTimeError
from reviewboard.admin.server import build_server_url
from reviewboard.diffviewer.errors import DiffTooBigError, DiffParserError, EmptyDiffError
from reviewboard.reviews.errors import CloseError, PermissionError, PublishError, ReopenError
from reviewboard.reviews.fields import get_review_request_field
from reviewboard.reviews.models import ReviewRequest
from reviewboard.scmtools.errors import AuthenticationError, ChangeNumberInUseError, EmptyChangeSetError, InvalidChangeNumberError, SCMError, RepositoryNotFoundError
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.ssh.errors import SSHError
from reviewboard.scmtools.models import Repository
from reviewboard.webapi.base import ImportExtraDataError, WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site, webapi_check_login_required
from reviewboard.webapi.errors import CHANGE_NUMBER_IN_USE, CLOSE_ERROR, COMMIT_ID_ALREADY_EXISTS, DIFF_EMPTY, DIFF_TOO_BIG, DIFF_PARSE_ERROR, EMPTY_CHANGESET, INVALID_CHANGE_NUMBER, INVALID_REPOSITORY, INVALID_USER, MISSING_REPOSITORY, PUBLISH_ERROR, REOPEN_ERROR, REPO_AUTHENTICATION_ERROR, REPO_INFO_ERROR
from reviewboard.webapi.mixins import MarkdownFieldsMixin
from reviewboard.webapi.resources import resources
from reviewboard.webapi.resources.repository import RepositoryResource
from reviewboard.webapi.resources.review_group import ReviewGroupResource
from reviewboard.webapi.resources.review_request_draft import ReviewRequestDraftResource
from reviewboard.webapi.resources.user import UserResource

class ReviewRequestResource(MarkdownFieldsMixin, WebAPIResource):
    """Provides information on review requests.

    Review requests are one of the central concepts in Review Board. They
    represent code or files that are being placed up for review.

    A review request has a number of fields that can be filled out, indicating
    the summary, description of the change, testing that was done, affected
    bugs, and more. These must be filled out through the associated Review
    Request Draft resource.

    When a review request is published, it can be reviewed by users. It can
    then be updated, again through the Review Request Draft resource, or closed
    as submitted or discarded.
    """
    model = ReviewRequest
    name = b'review_request'
    fields = {b'id': {b'type': int, 
               b'description': b'The numeric ID of the review request.'}, 
       b'approved': {b'type': bool, 
                     b'description': b'Whether the review request has been approved by reviewers.\n\nOn a default install, a review request is approved if it has at least one Ship It! and no open issues. Extensions may change these requirements.', 
                     b'added_in': b'2.0'}, 
       b'approval_failure': {b'type': six.text_type, 
                             b'description': b'The reason why the review request was not approved. This will be ``null`` if approved.', 
                             b'added_in': b'2.0'}, 
       b'blocks': {b'type': [
                           b'reviewboard.webapi.resources.review_request.ReviewRequestResource'], 
                   b'description': b'The list of review requests that this review request is blocking.', 
                   b'added_in': b'1.7.9'}, 
       b'close_description': {b'type': six.text_type, 
                              b'description': b'The text describing the closing of the review request.', 
                              b'added_in': b'2.0.12', 
                              b'supports_text_types': True}, 
       b'close_description_text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                                        b'description': b'The current or forced text type for the ``close_description`` field.', 
                                        b'added_in': b'2.0.12'}, 
       b'depends_on': {b'type': [
                               b'reviewboard.webapi.resources.review_request.ReviewRequestResource'], 
                       b'description': b'The list of review requests that this review request depends on.', 
                       b'added_in': b'1.7.9'}, 
       b'extra_data': {b'type': dict, 
                       b'description': b'Extra data as part of the review request. This can be set by the API or extensions.', 
                       b'added_in': b'2.0'}, 
       b'issue_dropped_count': {b'type': int, 
                                b'description': b'The number of dropped issues on this review request', 
                                b'added_in': b'2.0'}, 
       b'issue_open_count': {b'type': int, 
                             b'description': b'The number of open issues on this review request', 
                             b'added_in': b'2.0'}, 
       b'issue_resolved_count': {b'type': int, 
                                 b'description': b'The number of resolved issues on this review request', 
                                 b'added_in': b'2.0'}, 
       b'issue_verifying_count': {b'type': int, 
                                  b'description': b'The number of issues waiting for verification to resolve or drop on this review request', 
                                  b'added_in': b'3.0.3'}, 
       b'submitter': {b'type': UserResource, 
                      b'description': b'The user who submitted the review request.'}, 
       b'time_added': {b'type': six.text_type, 
                       b'description': b'The date and time that the review request was added (in ``YYYY-MM-DD HH:MM:SS`` format).'}, 
       b'last_updated': {b'type': six.text_type, 
                         b'description': b'The date and time that the review request was last updated (in ``YYYY-MM-DD HH:MM:SS`` format).'}, 
       b'text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                      b'description': b'Formerly responsible for indicating the text type for text fields. Replaced by ``close_description_text_type``, ``description_text_type``, and ``testing_done_text_type`` in 2.0.12.', 
                      b'added_in': b'2.0', 
                      b'deprecated_in': b'2.0.12'}, 
       b'status': {b'type': ('discarded', 'pending', 'submitted'), 
                   b'description': b'The current status of the review request.'}, 
       b'public': {b'type': bool, 
                   b'description': b'Whether or not the review request is currently visible to other users.'}, 
       b'changenum': {b'type': int, 
                      b'description': b'The change number that the review request represents. These are server-side repository-specific change numbers, and are not supported by all types of repositories. It may be ``null``.\n\nThis is deprecated in favor of the ``commit_id`` field.', 
                      b'deprecated_in': b'2.0'}, 
       b'commit_id': {b'type': six.text_type, 
                      b'description': b'The commit that the review request represents. This obsoletes the ``changenum`` field.', 
                      b'added_in': b'2.0'}, 
       b'repository': {b'type': RepositoryResource, 
                       b'description': b"The repository that the review request's code is stored on."}, 
       b'ship_it_count': {b'type': int, 
                          b'description': b'The number of Ship Its given to this review request.', 
                          b'added_in': b'2.0'}, 
       b'summary': {b'type': six.text_type, 
                    b'description': b"The review request's brief summary."}, 
       b'description': {b'type': six.text_type, 
                        b'description': b"The review request's description.", 
                        b'supports_text_types': True}, 
       b'description_text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                                  b'description': b'The current or forced text type for the ``description`` field.', 
                                  b'added_in': b'2.0.12'}, 
       b'testing_done': {b'type': six.text_type, 
                         b'description': b'The information on the testing that was done for the change.', 
                         b'supports_text_types': True}, 
       b'testing_done_text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                                   b'description': b'The current or forced text type for the ``testing_done`` field.', 
                                   b'added_in': b'2.0.12'}, 
       b'bugs_closed': {b'type': [
                                six.text_type], 
                        b'description': b'The list of bugs closed or referenced by this change.'}, 
       b'branch': {b'type': six.text_type, 
                   b'description': b'The branch that the code was changed on or that the code will be committed to. This is a free-form field that can store any text.'}, 
       b'target_groups': {b'type': [
                                  ReviewGroupResource], 
                          b'description': b'The list of review groups who were requested to review this change.'}, 
       b'target_people': {b'type': [
                                  UserResource], 
                          b'description': b'The list of users who were requested to review this change.'}, 
       b'url': {b'type': six.text_type, 
                b'description': b"The URL to the review request's page on the site. This is deprecated and will be removed in a future version.", 
                b'added_in': b'1.7.8', 
                b'deprecated_in': b'2.0'}, 
       b'absolute_url': {b'type': six.text_type, 
                         b'description': b"The absolute URL to the review request's page on the site.", 
                         b'added_in': b'2.0'}}
    uri_object_key = b'review_request_id'
    model_object_key = b'display_id'
    item_child_resources = [
     resources.change,
     resources.diff,
     resources.diff_context,
     resources.file_attachment,
     resources.review,
     resources.review_request_draft,
     resources.review_request_last_update,
     resources.screenshot,
     resources.status_update]
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    _close_type_map = {b'submitted': ReviewRequest.SUBMITTED, 
       b'discarded': ReviewRequest.DISCARDED}

    def get_related_links(self, obj=None, request=None, *args, **kwargs):
        """Return related links for the resource.

        This will serialize the ``latest_diff`` link when called for the
        item resource with a resource that has associated diffs.

        Args:
            obj (reviewboard.reviews.models.review_request.ReviewRequest, optional):
                The review request.

            request (django.http.HttpRequest, optional):
                The current HTTP request.

            *args (tuple):
                Additional positional arguments.

            **kwargs (dict):
                Additional keyword arguments.

        Returns:
            dict:
            A dictionary of links related to the resource.
        """
        links = super(ReviewRequestResource, self).get_related_links(obj=obj, request=request, *args, **kwargs)
        if obj:
            diffsets = list(obj.diffset_history.diffsets.all())
            if diffsets:
                latest_diffset = diffsets[(-1)]
                links[b'latest_diff'] = {b'href': build_server_url(local_site_reverse(b'diff-resource', request, kwargs={b'review_request_id': obj.display_id, 
                             b'diff_revision': latest_diffset.revision})), 
                   b'method': b'GET'}
        return links

    def get_queryset(self, request, is_list=False, local_site_name=None, *args, **kwargs):
        """Returns a queryset for ReviewRequest models.

        By default, this returns all published or formerly published
        review requests.

        If the queryset is being used for a list of review request
        resources, then it can be further filtered by one or more arguments
        in the URL. These are listed in @webapi_request_fields for get_list().

        Some arguments accept dates. The handling of dates is quite flexible,
        accepting a variety of date/time formats, but we recommend sticking
        with ISO8601 format.

        ISO8601 format defines a date as being in ``{yyyy}-{mm}-{dd}`` format,
        and a date/time as being in ``{yyyy}-{mm}-{dd}T{HH}:{MM}:{SS}``.
        A timezone can also be appended to this, using ``-{HH:MM}``.

        The following examples are valid dates and date/times:

            * ``2010-06-27``
            * ``2010-06-27T16:26:30``
            * ``2010-06-27T16:26:30-08:00``
        """
        local_site = self._get_local_site(local_site_name)
        if is_list:
            q = Q()
            if b'to-groups' in request.GET:
                for group_name in request.GET.get(b'to-groups').split(b','):
                    q = q & self.model.objects.get_to_group_query(group_name, local_site)

            if b'to-users' in request.GET:
                for username in request.GET.get(b'to-users').split(b','):
                    q = q & self.model.objects.get_to_user_query(username)

            if b'to-users-directly' in request.GET:
                to_users_directly = request.GET.get(b'to-users-directly').split(b',')
                for username in to_users_directly:
                    q = q & self.model.objects.get_to_user_directly_query(username)

            if b'to-users-groups' in request.GET:
                for username in request.GET.get(b'to-users-groups').split(b','):
                    q = q & self.model.objects.get_to_user_groups_query(username)

            if b'from-user' in request.GET:
                q = q & self.model.objects.get_from_user_query(request.GET.get(b'from-user'))
            if b'repository' in request.GET:
                q = q & Q(repository=int(request.GET.get(b'repository')))
            commit_q = Q()
            if b'changenum' in request.GET:
                try:
                    commit_q = Q(changenum=int(request.GET.get(b'changenum')))
                except (TypeError, ValueError):
                    pass

            commit_id = request.GET.get(b'commit-id', None)
            if commit_id is not None:
                commit_q = commit_q | Q(commit_id=commit_id)
            if commit_q:
                q = q & commit_q
            if b'branch' in kwargs:
                q &= Q(branch=kwargs[b'branch'])
            if b'ship-it' in request.GET:
                ship_it = request.GET.get(b'ship-it')
                if ship_it in ('1', 'true', 'True'):
                    q = q & Q(shipit_count__gt=0)
                elif ship_it in ('0', 'false', 'False'):
                    q = q & Q(shipit_count=0)
            q = q & self.build_queries_for_int_field(request, b'shipit_count', b'ship-it-count')
            for issue_field in ('issue_open_count', 'issue_dropped_count', 'issue_resolved_count',
                                'issue_verifying_count'):
                q = q & self.build_queries_for_int_field(request, issue_field)

            if b'time-added-from' in kwargs:
                q = q & Q(time_added__gte=kwargs[b'time-added-from'])
            if b'time-added-to' in kwargs:
                q = q & Q(time_added__lt=kwargs[b'time-added-to'])
            if b'last-updated-from' in kwargs:
                q = q & Q(last_updated__gte=kwargs[b'last-updated-from'])
            if b'last-updated-to' in kwargs:
                q = q & Q(last_updated__lt=kwargs[b'last-updated-to'])
            status = ReviewRequest.string_to_status(request.GET.get(b'status', b'pending'))
            can_submit_as = request.user.has_perm(b'reviews.can_submit_as_another_user', local_site)
            request_unpublished = request.GET.get(b'show-all-unpublished', b'0')
            if request_unpublished in ('0', 'false', 'False'):
                request_unpublished = False
            else:
                request_unpublished = True
            show_all_unpublished = request_unpublished and (can_submit_as or request.user.is_superuser)
            queryset = self.model.objects.public(user=request.user, status=status, local_site=local_site, extra_query=q, show_all_unpublished=show_all_unpublished)
            queryset = queryset.select_related(b'diffset_history').prefetch_related(b'changedescs', b'diffset_history__diffsets')
        else:
            queryset = self.model.objects.filter(local_site=local_site)
        return queryset

    def has_access_permissions(self, request, review_request, *args, **kwargs):
        return review_request.is_accessible_by(request.user)

    def has_modify_permissions(self, request, review_request, *args, **kwargs):
        return review_request.is_mutable_by(request.user)

    def has_delete_permissions(self, request, review_request, *args, **kwargs):
        return review_request.is_deletable_by(request.user)

    def get_extra_data_field_supports_markdown(self, review_request, key):
        field_cls = get_review_request_field(key)
        return field_cls and getattr(field_cls, b'enable_markdown', False)

    def get_is_close_description_rich_text(self, obj):
        if obj.status in (obj.SUBMITTED, obj.DISCARDED):
            if hasattr(obj, b'_close_description'):
                return obj._close_description_rich_text
            else:
                return obj.get_close_info()[b'is_rich_text']

        else:
            return False

    def serialize_bugs_closed_field(self, obj, **kwargs):
        return obj.get_bug_list()

    def serialize_close_description_field(self, obj, **kwargs):
        if obj.status in (obj.SUBMITTED, obj.DISCARDED):
            if hasattr(obj, b'_close_description'):
                return obj._close_description
            else:
                return obj.get_close_info()[b'close_description']

        else:
            return
        return

    def serialize_close_description_text_type_field(self, obj, **kwargs):
        return

    def serialize_description_text_type_field(self, obj, **kwargs):
        return

    def serialize_ship_it_count_field(self, obj, **kwargs):
        return obj.shipit_count

    def serialize_status_field(self, obj, **kwargs):
        return ReviewRequest.status_to_string(obj.status)

    def serialize_testing_done_text_type_field(self, obj, **kwargs):
        return

    def serialize_id_field(self, obj, **kwargs):
        return obj.display_id

    def serialize_url_field(self, obj, **kwargs):
        return obj.get_absolute_url()

    def serialize_absolute_url_field(self, obj, request, **kwargs):
        return request.build_absolute_uri(obj.get_absolute_url())

    def serialize_commit_id_field(self, obj, **kwargs):
        return obj.commit

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(NOT_LOGGED_IN, PERMISSION_DENIED, INVALID_USER, INVALID_REPOSITORY, CHANGE_NUMBER_IN_USE, INVALID_CHANGE_NUMBER, EMPTY_CHANGESET, REPO_AUTHENTICATION_ERROR, REPO_INFO_ERROR, MISSING_REPOSITORY, DIFF_EMPTY, DIFF_TOO_BIG, DIFF_PARSE_ERROR)
    @webapi_request_fields(optional={b'changenum': {b'type': int, 
                      b'description': b'The optional change number to look up for the review request details. This only works with repositories that support server-side changesets.\n\nThis is deprecated in favor of the ``commit_id`` field.', 
                      b'deprecated_in': b'2.0'}, 
       b'commit_id': {b'type': six.text_type, 
                      b'description': b'The optional commit to create the review request for. This should be used in place of the ``changenum`` field.\n\nIf ``create_from_commit_id=1`` is passed, then the review request information and diff will be based on this commit ID.', 
                      b'added_in': b'2.0'}, 
       b'create_from_commit_id': {b'type': bool, 
                                  b'description': b'If true, and if ``commit_id`` is provided, the review request information and (when supported) the idff will be based on the commit ID.', 
                                  b'added_in': b'2.0'}, 
       b'force_text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                            b'description': b'The text type, if any, to force for returned text fields. The contents will be converted to the requested type in the payload, but will not be saved as that type.', 
                            b'added_in': b'2.0.9'}, 
       b'repository': {b'type': six.text_type, 
                       b'description': b'The path or ID of the repository that the review request is for.'}, 
       b'submit_as': {b'type': six.text_type, 
                      b'description': b'The optional user to submit the review request as. This requires that the actual logged in user is either a superuser or has the ``reviews.can_submit_as_another_user`` permission.'}}, allow_unknown=True)
    def create(self, request, repository=None, submit_as=None, changenum=None, commit_id=None, local_site_name=None, create_from_commit_id=False, extra_fields={}, *args, **kwargs):
        """Creates a new review request.

        The new review request will start off as private and pending, and
        will normally be blank. However, if ``changenum`` or both
        ``commit_id`` and ``create_from_commit_id=1`` is passed and the given
        repository both supports server-side changesets and has changeset
        support in Review Board, some details (Summary, Description and
        Testing Done sections, for instance) may be automatically filled in
        from the server.

        Any new review request will have an associated draft (reachable
        through the ``draft`` link). All the details of the review request
        must be set through the draft. The new review request will be public
        when that first draft is published.

        A repository can be passed. This is required for diffs associated
        with a review request. A valid repository is in the form of a numeric
        repository ID, the name of a repository, or the path to a repository
        (matching exactly the registered repository's Path or Mirror Path
        fields in the adminstration interface).

        If a repository is not passed, this review request can only be
        used for attached files.

        Clients can create review requests on behalf of another user by setting
        the ``submit_as`` parameter to the username of the desired user. This
        requires that the client is currently logged in as a user that has the
        ``reviews.can_submit_as_another_user`` permission set. This capability
        is useful when writing automation scripts, such as post-commit hooks,
        that need to create review requests for another user.

        Extra data can be stored later lookup. See
        :ref:`webapi2.0-extra-data` for more information.
        """
        user = request.user
        local_site = self._get_local_site(local_site_name)
        changenum = changenum or None
        commit_id = commit_id or None
        if changenum is not None and commit_id is None:
            commit_id = six.text_type(changenum)
            create_from_commit_id = True
        if submit_as and user.username != submit_as:
            if not user.has_perm(b'reviews.can_submit_as_another_user', local_site):
                return self.get_no_access_error(request)
            user = self._find_user(submit_as, local_site, request)
            if not user:
                return INVALID_USER
        if repository is not None:
            try:
                try:
                    repository = Repository.objects.get(pk=int(repository), local_site=local_site)
                except ValueError:
                    repository = Repository.objects.get((Q(path=repository) | Q(mirror_path=repository) | Q(name=repository)) & Q(local_site=local_site))

            except Repository.DoesNotExist:
                return (
                 INVALID_REPOSITORY,
                 {b'repository': repository})
            except Repository.MultipleObjectsReturned:
                msg = b'Too many repositories matched "%s". Try specifying the repository by name instead.' % repository
                return (
                 INVALID_REPOSITORY.with_message(msg),
                 {b'repository': repository})

            if not repository.is_accessible_by(request.user):
                return self.get_no_access_error(request)
        try:
            review_request = ReviewRequest.objects.create(user, repository, commit_id, local_site, create_from_commit_id=create_from_commit_id)
            if extra_fields:
                try:
                    self.import_extra_data(review_request, review_request.extra_data, extra_fields)
                except ImportExtraDataError as e:
                    return e.error_payload

                review_request.save(update_fields=[b'extra_data'])
            return (201,
             {self.item_result_key: review_request})
        except AuthenticationError:
            return REPO_AUTHENTICATION_ERROR
        except RepositoryNotFoundError:
            return MISSING_REPOSITORY
        except ChangeNumberInUseError as e:
            return (
             CHANGE_NUMBER_IN_USE,
             {b'review_request': e.review_request})
        except InvalidChangeNumberError:
            return INVALID_CHANGE_NUMBER
        except EmptyChangeSetError:
            return EMPTY_CHANGESET
        except DiffTooBigError:
            return DIFF_TOO_BIG
        except EmptyDiffError:
            return DIFF_EMPTY
        except DiffParserError as e:
            return (
             DIFF_PARSE_ERROR,
             {b'linenum': e.linenum, 
                b'message': six.text_type(e)})
        except SSHError as e:
            logging.error(b'Got unexpected SSHError when creating repository: %s' % e, exc_info=1, request=request)
            return REPO_INFO_ERROR
        except SCMError as e:
            logging.error(b'Got unexpected SCMError when creating repository: %s' % e, exc_info=1, request=request)
            return REPO_INFO_ERROR
        except ValidationError:
            return COMMIT_ID_ALREADY_EXISTS

        return

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(optional={b'status': {b'type': ('discarded', 'pending', 'submitted'), 
                   b'description': b'The status of the review request. This can be changed to close or reopen the review request'}, 
       b'changenum': {b'type': int, 
                      b'description': b'The optional change number to set or update.\n\nThis can be used to re-associate with a new change number, or to create/update a draft with new information from the current change number.\n\nThis only works with repositories that support server-side changesets.\n\nThis is deprecated. Instead, set ``commit_id`` and ``update_from_commit_id=1``  on the draft.', 
                      b'added_in': b'1.5.4', 
                      b'deprecated_in': b'2.0'}, 
       b'close_description': {b'type': six.text_type, 
                              b'description': b'The description of the update. Should only be used if the review request have been submitted or discarded.\n\nThis replaces the old ``description`` field.', 
                              b'added_in': b'2.0.9', 
                              b'supports_text_types': True}, 
       b'close_description_text_type': {b'type': MarkdownFieldsMixin.SAVEABLE_TEXT_TYPES, 
                                        b'description': b'The text type for the close description of the update field.', 
                                        b'added_in': b'2.0', 
                                        b'deprecated_in': b'2.0.12'}, 
       b'description': {b'type': six.text_type, 
                        b'description': b'The description of the update. Should only be used if the review request have been submitted or discarded.\n\nThis is deprecated. Instead, set ``close_description``.', 
                        b'added_in': b'1.6', 
                        b'deprecated_in': b'2.0.9', 
                        b'supports_text_types': True}, 
       b'force_text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                            b'description': b'The text type, if any, to force for returned text fields. The contents will be converted to the requested type in the payload, but will not be saved as that type.', 
                            b'added_in': b'2.0.9'}, 
       b'text_type': {b'type': MarkdownFieldsMixin.SAVEABLE_TEXT_TYPES, 
                      b'description': b'The text type for the close description of the update field.\n\nThis is deprecated. Please use ``close_description_text_type`` instead.', 
                      b'added_in': b'2.0', 
                      b'deprecated_in': b'2.0.12'}}, allow_unknown=True)
    def update(self, request, status=None, changenum=None, close_description=None, close_description_text_type=None, description=None, text_type=None, extra_fields={}, *args, **kwargs):
        """Updates the status of the review request.

        The only supported update to a review request's resource is to change
        the status, the associated server-side, change number, or to update
        information from the existing change number.

        The status can be set in order to close the review request as
        discarded or submitted, or to reopen as pending.

        For Perforce, a change number can either be changed to a new number, or
        the current change number can be passed. In either case, a new draft
        will be created or an existing one updated to include information from
        the server based on the change number. This behavior is deprecated,
        and instead, the commit_id field should be set on the draft.

        Changes to a review request's fields, such as the summary or the
        list of reviewers, is made on the Review Request Draft resource.
        This can be accessed through the ``draft`` link. Only when that
        draft is published will the changes end up back in this resource.

        Extra data can be stored later lookup. See
        :ref:`webapi2.0-extra-data` for more information.
        """
        try:
            review_request = resources.review_request.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        is_mutating_field = changenum is not None or extra_fields
        if is_mutating_field and not self.has_modify_permissions(request, review_request) or status is not None and not review_request.is_status_mutable_by(request.user):
            return self.get_no_access_error(request)
        else:
            if status is not None and (review_request.status != ReviewRequest.string_to_status(status) or review_request.status != ReviewRequest.PENDING_REVIEW):
                try:
                    if status in self._close_type_map:
                        close_description = close_description or description
                        close_description_text_type = close_description_text_type or text_type
                        close_description_rich_text = close_description_text_type == self.TEXT_TYPE_MARKDOWN
                        try:
                            review_request.close(self._close_type_map[status], request.user, close_description, rich_text=close_description_rich_text)
                        except CloseError as e:
                            return CLOSE_ERROR.with_message(six.text_type(e))

                        review_request._close_description = close_description
                        review_request._close_description_rich_text = close_description_rich_text
                    elif status == b'pending':
                        try:
                            review_request.reopen(request.user)
                        except ReopenError as e:
                            return REOPEN_ERROR.with_message(six.text_type(e))

                    else:
                        raise AssertionError(b"Code path for invalid status '%s' should never be reached." % status)
                except PermissionError:
                    return self.get_no_access_error(request)
                except PublishError as e:
                    return PUBLISH_ERROR.with_message(six.text_type(e))

            changed_fields = []
            if changenum is not None:
                if review_request.repository is None:
                    return INVALID_CHANGE_NUMBER
                if changenum != review_request.changenum:
                    review_request.commit = six.text_type(changenum)
                    changed_fields.append(b'changenum')
                    changed_fields.append(b'commit_id')
                try:
                    review_request.reopen(request.user)
                except ReopenError as e:
                    return REOPEN_ERROR.with_message(six.text_type(e))

                try:
                    draft = ReviewRequestDraftResource.prepare_draft(request, review_request)
                except PermissionDenied:
                    return PERMISSION_DENIED

                try:
                    draft.update_from_commit_id(six.text_type(changenum))
                except InvalidChangeNumberError:
                    return INVALID_CHANGE_NUMBER
                except EmptyChangeSetError:
                    return EMPTY_CHANGESET

                draft.save()
            if extra_fields:
                try:
                    self.import_extra_data(review_request, review_request.extra_data, extra_fields)
                except ImportExtraDataError as e:
                    return e.error_payload

                changed_fields.append(b'extra_data')
            if changed_fields:
                review_request.save(update_fields=changed_fields)
            return (200,
             {self.item_result_key: review_request})

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def delete(self, *args, **kwargs):
        """Deletes the review request permanently.

        This is a dangerous call to make, as it will delete the review
        request, associated screenshots, diffs, and reviews. There is no
        going back after this call is made.

        Only users who have been granted the ``reviews.delete_reviewrequest``
        permission (which includes administrators) can perform a delete on
        the review request.

        After a successful delete, this will return :http:`204`.
        """
        pass

    @webapi_check_login_required
    @webapi_check_local_site
    @webapi_request_fields(optional={b'branch': {b'type': six.text_type, 
                   b'description': b'The branch field on a review request to filter by.', 
                   b'added_in': b'3.0.16'}, 
       b'changenum': {b'type': int, 
                      b'description': b'The change number the review requests must have set. This will only return one review request per repository, and only works for repository types that support server-side changesets. This is deprecated in favor of the ``commit_id`` field.'}, 
       b'commit-id': {b'type': six.text_type, 
                      b'description': b'The commit that review requests must have set. This will only return one review request per repository.\n\nThis obsoletes the ``changenum`` field.', 
                      b'added_in': b'2.0'}, 
       b'time-added-to': {b'type': six.text_type, 
                          b'description': b"The date/time that all review requests must be added before. This is compared against the review request's ``time_added`` field. This must be a valid :term:`date/time format`."}, 
       b'time-added-from': {b'type': six.text_type, 
                            b'description': b"The earliest date/time the review request could be added. This is compared against the review request's ``time_added`` field. This must be a valid :term:`date/time format`."}, 
       b'last-updated-to': {b'type': six.text_type, 
                            b'description': b"The date/time that all review requests must be last updated before. This is compared against the review request's ``last_updated`` field. This must be a valid :term:`date/time format`."}, 
       b'last-updated-from': {b'type': six.text_type, 
                              b'description': b"The earliest date/time the review request could be last updated. This is compared against the review request's ``last_updated`` field. This must be a valid :term:`date/time format`."}, 
       b'from-user': {b'type': six.text_type, 
                      b'description': b'The username that the review requests must be owned by.'}, 
       b'repository': {b'type': int, 
                       b'description': b'The ID of the repository that the review requests must be on.'}, 
       b'show-all-unpublished': {b'type': bool, 
                                 b'description': b'If set, and if the user is an admin or has the "reviews.can_submit_as_another_user" permission, unpublished review requests will also be returned.', 
                                 b'added_in': b'2.0.8'}, 
       b'issue-dropped-count': {b'type': int, 
                                b'description': b'The review request must have exactly the provided number of dropped issues.', 
                                b'added_in': b'2.0'}, 
       b'issue-dropped-count-lt': {b'type': int, 
                                   b'description': b'The review request must have less than the provided number of dropped issues.', 
                                   b'added_in': b'2.0'}, 
       b'issue-dropped-count-lte': {b'type': int, 
                                    b'description': b'The review request must have at most the provided number of dropped issues.', 
                                    b'added_in': b'2.0'}, 
       b'issue-dropped-count-gt': {b'type': int, 
                                   b'description': b'The review request must have more than the provided number of dropped issues.', 
                                   b'added_in': b'2.0'}, 
       b'issue-dropped-count-gte': {b'type': int, 
                                    b'description': b'The review request must have at least the provided number of dropped issues.', 
                                    b'added_in': b'2.0'}, 
       b'issue-open-count': {b'type': int, 
                             b'description': b'The review request must have exactly the provided number of open issues.', 
                             b'added_in': b'2.0'}, 
       b'issue-open-count-lt': {b'type': int, 
                                b'description': b'The review request must have less than the provided number of open issues.', 
                                b'added_in': b'2.0'}, 
       b'issue-open-count-lte': {b'type': int, 
                                 b'description': b'The review request must have at most the provided number of open issues.', 
                                 b'added_in': b'2.0'}, 
       b'issue-open-count-gt': {b'type': int, 
                                b'description': b'The review request must have more than the provided number of open issues.', 
                                b'added_in': b'2.0'}, 
       b'issue-open-count-gte': {b'type': int, 
                                 b'description': b'The review request must have at least the provided number of open issues.', 
                                 b'added_in': b'2.0'}, 
       b'issue-resolved-count': {b'type': int, 
                                 b'description': b'The review request must have exactly the provided number of resolved issues.', 
                                 b'added_in': b'2.0'}, 
       b'issue-resolved-count-lt': {b'type': int, 
                                    b'description': b'The review request must have less than the provided number of resolved issues.', 
                                    b'added_in': b'2.0'}, 
       b'issue-resolved-count-lte': {b'type': int, 
                                     b'description': b'The review request must have at most the provided number of resolved issues.', 
                                     b'added_in': b'2.0'}, 
       b'issue-resolved-count-gt': {b'type': int, 
                                    b'description': b'The review request must have more than the provided number of resolved issues.', 
                                    b'added_in': b'2.0'}, 
       b'issue-resolved-count-gte': {b'type': int, 
                                     b'description': b'The review request must have at least the provided number of resolved issues.', 
                                     b'added_in': b'2.0'}, 
       b'ship-it': {b'type': bool, 
                    b'description': b'The review request must have at least one review with Ship It set, if this is 1. Otherwise, if 0, it must not have any marked Ship It.', 
                    b'added_in': b'1.6', 
                    b'deprecated_in': b'2.0'}, 
       b'ship-it-count': {b'type': int, 
                          b'description': b'The review request must have exactly the provided number of Ship Its.', 
                          b'added_in': b'2.0'}, 
       b'ship-it-count-lt': {b'type': int, 
                             b'description': b'The review request must have less than the provided number of Ship Its.', 
                             b'added_in': b'2.0'}, 
       b'ship-it-count-lte': {b'type': int, 
                              b'description': b'The review request must have at most the provided number of Ship Its.', 
                              b'added_in': b'2.0'}, 
       b'ship-it-count-gt': {b'type': int, 
                             b'description': b'The review request must have more than the provided number of Ship Its.', 
                             b'added_in': b'2.0'}, 
       b'ship-it-count-gte': {b'type': int, 
                              b'description': b'The review request must have at least the provided number of Ship Its.', 
                              b'added_in': b'2.0'}, 
       b'status': {b'type': ('all', 'discarded', 'pending', 'submitted'), 
                   b'description': b'The status of the review requests.'}, 
       b'to-groups': {b'type': six.text_type, 
                      b'description': b'A comma-separated list of review group names that the review requests must have in the reviewer list.'}, 
       b'to-user-groups': {b'type': six.text_type, 
                           b'description': b'A comma-separated list of usernames who are in groups that the review requests must have in the reviewer list.'}, 
       b'to-users': {b'type': six.text_type, 
                     b'description': b'A comma-separated list of usernames that the review requests must either have in the reviewer list specifically or by way of a group.'}, 
       b'to-users-directly': {b'type': six.text_type, 
                              b'description': b'A comma-separated list of usernames that the review requests must have in the reviewer list specifically.'}}, allow_unknown=True)
    def get_list(self, request, *args, **kwargs):
        """Returns all review requests that the user has read access to.

        By default, this returns all published or formerly published
        review requests.

        The resulting list can be filtered down through the many
        request parameters.
        """
        invalid_fields = {}
        current_tz = get_current_timezone()
        for field in ('time-added-from', 'time-added-to', 'last-updated-from', 'last-updated-to'):
            if field in request.GET:
                try:
                    date = dateutil.parser.parse(request.GET[field])
                    if not is_aware(date):
                        date = make_aware(date, current_tz)
                    kwargs[field] = date
                except AmbiguousTimeError:
                    invalid_fields[field] = [
                     b'The given timestamp string was ambiguous because of daylight savings time changes. You may specify a UTC offset instead.']
                except ValueError:
                    invalid_fields[field] = [
                     b'The given timestamp could not be parsed.']

        if invalid_fields:
            return (INVALID_FORM_DATA,
             {b'fields': invalid_fields})
        else:
            return super(ReviewRequestResource, self).get_list(request, *args, **kwargs)

    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Returns information on a particular review request.

        This contains full information on the latest published review request.

        If the review request is not public, then the client's logged in user
        must either be the owner of the review request or must have the
        ``reviews.can_edit_reviewrequest`` permission set. Otherwise, an
        error will be returned.
        """
        pass

    def get_object(self, request, local_site_name=None, *args, **kwargs):
        """Returns an object, given captured parameters from a URL.

        This is an override of the djblets WebAPIResource get_object, which
        knows about local_id and local_site_name.
        """
        if local_site_name:
            id_field = b'local_id'
        else:
            id_field = b'pk'
        return super(ReviewRequestResource, self).get_object(request, id_field=id_field, local_site_name=local_site_name, *args, **kwargs)

    def get_href(self, obj, request, *args, **kwargs):
        """Returns the URL for this object.

        This is an override of WebAPIResource.get_href which will use the
        local_id instead of the pk.
        """
        if obj.local_site_id:
            local_site_name = obj.local_site.name
        else:
            local_site_name = None
        href_kwargs = {self.uri_object_key: obj.display_id}
        href_kwargs.update(self.get_href_parent_ids(obj))
        return request.build_absolute_uri(self.get_item_url(local_site_name=local_site_name, **href_kwargs))

    def _find_user(self, username, local_site, request):
        """Finds a User object matching ``username``.

        This will search all authentication backends, and may create the
        User object if the authentication backend knows that the user exists.
        """
        username = username.strip()
        if local_site:
            users = local_site.users
        else:
            users = User.objects
        try:
            user = users.get(username=username)
        except User.DoesNotExist:
            user = None
            if not local_site:
                for backend in auth.get_backends():
                    try:
                        return backend.get_or_create_user(username, request)
                    except Exception as e:
                        logging.error(b'Error when calling get_or_create_user for auth backend %r: %s', backend, e, exc_info=1)

        return user


review_request_resource = ReviewRequestResource()