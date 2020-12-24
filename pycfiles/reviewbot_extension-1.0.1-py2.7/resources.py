# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbotext/resources.py
# Compiled at: 2018-07-31 04:09:55
from __future__ import unicode_literals
import json
from django.core.exceptions import ObjectDoesNotExist
from djblets.webapi.decorators import webapi_login_required, webapi_request_fields, webapi_response_errors
from djblets.webapi.errors import DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED
from reviewboard.diffviewer.models import FileDiff
from reviewboard.reviews.models import BaseComment, Review
from reviewboard.webapi.decorators import webapi_check_local_site
from reviewboard.webapi.resources import resources, WebAPIResource
from reviewbotext.models import Tool

class ToolResource(WebAPIResource):
    """Resource for workers to update the installed tools list.

    This API endpoint isn't actually RESTful, and just provides a place
    for workers to "dump" their entire list of installed tools as a single
    POST. A GET request will not actually return a list of tools.
    """
    name = b'tool'
    allowed_methods = ('GET', 'POST')
    model_object_key = b'id'
    uri_object_key = b'tool_id'

    @webapi_login_required
    @webapi_check_local_site
    @webapi_response_errors(DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(required={b'hostname': {b'type': str, 
                     b'description': b'The hostname of the POSTing worker.'}, 
       b'tools': {b'type': str, 
                  b'description': b'A JSON payload containing tool information.'}})
    def create(self, request, hostname, tools, *args, **kwargs):
        """Add to the list of installed tools.

        The hostname field should contain the hostname the celery
        worker is using (This should be unique to that worker under
        proper configuration).

        The tools field should contain a JSON payload describing the
        list of tools installed at the worker. This payload should
        correspond to a list of dictionaries, with each dictionary
        corresponding to a tool. The dictionary should contain the
        following information:
            - 'name': The descriptive name of the tool.
            - 'entry_point': The entry point corresponding to the tool.
            - 'version': The tool version.
            - 'description': Longer description of the tool.
            - 'tool_options': A JSON payload describing the custom
              options the tool provides (see reviewbotext.models.Tool
              for a description of this payload).

        Here is an example tools payload:
        [
          {
            "name": "Example Tool 1",
            "entry_point": "example1",
            "version": "1.0.1",
            "description": "An example tool.",
            "tool_options": "[]"
          },
          {
            "name": "Example Tool 2",
            "entry_point": "example2",
            "version": "1.2.1",
            "description": "The second example tool.",
            "tool_options": "[]"
          },
        ]

        TODO: Use the hostname.
        """
        from reviewbotext.extension import ReviewBotExtension
        extension = ReviewBotExtension.instance
        if request.user.id != extension.settings[b'user']:
            return PERMISSION_DENIED
        try:
            tools = json.loads(tools)
        except:
            return (
             INVALID_FORM_DATA,
             {b'fields': {b'dtools': b'Malformed JSON.'}})

        for tool in tools:
            obj, created = Tool.objects.get_or_create(entry_point=tool[b'entry_point'], version=tool[b'version'], defaults={b'name': tool[b'name'], 
               b'description': tool[b'description'], 
               b'tool_options': tool[b'tool_options'], 
               b'in_last_update': True, 
               b'timeout': tool[b'timeout'], 
               b'working_directory_required': tool[b'working_directory_required']})
            if not created and not obj.in_last_update:
                obj.in_last_update = True
                obj.save()

        return (201, {})


tool_resource = ToolResource()

class ReviewBotReviewResource(WebAPIResource):
    """Resource for creating reviews with a single request.

    This resource allows Review Bot to create a full review using a single
    POST request. Using the traditional API would result in a high volume
    of requests from Review Bot, creating stress on the server.

    Each user may only have one review draft per request at a time. This
    resource allows concurrent review of a single request by creating
    the review and publishing it in a single transaction.
    """
    name = b'review_bot_review'
    allowed_methods = ('GET', 'POST')

    @webapi_login_required
    @webapi_check_local_site
    @webapi_response_errors(DOES_NOT_EXIST, INVALID_FORM_DATA, NOT_LOGGED_IN, PERMISSION_DENIED)
    @webapi_request_fields(required={b'review_request_id': {b'type': int, 
                              b'description': b'The ID of the review request.'}}, optional={b'ship_it': {b'type': bool, 
                    b'description': b'Whether or not to mark the review "Ship It!"'}, 
       b'body_top': {b'type': str, 
                     b'description': b'The review content above the comments.'}, 
       b'body_top_rich_text': {b'type': bool, 
                               b'description': b'Whether the body-top should be formatted using Markdown.'}, 
       b'body_bottom': {b'type': str, 
                        b'description': b'The review content below the comments.'}, 
       b'body_bottom_rich_text': {b'type': bool, 
                                  b'description': b'Whether the body-bottom should be formatted using Markdown.'}, 
       b'diff_comments': {b'type': str, 
                          b'description': b'A JSON payload containing the diff comments.'}})
    def create(self, request, review_request_id, ship_it=False, body_top=b'', body_top_rich_text=False, body_bottom=b'', body_bottom_rich_text=False, diff_comments=None, *args, **kwargs):
        """Creates a new review and publishes it."""
        try:
            review_request = resources.review_request.get_object(request, review_request_id=review_request_id, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not body_top:
            body_top = b''
        if not body_bottom:
            body_bottom = b''
        new_review = Review.objects.create(review_request=review_request, user=request.user, body_top=body_top, body_top_rich_text=body_top_rich_text, body_bottom=body_bottom, body_bottom_rich_text=body_bottom_rich_text, ship_it=ship_it)
        if diff_comments:
            try:
                diff_comments = json.loads(diff_comments)
                for comment in diff_comments:
                    filediff = FileDiff.objects.get(pk=comment[b'filediff_id'], diffset__history__review_request=review_request)
                    if comment[b'issue_opened']:
                        issue = True
                        issue_status = BaseComment.OPEN
                    else:
                        issue = False
                        issue_status = None
                    new_review.comments.create(filediff=filediff, interfilediff=None, text=comment[b'text'], first_line=comment[b'first_line'], num_lines=comment[b'num_lines'], issue_opened=issue, issue_status=issue_status, rich_text=comment[b'rich_text'])

            except KeyError:
                return (
                 INVALID_FORM_DATA,
                 {b'fields': {b'diff_comments': b'Diff comments were malformed'}})
            except ObjectDoesNotExist:
                return (INVALID_FORM_DATA,
                 {b'fields': {b'diff_comments': b'Invalid filediff_id'}})

        new_review.publish(user=request.user)
        return (
         201,
         {self.item_result_key: new_review})


review_bot_review_resource = ReviewBotReviewResource()