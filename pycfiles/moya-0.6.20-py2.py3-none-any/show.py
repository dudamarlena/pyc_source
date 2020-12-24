# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/show.py
# Compiled at: 2017-06-16 11:26:21
from __future__ import unicode_literals
from ...command import SubCommand
from ...wsgi import WSGIApplication
from ...compat import text_type

class Show(SubCommand):
    """Show an element's location and code"""
    help = b'show an element'

    def add_arguments(self, parser):
        parser.add_argument(dest=b'elementref', metavar=b'ELEMENTREF', help=b'an element reference to look up')
        parser.add_argument(b'-l', b'--location', dest=b'location', default=None, metavar=b'PATH', help=b'location of the Moya server code')
        parser.add_argument(b'-i', b'--ini', dest=b'settings', default=None, metavar=b'SETTINGSPATH', help=b'path to project settings file')
        return parser

    def run(self):
        args = self.args
        application = WSGIApplication(self.location, self.get_settings(), disable_autoreload=True)
        archive = application.archive
        try:
            app, element = archive.get_element(args.elementref)
        except Exception as e:
            self.error(text_type(e))
            return -1

        sibling = element.younger_sibling
        start = element.source_line
        node = element
        while node:
            if node.younger_sibling:
                node = node.younger_sibling
                break
            node = node.parent

        end = node.source_line if node else None
        file_line = (b'File "{}", line {}').format(element._location, start)
        self.console(file_line).nl()
        self.console.snippet(element._code, (
         start, end), highlight_line=start, line_numbers=True)
        return