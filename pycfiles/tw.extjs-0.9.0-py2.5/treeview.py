# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tw/extjs/treeview.py
# Compiled at: 2008-09-03 16:29:02
from tw.api import Widget, JSLink, CSSLink, JSSource
from tw.extjs import all

class TreeViewJS(JSSource):
    _resources = []
    source_vars = params = [
     'treeDiv', 'title', 'collapsible',
     'animCollapse', 'border',
     'autoScroll', 'animate',
     'enableDD', 'containerScroll', 'height',
     'width', 'fetch', 'rootID', 'rootText', 'divID', 'frame']
    treeDiv = 'treeView'
    title = 'My Tree'
    collapsible = True
    animCollapse = True
    border = True
    divID = 'treeView'
    autoScroll = True
    animate = True
    enableDD = True
    containerScroll = True
    height = 300
    width = 200
    fetch = 'fetch'
    frame = True
    rootText = 'Root'
    rootID = 'Root'
    src = '\nExt.onReady(function() {\n    // Define Tree.\n    var Tree_Category_Loader = new Ext.tree.TreeLoader({\n        dataUrl   :"${fetch}"\n    });\n    var Tree_Category = new Ext.tree.TreePanel({\n        title            : "$title",\n        collapsible      : $collapsible,\n        animCollapse     : $animCollapse,\n        border           : $border,\n        id               : "$divID",\n        el               : "$divID",\n        autoScroll       : $autoScroll,\n        animate          : $animate,\n        enableDD         : $enableDD,\n        containerScroll  : $containerScroll,\n        height           : $height,\n        width            : $width,\n        loader           : Tree_Category_Loader,\n        frame            : $frame,\n    });\n \n    // SET the root node.\n    var Tree_Category_Root = new Ext.tree.AsyncTreeNode({\n        text\t\t: \'$rootText\',\n        draggable\t: false,\n        id\t\t: \'$rootID\'\n    });\n \n    // Render the tree.\n    Tree_Category.setRootNode(Tree_Category_Root);\n    Tree_Category.render();\n    Tree_Category_Root.expand();\n});\n'
    template_engine = 'genshi'
    javascript = [all]

    def update_params(self, d):
        for param in self.source_vars:
            value = getattr(self, param)
            if isinstance(value, bool):
                d[param] = str(value).lower()

        super(TreeViewJS, self).update_params(d)

    def post_init(self, *args, **kw):
        pass


treeview_js = TreeViewJS()

class TreeView(Widget):
    treeview_js_obj = TreeViewJS
    params = js_params = ['treeDiv',
     'title',
     'collapsible',
     'animCollapse',
     'border',
     'autoScroll',
     'animate',
     'enableDD',
     'containerScroll',
     'height',
     'width',
     'fetch',
     'rootID',
     'rootText',
     'divID']
    template = '<div id="$divID" />'
    title = 'Override JS Title'

    def __new__(cls, *args, **kw):
        cls = Widget.__new__(cls, *args, **kw)
        d = {}
        for param in cls.js_params:
            value = getattr(cls, param)
            if value is not None:
                d[param] = getattr(cls, param)

        treeview_js = cls.treeview_js_obj(**d)
        cls.javascript = [treeview_js]
        return cls