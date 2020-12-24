# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dialtone/dev/Adroll/quebert/twisted/plugins/qexec_plugins.py
# Compiled at: 2009-07-31 18:32:56
"""
Quebert Executor plugin for Quebert.
"""
from zope.interface import classProvides
from twisted.plugin import IPlugin
from twisted.python.usage import Options, UsageError
from twisted.python import reflect
from twisted.application.service import IServiceMaker

class QuExecutorPlugin(object):
    """
    This plugin eases the process of creating an executor
    using a Twisted Web server.
    """
    classProvides(IPlugin, IServiceMaker)
    tapname = 'quexecutor'
    description = 'Create an AMQP tasks executor'

    class options(Options):
        optParameters = [
         [
          'with_syslog_prefix', 'p', None, 'Activate syslog and give it the specified prefix (default will not use syslog)'],
         [
          'function', 'f', None, 'The function that will setup the listeners and executors'],
         [
          'port', 'p', 8000, 'The port on which the qexecutor should listen', int],
         [
          'subconfig', 's', '', 'Optional configuration option for the subprocess', str]]

        def postOptions(self):
            """
            Check and finalize the value of the arguments.
            """
            if self['function'] is None:
                raise UsageError('Must specify a setup function')
            try:
                self['function'] = reflect.namedAny(self['function'])
            except:
                raise UsageError("%s doesn't exist." % (self['function'],))

            return

    @classmethod
    def makeService(cls, options):
        """
        Create an L{IService} for the parameters and return it
        """
        from quebert import service
        return service.makeExecutorService(options)