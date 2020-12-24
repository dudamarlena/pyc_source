# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/interim_cms/modules.py
# Compiled at: 2015-06-10 02:57:48
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from grappelli.dashboard.modules import DashboardModule
from interim_cms.views import ExampleTileView

class DashboardModuleViewBase(DashboardModule):
    column = 1

    def init_with_context(self, context):
        if self._initialized:
            return
        self.children = ContentType.objects.all()
        self.on_init_with_context(context)
        request = context['request']
        restore = False
        if request.method == 'POST':
            restore = True
            request.method = 'GET'
        if hasattr(self, 'view_class'):
            view = self.view_class.as_view()(request)
            self.template = view.template_name[0]
            context['rendered'] = view.rendered_content
        if restore:
            request.method = 'POST'
        self._initialized = True

    def on_init_with_context(self, context):
        pass


class ExampleModule(DashboardModuleViewBase):
    title = _('Example Module')
    view_class = ExampleTileView


class StaticModule(DashboardModuleViewBase):
    """Render a static template"""
    pass


class GraphModule(DashboardModule):
    template = 'interim_cms/graph_tile.html'
    column = 1

    def __init__(self, title=None, graph_type='bar', graph_labels=None, graph_data=None, graph_id='graph-tile', graph_colour='rgba(0, 131, 194, 1)', graph_highlight_colour=None, **kwargs):
        self.graph_type = graph_type
        self.graph_labels = graph_labels
        self.graph_data = graph_data
        self.graph_id = graph_id
        self.graph_colour = graph_colour
        if graph_highlight_colour is None:
            self.graph_highlight_colour = graph_colour
        else:
            self.graph_highlight_colour = graph_highlight_colour
        super(GraphModule, self).__init__(title, **kwargs)
        return

    def init_with_context(self, context):
        if self._initialized:
            return
        self.children = {'labels': self.graph_labels, 
           'data': self.graph_data}
        self._initialized = True