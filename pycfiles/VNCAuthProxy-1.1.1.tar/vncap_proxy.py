# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kennric/Projects/twisted_vncauthproxy/twisted/plugins/vncap_proxy.py
# Compiled at: 2014-05-21 16:51:12
from twisted.application.service import IServiceMaker
from twisted.application.strports import service
from twisted.plugin import IPlugin
from twisted.python.usage import Options
from zope.interface import implements

class ProxyOptions(Options):
    optParameters = [
     [
      'control', 'c', 'tcp:8888:interface=localhost',
      'Endpoint for the control socket']]


class ProxyServiceMaker(object):
    implements(IPlugin, IServiceMaker)
    tapname = 'vncap'
    description = 'Specialized VNC proxy with authentication'
    options = ProxyOptions

    def makeService(self, options):
        """
        Prepare a control socket.
        """
        from vncap.control import ControlFactory
        return service(options['control'], ControlFactory())


servicemaker = ProxyServiceMaker()