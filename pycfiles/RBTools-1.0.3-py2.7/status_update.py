# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/status_update.py
# Compiled at: 2020-04-14 20:27:46
"""Interact with review request status-updates on Review Board.

For getting or setting status-updates on review requests. Also for including a
review when creating a status-update.
"""
from __future__ import print_function, unicode_literals
import json, logging
from rbtools.api.errors import APIError
from rbtools.commands import Command, CommandError, CommandExit, Option, OptionGroup

class StatusUpdate(Command):
    """Interact with review request status updates on Review Board.

    This command allows setting, getting and deleting status updates for review
    requests.

    A status update is a way for a third-party service or extension to mark
    some kind of status on a review request.
    """
    name = b'status-update'
    author = b'The Review Board Project'
    description = b'Interact with review request status updates on Review Board.'
    args = b'<action>'
    option_list = [
     OptionGroup(name=b'Status Update Options', description=b'Controls the behavior of a status-update, including what review request the status update is attached to.', option_list=[
      Option(b'-r', b'--review-request-id', dest=b'rid', metavar=b'ID', type=int, required=True, help=b'Specifies which review request.'),
      Option(b'-s', b'--status-update-id', dest=b'sid', metavar=b'ID', type=int, help=b'Specifies which status update from the review request.'),
      Option(b'-j', b'--json', action=b'store_true', dest=b'json', default=False, help=b'Format command output in JSON.'),
      Option(b'--review', dest=b'review', metavar=b'FILE_PATH', default=None, help=b'JSON formatted file defining details of review(s) to add to status update.'),
      Option(b'--change-id', dest=b'change_id', metavar=b'ID', type=int, help=b'The change to a review request which this status update applies to. When not specified, the status update is for the review request as initially published.'),
      Option(b'--description', dest=b'description', metavar=b'TEXT', default=None, help=b'A user-visible description of the status update.'),
      Option(b'--service-id', dest=b'service_id', metavar=b'SERVICE_ID', default=None, help=b'A unique identifier for the service providing the status update.'),
      Option(b'--state', dest=b'state', metavar=b'STATE', default=None, help=b'The current state of the status update.'),
      Option(b'--summary', dest=b'summary', metavar=b'TEXT', default=None, help=b'A user-visible short summary of the status update.'),
      Option(b'--timeout', dest=b'timeout', metavar=b'TIMEOUT', type=int, help=b'Timeout for pending status updates, measured in seconds.'),
      Option(b'--url', dest=b'url', metavar=b'URL', default=None, help=b'URL to link to for more details about the status update.'),
      Option(b'--url-text', dest=b'url_text', metavar=b'URL_TEXT', default=None, help=b'The text to use for the --url link.')]),
     Command.server_options]

    def _print_status_update(self, status_update):
        """Print status update in a human readable format.

        Args:
            status_update (rbtools.api.transport.Transport):
                Representation of status-update API for a review request.
        """
        if status_update.get(b'description'):
            description = b': %s' % status_update.get(b'description')
        else:
            description = b''
        print(b' %d\t%s: <%s> %s%s' % (
         status_update.get(b'id'), status_update.get(b'service_id'),
         status_update.get(b'state'), status_update.get(b'summary'),
         description))

    def _dict_status_update(self, status_update):
        """Create a dict for status update.

        Args:
            status_update (rbtools.api.transport.Transport):
                Representation of status-update API for a review request.

        Returns:
            dict:
            Description of status_update that was passed in.
        """
        keys = [
         b'change', b'description', b'extra_data', b'id', b'review',
         b'service_id', b'state', b'summary', b'timeout', b'url',
         b'url_text']
        return {key:status_update.get(key) for key in keys if status_update.get(key)}

    def print(self, response):
        """Print output in format specified by user.

        Args:
            response (list, dict):
                Response from API with list of status-updates or a single
                status-update.
        """
        if self.options.json:
            if isinstance(response, list):
                output = [ self._dict_status_update(status_update) for status_update in response ]
            else:
                output = self._dict_status_update(response)
            print(json.dumps(output, indent=2, sort_keys=True))
        elif isinstance(response, list):
            for status_update in response:
                self._print_status_update(status_update)

        else:
            self._print_status_update(response)

    def add_review(self, api_root):
        """Handle adding a review to a review request from a json file.

        Args:
            api_root (rbtools.api.transport.Transport):
                Representation of the root level of the Review Board API for
                doing further requests to the Review Board API.

        Raises:
            rbtools.commands.CommandError:
                Error with the execution of the command.

        Looks for ``reviews``, ``diff_comments``, and ``general_comments`` keys
        in the json file contents and populates the review accordingly.

        To find appropriate inputs for each key:

        ``reviews``:
            Look at Web API documentation for POST on the Review List resource
            for available fields.

        ``diff_comments``:
            Look at Web API documentation for POST on the Review Diff Comment
            List resource for available fields. All diff comments require
            ``first_line``, ``filediff_id``, ``num_lines``, and ``text`` field
            to be specified.

        ``general_comments``:
            Look at Web API documentation for POST on the Review General
            Comment List resource for available fields. All general comments
            require ``text`` field to be specified.

        Example file contents:
        ```
        {
            "review": {
                "body_top": "Header comment"
            },
            "diff_comment": [
                {
                    "filediff_id": 10,
                    "first_line": 729,
                    "issue_opened": true,
                    "num_lines": 1,
                    "text": "Adding a comment on a diff line",
                    "text_type": "markdown"
                }
            ],
            "general_comments": [
                {
                    "text": "Adding a general comment",
                    "text_type": "markdown"
                }
            ]
        }
        ```
        """
        with open(self.options.review) as (f):
            file_contents = json.loads(f.read())
        review_draft = api_root.get_reviews(review_request_id=self.options.rid)
        if b'reviews' not in file_contents and b'diff_comments' not in file_contents and b'general_comments' not in file_contents:
            raise CommandError(b'No information in review file, this will create an empty review.')
        if b'reviews' in file_contents:
            file_contents[b'reviews'][b'public'] = False
            new_review_draft = review_draft.create(**file_contents[b'reviews'])
        else:
            new_review_draft = review_draft.create()
        if b'diff_comments' in file_contents:
            diff_comments = new_review_draft.get_diff_comments()
            for comment in file_contents[b'diff_comments']:
                try:
                    diff_comments.create(**comment)
                except APIError as e:
                    logging.warning(b'Failed to create diff comment: %s\nAPIError: %s', json.dumps(comment), e)

        if b'general_comments' in file_contents:
            general_comments = new_review_draft.get_general_comments()
            for comment in file_contents[b'general_comments']:
                try:
                    general_comments.create(**comment)
                except APIError as e:
                    logging.warning(b'Failed to create general comment: %s\nAPIError: %s', json.dumps(comment), e)

        return new_review_draft

    def get_status_update(self, api_root):
        """Handle getting status update information from Review Board.

        Args:
            api_root (rbtools.api.transport.Transport):
                Representation of the root level of the Review Board API for
                doing further requests to the Review Board API.

        Raises:
            rbtools.commands.CommandError:
                Error with the execution of the command.

            rbtools.commands.CommandExit:
                Stop executing and return an exit status.
        """
        try:
            if self.options.sid:
                self.print(api_root.get_status_update(review_request_id=self.options.rid, status_update_id=self.options.sid).rsp.get(b'status_update'))
            else:
                self.print(api_root.get_status_updates(review_request_id=self.options.rid).rsp.get(b'status_updates'))
        except APIError as e:
            if e.rsp:
                print(json.dumps(e.rsp, indent=2))
                raise CommandExit(1)
            else:
                raise CommandError(b'Could not retrieve the requested resource: %s' % e)

    def set_status_update(self, api_root):
        """Handle setting status update information on Review Board.

        Args:
            api_root (rbtools.api.transport.Transport):
                Representation of the root level of the Review Board API for
                doing further requests to the Review Board API.

        Raises:
            rbtools.commands.CommandError:
                Error with the execution of the command.

            rbtools.commands.CommandExit:
                Stop executing and return an exit status.
        """
        new_review_draft = None
        review_draft_id = None
        if self.options.review:
            new_review_draft = self.add_review(api_root)
            review_draft_id = new_review_draft.id
        allowed_state = [
         b'pending', b'done-failure', b'done-success', b'error']
        if self.options.state and self.options.state not in allowed_state:
            raise CommandError(b'--state must be one of: %s' % (b', ').join(allowed_state))
        request_parameters = [
         b'change_id', b'description', b'service_id',
         b'state', b'summary', b'timeout', b'url',
         b'url_text']
        options = vars(self.options)
        query_args = {parameter:options.get(parameter) for parameter in iter(request_parameters) if options.get(parameter)}
        if review_draft_id:
            query_args[b'review_id'] = review_draft_id
        try:
            if self.options.sid:
                status_update = api_root.get_status_update(review_request_id=self.options.rid, status_update_id=self.options.sid)
                status_update = status_update.update(**query_args)
            else:
                if not self.options.service_id or not self.options.summary:
                    raise CommandError(b'--service-id and --summary are required input for creating a new status update')
                status_update = api_root.get_status_updates(review_request_id=self.options.rid)
                status_update = status_update.create(**query_args)
            if new_review_draft:
                new_review_draft.update(public=True)
            self.print(status_update.rsp.get(b'status_update'))
        except APIError as e:
            if e.rsp:
                print(json.dumps(e.rsp, indent=2))
                raise CommandExit(1)
            else:
                raise CommandError(b'Could not set the requested resource: %s' % e)

        return

    def delete_status_update(self, api_root):
        """Handle deleting status updates on Review Board.

        Args:
            api_root (rbtools.api.transport.Transport):
                Representation of the root level of the Review Board API for
                doing further requests to the Review Board API.

        Raises:
            rbtools.commands.CommandError:
                Error with the execution of the command.
        """
        try:
            if not self.options.sid:
                raise CommandError(b'Status update ID is required for deleting a status update.')
            status_update = api_root.get_status_update(review_request_id=self.options.rid, status_update_id=self.options.sid)
            status_update.delete()
        except APIError as e:
            raise CommandError(b'Could not delete the requested resource: %s' % e)

    def main(self, action):
        """Call API for status-update.

        Args:
            action (unicode):
                Sub command argument input for specifying which action to do
                (can be ``get``, ``set``, or ``delete``).

        Raises:
            rbtools.command.CommandError:
                Error with the execution of the command.
        """
        if self.options.server:
            server_url = self.options.server
        else:
            repository_info, tool = self.initialize_scm_tool()
            server_url = self.get_server_url(repository_info, tool)
        api_client, api_root = self.get_api(server_url)
        if action == b'get':
            self.get_status_update(api_root)
        elif action == b'set':
            self.set_status_update(api_root)
        elif action == b'delete':
            self.delete_status_update(api_root)
        else:
            raise CommandError(b'Action "%s" not recognized.' % action)