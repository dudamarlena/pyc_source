# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/partialviews.py
# Compiled at: 2013-02-10 13:46:57


class PartialViews(object):

    def __init__(self, app):
        self.app = app
        self.views = {}

    def __getitem__(self, key):
        return self.views[key]

    def __setitem__(self, key, value):
        self.views[key] = value

    def register(self, name, template, **kwargs):
        if name not in self.views:
            self.views[name] = PartialView(self.app, name, template, **kwargs)
        else:
            raise KeyError('That name is already taken: %s' % name)


class PartialView(object):

    def __init__(self, app, name, template, **kwargs):
        self.app = app
        self.name = name
        self.template = template
        self.args = kwargs
        self._rendered_view = None
        return

    def __str__(self):
        if not self._rendered_view:
            self._rendered_view = self.app.environment.get_template(self.template).render(**self.args)
        return self._rendered_view