# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/timed/timedassessment.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 4319 bytes
__author__ = 'isaiahmayerchak'
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.common.runestonedirective import RunestoneIdDirective, RunestoneNode

def setup(app):
    app.add_directive('timed', TimedDirective)
    app.add_node(TimedNode, html=(visit_timed_node, depart_timed_node))


class TimedNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(TimedNode, self).__init__)(**kwargs)
        self.timed_options = content


def visit_timed_node(self, node):
    if 'timelimit' not in node.timed_options:
        node.timed_options['timelimit'] = ''
    else:
        node.timed_options['timelimit'] = 'data-time=' + str(node.timed_options['timelimit'])
    if 'noresult' in node.timed_options:
        node.timed_options['noresult'] = 'data-no-result'
    else:
        node.timed_options['noresult'] = ''
    if 'nofeedback' in node.timed_options:
        node.timed_options['nofeedback'] = 'data-no-feedback'
    else:
        node.timed_options['nofeedback'] = ''
    if 'notimer' in node.timed_options:
        node.timed_options['notimer'] = 'data-no-timer'
    else:
        node.timed_options['notimer'] = ''
    if 'fullwidth' in node.timed_options:
        node.timed_options['fullwidth'] = 'data-fullwidth'
    else:
        node.timed_options['fullwidth'] = ''
    res = TEMPLATE_START % node.timed_options
    self.body.append(res)


def depart_timed_node(self, node):
    res = TEMPLATE_END % node.timed_options
    self.body.append(res)


TEMPLATE_START = '\n    <ul data-component="timedAssessment" %(timelimit)s id="%(divid)s" %(noresult)s %(nofeedback)s %(notimer)s %(fullwidth)s>\n    '
TEMPLATE_END = '</ul>\n    '

class TimedDirective(RunestoneIdDirective):
    __doc__ = "\n.. timed:: identifier\n    :timelimit: Number of minutes student has to take the timed assessment--if not provided, no time limit\n    :noresult: Boolean, doesn't display score\n    :nofeedback: Boolean, doesn't display feedback\n    :notimer: Boolean, doesn't show timer\n    :fullwidth: Boolean, allows the items in the timed assessment to take the full width of the screen...\n\n    "
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {'timelimit':directives.positive_int, 
     'noresult':directives.flag, 
     'nofeedback':directives.flag, 
     'fullwidth':directives.flag, 
     'notimer':directives.flag}

    def run(self):
        super(TimedDirective, self).run()
        self.assert_has_content()
        timed_node = TimedNode((self.options), rawsource=(self.block_text))
        timed_node.source, timed_node.line = self.state_machine.get_source_and_line(self.lineno)
        self.state.nested_parse(self.content, self.content_offset, timed_node)
        return [
         timed_node]