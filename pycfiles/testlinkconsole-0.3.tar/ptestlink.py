# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbrun/Projets/Perso/projets/dev/testlinkconsole/testlinkconsole/plugins/ptestlink.py
# Compiled at: 2014-07-16 07:31:35
from libs.iBDTestPlugin import IBDTestPlugin
from testlink import TestlinkAPIClient
from ConfigParser import NoSectionError

class TestlinkPlugin(IBDTestPlugin):
    testlinkclient = ''
    serverUrl = ''
    serverKey = ''

    def init(self, config):
        try:
            self.serverUrl = config.get('testlink', 'serverUrl')
        except NoSectionError:
            self.serverUrl = ''

        try:
            self.serverKey = config.get('testlink', 'serverKey')
        except NoSectionError:
            self.serverKey = ''

        self.testlinkclient = TestlinkAPIClient(self.serverUrl, self.serverKey)

    def activate(self):
        super(TestlinkPlugin, self).activate()
        return 'Testlink plugin actif'

    def deactivate(self):
        super(TestlinkPlugin, self).deactivate()
        return 'Testlink plugin inactif'

    def run(self, browser, script):
        print 'Testlink run %s with %s' % (script, browser)

    def listProjects(self):
        result = []
        for project in self.testlinkclient.getProjects():
            result.append({'id': project['id'], 
               'name': project['name']})

        return result

    def listTestPlans(self, projectid):
        result = []
        for testplan in self.testlinkclient.getProjectTestPlans(testprojectid=projectid):
            result.append({'id': testplan['id'], 
               'name': testplan['name']})

        return result

    def listTestCases(self, testplanid):
        result = []
        for testcaseid, testcase in self.testlinkclient.getTestCasesForTestPlan(testplanid=testplanid, execution_type=2).items():
            result.append({'id': testcase[0]['tcase_id'], 
               'name': testcase[0]['tcase_name'], 
               'extid': testcase[0]['full_external_id']})

        return result