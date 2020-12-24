# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/rst/file.py
# Compiled at: 2020-03-20 06:59:09
# Size of source mod 2**32: 672 bytes
from docutils.parsers.rst import Directive, directives
from docutils.nodes import raw
from flamingo.core.plugins.media import add_media

def file(context):

    class File(Directive):
        required_arguments = 1
        has_content = True

        def run(self):
            media = add_media(context, context.content, self.arguments[0])
            return [
             raw('', ('<a href="{}">{}</a>'.format(media['link'], ' '.join(self.content).strip())),
               format='html')]

    return File


class rstFile:

    def parser_setup(self, context):
        directives.register_directive('file', file(context))