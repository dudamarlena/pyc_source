# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/controllers/admin.py
# Compiled at: 2008-06-20 03:40:59
import time, commands, logging
from pycrud.lib.base import *
log = logging.getLogger(__name__)
script = {}
script['sender'] = 'sender.py restart'
script['receiver'] = 'start-stop-sms.sh start'

class AdminController(BaseController):

    def index(self):
        return 'Hello World'

    def show_restart(self):
        return 'Restarting <a href="#" onclick="showStatus()">Refresh Page</a>'

    def restart_sender(self):
        output = commands.getstatusoutput(script['sender'])
        return render('/admin/sender.mako')

    def restart_receiver(self):
        output = commands.getstatusoutput(script['receiver'])
        return render('/admin/receiver.mako')

    def start_sender(self):
        output = commands.getstatusoutput(script['sender'])
        return render('/admin/sender.mako')

    def start_receiver(self):
        output = commands.getstatusoutput(script['receiver'])
        return render('/admin/receiver.mako')

    def show_status_sender(self):
        return render('/admin/sender.mako')

    def show_status_receiver(self):
        return render('/admin/receiver.mako')