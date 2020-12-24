# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\widgets\links.py
# Compiled at: 2011-07-14 06:58:06
"""TurboGears widgets for building menus"""
__all__ = [
 'Tabber', 'SyntaxHighlighter', 'JumpMenu']
import warnings
from turbojson.jsonify import encode
from turbogears.widgets.base import CSSLink, JSLink, CSSSource, JSSource, Widget, CoreWD, static, js_location
from turbogears.widgets.forms import SelectionField

class Tabber(Widget):
    """A tabbed-panel widget.

    This widget includes the tabber js and css into your rendered
    page so you can create tabbed divs by assigning them the 'tabber'
    and 'tabbertab' classes.

    """
    __module__ = __name__
    css = [
     CSSLink(static, 'tabber/tabber.css', media='screen')]

    def __init__(self, tabber_options=None, use_cookie=False, hide_on_load=True, *args, **kw):
        super(Tabber, self).__init__(*args, **kw)
        js = []
        if tabber_options is None:
            tabber_options = {}
        if use_cookie and ('onLoad' in tabber_options or 'onClick' in tabber_options):
            warnings.warn("Cannot use cookies if overriden by tabber_options['onClick'] or tabber_options['onLoad']. Undefined behavior.")
        if use_cookie:
            js.append(JSLink(static, 'tabber/tabber_cookie.js'))
        if tabber_options:
            js.append(JSSource('var tabberOptions = %s;' % encode(tabber_options)))
        if use_cookie:
            js.append(JSSource("\n                try {\n                    tabberOptions\n                } catch(e){\n                    tabberOptions = {};\n                }\n                tabberOptions['onLoad'] = tabber_onload;\n                tabberOptions['onClick'] = tabber_onclick;\n                tabberOptions['cookie'] = 'TGTabber';"))
        if hide_on_load:
            js.append(JSSource("document.write('%s');" % '<style type="text/css">.tabber{display:none;}</style>'))
        js.append(JSLink(static, 'tabber/tabber-minimized.js', location=js_location.bodytop))
        self.javascript = js
        return


class TabberDesc(CoreWD):
    __module__ = __name__
    name = 'Tabber'
    for_widget = Tabber()
    template = '<div class="tabber">\n        <div class="tabbertab"><h2>Tab 1</h2><p>This is page 1.</p></div>\n        <div class="tabbertab"><h2>Tab 2</h2><p>This is page 2.</p></div>\n        <div class="tabbertab"><h2>Tab 3</h2><p>This is page 3.</p></div>\n        </div>'


class SyntaxHighlighter(Widget):
    """A source code syntax-highlighter widget.

    This widget includes the syntax highlighter js and css into your
    rendered page to syntax-hightlight textareas named 'code'. The supported
    languages can be listed at the 'languages' __init__ parameter.

    """
    __module__ = __name__
    available_langs = set(['CSharp', 'Css', 'Delphi', 'Java', 'JScript', 'Php', 'Python', 'Ruby', 'Sql', 'Vb', 'Xml'])
    css = [
     CSSLink(static, 'sh/SyntaxHighlighter.css')]

    def __init__(self, languages=None):
        super(SyntaxHighlighter, self).__init__()
        javascript = [JSLink(static, 'sh/shCore.js', location=js_location.bodybottom)]
        for lang in languages or ['Python', 'Xml']:
            if lang not in self.available_langs:
                raise ValueError("Unsupported language %s. Available languages: '%s'" % (lang, (', ').join(self.available_langs)))
            source = 'sh/shBrush%s.js' % lang
            javascript.append(JSLink(static, source, location=js_location.bodybottom))

        javascript.append(JSSource("dp.SyntaxHighlighter.HighlightAll('code');", location=js_location.bodybottom))
        self.javascript = javascript


class SyntaxHighlighterDesc(CoreWD):
    __module__ = __name__
    name = 'Syntax Highlighter'
    for_widget = SyntaxHighlighter()
    template = '    <textarea name="code" class="py">\n        def say_hello():\n            print "Hello world!"\n    </textarea>'


class JumpMenu(SelectionField):
    """A widget for a select field to choose a destination link.

    Choose a link from the menu and the page will be redirected to the selected
    link.

    """
    __module__ = __name__
    js = JSSource('\n    <!--\n    function TG_jumpMenu(targ,f,restore){\n      eval(targ+".location=\'"+f.options[f.selectedIndex].value+"\'");\n      if (restore) f.selectedIndex=0;\n    }\n    //-->\n    ')
    template = '\n    <select xmlns:py="http://genshi.edgewall.org/"\n        name="${name}"\n        class="${field_class}"\n        id="${field_id}"\n        onchange="TG_jumpMenu(\'parent\',this,0)"\n        py:attrs="attrs"\n    >\n        <optgroup py:for="group, options in grouped_options"\n            label="${group}"\n            py:strip="not group"\n        >\n            <option py:for="value, desc, attrs in options"\n                value="${value}"\n                py:attrs="attrs"\n                py:content="desc"\n            />\n        </optgroup>\n    </select>\n    '
    javascript = [
     js]
    _selected_verb = 'selected'
    params = ['attrs']
    params_doc = {'attrs': 'Dictionary containing extra (X)HTML attributes for the select tag'}
    attrs = {}


class JumpMenuDesc(CoreWD):
    __module__ = __name__
    name = 'Jump Menu'
    for_widget = JumpMenu('your_jump_menu_field', options=[('http://www.python.org', 'Python'), ('http://www.turbogears.org', 'TurboGears'), ('http://www.python.org/pypi', 'Cheese Shop'), ('http://www.pythonware.com/daily/', 'Daily Python')], default='http://www.turbogears.org')