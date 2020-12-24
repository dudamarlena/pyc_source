# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/tests/api_v3/test_interfaces.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 1207 bytes
import unittest
from zope.interface.verify import verifyObject, verifyClass
from bookshelf.api_v3.gce import GCEInstance
from bookshelf.api_v3.ec2 import EC2Instance
from bookshelf.api_v3.rackspace import RackspaceInstance
from bookshelf.api_v3.cloud_instance import ICloudInstanceFactory, ICloudInstance

class TestGCEInterfaces(unittest.TestCase):

    def test_gce_provides_cloud_instance_factory(self):
        verifyObject(ICloudInstanceFactory, GCEInstance)

    def test_gce_implements_cloud_instance(self):
        verifyClass(ICloudInstance, GCEInstance)


class TestEC2Interfaces(unittest.TestCase):

    def test_ec2_provides_cloud_instance_factory(self):
        verifyObject(ICloudInstanceFactory, EC2Instance)

    def test_ec2_implements_cloud_instance(self):
        verifyClass(ICloudInstance, EC2Instance)


class TestRackspaceInterfaces(unittest.TestCase):

    def test_rackspace_provides_cloud_instance_factory(self):
        verifyObject(ICloudInstanceFactory, RackspaceInstance)

    def test_rackspaceee_implements_cloud_instance(self):
        verifyClass(ICloudInstance, RackspaceInstance)


if __name__ == '__main__':
    unittest.main(verbosity=4, failfast=True)