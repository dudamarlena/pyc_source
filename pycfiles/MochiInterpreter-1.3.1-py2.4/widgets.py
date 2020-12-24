# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mochiinterpreter/widgets.py
# Compiled at: 2006-06-30 19:35:51
import pkg_resources, turbogears
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, FormField, register_static_directory, JSSource
from turbogears.widgets.base import mochikit
js_dir = pkg_resources.resource_filename('mochiinterpreter', 'static/javascript')
register_static_directory('mochiinterpreter.javascript', js_dir)
css_dir = pkg_resources.resource_filename('mochiinterpreter', 'static/css')
register_static_directory('mochiinterpreter.css', css_dir)

class MochiInterpreter(FormField):
    """
    This widget is an implementation of the interpreter example from MochiKit
    code.  It is provided as a facility to develop TurboGears applications
    that needs JavaScript.

    It is based on code provided in
    http://trac.turbogears.org/turbogears/ticket/255 
    """
    __module__ = __name__
    js_head = JSSource(src="\n      function toggleinterpreter() {\n        if ($('interpreterswitch')) {\n          showElement('interpreter_form');\n          $('interpreterswitch').id='interpreterswitchoff';\n          $('interpreterswitchoff').innerHTML='Hide Interpreter';\n        } else {\n          hideElement('interpreter_form')\n          $('interpreterswitchoff').id='interpreterswitch';\n          $('interpreterswitch').innerHTML='Show Interpreter';\n        }\n      }\n    ")
    javascript = [
     mochikit,
     JSLink('mochiinterpreter.javascript', 'interpreter.js'), js_head]
    css = [CSSLink('mochiinterpreter.css', 'interpreter.css')]
    template = '\n    <div xmlns:py=\'http://purl.org/kid/ns#\' py:if="active">\n      <a id=\'interpreterswitch\' onclick=\'toggleinterpreter()\' href=\'#interpreterswitch\'>Show Interpreter</a>\n      <form id=\'interpreter_form\' autocomplete=\'off\'>\n        <div id=\'interpreter_area\'>\n          <div id=\'interpreter_output\'></div>\n        </div>\n        <div id=\'oneline\'>\n          <input id=\'interpreter_text\' name=\'input_text\' type=\'text\' class=\'textbox\' size=\'100\' />\n        </div>\n        <div id=\'multiline\'>\n          <textarea id=\'interpreter_textarea\' name=\'input_textarea\' type=\'text\' class=\'textbox\' cols=\'97\' rows=\'10\'></textarea>\n          <br />\n        </div>\n      </form>   \n    </div>\n    '
    params = [
     'active']
    active = True
    if turbogears.config.get('server.environment') != 'development':
        active = False


class MochiInterpreterDesc(WidgetDescription):
    __module__ = __name__
    name = 'MochiKit Interpreter'
    template = '\n    <div>\n      ${for_widget.display()}\n    </div>\n    '

    def __init__(self, *args, **kw):
        super(MochiInterpreterDesc, self).__init__(*args, **kw)
        self.for_widget = MochiInterpreter(name='mochiinterpreter_demo')