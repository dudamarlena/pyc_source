# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/yuiwidget/richtext.py
# Compiled at: 2008-09-11 20:30:06
from zope.app.form.browser.widget import UnicodeDisplayWidget
from zope.app.form.browser.textwidgets import TextAreaWidget
from zc.resourcelibrary import need
import xss

class HTMLDisplay(UnicodeDisplayWidget):

    def __call__(self):
        if self._renderedValueSet():
            value = self._data
        else:
            value = self.context.default
        if value == self.context.missing_value:
            return ''
        return unicode(value)


class HTMLTextEditor(TextAreaWidget):
    """
    a rich text editor using YUI's SimpleEditor
    """
    height = '300px'
    width = '500px'
    focus_start = 'false'
    dompath = 'false'
    markup = 'semantic'
    removeLineBreaks = 'false'
    extracss = ''

    def __call__(self):
        need('yui-editor')
        input_widget = super(HTMLTextEditor, self).__call__()
        jsid = self.name.replace('.', '_')
        input_widget += '\n        <script language="javascript">\n            options={ height:\'%s\', \n                      width:\'%s\', \n                      dompath:%s, \n                      focusAtStart:%s,\n                      removeLineBreaks:%s,\n                      extracss=%s,\n                      markup=%s};\n            var %s_editor = new YAHOO.widget.SimpleEditor(\'%s\', options); \n            YAHOO.util.Event.on(\n                %s_editor.get(\'element\').form, \n                \'submit\', \n                function( ev ) { \n                    %s_editor.saveHTML(); \n                    }\n                );            \n            %s_editor._defaultToolbar.titlebar = false;\n            %s_editor.render();     \n        </script>    \n        ' % (self.height,
         self.width,
         self.dompath,
         self.focus_start,
         self.removeLineBreaks,
         self.extracss,
         self.markup,
         jsid, self.name, jsid, jsid, jsid, jsid)
        return input_widget

    def _toFieldValue(self, value):
        return xss.filter(value)