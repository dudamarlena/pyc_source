# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/base_review_request_file_attachment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
import logging
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models import Q
from django.utils import six
from djblets.webapi.decorators import webapi_login_required, webapi_response_errors, webapi_request_fields
from djblets.webapi.errors import DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED
from reviewboard.attachments.forms import UploadFileForm
from reviewboard.attachments.models import FileAttachment
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import resources
from reviewboard.webapi.resources.base_file_attachment import BaseFileAttachmentResource

class BaseReviewRequestFileAttachmentResource(BaseFileAttachmentResource):
    """A base resource representing file attachments."""
    fields = dict({b'review_url': {b'type': six.text_type, 
                       b'description': b'The URL to a review UI for this file.', 
                       b'added_in': b'1.7'}, 
       b'url': {b'type': six.text_type, 
                b'description': b"The URL of the file, for downloading purposes. If this is not an absolute URL, then it's relative to the Review Board server's URL. This is deprecated and will be removed in a future version.", 
                b'deprecated_in': b'2.0'}, 
       b'revision': {b'type': int, 
                     b'description': b'The revision of the file attachment.', 
                     b'added_in': b'2.5'}, 
       b'attachment_history_id': {b'type': int, 
                                  b'description': b'ID of the corresponding FileAttachmentHistory.', 
                                  b'added_in': b'2.5'}}, **BaseFileAttachmentResource.fields)

    def get_queryset(self, request, is_list=False, *args, **kwargs):
        review_request = resources.review_request.get_object(request, *args, **kwargs)
        q = Q(review_request=review_request) & Q(added_in_filediff__isnull=True) & Q(repository__isnull=True) & Q(user__isnull=True)
        if not is_list:
            q = q | Q(inactive_review_request=review_request)
        if review_request.is_mutable_by(request.user):
            try:
                draft = resources.review_request_draft.get_object(request, *args, **kwargs)
                q = q | Q(drafts=draft)
                if not is_list:
                    q = q | Q(inactive_drafts=draft)
            except ObjectDoesNotExist:
                pass

        return self.model.objects.filter(q)

    def serialize_url_field(self, obj, **kwargs):
        return obj.get_absolute_url()

    def serialize_review_url_field(self, obj, **kwargs):
        if obj.review_ui:
            review_request = obj.get_review_request()
            if review_request.local_site_id:
                local_site_name = review_request.local_site.name
            else:
                local_site_name = None
            return local_site_reverse(b'file-attachment', local_site_name=local_site_name, kwargs={b'review_request_id': review_request.display_id, 
               b'file_attachment_id': obj.pk})
        else:
            return b''

    def serialize_revision_field(self, obj, *args, **kwargs):
        return obj.attachment_revision

    def has_access_permissions(self, request, obj, *args, **kwargs):
        return obj.get_review_request().is_accessible_by(request.user)

    def has_modify_permissions(self, request, obj, *args, **kwargs):
        return obj.get_review_request().is_mutable_by(request.user)

    def has_delete_permissions(self, request, obj, *args, **kwargs):
        return obj.get_review_request().is_mutable_by(request.user)

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, PERMISSION_DENIED, INVALID_FORM_DATA, NOT_LOGGED_IN)
    @webapi_request_fields(required={b'path': {b'type': file, 
                 b'description': b'The file to upload.'}}, optional={b'caption': {b'type': six.text_type, 
                    b'description': b'The optional caption describing the file.'}, 
       b'attachment_history': {b'type': int, 
                               b'description': b'ID of the corresponding FileAttachmentHistory.', 
                               b'added_in': b'2.5'}})
    def create(self, request, *args, **kwargs):
        """Creates a new file from a file attachment.

        This accepts any file type and associates it with a draft of a
        review request.

        It is expected that the client will send the data as part of a
        :mimetype:`multipart/form-data` mimetype. The file's name
        and content should be stored in the ``path`` field. A typical request
        may look like::

            -- SoMe BoUnDaRy
            Content-Disposition: form-data; name=path; filename="foo.zip"

            <Content here>
            -- SoMe BoUnDaRy --
        """
        try:
            review_request = resources.review_request.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not review_request.is_mutable_by(request.user):
            return self.get_no_access_error(request)
        form_data = request.POST.copy()
        form = UploadFileForm(review_request, form_data, request.FILES)
        if not form.is_valid():
            return (INVALID_FORM_DATA,
             {b'fields': self._get_form_errors(form)})
        try:
            file = form.create()
        except ValueError as e:
            return (
             INVALID_FORM_DATA,
             {b'fields': {b'path': [
                                    six.text_type(e)]}})

        return (
         201,
         {self.item_result_key: self.serialize_object(file, request=request, *args, **kwargs)})

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(optional={b'caption': {b'type': six.text_type, 
                    b'description': b'The new caption for the file.'}, 
       b'thumbnail': {b'type': six.text_type, 
                      b'description': b'The thumbnail data for the file.', 
                      b'added_in': b'1.7.7'}})
    def update(self, request, caption=None, thumbnail=None, *args, **kwargs):
        """Updates the file's data.

        This allows updating the file in a draft. Currently, only the caption
        and the thumbnail can be updated.
        """
        try:
            review_request = resources.review_request.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not review_request.is_mutable_by(request.user):
            return PERMISSION_DENIED
        else:
            try:
                file = resources.file_attachment.get_object(request, *args, **kwargs)
            except ObjectDoesNotExist:
                return DOES_NOT_EXIST

            if caption is not None:
                try:
                    resources.review_request_draft.prepare_draft(request, review_request)
                except PermissionDenied:
                    return self.get_no_access_error(request)

                file.draft_caption = caption
                file.save()
            if thumbnail is not None:
                try:
                    file.thumbnail = thumbnail
                except Exception as e:
                    logging.error(b'Failed to store thumbnail for attachment %d: %s', file.pk, e, request=request)
                    return (INVALID_FORM_DATA,
                     {b'fields': {b'thumbnail': [
                                                 six.text_type(e)]}})

            return (
             200,
             {self.item_result_key: self.serialize_object(file, request=request, *args, **kwargs)})

    @webapi_check_local_site
    @webapi_login_required
    @webapi_response_errors(DOES_NOT_EXIST, NOT_LOGGED_IN, PERMISSION_DENIED)
    def delete(self, request, *args, **kwargs):
        try:
            review_request = resources.review_request.get_object(request, *args, **kwargs)
            file_attachment = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not self.has_delete_permissions(request, file_attachment, *args, **kwargs):
            return self.get_no_access_error(request)
        else:
            if not file_attachment.review_request.exists() and not file_attachment.inactive_review_request.exists():
                file_attachment.delete()
            else:
                try:
                    draft = resources.review_request_draft.prepare_draft(request, review_request)
                except PermissionDenied:
                    return self.get_no_access_error(request)

                if file_attachment.attachment_history_id is None:
                    draft.inactive_file_attachments.add(file_attachment)
                    draft.file_attachments.remove(file_attachment)
                else:
                    all_revs = FileAttachment.objects.filter(attachment_history=file_attachment.attachment_history_id)
                    for revision in all_revs:
                        draft.inactive_file_attachments.add(revision)
                        draft.file_attachments.remove(revision)

                draft.save()
            return (204, {})