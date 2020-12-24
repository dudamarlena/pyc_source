# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sampedro/Documents/Dev/oide-project/dev-env/local/lib/python2.7/site-packages/oide_slurm_assist-0.0.dev1-py2.7.egg/oideslurm/handlers.py
# Compiled at: 2015-11-16 17:49:37
import tornado.web, json, oide.lib.decorators, oideslurm.settings as app_settings
from oideslurm.mixins.slurm_mixin import SlurmCmdMixin
from oide.lib.handlers.base import BaseHandler
from oideslurm.config_utils import ConfigLoader

class FormConfigHandler(BaseHandler):

    @oide.lib.decorators.authenticated
    def get(self):
        schema = ConfigLoader.getFormConfigs()
        ctx = {'formSchema': schema}
        self.write(ctx)


class JobListHandler(BaseHandler, SlurmCmdMixin):

    @oide.lib.decorators.authenticated
    def get(self):
        sacct_out = self.run_sacct()
        json_obj = json.dumps(sacct_out)
        self.write(json_obj)

    @oide.lib.decorators.authenticated
    def post(self):
        return_code, output = self.job_submit(filepath=json.loads(self.request.body)['content'])
        if return_code != 0:
            self.set_status(500)
            self.write(output)
        else:
            self.write('Successful Submission')


class JobHandler(BaseHandler, SlurmCmdMixin):

    @oide.lib.decorators.authenticated
    def get(self, jobid):
        self.write(self.run_sacct(jobid=jobid))

    @oide.lib.decorators.authenticated
    def delete(self, jobid):
        pass