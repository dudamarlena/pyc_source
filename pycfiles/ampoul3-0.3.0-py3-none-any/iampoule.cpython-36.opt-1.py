# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ampoule/iampoule.py
# Compiled at: 2017-12-10 09:58:00
# Size of source mod 2**32: 814 bytes
from zope.interface import Interface

class IStarter(Interface):

    def startAMPProcess(ampChild, ampParent=None):
        """
        @param ampChild: The AMP protocol spoken by the created child.
        @type ampChild: L{twisted.protocols.amp.AMP}

        @param ampParent: The AMP protocol spoken by the parent.
        @type ampParent: L{twisted.protocols.amp.AMP}
        """
        pass

    def startPythonProcess(prot, *args):
        """
        @param prot: a L{protocol.ProcessProtocol} subclass
        @type prot: L{protocol.ProcessProtocol}

        @param args: a tuple of arguments that will be passed to the
                    child process.

        @return: a tuple of the child process and the deferred finished.
                 finished triggers when the subprocess dies for any reason.
        """
        pass