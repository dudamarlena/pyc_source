# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/mx-theme/mxtheme/card.py
# Compiled at: 2019-04-28 16:30:45
# Size of source mod 2**32: 1395 bytes
from sphinx.locale import _
from docutils import nodes
from docutils.parsers.rst import Directive, directives

class card(nodes.General, nodes.Element):
    pass


class CardDirective(Directive):
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'title':directives.unchanged,  'link':directives.unchanged, 
     'is_head':directives.unchanged}
    has_content = True
    add_index = False

    def run(self):
        options = self.options
        cid = nodes.make_id('card-{}'.format(options['title']))
        classes = [
         'mx-card']
        if options.get('is_head', 'False').lower() == 'true':
            classes.append('head-card')
        container = nodes.container(ids=[cid], classes=classes)
        container += nodes.inline('', (options['title']), classes=['mx-card-title'])
        link = options.get('link')
        if link:
            container += nodes.inline('', link, classes=['mx-card-link'])
        para = nodes.paragraph(classes=['mx-card-text'])
        self.state.nested_parse(self.content, self.content_offset, para)
        container += para
        return [
         container]