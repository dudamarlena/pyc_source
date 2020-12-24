# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/tw/dojo/filepicker.py
# Compiled at: 2013-01-02 11:28:41
from tw.dojo.core import DojoBase

class DojoFilePicker(DojoBase):
    require = [
     'dojox.widget.FilePicker', 'dojox.data.FileStore']
    dojoType = 'dojox.widget.FilePicker'
    params = ['id',
     'attrs',
     'columns',
     'jsId',
     'cssclass']
    delayScroll = 'true'
    cssclass = ''
    rowsPerPage = 20
    columns = []
    columnReordering = 'true'
    columnResizing = 'false'
    include_dynamic_js_calls = True
    action = '.json'
    model = None
    actions = True
    engine_name = 'genshi'
    template = '<span xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/">\n                      <div dojoType="dojox.data.FileStore" url="${url}" jsId="${jsId}_filestore" pathAsQueryParam="true"></div>\n                      <div dojoType="dojox.widget.FilePicker" jsId="${jsId}" id="${jsId}" style="width: 50%;" store="${jsId}_filestore" query="{}"></div>\n                  </span>\n               '


class DojoTreeFilePicker(DojoBase):
    require = [
     'dojox.widget.ItemFileReadStore', 'dijit.Tree', 'dojo.parser']
    dojoType = 'dijit.Tree'
    params = ['id',
     'attrs',
     'jsId',
     'cssclass']
    delayScroll = 'true'
    cssclass = ''
    rowsPerPage = 20
    columns = []
    columnReordering = 'true'
    columnResizing = 'false'
    include_dynamic_js_calls = True
    action = '.json'
    model = None
    actions = True
    engine_name = 'genshi'
    template = '\n<span xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/">\n    <div dojoType="dojo.data.ItemFileReadStore"\n         url="${url}" jsid="${jsId}_store" />\n    <div dojoType="dijit.Tree" store="${jsId}_store" labelAttr="root"\n         label="Root">\n            <script type="dojo/method" event="getLabelClass" args="item">\n            if (item != null && ${jsId}.getValue(item, "type") == \'category\') {\n                    return ${jsId}.getValue(item, "name");\n            }\n        </script>\n    </div>\n'