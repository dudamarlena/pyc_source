# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\commands\status.py
# Compiled at: 2017-04-19 05:14:04
from __future__ import print_function, unicode_literals
import logging
from rbtools.commands import Command, Option
from rbtools.utils.repository import get_repository_id
from rbtools.utils.users import get_username

class Status(Command):
    """Display review requests for the current repository."""
    name = b'status'
    author = b'The Review Board Project'
    description = b'Output a list of your pending review requests.'
    args = b''
    option_list = [
     Option(b'--all', dest=b'all_repositories', action=b'store_true', default=False, help=b'Shows review requests for all repositories instead of just the detected repository.'),
     Command.server_options,
     Command.repository_options,
     Command.perforce_options,
     Command.tfs_options]

    def output_request(self, request):
        print(b'   r/%s - %s' % (request.id, request.summary))

    def output_draft(self, request, draft):
        print(b' * r/%s - %s' % (request.id, draft.summary))

    def main(self):
        repository_info, tool = self.initialize_scm_tool(client_name=self.options.repository_type)
        server_url = self.get_server_url(repository_info, tool)
        api_client, api_root = self.get_api(server_url)
        self.setup_tool(tool, api_root=api_root)
        username = get_username(api_client, api_root, auth_required=True)
        repository_info = repository_info.find_server_repository_info(api_root)
        query_args = {b'from_user': username, 
           b'status': b'pending', 
           b'expand': b'draft'}
        if not self.options.all_repositories:
            repo_id = get_repository_id(repository_info, api_root, repository_name=self.options.repository_name)
            if repo_id:
                query_args[b'repository'] = repo_id
            else:
                logging.warning(b'The repository detected in the current directory was not found on\nthe Review Board server. Displaying review requests from all repositories.')
        requests = api_root.get_review_requests(**query_args)
        for request in requests.all_items:
            if request.draft:
                self.output_draft(request, request.draft[0])
            else:
                self.output_request(request)