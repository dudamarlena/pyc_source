# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\commands\attach.py
# Compiled at: 2017-04-19 05:14:02
from __future__ import print_function, unicode_literals
import os
from rbtools.api.errors import APIError
from rbtools.commands import Command, CommandError, Option
from rbtools.utils.commands import get_review_request

class Attach(Command):
    """Attach a file to a review request."""
    name = b'attach'
    author = b'The Review Board Project'
    args = b'<review-request-id> <file>'
    option_list = [
     Option(b'--filename', dest=b'filename', default=None, help=b'Custom filename for the file attachment.'),
     Option(b'--caption', dest=b'caption', default=None, help=b'Caption for the file attachment.'),
     Command.server_options,
     Command.repository_options]

    def main(self, request_id, path_to_file):
        self.repository_info, self.tool = self.initialize_scm_tool(client_name=self.options.repository_type)
        server_url = self.get_server_url(self.repository_info, self.tool)
        api_client, api_root = self.get_api(server_url)
        request = get_review_request(request_id, api_root)
        try:
            with open(path_to_file, b'rb') as (f):
                content = f.read()
        except IOError:
            raise CommandError(b'%s is not a valid file.' % path_to_file)

        filename = self.options.filename or os.path.basename(path_to_file)
        try:
            request.get_file_attachments().upload_attachment(filename, content, self.options.caption)
        except APIError as e:
            raise CommandError(b'Error uploading file: %s' % e)

        print(b'Uploaded %s to review request %s.' % (
         path_to_file, request_id))