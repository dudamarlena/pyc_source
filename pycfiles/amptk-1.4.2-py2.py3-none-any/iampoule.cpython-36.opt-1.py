# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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