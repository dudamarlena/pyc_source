# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nameko_sendgrid.py
# Compiled at: 2018-03-08 08:37:25
# Size of source mod 2**32: 567 bytes
from nameko.extensions import DependencyProvider
from sendgrid import SendGridAPIClient

class SendGrid(DependencyProvider):

    def __init__(self, **options):
        self.options = options
        self.client = None
        self.key = None

    def setup(self):
        self.key = self.container.config['SENDGRID_KEY']

    def start(self):
        self.client = SendGridAPIClient(apikey=(self.key))

    def stop(self):
        self.client = None

    def kill(self):
        self.client = None

    def get_dependency(self, worker_ctx):
        return self.client