# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/blockly/blockly.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 8251 bytes
__author__ = 'bmiller'
import os
from docutils import nodes
from runestone.common import RunestoneIdDirective, RunestoneNode

def setup(app):
    app.add_directive('blockly', Blockly)
    app.add_node(BlocklyNode, html=(visit_block_node, depart_block_node))
    app.connect('doctree-resolved', process_activcode_nodes)
    app.connect('env-purge-doc', purge_activecodes)


class BlocklyNode(nodes.General, nodes.Element, RunestoneNode):

    def __init__(self, content, **kwargs):
        (super(BlocklyNode, self).__init__)(**kwargs)
        self.ac_components = content


START = '\n<html>\n<head>\n    <script src=\'blockly_compressed.js\' type="text/javascript"> </script>\n    <script src=\'blocks_compressed.js\' type="text/javascript"> </script>\n    <script src=\'javascript_compressed.js\' type="text/javascript"> </script>\n    <script src=\'python_compressed.js\' type="text/javascript"> </script>\n    <script src=\'msg/js/en.js\' type="text/javascript"> </script>\n    <link rel="stylesheet" href="bootstrap-3.0.0/css/bootstrap.min.css" type="text/css" />\n    <link rel="stylesheet" href="video.css" type="text/css" />\n    <script type="text/javascript">\n    // Get the objects we need to do logging from the parent frame.\n    // This seems better than reloading all of jQuery and bookfuncs into the frame. But\n    // Makes this a bit more dependent on the Runestone Environment.\n    eBookConfig = parent.eBookConfig\n    logBookEvent = parent.logBookEvent\n    jQuery = parent.jQuery\n    </script>\n    <style>\n      html, body {\n        background-color: #fff;\n        margin: 0;\n        padding: 0;\n      }\n      .blocklySvg {\n        height: 100%%;\n        width: 100%%;\n      }\n      .active_out {\n        margin-top: 5px;\n        margin-left: 10px;\n        margin-right: 5px;\n      }\n    </style>\n</head>\n<body>\n<p>\n    <button class="btn btn-default" onclick="showCode()">Show Python</button>\n    <button class="btn btn-success" onclick="runCode()">Run</button>\n</p>\n<div id="%(divid)s" style="height: 480px; width: 600px;"></div>\n'
CTRL_START = '<xml id="toolbox" style="display: none">'
CTRL_END = '</xml>'
END = '\n<script>\n    Blockly.inject(document.getElementById(\'%(divid)s\'),\n        {path: \'./\', toolbox: document.getElementById(\'toolbox\')});\n\n    function showCode() {\n      // Generate JavaScript code and display it.\n      Blockly.Python.INFINITE_LOOP_TRAP = null;\n      var code = Blockly.Python.workspaceToCode();\n      alert(code);\n    }\n\n    function runCode() {\n      // Generate JavaScript code and run it.\n      window.LoopTrap = 1000;\n      Blockly.JavaScript.INFINITE_LOOP_TRAP = \'if (--window.LoopTrap == 0) throw "Infinite loop.";\\n\';\n      var code = Blockly.JavaScript.workspaceToCode();\n      Blockly.JavaScript.INFINITE_LOOP_TRAP = null;\n      if(logBookEvent) {\n          logBookEvent({\'event\': \'blockly\', \'act\': \'run\', \'div_id\': \'%(divid)s\'});\n      } else {\n          console.log(\'logBookEvent is not defined.  This should be defined in the parent frame\')\n      }\n      try {\n        eval(code);\n      } catch (e) {\n        alert(e);\n      }\n    }\n\n    Blockly.JavaScript[\'text_print\'] = function(block) {\n      // Print statement override.\n      var argument0 = Blockly.JavaScript.valueToCode(block, \'TEXT\',\n          Blockly.JavaScript.ORDER_NONE) || \'\\\'\\\'\';\n      return \'my_custom_print(\' + argument0 + \', "%(divid)s" );\\n\';\n    };\n\n    function my_custom_print(text,divid) {\n      var p = document.getElementById(divid+"_pre");\n      p.innerHTML += text + "\\n"\n      }\n\n    var xmlText = \'%(preload)s\';\n    var xmlDom = Blockly.Xml.textToDom(xmlText);\n    Blockly.Xml.domToWorkspace(Blockly.mainWorkspace, xmlDom);\n\n  </script>\n\n  <pre class="active_out" id="%(divid)s_pre"></pre>\n  </body>\n  </html>\n'

def visit_block_node(self, node):
    res = START % node.ac_components
    res += CTRL_START
    for ctrl in node.ac_components['controls']:
        if ctrl == 'variables':
            res += '<category name="Variables" custom="VARIABLE"></category>'
        else:
            if ctrl == '':
                continue
            if ctrl[0] == '*':
                res += '<category name="%s">' % ctrl[2:]
            elif ctrl == '====':
                res += '</category>'
            else:
                res += '<block type="%s"></block>\n' % ctrl

    res += CTRL_END
    res += END % node.ac_components
    path = os.path.join(node.ac_components['blocklyHomePrefix'], '_static', node.ac_components['divid'] + '.html')
    final = '<iframe class="blk-iframe" seamless src="%s" width="600" height="600"></iframe>' % path
    f = open(path, 'w')
    f.write(res)
    f.close()
    self.body.append(final)


def depart_block_node(self, node):
    """ This is called at the start of processing an activecode node.  If activecode had recursive nodes
        etc and did not want to do all of the processing in visit_ac_node any finishing touches could be
        added here.
    """
    pass


def process_activcode_nodes(app, env, docname):
    pass


def purge_activecodes(app, env, docname):
    pass


class Blockly(RunestoneIdDirective):
    required_arguments = 1
    optional_arguments = 0
    has_content = True
    option_spec = {}

    def run(self):
        super(Blockly, self).run()
        document = self.state.document
        rel_filename, filename = document.settings.env.relfn2path(self.arguments[0])
        pathDepth = rel_filename.count('/')
        self.options['blocklyHomePrefix'] = '../' * pathDepth
        plstart = len(self.content)
        if 'preload::' in self.content:
            plstart = self.content.index('preload::')
            self.options['preload'] = ' '.join(self.content[plstart + 1:])
        if self.content:
            self.options['controls'] = self.content[:plstart]
        blockly_node = BlocklyNode((self.options), rawsource=(self.block_text))
        blockly_node.source, blockly_node.line = self.state_machine.get_source_and_line(self.lineno)
        return [
         blockly_node]