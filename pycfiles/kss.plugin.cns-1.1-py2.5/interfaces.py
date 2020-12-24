# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/kss/plugin/cns/commands/interfaces.py
# Compiled at: 2008-12-14 04:09:28
from zope.interface import Interface

class ICNSCommands(Interface):
    """Commands for additional operations.
    
    Registered as command set 'cns'
    """

    def redirectRequest(url):
        """ Redirects request to specified url. """
        pass

    def valueSetter(target_element, source_element=None, value=None):
        """ Sets a value of the target_element by either source_element value or given value """
        pass

    def alertText(message):
        """ Show alert box with a given message ( not for debugging purposes as core alert plugin does) """
        pass

    def openWindow(url):
        """ Open a new window with a given url """
        pass

    def removeAttribute(selector, name):
        """ Remove attribute from node defined by selector """
        pass