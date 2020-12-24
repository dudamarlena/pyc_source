# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.7/site-packages/cfn/cfn.py
# Compiled at: 2019-04-18 15:23:01
# Size of source mod 2**32: 4900 bytes
import sys, json, botocore, boto3, os
from botocore.exceptions import ClientError
cache = {}

class CfnObject:

    def read_file(self, file):
        with open(file) as (f):
            return f.read()

    def read_json(self, json_file):
        if '.json' in json_file or 'cfndeployrc' in json_file:
            data = self.read_file(json_file)
            return json.loads(data)
        print(json_file)
        return json.loads(json_file)

    def read_yaml(self, yaml_file):
        try:
            return open(yaml_file).read()
        except Exception as e:
            try:
                raise e
            finally:
                e = None
                del e


class CfnDeploy(CfnObject):

    def __init__(self, config='./.cfndeployrc'):
        self.stacks = []
        self.config = self.read_json(config)

    def generate_stacks(self):
        for stack in self.config['Stacks']:
            current_stack = CfnStack(**stack)
            self.stacks.append(current_stack)

    def deploy_stacks(self):
        if not len(self.stacks):
            self.generate_stacks()
        for stack in self.stacks:
            stack.deploy()


class CfnTemplate(CfnObject):

    def __init__(self, template):
        self._CfnTemplate__template = self.read_yaml(template)

    def get_template(self):
        return self._CfnTemplate__template


class CfnParameters(CfnObject):

    def __init__(self, params):
        self.params = self.read_json(params)

    def __getitem__(self, k):
        if k in self.params.keys():
            return self.params[k]
        return []

    def add(self, k, v):
        param = {'ParameterKey':k, 
         'ParameterValue':v}
        self.params['Parameters'].append(param)


class CfnStack(object):

    def __init__(self, stack_name, template_body, parameters=None, assumed_role=None, profile=None, outputs=None, imports=None):
        self._CfnStack__stack_name = stack_name
        self._CfnStack__template_body = CfnTemplate(template_body)
        if parameters is not None:
            self._CfnStack__params = CfnParameters(parameters)
        else:
            self._CfnStack__params = parameters
        self._CfnStack__assumed_role = assumed_role
        self._CfnStack__outputs = outputs
        self._CfnStack__imports = imports
        self._CfnStack__profile = profile

    def exists(self):
        try:
            resp = self._CfnStack__client.describe_stacks(StackName=(self._CfnStack__stack_name))
            return self._CfnStack__stack_name == resp['Stacks'][0]['StackName']
        except Exception as e:
            try:
                print('{} does not exist'.format(self._CfnStack__stack_name))
                return False
            finally:
                e = None
                del e

    def to_request_params(self):
        request_params = {}
        request_params['StackName'] = self._CfnStack__stack_name
        request_params['TemplateBody'] = self._CfnStack__template_body.get_template()
        if self._CfnStack__params is not None:
            request_params['Parameters'] = self._CfnStack__params['Parameters'] or 
            request_params['Capabilities'] = self._CfnStack__params['Capabilities'] or 
            request_params['Tags'] = self._CfnStack__params['Tags'] or 
        return request_params

    def create(self):
        try:
            request_params = self.to_request_params()
            res = (self._CfnStack__client.create_stack)(**request_params)
            return 'StackId' in res
        except Exception as e:
            try:
                print(e)
            finally:
                e = None
                del e

    def update(self):
        try:
            request_params = self.to_request_params()
            print(request_params)
            res = (self._CfnStack__client.update_stack)(**request_params)
            return 'StackId' in res
        except ClientError as e:
            try:
                print(f"Error updated stack -> {self._CfnStack__stack_name}")
                print(e)
            finally:
                e = None
                del e

    def wait_for_event(self, event_name):
        waiter = self._CfnStack__client.get_waiter(event_name)
        print('Waiting for {} to achieve status of {}'.format(self._CfnStack__stack_name, event_name))
        try:
            waiter.wait(StackName=(self._CfnStack__stack_name))
            print('{} completed'.format(event_name))
        except botocore.exceptions.WaiterError as e:
            try:
                print('{} received the error {}'.format(event_name, e))
            finally:
                e = None
                del e

    def check_for_outputs(self):
        if self._CfnStack__outputs:
            resp = self._CfnStack__client.describe_stacks(StackName=(self._CfnStack__stack_name))
            stack = resp['Stacks'][0]
            if 'Outputs' in stack:
                if len(stack['Outputs']):
                    for output in stack['Outputs']:
                        if self._CfnStack__outputs == output['OutputKey']:
                            cache[self._CfnStack__outputs] = output

    def check_for_imports(self):
        if not self._CfnStack__imports:
            return
        if self._CfnStack__imports in cache.keys():
            self._CfnStack__params.add(self._CfnStack__imports, cache[self._CfnStack__imports]['OutputValue'])

    def deploy(self):
        if self._CfnStack__profile is not None:
            print('Setting profile')
            session = boto3.Session(profile_name=(self._CfnStack__profile))
            self._CfnStack__client = session.client('cloudformation')
        else:
            self._CfnStack__client = boto3.client('cloudformation')
        self.check_for_imports()
        if self.exists():
            print(f"{self._CfnStack__stack_name} exists. Attempting to UPDATE")
            if self.update():
                self.wait_for_event('stack_update_complete')
        else:
            print(f"{self._CfnStack__stack_name} does not exist. Attempting to CREATE")
            if self.create():
                self.wait_for_event('stack_create_complete')
        self.check_for_outputs()
        print(cache)


if __name__ == '__main__':
    cfn_deploy = CfnDeploy()
    cfn_deploy.deploy()