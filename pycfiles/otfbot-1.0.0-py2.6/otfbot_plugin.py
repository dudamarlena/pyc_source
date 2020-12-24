# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted/plugins/otfbot_plugin.py
# Compiled at: 2011-04-22 06:35:42
""" Twistd plugin to start the bot
"""
from twisted.application import internet, service
from twisted.application.service import IServiceMaker, IService
from twisted.plugin import IPlugin
from twisted.python import log, usage
from twisted.python import versions as twversions
from twisted.internet import reactor
import twisted
from zope.interface import implements
import logging, logging.handlers
from logging.handlers import RotatingFileHandler
import sys, os
from otfbot.lib import version
from otfbot.services import config as configService
required_version = twversions.Version('twisted', 10, 0, 0)
if twisted._version.version < required_version:
    print 'Get %s or newer to run OTFBot' % required_version
    os._exit(1)

class Options(usage.Options):
    optParameters = [
     [
      'config', 'c', 'otfbot.yaml', 'Location of configfile']]
    optFlags = [
     [
      'otfbot-version', 'V', 'display version and quit']]


class MyMultiService(service.MultiService):

    def getServiceNamed(self, name):
        if name not in self.namedServices:
            return None
        else:
            return self.namedServices[name]


class MyServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'otfbot'
    description = 'OtfBot - The friendly Bot'
    options = Options

    def makeService(self, options):
        application = MyMultiService()
        application.version = version._version
        cfgS = configService.loadConfig(options['config'], 'plugins/*/*.yaml')
        if not cfgS:
            print 'Could not load configuration. Check the path or create' + " a new one by running 'twistd gen-otfbot-config'"
            os._exit(1)
        cfgS.setServiceParent(application)
        logging.getLogger('').setLevel(logging.DEBUG)
        root = logging.getLogger('')
        fmtPat = '%(asctime)s %(name)-10s %(module)-14s %(funcName)-20s'
        fmtPat += '%(levelname)-8s %(message)s'
        formatPattern = cfgS.get('format', fmtPat, 'logging')
        formatter = logging.Formatter(formatPattern)
        logfile = cfgS.get('file', False, 'logging')
        if logfile:
            filelogger = RotatingFileHandler(logfile, 'a', 1048576, 5)
            filelogger.setFormatter(formatter)
            root.addHandler(filelogger)
        errfile = cfgS.get('errfile', False, 'logging')
        if errfile:
            errorlogger = RotatingFileHandler(errfile, 'a', 1048576, 5)
            errorlogger.setFormatter(formatter)
            errorlogger.setLevel(logging.ERROR)
            root.addHandler(errorlogger)
        memorylogger = logging.handlers.MemoryHandler(1000)
        memorylogger.setFormatter(formatter)
        root.addHandler(memorylogger)
        stdout = cfgS.get('logToConsole', True, 'logging')
        if stdout:
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            root.addHandler(console)
        log.PythonLoggingObserver().start()
        corelogger = logging.getLogger('core')
        corelogger.info('  ___ _____ _____ ____        _   ')
        corelogger.info(' / _ \\_   _|  ___| __ )  ___ | |_ ')
        corelogger.info('| | | || | | |_  |  _ \\ / _ \\| __|')
        corelogger.info('| |_| || | |  _| | |_) | (_) | |_ ')
        corelogger.info(' \\___/ |_| |_|   |____/ \\___/ \\__|')
        _v = 'version %s' % application.version.short()
        corelogger.info(' ' * (34 - len(_v)) + _v)
        if options['otfbot-version'] == True:
            sys.exit(0)
        service_names = cfgS.get('services', [], 'main')
        service_classes = {}
        service_instances = []
        reactor.suggestThreadPoolSize(4)
        cannot_import = []
        for service_name in service_names:
            try:
                pkg = 'otfbot.services.' + service_name
                service_classes[service_name] = __import__(pkg, fromlist=['botService'])
                corelogger.info('imported %s' % pkg)
            except ImportError, e:
                corelogger.warning('Service %s cannot be loaded because of missing module: %s' % (
                 service_name, unicode(e)))
                cannot_import.append(service_name)

        service_names = list(set(service_names) - set(cannot_import))
        for service_name in service_names:
            if hasattr(service_classes[service_name], 'Meta') and hasattr(service_classes[service_name].Meta, 'depends') and not set(service_classes[service_name].Meta.depends).issubset(service_names):
                corelogger.error('service %s cannot be loaded because some dependencies are misssing: %s' % (service_name,
                 list(set(service_classes[service_name].Meta.depends) - set(service_names))))
                sys.exit(1)

        max_count = len(service_names) + 1
        while len(service_names):
            corelogger.debug('resolving dependencies, max_count=%d' % max_count)
            started = []
            for service_name in service_names:
                if not hasattr(service_classes[service_name], 'Meta') or not hasattr(service_classes[service_name].Meta, 'depends') or not len(set(service_classes[service_name].Meta.depends).intersection(service_names)):
                    srv = service_classes[service_name].botService(application, application)
                    srv.setServiceParent(application)
                    service_instances.append(srv)
                    started.append(service_name)
                    corelogger.info('started service %s' % service_name)
                    for service in service_instances:
                        if hasattr(service, 'serviceOnline'):
                            service.serviceOnline(service_name)

            for s in started:
                service_names.remove(s)

            max_count -= 1
            if max_count == 0:
                corelogger.error('Dependencies could not be resolved.')
                break

        return application


serviceMaker = MyServiceMaker()