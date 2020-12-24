# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/abl/jquery/examples/tabs/base.py
# Compiled at: 2011-02-18 13:00:51
from tg import TGController, tmpl_context, expose
from tw.api import Widget
from abl.jquery.ui.widgets import JQueryUITabs

class MyWidget(Widget):
    """
    A minimalistic widget that renders a div with a
    given value.
    """
    template = '<div>${value}</div>'
    engine_name = 'genshi'


w1 = MyWidget('w1')
w2 = MyWidget('w2')
dw = MyWidget('default')
tabs_widget = JQueryUITabs('tabs', tabs_id='example_tabs', children=[
 w1, w2], title_list=[
 'first tab', 'last tab'], default_field=dw)

class TabsController(TGController):

    @expose('abl.jquery.examples.tabs.templates.index')
    def index(self):
        tmpl_context.tabs_widget = tabs_widget
        return dict()