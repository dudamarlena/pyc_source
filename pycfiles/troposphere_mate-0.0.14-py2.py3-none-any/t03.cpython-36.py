# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/orch_example/t03.py
# Compiled at: 2019-08-08 16:17:45
# Size of source mod 2**32: 1393 bytes
from troposphere_mate.orch_example.config import Config as BaseConfig
from troposphere_mate import Template, Output, Export, Ref, iam

class Canned(BaseConfig):

    def do_create_template(self):
        policy_doc = {'Version':'2012-10-17', 
         'Statement':[
          {'Sid':'VisualEditor0', 
           'Effect':'Allow', 
           'Action':[
            's3:ListAllMyBuckets',
            's3:ListBucket',
            's3:HeadBucket'], 
           'Resource':'*'}]}
        tpl = Template()
        policy = iam.ManagedPolicy('IamPolicy3',
          template=tpl,
          ManagedPolicyName=('{}-policy3'.format(self.ENVIRONMENT_NAME.get_value())),
          PolicyDocument=policy_doc)
        tpl.add_output(Output((policy.title),
          Value=(Ref(policy)),
          Export=(Export('{}-{}'.format(self.ENVIRONMENT_NAME.get_value(), policy.title)))))
        self.template = tpl
        return self.template


if __name__ == '__main__':
    can = Canned(PROJECT_NAME='my_project', STAGE='dev')
    can.create_template()
    can.template.pprint()