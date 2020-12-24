# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/tests/cm_libcloud/test_libcloud_aws.py
# Compiled at: 2017-04-23 10:30:41
""" run with

python setup.py install; nosetests -v --nocapture  tests/cm_libcloud/test_libcloud_api.py:Test_image.test_001

nosetests -v --nocapture tests/libcloud/test_libcloud_api.py

or

nosetests -v tests/test_image.py

"""
from __future__ import print_function
from pprint import pprint
from time import sleep
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider
from cloudmesh_client.common.ConfigDict import ConfigDict

class Test_libcloud_aws:
    """
        This class tests the lib cloud connection to aws
    """

    def test_001(self):
        self.conf = ConfigDict('cloudmesh.yaml')
        self.credentials = self.conf['cloudmesh']['clouds']['aws']['credentials']
        self.default = self.conf['cloudmesh']['clouds']['aws']['default']
        pprint(self.credentials)
        self.cls = cls = get_driver(Provider.EC2_US_EAST)
        self.driver = cls(self.credentials['EC2_ACCESS_KEY'], self.credentials['EC2_SECRET_KEY'])
        assert True

    def test_002(self):
        """list VMs"""
        self.nodes = self.driver.list_nodes()
        print(self.nodes)
        assert True

    def test_003(self):
        """list images"""
        self.images = self.driver.list()
        assert True

    def test__004(self):
        """list flavors"""
        self.sizes = self.driver.list_sizes()
        assert True

    def test_005(self):
        self.myflavor = self.default['flavor']
        self.myimage = self.default['image']
        assert True

    def test_006(self):
        size = [ s for s in self.sizes if s.id == self.myflavor ][0]
        image = [ i for i in self.images if i.id == self.myimage ][0]
        assert True

    def test_007(self):
        """launch a new VM"""
        name = ('{:}-libcloud').format(self.credentials['userid'])
        self.node = self.driver.create_node(name=name, image=self.myimage, size=self.myflavor)
        assert True

    def test_008(self):
        """check if the new VM is in the list"""
        nodes = self.driver.list_nodes()
        print(nodes)
        assert True

    def test_009(self):
        """public ip"""
        sleep(10)
        elastic_ip = self.driver.ex_allocate_address()
        self.driver.ex_associate_address_with_node(self.node, elastic_ip)
        nodes = self.driver.list_nodes()
        print(nodes)
        assert True

    def test_010(self):
        """remove node"""
        self.node.destroy()
        assert True