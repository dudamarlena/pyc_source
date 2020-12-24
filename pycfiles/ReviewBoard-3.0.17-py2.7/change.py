# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/resources/change.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.utils import six
from djblets.util.decorators import augment_method_from
from reviewboard.changedescs.models import ChangeDescription
from reviewboard.reviews.fields import get_review_request_field
from reviewboard.webapi.base import WebAPIResource
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.mixins import MarkdownFieldsMixin
from reviewboard.webapi.resources import resources

class ChangeResource(MarkdownFieldsMixin, WebAPIResource):
    """Provides information on a change made to a public review request.

    A change includes, optionally, text entered by the user describing the
    change, and also includes a list of fields that were changed on the
    review request.

    The list of fields changed are in ``fields_changed``. The keys are the
    names of the fields, and the values are details on that particular
    change to the field.

    """
    added_in = b'1.6'
    model = ChangeDescription
    name = b'change'
    fields = {b'id': {b'type': int, 
               b'description': b'The numeric ID of the change description.'}, 
       b'fields_changed': {b'type': dict, 
                           b'description': b'\n                The fields that were changed. Each key is the name of a\n                changed field, and each value is a dictionary of details on\n                that change.\n\n                For ``summary``, ``description``, ``testing_done`` and\n                ``branch`` fields, the following detail keys will be\n                available:\n\n                * ``old``: The old value of the field.\n                * ``new``: The new value of the field.\n\n                For ``diff`` fields:\n\n                * ``added``: The diff that was added.\n\n                For ``bugs_closed`` fields:\n\n                * ``old``: A list of old bugs.\n                * ``new``: A list of new bugs.\n                * ``removed``: A list of bugs that were removed, if any.\n                * ``added``: A list of bugs that were added, if any.\n\n                For ``file_attachments``, ``screenshots``, ``target_people``\n                and ``target_groups`` fields:\n\n                * ``old``: A list of old items.\n                * ``new``: A list of new items.\n                * ``removed``: A list of items that were removed, if any.\n                * ``added``: A list of items that were added, if any.\n\n                For ``screenshot_captions`` and ``file_captions`` fields:\n\n                * ``old``: The old caption.\n                * ``new``: The new caption.\n                * ``screenshot``: The screenshot that was updated.\n            '}, 
       b'text': {b'type': six.text_type, 
                 b'description': b'The description of the change written by the submitter.', 
                 b'supports_text_types': True}, 
       b'text_type': {b'type': MarkdownFieldsMixin.TEXT_TYPES, 
                      b'description': b'The mode for the text field.', 
                      b'added_in': b'2.0'}, 
       b'timestamp': {b'type': six.text_type, 
                      b'description': b'The date and time that the change was made (in ``YYYY-MM-DD HH:MM:SS`` format).'}}
    uri_object_key = b'change_id'
    model_parent_key = b'review_request'
    allowed_methods = ('GET', )
    mimetype_list_resource_name = b'review-request-changes'
    mimetype_item_resource_name = b'review-request-change'

    def serialize_fields_changed_field(self, obj, **kwargs):
        review_request = obj.review_request.get()
        fields_changed = {}
        for field_name, data in six.iteritems(obj.fields_changed):
            field_cls = get_review_request_field(field_name)
            if field_cls:
                field = field_cls(review_request)
                fields_changed[field.field_id] = field.serialize_change_entry(obj)

        return fields_changed

    def has_access_permissions(self, request, obj, *args, **kwargs):
        return obj.review_request.get().is_accessible_by(request.user)

    def get_queryset(self, request, *args, **kwargs):
        review_request = resources.review_request.get_object(request, *args, **kwargs)
        return review_request.changedescs.filter(public=True)

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get_list(self, *args, **kwargs):
        """Returns a list of changes made on a review request."""
        pass

    @webapi_check_local_site
    @augment_method_from(WebAPIResource)
    def get(self, *args, **kwargs):
        """Returns the information on a change to a review request."""
        pass


change_resource = ChangeResource()