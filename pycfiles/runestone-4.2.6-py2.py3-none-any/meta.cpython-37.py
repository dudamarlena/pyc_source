# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/meta/meta.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 1882 bytes
__author__ = 'bmiller'
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.common.runestonedirective import RunestoneDirective

def setup(app):
    app.add_directive('shortname', Meta)
    app.add_directive('description', Meta)


class Meta(RunestoneDirective):
    required_arguments = 1
    optional_arguments = 50

    def run(self):
        """
        process the video directive and generate html for output.
        :param self:
        :return:
        """
        raw_node = nodes.raw((self.block_text), '', format='html')
        raw_node.source, raw_node.line = self.state_machine.get_source_and_line(self.lineno)
        return [
         raw_node]


source = 'This is some text.\n\n.. shortname:: divid\n.. description::  foo bar baz\n\nThis is some more text.\n'
if __name__ == '__main__':
    from docutils.core import publish_parts
    directives.register_directive('shortname', Meta)
    directives.register_directive('description', Meta)
    doc_parts = publish_parts(source,
      settings_overrides={'output_encoding':'utf8', 
     'initial_header_level':2},
      writer_name='html')
    print(doc_parts['html_body'])