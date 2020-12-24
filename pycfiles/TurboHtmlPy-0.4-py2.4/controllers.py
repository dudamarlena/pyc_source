# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/turbohtmlpy/examples/controllers.py
# Compiled at: 2006-01-12 16:12:29


class Root(controllers.Root):
    __module__ = __name__

    @turbogears.expose(template='htmlpy:project.templates.index')
    def index(self):
        return dict(title='My Page', content='home.htmlpy', menu=['home', 'about'], render_text=self.render_text)

    def render_text(self, context, data):
        return context.tag(style='color: red')['This text is dynamic']