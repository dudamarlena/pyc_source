# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: testlinkconsole.py
# Compiled at: 2014-07-09 16:51:09
import ConfigParser, os, sys, datetime, string, logging
from termcolor import colored
from progressbar import ProgressBar, Bar
from yapsy.PluginManager import PluginManagerSingleton
from libs.iRunnerPlugin import IRunnerPlugin
from libs.iBDTestPlugin import IBDTestPlugin
from libs.consoleBase import ConsoleBase

class TestLinkConsole(ConsoleBase):
    prompt = colored('testlink : ', 'green')
    intro = colored('Testlink Console client', 'grey')
    section = 'testlink'
    configFile = 'testlinkclient.cfg'
    logger = 0
    projectid = 0
    testplanid = 0
    serverUrl = ''
    serverKey = ''
    apiclient = ''
    output = False
    runner = ''
    storage = ''
    plugins = ''
    LIST_OBJECTS = [
     'projects', 'testplans', 'testcases']
    LIST_VARIABLE = {'projectid': 'ID projet', 
       'testplanid': 'ID campagne', 
       'serverUrl': 'Url du serveur testlink', 
       'serverKey': 'API Key du server', 
       'output': 'Output', 
       'runner': 'test runner (plugin : behat, behave ...)', 
       'storage': 'Tests storage (testlink, filesystem ...)'}

    def __init__(self, config, logger):
        ConsoleBase.__init__(self, config)
        self.logger = logger
        self.plugins = PluginManagerSingleton.get()
        self.plugins.app = self
        self.plugins.setCategoriesFilter({'Runner': IRunnerPlugin, 
           'Storage': IBDTestPlugin})
        self.plugins.setPluginPlaces(['%s/plugins' % os.path.dirname(os.path.realpath(__file__))])
        self.plugins.collectPlugins()
        for pluginInfo in self.plugins.getAllPlugins():
            self.plugins.activatePluginByName(pluginInfo.name)

    def initConnexion(self):
        try:
            print 'TODO'
        except:
            raise Exception('Connection impossible')

    def do_plugins(self, line):
        for categorie in self.plugins.getCategories():
            print colored('%s' % categorie, 'white')
            for pluginInfo in self.plugins.getPluginsOfCategory(categorie):
                print colored('%25s : %s' % (pluginInfo.name, pluginInfo.description), 'grey')

        print 'runner actif : %s ' % self.runner
        print 'storage      : %s ' % self.storage

    def do_list(self, content):
        storage = self.plugins.getPluginByName(self.storage, 'Storage').plugin_object
        storage.init(self.config)
        if content == 'projects':
            projects = storage.listProjects()
            for project in projects:
                print '%6s --> %50s' % (project['id'], project['name'])

        elif content == 'testplans':
            if self.projectid == '0':
                print colored('set projectid before', 'red')
                self.perror('set projectid before')
            else:
                testplans = storage.listTestPlans(projectid=self.projectid)
                for testplan in testplans:
                    print '%6s --> %50s' % (testplan['id'], testplan['name'])

        elif content == 'testcases':
            if self.testplanid == 0:
                print colored('set campagneid before', 'red')
            else:
                tests = storage.listTestCases(testplanid=self.testplanid)
                for test in tests:
                    print '%6s --> %50s' % (test['id'], test['name'])

        else:
            print 'list'

    def complete_list(self, text, line, begidx, endidx):
        if not text:
            completions = self.LIST_OBJECTS[:]
        else:
            completions = [ f for f in self.LIST_OBJECTS if f.startswith(text) ]
        return completions

    def help_list(self):
        print ('\n').join(['list [content]',
         ' list content from testlink'])

    def do_run(self, line):
        starttime = datetime.datetime.now()
        self.logger.info('Debut de la campagne : %s' % starttime)
        i = 0
        resultLog = []
        runner = self.plugins.getPluginByName(self.runner, 'Runner').plugin_object
        storage = self.plugins.getPluginByName(self.storage, 'Storage').plugin_object
        storage.init(self.config)
        tests = storage.listTestCases(testplanid=self.testplanid)
        self.apiclient = storage.testlinkclient
        nbtest = len(tests)
        progressbar = ProgressBar(maxval=nbtest, widgets=[Bar(marker='|')]).start()
        for test in tests:
            notes = ''
            script_behat = self.apiclient.getTestCaseCustomFieldDesignValue(testcaseexternalid=test['extid'], version=1, testprojectid=self.projectid, customfieldname='scriptBehat', details='full')
            scriptALancer = script_behat['value']
            browsers = self.apiclient.getTestCaseCustomFieldDesignValue(testcaseexternalid=test['extid'], version=1, testprojectid=self.projectid, customfieldname='Browsers', details='full')
            if browsers['value'] == '':
                browserlist = [
                 'default']
            else:
                browserlist = browsers['value'].split('|')
            for browser in browserlist:
                notes = notes + ' ====> Browser : %s\n' % browser
                runner.run(browser, scriptALancer)
                result, notes = runner.result(browser, scriptALancer)

            try:
                retour = self.apiclient.reportTCResult(testcaseid=test['id'], testplanid=self.testplanid, buildname='Validation bascule production', status=result, notes='Resultats du Test Auto (Behat) \n\n %s' % notes)
                if result == 'p':
                    msg = '%6s : %60s : OK' % (test['id'], test['name'])
                    resultLog.append(colored(msg, 'green'))
                    self.logger.info(msg)
                else:
                    msg = '%6s : %60s : NOK' % (test['id'], test['name'])
                    resultLog.append(colored(msg, 'red'))
                    self.logger.error(msg)
            except:
                try:
                    retour = self.apiclient.reportTCResult(testcaseid=test['id'], testplanid=self.testplanid, buildname='Validation bascule production', status=resultglobal, notes='Resultats du Test Auto (Behat) \n\n Erreur execution : site non accessible par exemple')
                except:
                    retour = 'Erreur de remonte de retour'

            i += 1
            progressbar.update(i)

        progressbar.finish()
        endtime = datetime.datetime.now()
        self.logger.info('Fin de la campagne : %s' % endtime)
        for i in resultLog:
            print i

        difftime = endtime - starttime
        print 'Execution : %s' % difftime
        self.logger.info('Temps Execution de la campagne : %s ' % difftime)

    def help_run(self):
        print ('\n').join(['run',
         '  run campagne'])


if __name__ == '__main__':
    config = ConfigParser.RawConfigParser()
    logger = logging.getLogger('logger')
    logger.addHandler(logging.FileHandler(filename='testlinkconsole.log'))
    logger.setLevel(logging.INFO)
    console = TestLinkConsole(config, logger)
    console.initConnexion()
    console.cmdloop()