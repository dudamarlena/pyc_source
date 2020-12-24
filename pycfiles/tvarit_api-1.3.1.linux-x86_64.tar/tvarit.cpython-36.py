# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/narendra/.pyenv/versions/aws/lib/python3.6/site-packages/tvarit_api/tvarit.py
# Compiled at: 2019-09-30 09:22:13
# Size of source mod 2**32: 1595 bytes
from .api import TvaritAPI
from .resources import Admin, Dashboard, Datasource, Folder, Organization, Organizations, Search, User, Users, Teams, Annotations, Alerting, Snapshot, Machine, Model, Parameter, Pipeline, Handler, Task, Output, Job

class Tvarit:

    def __init__(self, auth, host='localhost', port=None, url_path_prefix='', protocol='http', verify=True):
        self.api = TvaritAPI(auth,
          host=host,
          port=port,
          url_path_prefix=url_path_prefix,
          protocol=protocol,
          verify=verify)
        self.admin = Admin(self.api)
        self.dashboard = Dashboard(self.api)
        self.datasource = Datasource(self.api)
        self.folder = Folder(self.api)
        self.organization = Organization(self.api)
        self.organizations = Organizations(self.api)
        self.search = Search(self.api)
        self.user = User(self.api)
        self.users = Users(self.api)
        self.teams = Teams(self.api)
        self.annotations = Annotations(self.api)
        self.alerting = Alerting(self.api)
        self.snapshot = Snapshot(self.api)
        self.machine = Machine(self.api)
        self.model = Model(self.api)
        self.parameter = Parameter(self.api)
        self.pipeline = Pipeline(self.api)
        self.handler = Handler(self.api)
        self.task = Task(self.api)
        self.output = Output(self.api)
        self.job = Job(self.api)