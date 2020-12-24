# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/mootools/kwick.py
# Compiled at: 2009-11-30 09:56:23
from toscawidgets.api import Widget, JSLink, CSSLink, CSSSource
from genshi.template.text import TextTemplate
from tw.mootools.base import moo_core_js_compressed, moo_js, moo_more_js
kwick_js = JSLink(modname=__name__, filename='static/kwicks.js', javascript=[])

class KwickWidget(Widget):
    template = 'genshi:tw.mootools.templates.kwick'
    javascript = [
     moo_core_js_compressed, kwick_js]
    attrs = {'height': '100px', 'backround-color': 'white'}
    blockAttrs = {'height': '100px', 'width': '117px', 'backround-color': 'white'}
    params = [
     'attrs', 'blockAttrs', 'moo_css']

    def update_params(self, d):
        self._my_update_params(d)
        Widget.update_params(self, d)
        return d

    def _my_update_params(self, d):
        values = d['value']
        d['moo_css'] = [CSSSource(self._generateCSS(values))]
        return d

    cssTemplate = '${"#"}kwicks_container { \n    background-color: ${attrs.backgroundColor};\n    height: ${attrs[\'height\']};\n}\n${"#"}kwicks {\n    position: relative;\n    float: left;\n    display: block;\n\n}\n \n${"#"}kwicks .kwick {\n    #for a, v in attrs.iteritems()\n        $a : $v ;\n    #end\n}\n  \n#for value in values\n${"#"}kwick_${value.id} {\n    float: left;\n    display: block;\n    #for a, v in value.attrs.iteritems()\n         $a : $v;\n    #end\n    }\n#end\n'

    def _generateCSS(self, values):
        template = TextTemplate(self.cssTemplate)
        s = template.generate(values=values, attrs=self.attrs, blockAttrs=self.blockAttrs).render()
        return s