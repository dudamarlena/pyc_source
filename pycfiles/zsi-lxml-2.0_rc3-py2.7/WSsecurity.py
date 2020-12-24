# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZSI/twisted/WSsecurity.py
# Compiled at: 2006-10-25 20:33:21
import sys, time, warnings, sha, base64
from zope.interface import classProvides, implements, Interface
from twisted.python import log, failure
from twisted.web.error import NoResource
from twisted.web.server import NOT_DONE_YET
from twisted.internet import reactor
import twisted.web.http, twisted.web.resource
from ZSI import _get_element_nsuri_name, EvaluateException, ParseException
from ZSI.parse import ParsedSoap
from ZSI.writer import SoapWriter
from ZSI.TC import _get_global_element_declaration as GED
from ZSI import fault
from ZSI.wstools.Namespaces import OASIS, DSIG
from WSresource import DefaultHandlerChain, HandlerChainInterface, WSAddressCallbackHandler, DataHandler, WSAddressHandler
UsernameTokenDec = GED(OASIS.WSSE, 'UsernameToken')
SecurityDec = GED(OASIS.WSSE, 'Security')
SignatureDec = GED(DSIG.BASE, 'Signature')
PasswordDec = GED(OASIS.WSSE, 'Password')
NonceDec = GED(OASIS.WSSE, 'Nonce')
CreatedDec = GED(OASIS.UTILITY, 'Created')
if None in [UsernameTokenDec, SecurityDec, SignatureDec, PasswordDec, NonceDec, CreatedDec]:
    raise ImportError, 'required global element(s) unavailable: %s ' % {(OASIS.WSSE, 'UsernameToken'): UsernameTokenDec, 
       (OASIS.WSSE, 'Security'): SecurityDec, 
       (DSIG.BASE, 'Signature'): SignatureDec, 
       (OASIS.WSSE, 'Password'): PasswordDec, 
       (OASIS.WSSE, 'Nonce'): NonceDec, 
       (OASIS.UTILITY, 'Created'): CreatedDec}

