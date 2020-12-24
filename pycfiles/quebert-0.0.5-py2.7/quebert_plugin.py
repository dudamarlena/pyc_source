# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dialtone/dev/Adroll/quebert/twisted/plugins/quebert_plugin.py
# Compiled at: 2009-08-14 14:39:46
"""
Quebert plugin for Twisted.
"""
from zope.interface import classProvides
from twisted.plugin import IPlugin
from twisted.python.usage import Options, UsageError
from twisted.python import reflect
from twisted.application.service import IServiceMaker

class QuebertPlugin(object):
    """
    This plugin eases the process of creating a mediator that pulls
    tasks from AMQP.
    """
    classProvides(IPlugin, IServiceMaker)
    tapname = 'quebert'
    description = 'Create an AMQP tasks mediator'

    class options(Options):
        optParameters = [
         [
          'with_syslog_prefix', 'p', None, 'Activate syslog and give it the specified prefix (default will not use syslog)'],
         [
          'config', 'c', None, 'The Python configuration function that you need to be called to create your environment']]

        def postOptions(self):
            """
            Check and finalize the value of the arguments.
            """
            if self['config'] is None:
                raise UsageError('Must specify a config function')
            try:
                self['config'] = reflect.namedAny(self['config'])
            except:
                raise UsageError("%s doesn't exist." % (self['config'],))

            return

    @classmethod
    def makeService(cls, options):
        """
        Create an L{IService} for the parameters and return it
        """
        from quebert import service
        return service.makeService(options)