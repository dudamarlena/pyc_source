# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ampoule/rpool.py
# Compiled at: 2017-12-10 09:58:00
# Size of source mod 2**32: 2760 bytes
"""
This module implements a remote pool to use with AMP.
"""
from twisted.protocols import amp

class AMPProxy(amp.AMP):
    __doc__ = '\n    A Proxy AMP protocol that forwards calls to a wrapped\n    callRemote-like callable.\n    '

    def __init__(self, wrapped, child):
        """
        @param wrapped: A callRemote-like callable that takes an
                        L{amp.Command} as first argument and other
                        optional keyword arguments afterwards.
        @type wrapped: L{callable}.

        @param child: The protocol class of the process pool children.
                      Used to forward only the methods that are actually
                      understood correctly by them.
        @type child: L{amp.AMP}
        """
        amp.AMP.__init__(self)
        self.wrapped = wrapped
        self.child = child
        localCd = set(self._commandDispatch.keys())
        childCd = set(self.child._commandDispatch.keys())
        assert localCd.intersection(childCd) == set([b'StartTLS']), 'Illegal method overriding in Proxy'

    def locateResponder(self, name):
        """
        This is a custom locator to forward calls to the children
        processes while keeping the ProcessPool a transparent MITM.

        This way of working has a few limitations, the first of which
        is the fact that children won't be able to take advantage of
        any dynamic locator except for the default L{CommandLocator}
        that is based on the _commandDispatch attribute added by the
        metaclass. This limitation might be lifted in the future.
        """
        if name == 'StartTLS':
            return amp.AMP.locateResponder(self, 'StartTLS')
        else:
            cd = self.child._commandDispatch
            if name in cd:
                commandClass, _responderFunc = cd[name]
                doWork = lambda **kw: (self.wrapped)(commandClass, **kw)
                return self._wrapWithSerialization(doWork, commandClass)
            return amp.AMP.locateResponder(self, name)