# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/mootools/omnigrid.py
# Compiled at: 2009-11-30 09:56:23
from tw.api import Widget, JSLink, CSSLink, CSSSource
from genshi.template.text import TextTemplate
import tw.forms
from tw.mootools.base import moo_core_js_compressed, moo_more_js_compressed
omnigrid_js = JSLink(modname=__name__, filename='static/omnigrid/omnigrid11.js', javascript=[])
omnigrid_css = CSSLink(modname=__name__, filename='static/omnigrid/omnigrid.css', javascript=[])

class SimpleGridWidget(tw.forms.datagrid.DataGrid):
    template = 'genshi:tw.mootools.templates.simplegrid'
    javascript = [
     moo_core_js_compressed, moo_more_js_compressed, omnigrid_js]
    css = [omnigrid_css]