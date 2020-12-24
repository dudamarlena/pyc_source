# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/twisted/plugins/turtl_plugin.py
# Compiled at: 2009-08-21 14:13:15
"""
Turtl plugin for Twisted.
"""
from zope.interface import classProvides
from twisted.plugin import IPlugin
from twisted.python.usage import Options, UsageError
from twisted.python import filepath
from twisted.application.service import IServiceMaker

class TurtlPlugin(object):
    """
    This plugin provides ways to throttle web request through
    a proxy server that can be configured on a hostname basis.
    """
    classProvides(IPlugin, IServiceMaker)
    tapname = 'turtl'
    description = 'Throttling proxy a given set of destination hostnames'

    class options(Options):
        optParameters = [
         [
          'with_syslog_prefix', 'p', None, 'Activate syslog and give it the specified prefix (default will not use syslog)'],
         [
          'config', 'c', None, 'The yaml configuration file that should be used']]

        def postOptions(self):
            """
            Check and finalize the value of the arguments.
            """
            if self['config'] is None:
                raise UsageError('Must specify a config file')
            fp = filepath.FilePath(self['config'])
            if not fp.exists():
                raise UsageError("%s doesn't exist." % (fp.path,))
            self['config'] = fp
            return

    @classmethod
    def makeService(cls, options):
        """
        Create an L{IService} for the parameters and return it
        """
        from turtl import service
        return service.makeService(options)