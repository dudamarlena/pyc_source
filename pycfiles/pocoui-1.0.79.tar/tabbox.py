# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/tabbox.py
# Compiled at: 2006-12-26 17:17:53
__doc__ = '\n    pocoo.utils.tabbox\n    ~~~~~~~~~~~~~~~~~~\n\n    This file helps creating a TabBox.\n\n    TabBox Implementation\n    ===================\n\n    Creating a new TabBox instance works like this::\n\n        from pocoo.utils.tabbox import TabBox, Tab\n\n        box = TabBox(request, call_function, is_inside_form,\n            #tabs\n        )\n\n    ``call_function`` is executed to get the content for a tab.\n    It\'s called with the following arguments:\n\n        1: The id of the requested tab\n        2 - n: Values of other text fields (see later)\n\n    The ``call_function`` must return a string containing the HTML code for the\n    tab content.\n\n    If ``is_inside_form`` is set to ``True``, Pocoo uses <input>s instead of\n    <a>s.  This has the advantage that the content of other text fields will\n    still exist if a user without JS/AJAX has to reload the page for selecting a\n    new tab.\n\n    The final arguments are the tabs. The creation of a tab looks like this::\n\n        Tab(tab_title, static [True], send [[]])\n\n    ``tab_title`` is the name of the tab.\n\n    ``static`` defines whether the tab content should be loaded only on request.\n    If ``static`` is set to ``True``, the content of the tab is provided by the\n    html source; else the content will be loaded later when the user selects the\n    tab.\n\n    ``send`` contains a list of other text fields whose contents are sent as\n    additional arguments to the ``call_function`` (see above).\n\n    Every `TabBox` instance has an attribute ``html`` containing the HTML source\n    for the TabBox.\n\n    A working example of a box would look like this::\n\n        # inside the Python file\n\n        from pocoo.utils.tabbox import TabBox, Tab\n        import time\n\n        def get_content(req, page):\n            page = int(page)\n            if page == 0:\n                return "Good morning"\n            elif page == 1:\n                return "Good night"\n            elif page == 2:\n                return time.asctime()\n\n        box = TabBox(req, get_content, False,\n            Tab(_("7 pm")),\n            Tab(_("11 am")),\n            Tab(_("Clock"), static=False)\n        )\n\n        return TemplateResponse(\'test.html\',\n            box = box\n        )\n\n        # inside test.html\n\n        {{ box.html }}\n\n    :copyright: 2006 by Benjamin Wiegand.\n    :license: GNU GPL, see LICENSE for more details.\n'

class TabBox(object):
    __module__ = __name__

    def __init__(self, req, func, is_form, *tabs):
        self.req = req
        self.func = func
        self.is_form = is_form
        self.selected = int(req.args.get('partial') or req.form.get('partial') or 0)
        self.tabs = tabs
        self.indexes = {}
        for tab in self.tabs:
            if tab.short_name:
                self.indexes[tab.short_name] = list(self.tabs).index(tab)

    @property
    def html(self):
        html = ['<ul class="tabs">']
        boxes = []
        for (i, tab) in enumerate(self.tabs):
            selected = self.selected == i
            html.append(tab.get_html(i, '%s.%s' % (self.func.__module__.split('.')[2], self.func.rpc_name), self.is_form, selected))
            if tab.static or selected and not tab.lazy:
                args = [ self.req.form.get(send) for send in tab.send ]
                content = self.func(self.req, i, *args)
            (boxes.append('<div class="tabbox%s" id="box_%s"%s>%s</div>' % (tab.lazy and ' indicator' or '', tab.short_name or i, selected and ' style="display: block"' or '', (tab.static or selected) and content or '')),)

        boxes.append('<div class="tabbox" id="tabbox"></div>')
        return ('\n').join(html + ['</ul>', '<div>'] + boxes + ['</div>'])


class Tab(object):
    __module__ = __name__

    def __init__(self, name, short_name=None, static=True, send=[], lazy=False):
        self.name = name
        self.short_name = short_name
        self.static = static
        self.send = send
        self.lazy = lazy

    def get_html(self, index, method, is_form, selected):
        if self.static:
            onclick = "loadTab('box_%s', this.parentNode); return false;" % (self.short_name or index)
        else:
            onclick = "return ajax(AJS.partial(loadTab, 'box_%s', this.parentNode, '%s', [%s], [%s]))" % (self.short_name or index, method, index, (',').join(self.send))
        if is_form:
            id = 'tab%s' % index
            elem = '<input type="submit" name="partial" value="%s" onclick="%s"id="%s" /><label for="%s">%s</label>' % (index, onclick, id, id, self.name)
        else:
            elem = '<a href="?partial=%s" onclick="%s">%s</a>' % (index, onclick, self.name)
        return '<li class="tab%s">%s</li>' % (selected and ' active_tab' or '', elem)