# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /codebuild/output/src613133936/src/github.com/awslabs/aws-service-catalog-puppet/servicecatalog_puppet/workflow/management.py
# Compiled at: 2020-05-13 08:59:18
# Size of source mod 2**32: 859 bytes
import luigi
from servicecatalog_puppet import sdk
from servicecatalog_puppet.workflow import tasks

class BootstrapSpokeAsTask(tasks.PuppetTask):
    puppet_account_id = luigi.Parameter()
    account_id = luigi.Parameter()
    iam_role_arns = luigi.ListParameter()
    role_name = luigi.Parameter()
    permission_boundary = luigi.Parameter()

    def params_for_results_display(self):
        return {'account_id': self.account_id}

    def run(self):
        iam_role_arns_to_use = [iam_role_arn for iam_role_arn in self.iam_role_arns]
        iam_role_arns_to_use.append(f"arn:aws:iam::{self.account_id}:role/{self.role_name}")
        sdk.bootstrap_spoke_as(self.puppet_account_id, iam_role_arns_to_use, self.permission_boundary)
        self.write_output({})