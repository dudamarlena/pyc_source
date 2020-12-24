# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/abl/jquery/examples/update_content/base.py
# Compiled at: 2013-08-29 10:09:55
from tg import TGController, expose
from tg import tmpl_context as c
from tg.decorators import with_trailing_slash
from tw.api import Widget
from abl.jquery.core.widgets import AjaxUpdateContentWidget
update_widget = AjaxUpdateContentWidget('update_widget')

class UpdateContentController(TGController):

    @expose('abl.jquery.examples.update_content.templates.index')
    @with_trailing_slash
    def index(self, **kwargs):
        c.update_widget = update_widget
        return dict()

    @expose('abl.jquery.core.templates.update_content')
    @with_trailing_slash
    def content(self):
        return dict(content=dict(box1='New content for box1', box2='And new stuff for box2'))