# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/dragndrop/dragndrop.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 6274 bytes
__author__ = 'isaiahmayerchak'
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
from runestone.server.componentdb import addQuestionToDB, addHTMLToDB
from runestone.common.runestonedirective import RunestoneIdDirective, RunestoneNode, add_i18n_js

def setup(app):
    app.add_directive('dragndrop', DragNDrop)
    app.add_node(DragNDropNode, html=(visit_dnd_node, depart_dnd_node))
    app.add_config_value('dragndrop_div_class', 'runestone', 'html')


TEMPLATE_START = '\n<div class="%(divclass)s">\n<ul data-component="dragndrop" id="%(divid)s">\n    <span data-component="question">%(qnumber)s: %(question)s</span>\n\t%(feedback)s\n'
TEMPLATE_OPTION = '\n    <li data-component="draggable" id="%(divid)s_drag%(dnd_label)s">%(dragText)s</li>\n    <li data-component="dropzone" for="%(divid)s_drag%(dnd_label)s">%(dropText)s</li>\n'
TEMPLATE_END = '</ul></div>'

class DragNDropNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(DragNDropNode, self).__init__)(**kwargs)
        self.dnd_options = content


def visit_dnd_node(self, node):
    res = TEMPLATE_START
    node.delimiter = '_start__{}_'.format(node.dnd_options['divid'])
    self.body.append(node.delimiter)
    if 'feedback' in node.dnd_options:
        node.dnd_options['feedback'] = '<span data-component=feedback>' + node.dnd_options['feedback'] + '</span>'
    else:
        node.dnd_options['feedback'] = ''
    res = res % node.dnd_options
    self.body.append(res)


def depart_dnd_node(self, node):
    res = ''
    okeys = list(node.dnd_options.keys())
    okeys.sort()
    for k in okeys:
        if 'match' in k:
            x, label = k.split('_')
            node.dnd_options['dnd_label'] = label
            dragE, dropE = node.dnd_options[k].split('|||')
            node.dnd_options['dragText'] = dragE
            node.dnd_options['dropText'] = dropE
            res += node.template_option % node.dnd_options

    res += node.template_end % node.dnd_options
    self.body.append(res)
    addHTMLToDB(node.dnd_options['divid'], node.dnd_options['basecourse'], ''.join(self.body[self.body.index(node.delimiter) + 1:]))
    self.body.remove(node.delimiter)


class DragNDrop(RunestoneIdDirective):
    __doc__ = "\n.. dragndrop:: identifier\n    :feedback: Feedback that is displayed if things are incorrectly matched--is optional\n    :match_1: Draggable element text|||Dropzone to be matched with text\n    :match_2: Drag to Answer B|||Answer B\n    :match_3: Draggable text|||Text of dropzone\n    etc. (up to 20 matches)\n\n    The question goes here.\n\nconfig values (conf.py):\n\n- dragndrop_div_class - custom CSS class of the component's outermost div\n    "
    required_arguments = 1
    optional_arguments = 0
    has_content = True
    option_spec = RunestoneIdDirective.option_spec.copy()
    option_spec.update({'feedback':directives.unchanged, 
     'match_1':directives.unchanged, 
     'match_2':directives.unchanged, 
     'match_3':directives.unchanged, 
     'match_4':directives.unchanged, 
     'match_5':directives.unchanged, 
     'match_6':directives.unchanged, 
     'match_7':directives.unchanged, 
     'match_8':directives.unchanged, 
     'match_9':directives.unchanged, 
     'match_10':directives.unchanged, 
     'match_11':directives.unchanged, 
     'match_12':directives.unchanged, 
     'match_13':directives.unchanged, 
     'match_14':directives.unchanged, 
     'match_15':directives.unchanged, 
     'match_16':directives.unchanged, 
     'match_17':directives.unchanged, 
     'match_18':directives.unchanged, 
     'match_19':directives.unchanged, 
     'match_20':directives.unchanged})

    def run(self):
        super(DragNDrop, self).run()
        addQuestionToDB(self)
        if self.content:
            source = '\n'.join(self.content)
        else:
            source = '\n'
        self.options['question'] = source
        env = self.state.document.settings.env
        self.options['divclass'] = env.config.dragndrop_div_class
        dndNode = DragNDropNode((self.options), rawsource=(self.block_text))
        dndNode.source, dndNode.line = self.state_machine.get_source_and_line(self.lineno)
        dndNode.template_start = TEMPLATE_START
        dndNode.template_option = TEMPLATE_OPTION
        dndNode.template_end = TEMPLATE_END
        return [
         dndNode]