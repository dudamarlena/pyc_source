# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/mootools/sortable.py
# Compiled at: 2009-11-30 09:56:23
from tw.api import Widget, JSLink, CSSLink, CSSSource, JSSource
from genshi.template.text import TextTemplate
from base import DomElementWithValue, moo_core_compressed_js
widget_js = JSLink(modname=__name__, filename='static/sortable.js', javascript=[])

class SortableWidget(Widget):
    template = 'genshi:tw.mootools.templates.sortable'
    javascript = [
     moo_core_js]
    attrs = {'width': '300px', 'backround-color': 'white'}
    blockAttrs = {}
    params = [
     'attrs', 'blockAttrs', 'widget_css', 'widget_js', 'onComplete']
    onComplete = "console.log('got to onComplete')"

    def update_params(self, d):
        self._my_update_params(d)
        Widget.update_params(self, d)
        return d

    def _my_update_params(self, d):
        values = d['value']
        d['widget_css'] = [CSSSource(self._generateCSS(values))]
        return d

    cssTemplate = '${"#"}${id} { \n\tposition: inherit;\n}\n \nul${"#"}sortables {\n\twidth: 300px;\n\tmargin: 0;\n\tpadding: 0;\n#for a, v in attrs.iteritems()\n    ${a} : ${v};\n#end\n}\n \n#for value in values\n    li.sortable_${value.id} {\n            padding: 4px 8px;\n            cursor: pointer;\n            list-style: none;\n    #for a, v in value.attrs.iteritems()\n            ${a} : ${v};\n    #end\n    }\n#end\n \nul${"#"}sortables li {\n\tmargin: 10px 0;\n}\n\n\n'

    def _generateCSS(self, values):
        template = TextTemplate(self.cssTemplate)
        s = template.generate(values=values, blockAttrs=self.blockAttrs, attrs=self.attrs, id=self.id).render()
        return s