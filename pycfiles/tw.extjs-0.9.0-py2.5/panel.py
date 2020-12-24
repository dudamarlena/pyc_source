# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tw/extjs/panel.py
# Compiled at: 2008-09-03 16:29:00
from tw.api import Widget, js_function
from tw.extjs import all_debug as all, all_css

class Panel(Widget):
    javascript = [
     all]
    css = [all_css]
    params = source_vars = ['title', 'width', 'html', 'renderTo', 'collapsible']
    collapsible = True
    title = 'My Panel Widget'
    renderTo = title.replace(' ', '').lower()
    width = '300'
    html = 'This is a new ExtJS based ToscaWidget Widget ;-)'
    include_dynamic_js_calls = True
    engine_name = 'genshi'
    template = '\n        <div id="${renderTo}" />\n    '

    def update_params(self, d):
        super(Panel, self).update_params(d)
        for param in self.source_vars:
            value = getattr(self, param)
            if not param == 'renderTo':
                d[param] = value
            else:
                d[param] = self.title.replace(' ', '').lower()

        jsParams = dict(title=self.title, width=self.width, html=self.html, renderTo=self.title.replace(' ', '').lower(), collapsible=str(self.collapsible).lower())
        call = js_function('new Ext.Panel')(jsParams)
        self.add_call(call)