# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_aws/test_aws_API.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = ' run with\n\npython setup.py install; nosetests -v --nocapture  tests/cm_cloud/test_aws_API.py:Test_aws_api.test_001\npython setup.py install; py.test tests/cm_cloud/test_aws_API.py:Test_aws_api.test_001\nnosetests -v --nocapture tests/test_list.py\n\nor\n\nnosetests -v tests/test_list.py\n\n'
from pprint import pprint
from cloudmesh_client import ConfigDict
from cloudmesh_client.cloud.iaas.provider.aws.CloudProviderAwsAPI import CloudProviderAwsAPI
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.dotdict import dotdict
from cloudmesh_client.common.util import HEADING
from cloudmesh_client.common.util import banner
from cloudmesh_client.default import Default

class Test_aws_API:
    data = dotdict({'cloud': Default.cloud, 
       'format': 'json', 
       'user': 'fake', 
       'wrong_cloud': 'no_cloud', 
       'key': 'my_default_key', 
       'value': 'my_default_value'})

    def run(self, command):
        command = command.format(**self.data)
        banner(command, c='-')
        print command
        parameter = command.split(' ')
        shell_command = parameter[0]
        args = parameter[1:]
        result = Shell.execute(shell_command, args)
        print result
        return str(result)

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_001(self):
        HEADING('aws API')
        cloudname = 'aws'
        d = ConfigDict('cloudmesh.yaml')
        cloud_details = d['cloudmesh']['clouds'][cloudname]
        cp = CloudProviderAwsAPI(cloudname, cloud_details)
        pprint(cp.list_vm(cloudname))