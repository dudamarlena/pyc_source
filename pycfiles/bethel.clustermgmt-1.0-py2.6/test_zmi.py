# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bethel/clustermgmt/tests/test_zmi.py
# Compiled at: 2012-04-30 10:16:39
import json
from zExceptions import BadRequest
from HealthTestCase import HealthTestCase

class HealthFunctionalTestCase(HealthTestCase):

    def setUp(self):
        super(HealthFunctionalTestCase, self).setUp()
        self.browser = self.layer.get_browser()
        self.browser.options.handle_errors = False
        self.hr_url = self.layer.hr.absolute_url()
        self.root = self.layer.get_application()

    def test_add(self):
        b = self.browser
        b.login('manager')
        code = b.open('/root/manage_addProduct/bethel.clustermgmt/manage_addHealthReporterForm')
        self.assertEquals(code, 200)
        f = b.get_form(name='addform')
        f.get_control('name').value = 'healthreporter'
        code = f.submit(name='submit_add')
        self.assertEquals(code, 200)
        self.assertTrue(getattr(self.root, 'healthreporter', None) is not None)
        code = b.open('/root/manage_addProduct/bethel.clustermgmt/manage_addHealthReporterForm')
        self.assertEquals(code, 200)
        f = b.get_form(name='addform')
        f.get_control('name').value = 'healthreporter1'
        code = f.submit(name='submit_edit')
        self.assertEquals(code, 200)
        self.assertEquals(b.url, '/root/healthreporter1/managenodes')
        return

    def test_managemain(self):
        b = self.browser
        b.login('manager')
        code = b.open(self.hr_url + '/manage_main')
        self.assertEquals(b.url, '/root/hr/managenodes')

    def test_zmi_form_nodelist(self):
        b = self.browser
        root = self.layer.get_application()
        b.login('dummy')
        code = b.open(self.hr_url + '/managenodes')
        self.assertEquals(code, 401)
        b.login('manager')
        b.open(self.hr_url + '/managenodes')
        f = b.get_form(name='nodelist')
        f.get_control('nodelist.field.nodes_in_cluster').value = 'zope1\r\nzope2'
        code = f.submit(name='nodelist.action.save-nodes')
        self.assertEquals(root.hr.nodes_in_cluster, set(['zope1', 'zope2']))
        b.open(self.hr_url + '/managenodes')
        f = b.get_form(name='nodelist')
        f.get_control('nodelist.field.nodes_in_cluster').value = 'zope1\r\nzope2\r\nzope1'
        code = f.submit(name='nodelist.action.save-nodes')
        self.assertEquals(root.hr.nodes_in_cluster, set(['zope1', 'zope2']))

    def test_zmi_form_offline(self):
        b = self.browser
        root = self.layer.get_application()
        b.login('manager')
        root.hr.nodes_in_cluster = set(['zope1', 'zope2'])
        root.hr.offline_nodes = ['zope1']
        b.open(self.hr_url + '/managenodes')
        f = b.get_form(name='offlinenodes')
        nodes = f.get_control('offlinenodes.field.offline_nodes')
        self.assertEquals(root.hr.offline_nodes, nodes.value)
        nodes.value = [
         'zope2']
        code = f.submit(name='offlinenodes.action.save-offline-nodes')
        self.assertEquals(root.hr.offline_nodes, set(['zope2']))
        f = b.get_form(name='offlinenodes')
        nodes = f.get_control('offlinenodes.field.offline_nodes')
        nodes.value = []
        code = f.submit(name='offlinenodes.action.save-offline-nodes')
        self.assertEquals(root.hr.offline_nodes, set([]))

    def test_rest_status(self):
        b = self.browser
        root = self.layer.get_application()
        b.login('manager')
        root.hr.nodes_in_cluster = set(['zope1', 'zope2'])
        root.hr.offline_nodes = set(['zope1'])
        code = b.open(self.hr_url + '/++rest++nodestatus')
        self.assertEquals(code, 200)
        self.assertEquals(b.contents, '{"zope1": {"status": "offline"}, "zope2": {"status": "online"}}')
        root.hr.offline_nodes = set([])
        code = b.open(self.hr_url + '/++rest++nodestatus')
        self.assertEquals(code, 200)
        self.assertEquals(b.contents, '{"zope1": {"status": "online"}, "zope2": {"status": "online"}}')

    def test_rest_setstatus(self):
        b = self.browser
        root = self.layer.get_application()
        change = {'zope1': {'status': 'offline'}}
        b.login('chiefeditor')
        code = b.open(self.hr_url + '/++rest++setstatus', method='POST', form={'change': json.dumps(change)})
        self.assertEquals(code, 401)
        b.login('manager')
        root.hr.nodes_in_cluster = set(['zope1', 'zope2'])
        code = b.open(self.hr_url + '/++rest++setstatus', method='POST', form={'change': json.dumps(change)})
        self.assertEquals(root.hr.offline_nodes, set(['zope1']))
        change['zope1']['status'] = 'online'
        code = b.open(self.hr_url + '/++rest++setstatus', method='POST', form={'change': json.dumps(change)})
        self.assertEquals(root.hr.offline_nodes, set([]))

    def test_call(self):
        b = self.browser
        root = self.layer.get_application()
        root.hr.nodes_in_cluster = set(['zope1', 'zope2'])
        root.hr.offline_nodes = set(['zope1'])
        self.assertRaises(BadRequest, b.open, self.hr_url, query={'node': 'zope1'})
        code = b.open(self.hr_url, query={'node': 'zope2'})
        self.assertEquals(code, 200)


import unittest

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(HealthFunctionalTestCase))
    return suite