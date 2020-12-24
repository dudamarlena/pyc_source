# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/tw/dojo/tree.py
# Compiled at: 2013-01-02 11:28:47
from tw.dojo.core import DojoBase, DojoCSSLink
from tw.core import JSLink
tree_css = DojoCSSLink(basename='dijit/themes/tundra/Tree')
dijit_css = DojoCSSLink(basename='dijit/themes/dijit')

class DojoTreeFilePicker(DojoBase):
    require = [
     'dojox.data.JsonRestStore',
     'dijit.Tree',
     'dijit.ColorPalette',
     'dijit.Menu',
     'dojo.parser']
    dojoType = 'dijit.Tree'
    params = ['id',
     'attrs',
     'jsId',
     'cssclass',
     'url']
    delayScroll = 'true'
    css = [tree_css, dijit_css]
    cssclass = ''
    rowsPerPage = 20
    columns = []
    columnReordering = 'true'
    columnResizing = 'false'
    include_dynamic_js_calls = True
    action = '.json'
    model = None
    actions = True
    template = 'genshi:tw.dojo.templates.dojotreepicker'


class DojoTreeFileOnlyCheckboxPicker(DojoTreeFilePicker):
    require = [
     'dojox.data.JsonRestStore',
     'dijit.Tree',
     'dijit.ColorPalette',
     'dijit.Menu',
     'dojo.parser',
     'twdojo.CheckedTree']
    dojoType = 'twdojo.FileOnlyCheckedTree'
    template = 'genshi:tw.dojo.templates.dojotreecheckboxpicker'


class DojoTreeCheckboxPicker(DojoTreeFilePicker):
    require = [
     'dojox.data.JsonRestStore',
     'dijit.Tree',
     'dijit.ColorPalette',
     'dijit.Menu',
     'dojo.parser',
     'twdojo.CheckedTree']
    dojoType = 'twdojo.CheckedTree'
    template = 'genshi:tw.dojo.templates.dojotreecheckboxpicker'