class WSSecurityHandler():
    """Web Services Security: SOAP Message Security 1.0
    
    Class Variables:
        debug -- If True provide more detailed SOAP:Fault information to clients.
    """
    classProvides(HandlerChainInterface)
    debug = True

    @classmethod
    def processRequest(cls, ps, **kw):
        if type(ps) is not ParsedSoap:
            raise TypeError, 'Expecting ParsedSoap instance'
        security = ps.ParseHeaderElements([cls.securityDec])
        for pyobj in security or []:
            for any in pyobj.Any or []:
                if any.typecode is UsernameTokenDec:
                    try:
                        ps = cls.UsernameTokenProfileHandler.processRequest(ps, any)
                    except Exception as ex:
                        if cls.debug:
                            raise
                        raise RuntimeError, 'Unauthorized Username/passphrase combination'

                    continue
                if any.typecode is SignatureDec:
                    try:
                        ps = cls.SignatureHandler.processRequest(ps, any)
                    except Exception as ex:
                        if cls.debug:
                            raise
                        raise RuntimeError, 'Invalid Security Header'

                    continue
                raise RuntimeError, 'WS-Security, Unsupported token %s' % str(any)

        return ps

    @classmethod
    def processResponse(cls, output, **kw):
        return output

    class UsernameTokenProfileHandler:
        """Web Services Security UsernameToken Profile 1.0
        
        Class Variables:
            targetNamespace --
        """
        classProvides(HandlerChainInterface)
        targetNamespace = OASIS.WSSE
        sweepInterval = 300
        nonces = None
        PasswordText = targetNamespace + '#PasswordText'
        PasswordDigest = targetNamespace + '#PasswordDigest'
        passwordCallback = lambda cls, username: None

        @classmethod
        def sweep(cls, index):
            """remove nonces every sweepInterval.
            Parameters:
                index -- remove all nonces up to this index.
            """
            if cls.nonces is None:
                cls.nonces = []
            seconds = cls.sweepInterval
            cls.nonces = cls.nonces[index:]
            reactor.callLater(seconds, cls.sweep, len(cls.nonces))
            return

        @classmethod
        def processRequest(cls, ps, token, **kw):
            """
            Parameters:
                ps -- ParsedSoap instance
                token -- UsernameToken pyclass instance
            """
            if token.typecode is not UsernameTokenDec:
                raise TypeError, 'expecting GED (%s,%s) representation.' % (
                 UsernameTokenDec.nspname, UsernameTokenDec.pname)
            username = token.Username
            password = nonce = timestamp = None
            for any in token.Any or []:
                if any.typecode is PasswordDec:
                    password = any
                    continue
                if any.typecode is NonceTypeDec:
                    nonce = any
                    continue
                if any.typecode is CreatedTypeDec:
                    timestamp = any
                    continue
                raise TypeError, 'UsernameTokenProfileHander unexpected %s' % str(any)

            if password is None:
                raise RuntimeError, 'Unauthorized, no password'
            attrs = getattr(password, password.typecode.attrs_aname, {})
            pwtype = attrs.get('Type', cls.PasswordText)
            if cls.PasswordText is not None and pwtype == cls.PasswordText:
                if password == cls.passwordCallback(username):
                    return ps
                raise RuntimeError, 'Unauthorized, clear text password failed'
            if cls.nonces is None:
                cls.sweep(0)
            if nonce is not None:
                if nonce in cls.nonces:
                    raise RuntimeError, 'Invalid Nonce'
                if created is not None and created < time.gmtime(time.time() - 10):
                    raise RuntimeError, 'UsernameToken created is expired'
                cls.nonces.append(nonce)
            if cls.PasswordDigest is not None and pwtype == cls.PasswordDigest:
                digest = sha.sha()
                for i in (nonce, created, cls.passwordCallback(username)):
                    if i is None:
                        continue
                    digest.update(i)

                if password == base64.encodestring(digest.digest()).strip():
                    return ps
                raise RuntimeError, 'Unauthorized, digest failed'
            raise RuntimeError, 'Unauthorized, contents of UsernameToken unknown'
            return

        @classmethod
        def processResponse(cls, output, **kw):
            return output

    @staticmethod
    def hmac_sha1(xml):
        pass

    class SignatureHandler:
        """Web Services Security UsernameToken Profile 1.0
        """
        digestMethods = {DSIG.BASE + '#sha1': sha.sha}
        signingMethods = {DSIG.BASE + '#hmac-sha1': hmac_sha1}
        canonicalizationMethods = {DSIG.C14N_EXCL: lambda node: Canonicalize(node, unsuppressedPrefixes=[]), 
           DSIG.C14N: lambda node: Canonicalize(node)}

        @classmethod
        def processRequest(cls, ps, signature, **kw):
            """
            Parameters:
                ps -- ParsedSoap instance
                signature -- Signature pyclass instance
            """
            if token.typecode is not SignatureDec:
                raise TypeError, 'expecting GED (%s,%s) representation.' % (
                 SignatureDec.nspname, SignatureDec.pname)
            si = signature.SignedInfo
            si.CanonicalizationMethod
            calgo = si.CanonicalizationMethod.get_attribute_Algorithm()
            for any in si.CanonicalizationMethod.Any:
                pass

            si.Reference
            context = XPath.Context.Context(ps.dom, processContents={'wsu': OASIS.UTILITY})
            exp = XPath.Compile('//*[@wsu:Id="%s"]' % si.Reference.get_attribute_URI())
            nodes = exp.evaluate(context)
            if len(nodes) != 1:
                raise RuntimeError, 'A SignedInfo Reference must refer to one node %s.' % si.Reference.get_attribute_URI()
            try:
                xml = cls.canonicalizeMethods[calgo](nodes[0])
            except IndexError:
                raise RuntimeError, 'Unsupported canonicalization algorithm'

            try:
                digest = cls.digestMethods[salgo]
            except IndexError:
                raise RuntimeError, 'unknown digestMethods Algorithm'

            digestValue = base64.encodestring(digest(xml).digest()).strip()
            if si.Reference.DigestValue != digestValue:
                raise RuntimeError, 'digest does not match'
            if si.Reference.Transforms:
                pass
            signature.KeyInfo
            signature.KeyInfo.KeyName
            signature.KeyInfo.KeyValue
            signature.KeyInfo.RetrievalMethod
            signature.KeyInfo.X509Data
            signature.KeyInfo.PGPData
            signature.KeyInfo.SPKIData
            signature.KeyInfo.MgmtData
            signature.KeyInfo.Any
            signature.Object
            signature.SignatureValue
            si.SignatureMethod
            salgo = si.SignatureMethod.get_attribute_Algorithm()
            if si.SignatureMethod.HMACOutputLength:
                pass
            for any in si.SignatureMethod.Any:
                pass

            exp = XPath.Compile('//child::*[attribute::URI = "%s"]/..' % si.Reference.get_attribute_URI())
            nodes = exp.evaluate(context)
            if len(nodes) != 1:
                raise RuntimeError, 'A SignedInfo Reference must refer to one node %s.' % si.Reference.get_attribute_URI()
            try:
                xml = cls.canonicalizeMethods[calgo](nodes[0])
            except IndexError:
                raise RuntimeError, 'Unsupported canonicalization algorithm'

        @classmethod
        def processResponse(cls, output, **kw):
            return output

    class X509TokenProfileHandler:
        """Web Services Security UsernameToken Profile 1.0
        """
        targetNamespace = DSIG.BASE
        singleCertificate = targetNamespace + '#X509v3'
        certificatePath = targetNamespace + '#X509PKIPathv1'
        setCerticatesCRLs = targetNamespace + '#PKCS7'

        @classmethod
        def processRequest(cls, ps, signature, **kw):
            return ps


class WSSecurityHandlerChainFactory():
    protocol = DefaultHandlerChain

    @classmethod
    def newInstance(cls):
        return cls.protocol(WSAddressCallbackHandler, DataHandler, WSSecurityHandler, WSAddressHandler())