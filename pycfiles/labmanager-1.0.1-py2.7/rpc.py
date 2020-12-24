# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/suds/bindings/rpc.py
# Compiled at: 2014-02-26 03:37:27
"""
Provides classes for the (WS) SOAP I{rpc/literal} and I{rpc/encoded} bindings.
"""
from logging import getLogger
from suds.mx.encoded import Encoded as MxEncoded
from suds.umx.encoded import Encoded as UmxEncoded
from suds.bindings.binding import Binding, envns
from suds.sax.element import Element
log = getLogger(__name__)
encns = ('SOAP-ENC', 'http://schemas.xmlsoap.org/soap/encoding/')

class RPC(Binding):
    """
    RPC/Literal binding style.
    """

    def param_defs(self, method):
        return self.bodypart_types(method)

    def envelope(self, header, body):
        env = Binding.envelope(self, header, body)
        env.addPrefix(encns[0], encns[1])
        env.set('%s:encodingStyle' % envns[0], 'http://schemas.xmlsoap.org/soap/encoding/')
        return env

    def bodycontent(self, method, args, kwargs):
        n = 0
        root = self.method(method)
        for pd in self.param_defs(method):
            if n < len(args):
                value = args[n]
            else:
                value = kwargs.get(pd[0])
            p = self.mkparam(method, pd, value)
            if p is not None:
                root.append(p)
            n += 1

        return root

    def replycontent(self, method, body):
        return body[0].children

    def method(self, method):
        """
        Get the document root.  For I{rpc/(literal|encoded)}, this is the
        name of the method qualifed by the schema tns.
        @param method: A service method.
        @type method: I{service.Method}
        @return: A root element.
        @rtype: L{Element}
        """
        ns = method.soap.input.body.namespace
        if ns[0] is None:
            ns = (
             'ns0', ns[1])
        method = Element(method.name, ns=ns)
        return method


class Encoded(RPC):
    """
    RPC/Encoded (section 5)  binding style.
    """

    def marshaller(self):
        return MxEncoded(self.schema())

    def unmarshaller(self, typed=True):
        """
        Get the appropriate XML decoder.
        @return: Either the (basic|typed) unmarshaller.
        @rtype: L{UmxTyped}
        """
        if typed:
            return UmxEncoded(self.schema())
        else:
            return RPC.unmarshaller(self, typed)