# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ely/codebase/refstis/refstis/SignStsciRequest.py
# Compiled at: 2016-06-01 14:00:53
usexml = True
try:
    import xmlsec, libxml2
except ImportError:
    usexml = False

try:
    from urllib.request import Request
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
    from urllib2 import Request

from six.moves.urllib.request import urlopen
import warnings, re

class SignStsciRequest:

    def __init__(self):
        self.init()

    @staticmethod
    def init():
        global usexml
        if not usexml:
            return
        else:
            try:
                libxml2.initParser()
                libxml2.substituteEntitiesDefault(1)
                assert xmlsec.init() >= 0, 'Error: xmlsec initialization failed.'
                assert xmlsec.checkVersion() == 1, 'Error: loaded xmlsec library version is not compatible.'
                assert xmlsec.cryptoAppInit(None) >= 0, 'Error: crypto initialization failed.'
                assert xmlsec.cryptoInit() >= 0, 'Error: xmlsec-crypto initialization failed.'
            except:
                usexml = False

            return

    @staticmethod
    def signRequest(file, request, dtd='http://dmswww.stsci.edu/dtd/sso/distribution.dtd', cgi='https://archive.stsci.edu/cgi-bin/dads.cgi', mission='HST'):
        global usexml
        if usexml:
            try:
                keysmngr = xmlsec.KeysMngr()
                if keysmngr is None:
                    raise RuntimeError('Error: failed to create keys manager.')
                if xmlsec.cryptoAppDefaultKeysMngrInit(keysmngr) < 0:
                    keysmngr.destroy()
                    raise RuntimeError('Error: failed to initialize keys manager.')
                key = xmlsec.cryptoAppKeyLoad(filename=file, pwd=None, format=xmlsec.KeyDataFormatPem, pwdCallback=None, pwdCallbackCtx=None)
                if xmlsec.cryptoAppDefaultKeysMngrAdoptKey(keysmngr, key) < 0:
                    keysmngr.destroy()
                    raise RuntimeError('Error: failed to load key into keys manager')
                dsig_ctx = xmlsec.DSigCtx(keysmngr)
                pat = re.compile('(^.*<!DOCTYPE.*distributionRequest[^>]*SYSTEM[ \t]*")([^"]*)("[^>]*>.*$)', re.DOTALL)
                m = pat.match(request)
                request = m.group(1) + dtd + m.group(3)
                ctxt = libxml2.createMemoryParserCtxt(request, len(request))
                ctxt.validate(1)
                ctxt.parseDocument()
                doc = ctxt.doc()
                if doc is None or doc.getRootElement() is None:
                    keysmngr.destroy()
                    raise RuntimeError('Error: unable to parse XML data')
                node = xmlsec.findNode(doc.getRootElement(), xmlsec.NodeSignature, xmlsec.DSigNs)
                if node is None:
                    fragment = libxml2.parseDoc('<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">\n<SignedInfo>\n  <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>\n  <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>\n  <Reference URI="#distributionRequest">\n    <Transforms>\n      <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>\n      <Transform Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#WithComments" />\n    </Transforms>\n    <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>\n    <DigestValue></DigestValue>\n  </Reference>\n</SignedInfo>\n<SignatureValue></SignatureValue>\n<KeyInfo>\n <KeyValue><RSAKeyValue>\n  <Modulus></Modulus>\n  <Exponent></Exponent>\n </RSAKeyValue></KeyValue>\n</KeyInfo>\n</Signature>\n')
                    fragment = fragment.getRootElement()
                    ctxt = doc.xpathNewContext()
                    nodeList = ctxt.xpathEval('/distributionRequest')
                    for child in nodeList:
                        child.addChild(fragment)
                        if child.prop('Id') == None:
                            child.setProp('Id', 'distributionRequest')

                    node = xmlsec.findNode(doc.getRootElement(), xmlsec.NodeSignature, xmlsec.DSigNs)
                ctxt = doc.xpathNewContext()
                nodeList = ctxt.xpathEval('//requester')
                for child in nodeList:
                    child.unsetProp('archivePassword')

                nodeList = ctxt.xpathEval('//ftp')
                for child in nodeList:
                    if child.hasProp('loginPassword'):
                        child.unsetProp('loginPassword')
                        warnings.warn('ftp password is not allowed in user requests.')

                status = dsig_ctx.sign(node)
                output = str(doc)
                doc.freeDoc()
                keysmngr.destroy()
                if status < 0:
                    raise RuntimeError('Error: signature failed')
                return output
            except:
                usexml = False
                return signRequest(file, request, dtd, cgi)

        else:
            values = {'request': request, 'privatekey': open(file).read(), 'mission': mission}
            data = urlencode(values)
            req = Request(url=cgi, data=data)
            f = urlopen(req)
            return f.read()
        return

    def __del__(self):
        self.cleanup()

    @staticmethod
    def cleanup():
        if usexml:
            xmlsec.cryptoShutdown()
            xmlsec.cryptoAppShutdown()
            xmlsec.shutdown()
            libxml2.cleanupParser()