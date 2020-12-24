# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/publish.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import print_function, unicode_literals
import logging
from rbtools.api.errors import APIError
from rbtools.commands import Command, CommandError, Option

class Publish(Command):
    """Publish a specific review request from a draft."""
    name = b'publish'
    author = b'The Review Board Project'
    args = b'<review-request-id>'
    option_list = [
     Command.server_options,
     Command.repository_options,
     Option(b'-t', b'--trivial', dest=b'trivial_publish', action=b'store_true', default=False, help=b'Publish the review request without sending an e-mail notification.', added_in=b'1.0'),
     Option(b'--markdown', dest=b'markdown', action=b'store_true', config_key=b'MARKDOWN', default=False, help=b'Specifies if the change description should should be interpreted as Markdown-formatted text.', added_in=b'1.0'),
     Option(b'-m', b'--change-description', dest=b'change_description', default=None, help=b'The change description to use for the publish.', added_in=b'1.0')]

    def main(self, review_request_id):
        """Run the command."""
        repository_info, tool = self.initialize_scm_tool(client_name=self.options.repository_type)
        server_url = self.get_server_url(repository_info, tool)
        api_client, api_root = self.get_api(server_url)
        try:
            review_request = api_root.get_review_request(review_request_id=review_request_id, only_fields=b'public', only_links=b'draft')
        except APIError as e:
            raise CommandError(b'Error getting review request %s: %s' % (
             review_request_id, e))

        self.setup_tool(tool, api_root)
        update_fields = {b'public': True}
        if self.options.trivial_publish and tool.capabilities.has_capability(b'review_requests', b'trivial_publish'):
            update_fields[b'trivial'] = True
        if self.options.change_description is not None:
            if review_request.public:
                update_fields[b'changedescription'] = self.options.change_description
                if self.options.markdown and tool.capabilities.has_capability(b'text', b'markdown'):
                    update_fields[b'changedescription_text_type'] = b'markdown'
                else:
                    update_fields[b'changedescription_text_type'] = b'plain'
            else:
                logging.error(b'The change description field can only be set when publishing an update.')
        try:
            draft = review_request.get_draft(only_fields=b'')
            draft.update(**update_fields)
        except APIError as e:
            raise CommandError(b'Error publishing review request (it may already be published): %s' % e)

        print(b'Review request #%s is published.' % review_request_id)
        return