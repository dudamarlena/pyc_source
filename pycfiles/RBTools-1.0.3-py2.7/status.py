# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/status.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import print_function, unicode_literals
import logging, texttable as tt
try:
    from backports.shutil_get_terminal_size import get_terminal_size
except ImportError:
    from shutil import get_terminal_size

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
    TAB_SIZE = 3
    PADDING = 5

    def tabulate(self, request_stats):
        """Print review request summary and status in a table.

        Args:
            request_stats (dict):
                A dict that contains statistics about each review request.
        """
        if len(request_stats):
            has_branches = False
            has_bookmarks = False
            table = tt.Texttable(get_terminal_size().columns)
            header = [b'Status', b'Review Request']
            for request in request_stats:
                if b'branch' in request:
                    has_branches = True
                if b'bookmark' in request:
                    has_bookmarks = True

            if has_branches:
                header.append(b'Branch')
            if has_bookmarks:
                header.append(b'Bookmark')
            table.header(header)
            for request in request_stats:
                row = [request[b'status'], request[b'summary']]
                if has_branches:
                    row.append(request.get(b'branch') or b'')
                if has_bookmarks:
                    row.append(request.get(b'bookmark') or b'')
                table.add_row(row)

            print(table.draw())
        else:
            print(b'No review requests found.')
        print()

    def get_data(self, requests):
        """Return current status and review summary for all reviews.

        Args:
            requests (ListResource):
                A ListResource that contains data on all open/draft requests.

        Returns:
            list: A list whose elements are dicts of each request's statistics.
        """
        requests_stats = []
        request_stats = {}
        for request in requests.all_items:
            if request.draft:
                status = b'Draft'
            elif request.issue_open_count:
                status = b'Open Issues (%s)' % request.issue_open_count
            elif request.ship_it_count:
                status = b'Ship It! (%s)' % request.ship_it_count
            else:
                status = b'Pending'
            request_stats = {b'status': status, 
               b'summary': b'r/%s - %s' % (request.id, request.summary)}
            if b'local_branch' in request.extra_data:
                request_stats[b'branch'] = request.extra_data[b'local_branch']
            elif b'local_bookmark' in request.extra_data:
                request_stats[b'bookmark'] = request.extra_data[b'local_bookmark']
            requests_stats.append(request_stats)

        return requests_stats

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
        request_stats = self.get_data(requests)
        self.tabulate(request_stats)