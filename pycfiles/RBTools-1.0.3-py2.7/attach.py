# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/attach.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import print_function, unicode_literals
import os
from rbtools.api.errors import APIError
from rbtools.commands import Command, CommandError, Option

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

    def main(self, review_request_id, path_to_file):
        self.repository_info, self.tool = self.initialize_scm_tool(client_name=self.options.repository_type)
        server_url = self.get_server_url(self.repository_info, self.tool)
        api_client, api_root = self.get_api(server_url)
        try:
            review_request = api_root.get_review_request(review_request_id=review_request_id)
        except APIError as e:
            raise CommandError(b'Error getting review request %s: %s' % (
             review_request_id, e))

        try:
            with open(path_to_file, b'rb') as (f):
                content = f.read()
        except IOError:
            raise CommandError(b'%s is not a valid file.' % path_to_file)

        filename = self.options.filename or os.path.basename(path_to_file)
        try:
            review_request.get_file_attachments().upload_attachment(filename, content, self.options.caption)
        except APIError as e:
            raise CommandError(b'Error uploading file: %s' % e)

        print(b'Uploaded %s to review request %s.' % (
         path_to_file, review_request_id))