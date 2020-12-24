# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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