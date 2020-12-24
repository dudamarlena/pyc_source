# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\commands\publish.py
# Compiled at: 2017-04-19 05:14:04
from __future__ import print_function, unicode_literals
from rbtools.api.errors import APIError
from rbtools.commands import Command, CommandError
from rbtools.utils.commands import get_review_request

class Publish(Command):
    """Publish a specific review request from a draft."""
    name = b'publish'
    author = b'The Review Board Project'
    args = b'<review-request-id>'
    option_list = [
     Command.server_options,
     Command.repository_options]

    def main(self, request_id):
        """Run the command."""
        repository_info, tool = self.initialize_scm_tool(client_name=self.options.repository_type)
        server_url = self.get_server_url(repository_info, tool)
        api_client, api_root = self.get_api(server_url)
        request = get_review_request(request_id, api_root)
        try:
            draft = request.get_draft()
            draft = draft.update(public=True)
        except APIError as e:
            raise CommandError(b'Error publishing review request (it may already be published): %s' % e)

        print(b'Review request #%s is published.' % request_id)