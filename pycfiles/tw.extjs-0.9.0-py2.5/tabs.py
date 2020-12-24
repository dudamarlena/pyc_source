# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tw/extjs/tabs.py
# Compiled at: 2008-09-03 16:29:02
from tw.api import Widget, js_function
from tw.extjs import all, all_css

class SimpleTab(Widget):
    javascript = [
     all]
    css = [all_css]
    params = source_vars = ['tabs', 'items', 'width', 'renderTo', 'activeTab', 'frame', 'tabList']
    tabs = {'Tab Title 1': 'Tab content 1', 'Tab Title 2': 'Tab content 2'}
    items = [ {'contentEl': k.replace(' ', '').lower(), 'title': k} for k in tabs.keys() ]
    tabList = [ (k.replace(' ', '').lower(), v) for (k, v) in tabs.items() ]
    frame = True
    renderTo = 'tab1'
    activeTab = 0
    width = '300'
    include_dynamic_js_calls = True
    engine_name = 'genshi'
    template = '\n    <div  xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/" >\n        <div  id="${renderTo}">\n            <div py:for="tab in tabList" id="${tab[0]}">\n                <p> ${tab[1]} </p>\n            </div>\n        </div>\n    </div>\n    '

    def update_params(self, d):
        super(SimpleTab, self).update_params(d)
        for param in self.source_vars:
            value = getattr(self, param)
            d[param] = value

        jsParams = dict(items=self.items, width=self.width, renderTo=self.renderTo, frame=str(self.frame).lower(), activeTab=self.activeTab)
        call = js_function('new Ext.TabPanel')(jsParams)
        self.add_call(call)