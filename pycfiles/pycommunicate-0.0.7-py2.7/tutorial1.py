# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\docs\tutorial\tutorial1.py
# Compiled at: 2016-06-11 15:57:34
import eventlet
from pycommunicate.server.bases.views import View
from pycommunicate.server.bases.controller import ControllerFactory
from pycommunicate.server.app.communicate import CommunicateApp
app = CommunicateApp()

class TodoView(View):

    def render(self):
        return self.controller.templater.render('home.html')


controller = ControllerFactory().add_view(TodoView).set_default_view(TodoView)
app.add_controller('/', controller)
app.set_secret_key('secret!')
app.run()