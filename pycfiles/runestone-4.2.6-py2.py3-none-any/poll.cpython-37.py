# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/poll/poll.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 5602 bytes
__author__ = 'isaiahmayerchak'
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.common.runestonedirective import RunestoneIdDirective, RunestoneNode
from runestone.server.componentdb import addQuestionToDB, addHTMLToDB

def setup(app):
    app.add_directive('poll', Poll)
    app.add_node(PollNode, html=(visit_poll_node, depart_poll_node))
    app.add_config_value('poll_div_class', 'alert alert-warning', 'html')


TEMPLATE_START = '\n<div class="runestone">\n<ul data-component="poll" id=%(divid)s %(comment)s class=\'%(divclass)s\' data-results=\'%(results)s\'>\n%(question)s\n'
TEMPLATE_OPTION = '\n<li>%(optiontext)s</li>\n'
TEMPLATE_END = '</ul></div>'

class PollNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(PollNode, self).__init__)(**kwargs)
        self.poll_content = content


def visit_poll_node(self, node):
    res = TEMPLATE_START
    res = res % node.poll_content
    if node.poll_content['scale'] == '':
        okeys = list(node.poll_content.keys())
        okeys.sort()
        for k in okeys:
            if 'option_' in k:
                node.poll_content['optiontext'] = node.poll_content[k]
                res += TEMPLATE_OPTION % node.poll_content

    else:
        for i in range(node.poll_content['scale']):
            node.poll_content['optiontext'] = i + 1
            res += TEMPLATE_OPTION % node.poll_content

    res += TEMPLATE_END
    addHTMLToDB(node.poll_content['divid'], node.poll_content['basecourse'], res)
    self.body.append(res)


def depart_poll_node(self, node):
    """ This is called at the start of processing a poll node.  If poll had recursive nodes
        etc and did not want to do all of the processing in visit_poll_node any finishing touches could be
        added here.
    """
    pass


class Poll(RunestoneIdDirective):
    __doc__ = '\n.. poll:: identifier\n    :scale: <X>  Setting the scale creates an "On a scale of 1 to <X>" type of question\n    :allowcomment: Boolean--provides comment box\n    :option_1: Providing Question text for each option creates a "Choose one of these options" type of poll.\n    :option_2: Option 2\n    :option_3: Option 3    ...etc...(Up to 10 options in mode 2)\n    :results: One of all, instructor, superuser - who should see results?\n\n\nconfig values (conf.py):\n\n- poll_div_class - custom CSS class of the component\'s outermost div\n    '
    required_arguments = 1
    optional_arguments = 0
    has_content = True
    option_spec = {'scale':directives.positive_int, 
     'allowcomment':directives.flag, 
     'option_1':directives.unchanged, 
     'option_2':directives.unchanged, 
     'option_3':directives.unchanged, 
     'option_4':directives.unchanged, 
     'option_5':directives.unchanged, 
     'option_6':directives.unchanged, 
     'option_7':directives.unchanged, 
     'option_8':directives.unchanged, 
     'option_9':directives.unchanged, 
     'option_10':directives.unchanged, 
     'results':directives.unchanged}

    def run(self):
        super(Poll, self).run()
        addQuestionToDB(self)
        if self.content:
            source = '\n'.join(self.content)
        else:
            source = '\n'
        self.options['question'] = source
        if 'scale' not in self.options:
            self.options['scale'] = ''
        elif 'allowcomment' in self.options:
            self.options['comment'] = 'data-comment'
        else:
            self.options['comment'] = ''
        if 'results' not in self.options:
            self.options['results'] = 'instructor'
        env = self.state.document.settings.env
        self.options['divclass'] = env.config.poll_div_class
        poll_node = PollNode((self.options), rawsource=(self.block_text))
        poll_node.source, poll_node.line = self.state_machine.get_source_and_line(self.lineno)
        return [
         poll_node]