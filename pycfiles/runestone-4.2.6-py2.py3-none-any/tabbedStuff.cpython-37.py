# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/tabbedStuff/tabbedStuff.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 6270 bytes
__author__ = 'isaiahmayerchak'
from docutils import nodes
from docutils.parsers.rst import directives
from runestone.common.runestonedirective import RunestoneDirective, RunestoneNode

def setup(app):
    app.add_directive('tabbed', TabbedStuffDirective)
    app.add_directive('tab', TabDirective)
    app.add_node(TabNode, html=(visit_tab_node, depart_tab_node))
    app.add_node(TabbedStuffNode,
      html=(visit_tabbedstuff_node, depart_tabbedstuff_node))
    app.add_config_value('tabbed_div_class', 'alert alert-warning', 'html')


BEGIN = '<div id=\'%(divid)s\' data-component="tabbedStuff" %(inactive)s class=\'%(divclass)s\'>'
TABDIV_BEGIN = '<div data-component="tab" data-tabname="%(tabname)s" %(active)s>\n'
TABDIV_END = '</div>'
END = '\n    </div>\n\n'

class TabNode(nodes.General, nodes.Element):

    def __init__(self, content, **kwargs):
        (super(TabNode, self).__init__)(**kwargs)
        self.tabnode_options = content
        self.tabname = content['tabname']


def visit_tab_node(self, node):
    divid = node.parent.divid
    tabname = node.tabname
    if 'active' in node.tabnode_options:
        node.tabnode_options['active'] = 'data-active'
    else:
        node.tabnode_options['active'] = ''
    res = TABDIV_BEGIN % {'divid':divid, 
     'tabname':tabname, 
     'active':node.tabnode_options['active']}
    self.body.append(res)


def depart_tab_node(self, node):
    self.body.append(TABDIV_END)


class TabbedStuffNode(nodes.General, nodes.Element, RunestoneNode):
    __doc__ = 'A TabbedStuffNode contains one or more TabNodes'

    def __init__(self, content, **kwargs):
        (super(TabbedStuffNode, self).__init__)(**kwargs)
        self.tabbed_stuff_options = content
        self.divid = content['divid']


def visit_tabbedstuff_node(self, node):
    divid = node.divid
    if 'inactive' in node.tabbed_stuff_options:
        node.tabbed_stuff_options['inactive'] = 'data-inactive'
    else:
        node.tabbed_stuff_options['inactive'] = ''
    res = BEGIN % {'divid':divid, 
     'divclass':node.tabbed_stuff_options['divclass'], 
     'inactive':node.tabbed_stuff_options['inactive']}
    self.body.append(res)


def depart_tabbedstuff_node(self, node):
    divid = node.divid
    res = ''
    res += END
    res = res % {'divid': divid}
    self.body.append(res)


class TabDirective(RunestoneDirective):
    __doc__ = "\n.. tab:: identifier\n   :active: Optional flag that specifies this tab to be opened when page is loaded (default is first tab)--overridden by :inactive: flag on tabbedStuff\n\n   Content\n   ...\n\n\nconfig values (conf.py):\n\n- tabbed_div_class - custom CSS class of the component's outermost div\n    "
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {'active': directives.flag}
    node_class = TabNode

    def run(self):
        """
            process the tab directive and generate html for output.
            :param self:
            :return:
            .. tab:: identifier
            :active: Optional flag that specifies this tab to be opened when page is loaded (default is first tab)--overridden by :inactive: flag on tabbedStuff

            Content
            ...
            """
        self.assert_has_content()
        self.options['tabname'] = self.arguments[0]
        tab_node = TabNode((self.options), rawsource=(self.block_text))
        self.state.nested_parse(self.content, self.content_offset, tab_node)
        return [tab_node]


class TabbedStuffDirective(RunestoneDirective):
    __doc__ = "\n.. tabbed:: identifier\n   :inactive: Optional flag that calls for no tabs to be open on page load\n\n   Content (put tabs here)\n   ...\n\n\n\nconfig values (conf.py):\n\n- tabbed_div_class - custom CSS class of the component's outermost div\n    "
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True
    option_spec = {'inactive': directives.flag}

    def run(self):
        """
            process the tabbedStuff directive and generate html for output.
            :param self:
            :return:
            .. tabbed:: identifier
            :inactive: Optional flag that calls for no tabs to be open on page load

            Content (put tabs here)
            ...
            """
        self.assert_has_content()
        self.options['divid'] = self.arguments[0]
        env = self.state.document.settings.env
        self.options['divclass'] = env.config.tabbed_div_class
        tabbedstuff_node = TabbedStuffNode((self.options), rawsource=(self.block_text))
        tabbedstuff_node.source, tabbedstuff_node.line = self.state_machine.get_source_and_line(self.lineno)
        self.state.nested_parse(self.content, self.content_offset, tabbedstuff_node)
        return [tabbedstuff_node]