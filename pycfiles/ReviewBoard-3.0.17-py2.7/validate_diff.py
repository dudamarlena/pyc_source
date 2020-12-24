# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/validate_diff.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
import logging
from django.db.models import Q
from django.utils import six
from djblets.webapi.decorators import webapi_login_required, webapi_response_errors, webapi_request_fields
from djblets.webapi.errors import DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED
from reviewboard.diffviewer.errors import DiffParserError, DiffTooBigError, EmptyDiffError
from reviewboard.diffviewer.models import DiffSet
from reviewboard.scmtools.models import Repository
from reviewboard.scmtools.errors import FileNotFoundError, SCMError
from reviewboard.scmtools.git import ShortSHA1Error
from reviewboard.webapi.decorators import webapi_check_login_required, webapi_check_local_site
from reviewboard.webapi.errors import DIFF_EMPTY, DIFF_PARSE_ERROR, DIFF_TOO_BIG, INVALID_REPOSITORY, REPO_FILE_NOT_FOUND
from reviewboard.webapi.resources.diff import DiffResource

class ValidateDiffResource(DiffResource):
    """Verifies whether a diff file will work.

    This allows clients to validate whether a diff file (with optional parent
    diff) can be parsed and displayed, without actually creating a review
    request first.
    """
    added_in = b'2.0'
    singleton = True
    name = b'diff_validation'
    uri_name = b'diffs'
    uri_object_key = None
    allowed_methods = ('GET', 'POST')
    item_child_resources = []
    list_child_resources = []

    @webapi_check_local_site
    @webapi_check_login_required
    def get(self, request, *args, **kwargs):
        """Returns links for using this resource."""
        return (
         200,
         {b'links': self.get_links(request=request, *args, **kwargs)})

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED, REPO_FILE_NOT_FOUND, INVALID_FORM_DATA, INVALID_REPOSITORY, DIFF_EMPTY, DIFF_TOO_BIG, DIFF_PARSE_ERROR)
    @webapi_request_fields(required={b'repository': {b'type': six.text_type, 
                       b'description': b'The path or ID of the repository.'}, 
       b'path': {b'type': file, 
                 b'description': b'The main diff file.'}}, optional={b'basedir': {b'type': six.text_type, 
                    b'description': b'The base directory that will prepended to all paths in the diff. This is needed for some types of repositories. The directory must be between the root of the repository and the top directory referenced in the diff paths.'}, 
       b'parent_diff_path': {b'type': file, 
                             b'description': b'The optional parent diff to upload.'}, 
       b'base_commit_id': {b'type': six.text_type, 
                           b'description': b'The ID/revision this change is built upon. If using a parent diff, then this is the base for that diff. This may not be provided for all diffs or repository types, depending on how the diff was uploaded.'}})
    def create(self, request, repository, basedir=None, local_site_name=None, base_commit_id=None, *args, **kwargs):
        """Validate a diff.

        This API has a similar signature to the ReviewRequest resource POST
        API, but instead of actually creating a review request, will return
        either OK or an error, depending on whether the included diff file
        parsed correctly.
        """
        local_site = self._get_local_site(local_site_name)
        path = request.FILES.get(b'path')
        parent_diff_path = request.FILES.get(b'parent_diff_path')
        try:
            q = Q(pk=int(repository))
        except ValueError:
            q = Q(path=repository) | Q(mirror_path=repository) | Q(name=repository)

        repositories = Repository.objects.accessible(request.user, local_site=local_site).filter(q)
        repository_count = repositories.count()
        if repository_count == 0:
            return (
             INVALID_REPOSITORY,
             {b'repository': repository})
        if repository_count > 1:
            msg = b'Too many repositories matched "%s". Try specifying the repository by name instead.' % repository
            return (
             INVALID_REPOSITORY.with_message(msg),
             {b'repository': repository})
        else:
            repository = repositories.first()
            if not repository.get_scmtool().diffs_use_absolute_paths and basedir is None:
                return (
                 INVALID_FORM_DATA,
                 {b'fields': {b'basedir': [
                                           b'Given repository requires a base directory']}})
            if basedir is None:
                basedir = b''
            try:
                DiffSet.objects.create_from_upload(repository=repository, diff_file=path, parent_diff_file=parent_diff_path, basedir=basedir, request=request, base_commit_id=base_commit_id, validate_only=True)
            except FileNotFoundError as e:
                return (
                 REPO_FILE_NOT_FOUND,
                 {b'file': e.path, 
                    b'revision': six.text_type(e.revision)})
            except EmptyDiffError:
                return DIFF_EMPTY
            except DiffTooBigError as e:
                return (
                 DIFF_TOO_BIG,
                 {b'reason': six.text_type(e), 
                    b'max_size': e.max_diff_size})
            except DiffParserError as e:
                return (
                 DIFF_PARSE_ERROR,
                 {b'reason': six.text_type(e), 
                    b'linenum': e.linenum})
            except ShortSHA1Error as e:
                return (
                 REPO_FILE_NOT_FOUND,
                 {b'reason': six.text_type(e), 
                    b'file': e.path, 
                    b'revision': six.text_type(e.revision)})
            except SCMError as e:
                return DIFF_PARSE_ERROR.with_message(six.text_type(e))
            except Exception as e:
                logging.exception(b'Unexpected error when validating diff.')
                return DIFF_PARSE_ERROR.with_message(b'Unexpected error when validating the diff: %s' % e)

            return (200, {})

    def _build_named_url(self, name):
        """Builds a Django URL name from the provided name."""
        return b'validate-diffs-resource'


validate_diff_resource = ValidateDiffResource()