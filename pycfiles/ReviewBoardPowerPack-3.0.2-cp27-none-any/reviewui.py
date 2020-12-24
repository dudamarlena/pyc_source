# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/pdf/reviewui.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import logging
from django.utils.functional import cached_property
from django.utils.html import escape
from django.utils.six.moves.urllib.parse import urlparse
from djblets.cache.backend import cache_memoize
from djblets.util.templatetags.djblets_images import save_image_to_storage
from PIL import Image
from reviewboard.admin.server import build_server_url
from reviewboard.reviews.ui.base import FileAttachmentReviewUI
from reviewboard.site.urlresolvers import local_site_reverse
from rbpowerpack.pdf.diffs import make_diff_cache_key
from rbpowerpack.pdf.utils import convert_data_uri_to_image, get_pdf_worker_url
from rbpowerpack.utils.extension import get_powerpack_extension

class PDFReviewUI(FileAttachmentReviewUI):
    """A review UI for PDF files."""
    name = b'PDF'
    object_key = b'pdf'
    supported_mimetypes = [
     b'application/pdf', b'application/x-pdf']
    supports_diffing = True
    js_model_class = b'PowerPack.PDF.Reviewable'
    js_view_class = b'PowerPack.PDF.ReviewableView'

    def __init__(self, review_request, obj):
        """Initialize the review UI.

        Args:
            review_request (reviewboard.reviews.models.review_request.
                            ReviewRequest):
                The review request.

            obj (reviewboard.attachments.models.FileAttachment):
                The file attachment to review.
        """
        super(PDFReviewUI, self).__init__(review_request, obj)
        self.extension = get_powerpack_extension()
        filename = obj.orig_filename or obj.file.name
        if not filename.lower().endswith(b'.pdf'):
            raise Exception(b'PDFReviewUI: rejecting document %s because of incorrect extension' % obj.filename)

    def is_enabled_for(self, user=None, review_request=None, **kwargs):
        """Return whether this review UI is enabled for the given user.

        Args:
            user (django.contrib.auth.models.User, optional):
                The user to check.

            review_request (reviewboard.reviews.models.review_request.
                            ReviewRequest, optional):
                The review request.

            **kwargs (dict):
                Additional keyword arguments.

        Returns:
            bool:
            Whether this review UI should be enabled.
        """
        return self.extension.policy.is_pdf_enabled(user, review_request)

    @cached_property
    def css_bundle_names(self):
        """The list of CSS bundles for the review UI."""
        return [
         self.extension.get_bundle_id(b'powerpack-pdf')]

    @cached_property
    def js_bundle_names(self):
        """The list of JavaScript bundles for the review UI."""
        return [
         self.extension.get_bundle_id(b'libpdf'),
         self.extension.get_bundle_id(b'powerpack-pdf')]

    @cached_property
    def pdf_worker_url(self):
        """The URL for the pdf.worker script."""
        return get_pdf_worker_url(self.extension)

    def serialize_comments(self, comments):
        """Serialize all comments to send to the client.

        Args:
            comments (list of reviewboard.reviews.models.
                      file_attachment_comment.FileAttachmentComment):
                The comments to serialize.

        Returns:
            dict:
            The serialized comments, suitable for passing through to the
            frontend as JSON.
        """
        result = {}
        for comment in comments:
            try:
                position = b'%(x)sx%(y)s+%(width)s+%(height)s@%(page)s' % comment.extra_data
            except KeyError:
                continue

            result.setdefault(position, []).append(self.serialize_comment(comment))

        return result

    def serialize_comment(self, comment):
        """Serialize a comment sent to the client.

        This will invoke the default behavior for comment serialization,
        but will also sanity-check that thumbnailData is not present in
        the comment. This could appear if a comment formerly failed to
        post for some reason.

        Args:
            comment (reviewboard.reviews.models.file_attachment_comment.
                     FileAttachmentComment):
                The comment to serialize.

        Returns:
            dict:
            The serialized comment.
        """
        data = super(PDFReviewUI, self).serialize_comment(comment)
        try:
            del data[b'thumbnailData']
        except KeyError:
            pass

        return data

    def get_comment_link_url(self, comment):
        """Return the URL to link the comment to.

        Args:
            comment (reviewboard.reviews.models.file_attachment_comment.
                     FileAttachmentComment):
                The comment to link to.

        Returns:
            unicode:
            The URL to link to the comment in the Review UI.
        """
        if comment.reply_to:
            comment = comment.reply_to
        ui_url = super(PDFReviewUI, self).get_comment_link_url(comment)
        extra_data = comment.extra_data
        try:
            page = int(extra_data[b'page'])
        except (KeyError, ValueError) as e:
            logging.error(b'PDF Review UI: Could not fetch comment details for file attachment comment %d from comment extra_data: %s.', comment.pk, e)
            return ui_url

        return ui_url + b'#page-%d' % page

    def get_comment_link_text(self, comment):
        """Return the text to use when linking this comment.

        Args:
            comment (reviewboard.reviews.models.file_attachment_comment.
                     FileAttachmentComment):
                The comment to link to.

        Returns:
            unicode:
            The text for the link.
        """
        if comment.reply_to:
            comment = comment.reply_to
        extra_data = comment.extra_data
        try:
            page = int(extra_data[b'page'])
        except (KeyError, ValueError) as e:
            logging.error(b'PDF Review UI: Could not fetch comment details for file attachment comment %d from comment extra_data: %s.', comment.pk, e)
            return super(PDFReviewUI, self).get_comment_link_text(comment)

        return b'%s, Page %d' % (comment.file_attachment.filename, page)

    def get_comment_thumbnail(self, comment):
        """Return the HTML to insert for the comment thumbnail.

        Args:
            comment (reviewboard.reviews.models.file_attachment_comment.
                     FileAttachmentComment):
                The comment to link to.

        Returns:
            unicode:
            HTML to display the comment thumbnail (the excerpted section of the
            document).
        """
        if comment.reply_to:
            comment = comment.reply_to
        extra_data = comment.extra_data
        try:
            x = int(extra_data[b'x'])
            y = int(extra_data[b'y'])
            width = int(extra_data[b'width'])
            height = int(extra_data[b'height'])
        except (KeyError, ValueError) as e:
            logging.error(b'PDF Review UI: Could not fetch comment details for file attachment comment %d from comment extra_data: %s.', comment.pk, e)
            return

        filename = b'%s_%d_%d_%d_%d.png' % (comment.file_attachment.file.name,
         x, y, width, height)
        storage = comment.file_attachment.file.storage
        if not storage.exists(filename):
            try:
                image_data = extra_data[b'thumbnailData']
            except (KeyError, ValueError):
                logging.error(b'PDF Review UI: Could not fetch thumbnailData for file attachment comment %d from comment extra_data.', comment.pk)
                return

            try:
                image = convert_data_uri_to_image(image_data)
                if image.size[0] != width or image.size[1] != height:
                    image.resize((width, height), Image.ANTIALIAS)
                save_image_to_storage(image, storage, filename)
                del extra_data[b'thumbnailData']
                comment.extra_data = extra_data
                comment.save()
            except Exception as e:
                logging.error(b'PDF Review UI: Could not convert thumbnailData to stored image for file attachment comment %d: %s', comment.pk, e)
                return

        image_url = storage.url(filename)
        if not urlparse(image_url).netloc:
            image_url = build_server_url(image_url)
        return b'<img src="%s" width="%s" height="%s" alt="%s" />' % (
         image_url, width, height, escape(comment.text))

    def get_js_model_data(self):
        """Return model data for the JavaScript AbstractReviewable subclass.

        This will return information on the file attachment, its history,
        and any information on an attachment being diffed against.

        Returns:
            dict:
            The attributes to pass to the model.
        """
        data = super(PDFReviewUI, self).get_js_model_data()
        data[b'workerURL'] = self.pdf_worker_url
        data[b'pdfURL'] = self.obj.file.url
        if self.diff_against_obj:
            data[b'diffAgainstPDFURL'] = self.diff_against_obj.file.url
            data[b'diffURL'] = local_site_reverse(b'powerpack-pdf-diff', local_site=self.obj.local_site, kwargs={b'old_attachment_id': self.diff_against_obj.pk, 
               b'new_attachment_id': self.obj.pk})
            cache_key = make_diff_cache_key(self.diff_against_obj, self.obj)
            try:

                def _raise_key_error():
                    raise KeyError

                data[b'diffData'] = cache_memoize(cache_key, _raise_key_error, large_data=True)
            except KeyError:
                data[b'diffData'] = None

        return data