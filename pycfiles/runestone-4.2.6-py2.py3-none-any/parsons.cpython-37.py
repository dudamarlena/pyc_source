# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/parsons/parsons.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 6066 bytes
__author__ = 'isaiahmayerchak'
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.mchoice import Assessment
from runestone.server.componentdb import addQuestionToDB, addHTMLToDB
from runestone.common.runestonedirective import RunestoneNode, add_i18n_js

def setup(app):
    app.add_directive('parsonsprob', ParsonsProblem)
    app.add_node(ParsonsNode, html=(visit_parsons_node, depart_parsons_node))
    app.add_config_value('parsons_div_class', 'runestone', 'html')


TEMPLATE = '\n        <div class="%(divclass)s" style="max-width: none;">\n        <pre data-component="parsons" id="%(divid)s" %(adaptive)s %(maxdist)s %(order)s %(noindent)s %(language)s %(numbered)s>\n        <span data-question>%(qnumber)s: %(instructions)s</span>%(code)s\n        </pre>\n        </div>\n    '

class ParsonsNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, options, **kwargs):
        (super(ParsonsNode, self).__init__)(**kwargs)
        self.parsonsnode_components = options


def visit_parsons_node(self, node):
    div_id = node.parsonsnode_components['divid']
    components = dict(node.parsonsnode_components)
    components.update({'divid': div_id})
    res = TEMPLATE % components
    addHTMLToDB(div_id, components['basecourse'], res)
    self.body.append(res)


def depart_parsons_node(self, node):
    pass


class ParsonsProblem(Assessment):
    __doc__ = "\n.. parsonsprob:: unqiue_problem_id_here\n   :maxdist:\n   :order:\n   :language:\n   :noindent:\n   :adaptive:\n   :numbered:\n\n   Solve my really cool parsons problem...if you can.\n   -----\n   def findmax(alist):\n   =====\n      if len(alist) == 0:\n         return None\n   =====\n      curmax = alist[0]\n      for item in alist:\n   =====\n         if item &gt; curmax:\n   =====\n            curmax = item\n   =====\n      return curmax\n\n\nconfig values (conf.py):\n\n- parsons_div_class - custom CSS class of the component's outermost div\n    "
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = Assessment.option_spec.copy()
    option_spec.update({'maxdist':directives.unchanged, 
     'order':directives.unchanged, 
     'language':directives.unchanged, 
     'noindent':directives.flag, 
     'adaptive':directives.flag, 
     'numbered':directives.unchanged})
    has_content = True

    def run(self):
        super(ParsonsProblem, self).run()
        addQuestionToDB(self)
        env = self.state.document.settings.env
        self.options['instructions'] = ''
        self.options['code'] = self.content
        self.options['divclass'] = env.config.parsons_div_class
        if 'numbered' in self.options:
            self.options['numbered'] = ' data-numbered="' + self.options['numbered'] + '"'
        else:
            self.options['numbered'] = ''
        if 'maxdist' in self.options:
            self.options['maxdist'] = ' data-maxdist="' + self.options['maxdist'] + '"'
        else:
            self.options['maxdist'] = ''
        if 'order' in self.options:
            self.options['order'] = ' data-order="' + self.options['order'] + '"'
        else:
            self.options['order'] = ''
        if 'noindent' in self.options:
            self.options['noindent'] = ' data-noindent="true"'
        else:
            self.options['noindent'] = ''
        if 'adaptive' in self.options:
            self.options['adaptive'] = ' data-adaptive="true"'
        else:
            self.options['adaptive'] = ''
        if 'language' in self.options:
            self.options['language'] = ' data-language="' + self.options['language'] + '"'
        else:
            self.options['language'] = ''
        if '-----' in self.content:
            index = self.content.index('-----')
            self.options['instructions'] = '\n'.join(self.content[:index])
            self.options['code'] = self.content[index + 1:]
        elif '=====' in self.options['code']:
            self.options['code'] = '\n'.join(self.options['code'])
            self.options['code'] = self.options['code'].replace('=====', '---')
        else:
            self.options['code'] = '\n'.join(self.options['code'])
        self.assert_has_content()
        parsons_node = ParsonsNode((self.options), rawsource=(self.block_text))
        parsons_node.source, parsons_node.line = self.state_machine.get_source_and_line(self.lineno)
        return [
         parsons_node]