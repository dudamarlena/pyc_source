# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/new.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import unicode_literals
from __future__ import print_function
from ...command import SubCommand
import os
MOYA_TEMPLATE_XML = b'<?xml version="1.0" encoding="UTF-8"?>\n<moya xmlns="http://moyaproject.com"\n    xmlns:m="http://moyaproject.com"\n    xmlns:let="http://moyaproject.com/let"\n    xmlns:db="http://moyaproject.com/db"\n    xmlns:forms="http://moyaproject.com/forms"\n    xmlns:w="http://moyaproject.com/widgets"\n    xmlns:html="http://moyaproject.com/html">\n\n    <!-- your content here -->\n\n</moya>\n'

class New(SubCommand):
    """Create a boilerplate moya file"""
    help = b'create a new boilerplate moya file'

    def add_arguments(self, parser):
        parser.add_argument(dest=b'filename', metavar=b'PATH', help=b'path / filename for new file')
        parser.add_argument(b'-f', b'-force', dest=b'force', action=b'store_true', help=b'fore overwriting')

    def run(self):
        args = self.args
        if not args.force and os.path.exists(args.filename):
            self.console.error(b'destination exists, use --force to overwrite')
            return -1
        td = {}
        file_data = MOYA_TEMPLATE_XML.format(td)
        try:
            with open(args.filename, b'wt') as (f):
                f.write(file_data)
        except Exception as e:
            self.console.error((b'unable to write file ({})').format(e))
            return -1