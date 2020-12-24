# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./scripts/../apps/example/webapp/controller/http.py
# Compiled at: 2011-12-01 01:43:44
from chula.www import controller

class Http(controller.Controller):

    def _format(self, d):
        return ('\n').join('%s==%s' % (k, v) for k, v in d.items())

    def render_form(self):
        return self._format(self.env.form)

    def render_form_get(self):
        return self._format(self.env.form_get)

    def render_form_post(self):
        return self._format(self.env.form_post)

    def render_form_raw(self):
        return self.env.form_raw