# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/disqus/disqus.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 4075 bytes
__author__ = 'isaacdontjelindell'
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.common.runestonedirective import RunestoneDirective, RunestoneNode
DISQUS_BOX = '<script type="text/javascript">\n    function %(identifier)s_disqus(source) {\n        if (window.DISQUS) {\n\n            $(\'#disqus_thread\').insertAfter(source); //put the DIV for the Disqus box after the link\n\n            //if Disqus exists, call it\'s reset method with new parameters\n            DISQUS.reset({\n                reload: true,\n                config: function () {\n                    this.page.identifier = \'%(identifier)s_\' + eBookConfig.course;\n                    this.page.url = \'https://%(identifier)s_\'+eBookConfig.course+\'.interactivepython.com/#!\';\n                }\n            });\n\n        } else {\n            //insert a wrapper in HTML after the relevant "show comments" link\n            $(\'<div id="disqus_thread"></div>\').insertAfter(source);\n\n            // set Disqus required vars\n            disqus_shortname = \'%(shortname)s\';\n            disqus_identifier = \'%(identifier)s_\' + eBookConfig.course;\n            disqus_url = \'http://%(identifier)s_\'+eBookConfig.course+\'.interactivepython.com/#!\';\n\n            //append the Disqus embed script to HTML\n            var dsq = document.createElement(\'script\'); dsq.type = \'text/javascript\'; dsq.async = true;\n            dsq.src = \'https://\' + disqus_shortname + \'.disqus.com/embed.js\';\n            $(\'head\').append(dsq);\n\n        }\n    }\n</script>\n'
DISQUS_LINK = '\n<a href="#disqus_thread" class=\'disqus_thread_link\' data-disqus-identifier="%(identifier)s" onclick="%(identifier)s_disqus(this);">Show Comments</a>\n<script type=\'text/javascript\'>\n    $("a[data-disqus-identifier=\'%(identifier)s\']").attr(\'data-disqus-identifier\', \'%(identifier)s_\' + eBookConfig.course);\n</script>\n'

def setup(app):
    app.add_directive('disqus', DisqusDirective)
    app.add_node(DisqusNode, html=(visit_disqus_node, depart_disqus_node))
    app.connect('doctree-resolved', process_disqus_nodes)
    app.connect('env-purge-doc', purge_disqus_nodes)


class DisqusNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(DisqusNode, self).__init__)(**kwargs)
        self.disqus_components = content


def visit_disqus_node(self, node):
    res = DISQUS_BOX
    res += DISQUS_LINK
    res = res % node.disqus_components
    self.body.append(res)


def depart_disqus_node(self, node):
    pass


def process_disqus_nodes(app, env, docname):
    pass


def purge_disqus_nodes(app, env, docname):
    pass


class DisqusDirective(RunestoneDirective):
    __doc__ = '\n.. disqus::\n   :shortname: Your registered disqus id\n   :identifier: unique id for this discussion\n    '
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = False
    option_spec = {'shortname':directives.unchanged_required, 
     'identifier':directives.unchanged_required}

    def run(self):
        """
        generate html to include Disqus box.
        :param self:
        :return:
        """
        disqus_node = DisqusNode((self.options), rawsource=(self.block_text))
        disqus_node.source, disqus_node.line = self.state_machine.get_source_and_line(self.lineno)
        return [
         disqus_node]