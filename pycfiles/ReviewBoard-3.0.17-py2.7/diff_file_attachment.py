# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/diff_file_attachment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.db.models import Q
from django.utils import six
from djblets.util.decorators import augment_method_from
from djblets.webapi.decorators import webapi_request_fields
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import resources
from reviewboard.webapi.resources.base_review_request_file_attachment import BaseReviewRequestFileAttachmentResource

class DiffFileAttachmentResource(BaseReviewRequestFileAttachmentResource):
    """Provides information on file attachments associated with files in diffs.

    The list of file attachments are tied to files either committed to the
    repository or proposed in diffs to a review request on the repository.
    All are associated with a file in a diff.

    Files that are newly introduced in a diff and do not have a revision as
    of that diff will have the ``added_in_filediff`` link set, and
    ``repository_revision`` will be null.
    """
    added_in = b'2.0'
    name = b'diff_file_attachment'
    model_parent_key = b'repository'
    mimetype_list_resource_name = b'diff-file-attachments'
    mimetype_item_resource_name = b'diff-file-attachment'
    fields = dict({b'repository_file_path': {b'type': six.text_type, 
                                 b'description': b'The file path inside the repository that this file attachment represents.'}, 
       b'repository_revision': {b'type': six.text_type, 
                                b'description': b'The revision that introduced this version of the file, if committed in the repository.'}, 
       b'added_in_filediff': {b'type': b'reviewboard.webapi.resources.filediff.FileDiffResource', 
                              b'description': b'The file diff that introduced this file. If set, this file is just part of a proposed change, and not necessarily committed in the repository.'}}, **BaseReviewRequestFileAttachmentResource.fields)

    def serialize_repository_file_path_field(self, attachment, **kwargs):
        if attachment.added_in_filediff_id:
            return attachment.added_in_filediff.dest_file
        else:
            return attachment.repo_path

    def serialize_repository_revision_field(self, attachment, **kwargs):
        return attachment.repo_revision or None

    def has_access_permissions(self, request, obj, *args, **kwargs):
        repository = self.get_parent_object(obj)
        return repository.is_accessible_by(request.user)

    def get_queryset(self, request, is_list=False, *args, **kwargs):
        repository = resources.repository.get_object(request, *args, **kwargs)
        queryset = self.model.objects.filter_for_repository(repository)
        if is_list:
            q = Q()
            if b'repository-file-path' in kwargs:
                path = kwargs[b'repository-file-path']
                q = q & (Q(repo_path=path) | Q(added_in_filediff__source_file=path))
            if b'repository-revision' in kwargs:
                q = q & Q(repo_revision=kwargs[b'repository-revision'])
            if b'mimetype' in kwargs:
                q = q & Q(mimetype=kwargs[b'mimetype'])
            queryset = queryset.filter(q)
        return queryset

    def get_parent_object(self, obj):
        if obj.repository_id is None:
            assert obj.added_in_filediff_id is not None
            return obj.added_in_filediff.diffset.repository
        else:
            return obj.repository
            return

    @webapi_check_local_site
    @webapi_request_fields(optional=dict({b'repository-file-path': {b'type': six.text_type, 
                                 b'description': b'Filter file attachments with the given path in the repository.'}, 
       b'repository-revision': {b'type': six.text_type, 
                                b'description': b'Filter file attachments for files with the given revision.'}, 
       b'mimetype': {b'type': six.text_type, 
                     b'description': b'Filter file attachments with the given mimetype.'}}, **BaseReviewRequestFileAttachmentResource.get_list.optional_fields), required=BaseReviewRequestFileAttachmentResource.get_list.required_fields)
    @augment_method_from(BaseReviewRequestFileAttachmentResource)
    def get_list(self, request, *args, **kwargs):
        """Returns the list of file attachments associated with diffs.

        Each item in this list is a file attachment associated with a file
        or a proposed change against the parent repository. A file attachment
        may be referenced by one or more diffs.
        """
        pass


diff_file_attachment_resource = DiffFileAttachmentResource()