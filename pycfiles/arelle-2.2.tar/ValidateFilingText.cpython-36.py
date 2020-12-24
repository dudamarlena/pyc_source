# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\ValidateFilingText.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 44883 bytes
"""
Created on Oct 17, 2010

@author: Mark V Systems Limited
(c) Copyright 2010 Mark V Systems Limited, All rights reserved.
"""
from lxml.etree import XML, DTD, SubElement, _ElementTree, _Comment, _ProcessingInstruction, XMLSyntaxError, XMLParser
import os, re, io
from arelle.XbrlConst import ixbrlAll, xhtml
from arelle.XmlUtil import setXmlns, xmlstring
from arelle.ModelObject import ModelObject
from arelle.UrlUtil import isHttpUrl, scheme
XMLdeclaration = re.compile('<\\?xml.*\\?>', re.DOTALL)
XMLpattern = re.compile('.*(<|&lt;|&#x3C;|&#60;)[A-Za-z_]+[A-Za-z0-9_:]*[^>]*(/>|>|&gt;|/&gt;).*', re.DOTALL)
CDATApattern = re.compile('<!\\[CDATA\\[(.+)\\]\\]')
docCheckPattern = re.compile('&\\w+;|[^0-9A-Za-z`~!@#$%&\\*\\(\\)\\.\\-+ \\[\\]\\{\\}\\|\\\\:;\\"\'<>,_?/=\\t\\n\\r\\f]')
namedEntityPattern = re.compile('&[_A-Za-zÀ-ÖØ-öø-ÿĀ-˿Ͱ-ͽͿ-\u1fff\u200c-\u200d⁰-\u218fⰀ-\u2fef、-\ud7ff豈-\ufdcfﷰ-�][_\\-\\.:·A-Za-z0-9À-ÖØ-öø-ÿĀ-˿Ͱ-ͽͿ-\u1fff\u200c-\u200d⁰-\u218fⰀ-\u2fef、-\ud7ff豈-\ufdcfﷰ-�̀-ͯ‿-⁀]*;')
edbodyDTD = None
isInlineDTD = None
xhtmlEntities = {'&nbsp;':'&#160;', 
 '&iexcl;':'&#161;', 
 '&cent;':'&#162;', 
 '&pound;':'&#163;', 
 '&curren;':'&#164;', 
 '&yen;':'&#165;', 
 '&brvbar;':'&#166;', 
 '&sect;':'&#167;', 
 '&uml;':'&#168;', 
 '&copy;':'&#169;', 
 '&ordf;':'&#170;', 
 '&laquo;':'&#171;', 
 '&not;':'&#172;', 
 '&shy;':'&#173;', 
 '&reg;':'&#174;', 
 '&macr;':'&#175;', 
 '&deg;':'&#176;', 
 '&plusmn;':'&#177;', 
 '&sup2;':'&#178;', 
 '&sup3;':'&#179;', 
 '&acute;':'&#180;', 
 '&micro;':'&#181;', 
 '&para;':'&#182;', 
 '&middot;':'&#183;', 
 '&cedil;':'&#184;', 
 '&sup1;':'&#185;', 
 '&ordm;':'&#186;', 
 '&raquo;':'&#187;', 
 '&frac14;':'&#188;', 
 '&frac12;':'&#189;', 
 '&frac34;':'&#190;', 
 '&iquest;':'&#191;', 
 '&Agrave;':'&#192;', 
 '&Aacute;':'&#193;', 
 '&Acirc;':'&#194;', 
 '&Atilde;':'&#195;', 
 '&Auml;':'&#196;', 
 '&Aring;':'&#197;', 
 '&AElig;':'&#198;', 
 '&Ccedil;':'&#199;', 
 '&Egrave;':'&#200;', 
 '&Eacute;':'&#201;', 
 '&Ecirc;':'&#202;', 
 '&Euml;':'&#203;', 
 '&Igrave;':'&#204;', 
 '&Iacute;':'&#205;', 
 '&Icirc;':'&#206;', 
 '&Iuml;':'&#207;', 
 '&ETH;':'&#208;', 
 '&Ntilde;':'&#209;', 
 '&Ograve;':'&#210;', 
 '&Oacute;':'&#211;', 
 '&Ocirc;':'&#212;', 
 '&Otilde;':'&#213;', 
 '&Ouml;':'&#214;', 
 '&times;':'&#215;', 
 '&Oslash;':'&#216;', 
 '&Ugrave;':'&#217;', 
 '&Uacute;':'&#218;', 
 '&Ucirc;':'&#219;', 
 '&Uuml;':'&#220;', 
 '&Yacute;':'&#221;', 
 '&THORN;':'&#222;', 
 '&szlig;':'&#223;', 
 '&agrave;':'&#224;', 
 '&aacute;':'&#225;', 
 '&acirc;':'&#226;', 
 '&atilde;':'&#227;', 
 '&auml;':'&#228;', 
 '&aring;':'&#229;', 
 '&aelig;':'&#230;', 
 '&ccedil;':'&#231;', 
 '&egrave;':'&#232;', 
 '&eacute;':'&#233;', 
 '&ecirc;':'&#234;', 
 '&euml;':'&#235;', 
 '&igrave;':'&#236;', 
 '&iacute;':'&#237;', 
 '&icirc;':'&#238;', 
 '&iuml;':'&#239;', 
 '&eth;':'&#240;', 
 '&ntilde;':'&#241;', 
 '&ograve;':'&#242;', 
 '&oacute;':'&#243;', 
 '&ocirc;':'&#244;', 
 '&otilde;':'&#245;', 
 '&ouml;':'&#246;', 
 '&divide;':'&#247;', 
 '&oslash;':'&#248;', 
 '&ugrave;':'&#249;', 
 '&uacute;':'&#250;', 
 '&ucirc;':'&#251;', 
 '&uuml;':'&#252;', 
 '&yacute;':'&#253;', 
 '&thorn;':'&#254;', 
 '&yuml;':'&#255;', 
 '&quot;':'&#34;', 
 '&amp;':'&#38;#38;', 
 '&lt;':'&#38;#60;', 
 '&gt;':'&#62;', 
 '&apos;':'&#39;', 
 '&OElig;':'&#338;', 
 '&oelig;':'&#339;', 
 '&Scaron;':'&#352;', 
 '&scaron;':'&#353;', 
 '&Yuml;':'&#376;', 
 '&circ;':'&#710;', 
 '&tilde;':'&#732;', 
 '&ensp;':'&#8194;', 
 '&emsp;':'&#8195;', 
 '&thinsp;':'&#8201;', 
 '&zwnj;':'&#8204;', 
 '&zwj;':'&#8205;', 
 '&lrm;':'&#8206;', 
 '&rlm;':'&#8207;', 
 '&ndash;':'&#8211;', 
 '&mdash;':'&#8212;', 
 '&lsquo;':'&#8216;', 
 '&rsquo;':'&#8217;', 
 '&sbquo;':'&#8218;', 
 '&ldquo;':'&#8220;', 
 '&rdquo;':'&#8221;', 
 '&bdquo;':'&#8222;', 
 '&dagger;':'&#8224;', 
 '&Dagger;':'&#8225;', 
 '&permil;':'&#8240;', 
 '&lsaquo;':'&#8249;', 
 '&rsaquo;':'&#8250;', 
 '&euro;':'&#8364;', 
 '&fnof;':'&#402;', 
 '&Alpha;':'&#913;', 
 '&Beta;':'&#914;', 
 '&Gamma;':'&#915;', 
 '&Delta;':'&#916;', 
 '&Epsilon;':'&#917;', 
 '&Zeta;':'&#918;', 
 '&Eta;':'&#919;', 
 '&Theta;':'&#920;', 
 '&Iota;':'&#921;', 
 '&Kappa;':'&#922;', 
 '&Lambda;':'&#923;', 
 '&Mu;':'&#924;', 
 '&Nu;':'&#925;', 
 '&Xi;':'&#926;', 
 '&Omicron;':'&#927;', 
 '&Pi;':'&#928;', 
 '&Rho;':'&#929;', 
 '&Sigma;':'&#931;', 
 '&Tau;':'&#932;', 
 '&Upsilon;':'&#933;', 
 '&Phi;':'&#934;', 
 '&Chi;':'&#935;', 
 '&Psi;':'&#936;', 
 '&Omega;':'&#937;', 
 '&alpha;':'&#945;', 
 '&beta;':'&#946;', 
 '&gamma;':'&#947;', 
 '&delta;':'&#948;', 
 '&epsilon;':'&#949;', 
 '&zeta;':'&#950;', 
 '&eta;':'&#951;', 
 '&theta;':'&#952;', 
 '&iota;':'&#953;', 
 '&kappa;':'&#954;', 
 '&lambda;':'&#955;', 
 '&mu;':'&#956;', 
 '&nu;':'&#957;', 
 '&xi;':'&#958;', 
 '&omicron;':'&#959;', 
 '&pi;':'&#960;', 
 '&rho;':'&#961;', 
 '&sigmaf;':'&#962;', 
 '&sigma;':'&#963;', 
 '&tau;':'&#964;', 
 '&upsilon;':'&#965;', 
 '&phi;':'&#966;', 
 '&chi;':'&#967;', 
 '&psi;':'&#968;', 
 '&omega;':'&#969;', 
 '&thetasym;':'&#977;', 
 '&upsih;':'&#978;', 
 '&piv;':'&#982;', 
 '&bull;':'&#8226;', 
 '&hellip;':'&#8230;', 
 '&prime;':'&#8242;', 
 '&Prime;':'&#8243;', 
 '&oline;':'&#8254;', 
 '&frasl;':'&#8260;', 
 '&weierp;':'&#8472;', 
 '&image;':'&#8465;', 
 '&real;':'&#8476;', 
 '&trade;':'&#8482;', 
 '&alefsym;':'&#8501;', 
 '&larr;':'&#8592;', 
 '&uarr;':'&#8593;', 
 '&rarr;':'&#8594;', 
 '&darr;':'&#8595;', 
 '&harr;':'&#8596;', 
 '&crarr;':'&#8629;', 
 '&lArr;':'&#8656;', 
 '&uArr;':'&#8657;', 
 '&rArr;':'&#8658;', 
 '&dArr;':'&#8659;', 
 '&hArr;':'&#8660;', 
 '&forall;':'&#8704;', 
 '&part;':'&#8706;', 
 '&exist;':'&#8707;', 
 '&empty;':'&#8709;', 
 '&nabla;':'&#8711;', 
 '&isin;':'&#8712;', 
 '&notin;':'&#8713;', 
 '&ni;':'&#8715;', 
 '&prod;':'&#8719;', 
 '&sum;':'&#8721;', 
 '&minus;':'&#8722;', 
 '&lowast;':'&#8727;', 
 '&radic;':'&#8730;', 
 '&prop;':'&#8733;', 
 '&infin;':'&#8734;', 
 '&ang;':'&#8736;', 
 '&and;':'&#8743;', 
 '&or;':'&#8744;', 
 '&cap;':'&#8745;', 
 '&cup;':'&#8746;', 
 '&int;':'&#8747;', 
 '&there;':'&#8756;', 
 '&sim;':'&#8764;', 
 '&cong;':'&#8773;', 
 '&asymp;':'&#8776;', 
 '&ne;':'&#8800;', 
 '&equiv;':'&#8801;', 
 '&le;':'&#8804;', 
 '&ge;':'&#8805;', 
 '&sub;':'&#8834;', 
 '&sup;':'&#8835;', 
 '&nsub;':'&#8836;', 
 '&sube;':'&#8838;', 
 '&supe;':'&#8839;', 
 '&oplus;':'&#8853;', 
 '&otimes;':'&#8855;', 
 '&perp;':'&#8869;', 
 '&sdot;':'&#8901;', 
 '&lceil;':'&#8968;', 
 '&rceil;':'&#8969;', 
 '&lfloor;':'&#8970;', 
 '&rfloor;':'&#8971;', 
 '&lang;':'&#9001;', 
 '&rang;':'&#9002;', 
 '&loz;':'&#9674;', 
 '&spades;':'&#9824;', 
 '&clubs;':'&#9827;', 
 '&hearts;':'&#9829;', 
 '&diams;':'&#9830;'}
efmBlockedInlineHtmlElements = {
 'acronym', 'area', 'base', 'bdo', 'button', 'cite', 'col', 'colgroup',
 'dd', 'del', 'embed', 'fieldset', 'form', 'input', 'ins', 'label', 'legend',
 'map', 'object', 'option', 'param', 'q', 'script', 'select', 'style',
 'textarea'}
efmBlockedInlineHtmlElementAttributes = {'a':('name', ), 
 'body':('link', ), 
 'html':('lang', ), 
 'link':('rel', 'rev')}

def checkfile(modelXbrl, filepath):
    result = []
    lineNum = 1
    foundXmlDeclaration = False
    isEFM = modelXbrl.modelManager.disclosureSystem.validationType == 'EFM'
    file, encoding = modelXbrl.fileSource.file(filepath)
    parserResults = {}

    class checkFileType(object):

        def start(self, tag, attr):
            parserResults['rootIsTestcase'] = tag.rpartition('}')[2] in ('testcases',
                                                                         'documentation',
                                                                         'testSuite',
                                                                         'testcase',
                                                                         'testSet')

        def end(self, tag):
            pass

        def data(self, data):
            pass

        def close(self):
            pass

    _parser = XMLParser(target=(checkFileType()))
    _isTestcase = False
    with file as (f):
        while True:
            line = f.readline()
            if line == '':
                break
            for match in docCheckPattern.finditer(line):
                text = match.group()
                if text.startswith('&'):
                    if text not in xhtmlEntities:
                        modelXbrl.error(('EFM.5.02.02.06', 'GFM.1.01.02'), (_('Disallowed entity code %(text)s in file %(file)s line %(line)s column %(column)s')),
                          modelDocument=filepath,
                          text=text,
                          file=(os.path.basename(filepath)),
                          line=lineNum,
                          column=(match.start()))
                else:
                    if isEFM and not _isTestcase:
                        if len(text) == 1:
                            modelXbrl.error('EFM.5.02.01.01', (_("Disallowed character '%(text)s' (%(unicodeIndex)s) in file %(file)s at line %(line)s col %(column)s")),
                              modelDocument=filepath,
                              text=text,
                              unicodeIndex=('U+{:04X}'.format(ord(text))),
                              file=(os.path.basename(filepath)),
                              line=lineNum,
                              column=(match.start()))
                        else:
                            modelXbrl.error('EFM.5.02.01.01', (_("Disallowed character '%(text)s' in file %(file)s at line %(line)s col %(column)s")),
                              modelDocument=filepath,
                              text=text,
                              file=(os.path.basename(filepath)),
                              line=lineNum,
                              column=(match.start()))

            if lineNum == 1:
                xmlDeclarationMatch = XMLdeclaration.search(line)
                if xmlDeclarationMatch:
                    start, end = xmlDeclarationMatch.span()
                    line = line[0:start] + line[end:]
                    foundXmlDeclaration = True
            if _parser:
                _parser.feed(line.encode('utf-8', 'ignore'))
                if 'rootIsTestcase' in parserResults:
                    _isTestcase = parserResults['rootIsTestcase']
                    _parser = None
            result.append(line)
            lineNum += 1

    result = ''.join(result)
    if not foundXmlDeclaration:
        xmlDeclarationMatch = XMLdeclaration.search(result)
        if xmlDeclarationMatch:
            start, end = xmlDeclarationMatch.span()
            result = result[0:start] + result[end:]
            foundXmlDeclaration = True
    return (
     io.StringIO(initial_value=result), encoding)


ModelDocumentTypeINLINEXBRL = None

def loadDTD(modelXbrl):
    global ModelDocumentTypeINLINEXBRL
    global edbodyDTD
    global isInlineDTD
    if ModelDocumentTypeINLINEXBRL is None:
        from arelle.ModelDocument import Type
        ModelDocumentTypeINLINEXBRL = Type.INLINEXBRL
    _isInline = modelXbrl.modelDocument.type == ModelDocumentTypeINLINEXBRL
    if isInlineDTD is None or isInlineDTD != _isInline:
        isInlineDTD = _isInline
        with open(os.path.join(modelXbrl.modelManager.cntlr.configDir, 'xhtml1-strict-ix.dtd' if _isInline else 'edbody.dtd')) as (fh):
            edbodyDTD = DTD(fh)


def removeEntities(text):
    """ ARELLE-128
    entitylessText = []
    findAt = 0
    while (True):
        entityStart = text.find('&',findAt)
        if entityStart == -1: break
        entityEnd = text.find(';',entityStart)
        if entityEnd == -1: break
        entitylessText.append(text[findAt:entityStart])
        findAt = entityEnd + 1
    entitylessText.append(text[findAt:])
    return ''.join(entitylessText)
    """
    return namedEntityPattern.sub('', text).replace('&', '&amp;')


def validateTextBlockFacts(modelXbrl):
    loadDTD(modelXbrl)
    checkedGraphicsFiles = set()
    if isInlineDTD:
        htmlBodyTemplate = '<body><div>\n{0}\n</div></body>\n'
    else:
        htmlBodyTemplate = '<body>\n{0}\n</body>\n'
    _xhtmlNs = '{{{}}}'.format(xhtml)
    _xhtmlNsLen = len(_xhtmlNs)
    for f1 in modelXbrl.facts:
        concept = f1.concept
        if f1.xsiNil != 'true' and concept is not None and concept.isTextBlock and XMLpattern.match(f1.value):
            for match in namedEntityPattern.finditer(f1.value):
                entity = match.group()
                if entity not in xhtmlEntities:
                    modelXbrl.error(('EFM.6.05.16', 'GFM.1.2.15'), (_('Fact %(fact)s contextID %(contextID)s has disallowed entity %(entity)s')),
                      modelObject=f1,
                      fact=(f1.qname),
                      contextID=(f1.contextID),
                      entity=entity,
                      error=entity)

            for xmltext in [f1.value] + CDATApattern.findall(f1.value):
                xmlBodyWithoutEntities = htmlBodyTemplate.format(removeEntities(xmltext))
                try:
                    textblockXml = XML(xmlBodyWithoutEntities)
                    if not edbodyDTD.validate(textblockXml):
                        errors = edbodyDTD.error_log.filter_from_errors()
                        htmlError = any(e.type_name in ('DTD_INVALID_CHILD', 'DTD_UNKNOWN_ATTRIBUTE') for e in errors)
                        modelXbrl.error(('EFM.6.05.16' if htmlError else ('EFM.6.05.15.dtdError',
                                                                          'GFM.1.02.14')), (_('Fact %(fact)s contextID %(contextID)s has text which causes the XML error %(error)s')),
                          modelObject=f1,
                          fact=(f1.qname),
                          contextID=(f1.contextID),
                          error=(', '.join(e.message for e in errors)),
                          messageCodes=('EFM.6.05.16', 'EFM.6.05.15.dtdError', 'GFM.1.02.14'))
                    for elt in textblockXml.iter():
                        eltTag = elt.tag
                        if isinstance(elt, ModelObject):
                            if elt.namespaceURI == xhtml:
                                eltTag = elt.localName
                        if isinstance(elt, (_ElementTree, _Comment, _ProcessingInstruction)):
                            continue
                        else:
                            eltTag = elt.tag
                        if eltTag.startswith(_xhtmlNs):
                            eltTag = eltTag[_xhtmlNsLen:]
                        if isInlineDTD:
                            if eltTag in efmBlockedInlineHtmlElements:
                                modelXbrl.error('EFM.5.02.05.disallowedElement', (_('%(validatedObjectLabel)s has disallowed element <%(element)s>')),
                                  modelObject=elt,
                                  validatedObjectLabel=(f1.qname),
                                  element=eltTag)
                            for attrTag, attrValue in elt.items():
                                if isInlineDTD:
                                    if attrTag in efmBlockedInlineHtmlElementAttributes.get(eltTag, ()):
                                        modelXbrl.error('EFM.5.02.05.disallowedAttribute', (_('%(validatedObjectLabel)s has disallowed attribute on element <%(element)s>: %(attribute)s="%(value)s"')),
                                          modelObject=elt,
                                          validatedObjectLabel=validatedObjectLabel,
                                          element=eltTag,
                                          attribute=attrTag,
                                          value=attrValue)
                                    if attrTag == 'href' and eltTag == 'a' or attrTag == 'src' and eltTag == 'img':
                                        if 'javascript:' in attrValue:
                                            modelXbrl.error('EFM.6.05.16.activeContent', (_("Fact %(fact)s of context %(contextID)s has javascript in '%(attribute)s' for <%(element)s>")),
                                              modelObject=f1,
                                              fact=(f1.qname),
                                              contextID=(f1.contextID),
                                              attribute=attrTag,
                                              element=eltTag)
                                        else:
                                            if attrValue.startswith('http://www.sec.gov/Archives/edgar/data/'):
                                                if eltTag == 'a':
                                                    pass
                                        if scheme(attrValue) in ('http', 'https', 'ftp'):
                                            modelXbrl.error('EFM.6.05.16.externalReference', (_("Fact %(fact)s of context %(contextID)s has an invalid external reference in '%(attribute)s' for <%(element)s>")),
                                              modelObject=f1,
                                              fact=(f1.qname),
                                              contextID=(f1.contextID),
                                              attribute=attrTag,
                                              element=eltTag)
                                        if attrTag == 'src':
                                            if attrValue not in checkedGraphicsFiles:
                                                if scheme(attrValue) == 'data':
                                                    modelXbrl.error('EFM.6.05.16.graphicDataUrl', (_("Fact %(fact)s of context %(contextID)s references a graphics data URL which isn't accepted '%(attribute)s' for <%(element)s>")),
                                                      modelObject=f1,
                                                      fact=(f1.qname),
                                                      contextID=(f1.contextID),
                                                      attribute=(attrValue[:32]),
                                                      element=eltTag)
                                                else:
                                                    if attrValue.lower()[-4:] not in ('.jpg',
                                                                                      '.gif'):
                                                        modelXbrl.error('EFM.6.05.16.graphicFileType', (_("Fact %(fact)s of context %(contextID)s references a graphics file which isn't .gif or .jpg '%(attribute)s' for <%(element)s>")),
                                                          modelObject=f1,
                                                          fact=(f1.qname),
                                                          contextID=(f1.contextID),
                                                          attribute=attrValue,
                                                          element=eltTag)
                                                    else:
                                                        try:
                                                            if validateGraphicFile(f1, attrValue) != attrValue.lower()[-3:]:
                                                                modelXbrl.error('EFM.6.05.16.graphicFileContent', (_("Fact %(fact)s of context %(contextID)s references a graphics file which doesn't have expected content '%(attribute)s' for <%(element)s>")),
                                                                  modelObject=f1,
                                                                  fact=(f1.qname),
                                                                  contextID=(f1.contextID),
                                                                  attribute=attrValue,
                                                                  element=eltTag)
                                                        except IOError as err:
                                                            modelXbrl.error('EFM.6.05.16.graphicFileError', (_("Fact %(fact)s of context %(contextID)s references a graphics file which isn't openable '%(attribute)s' for <%(element)s>, error: %(error)s")),
                                                              modelObject=f1,
                                                              fact=(f1.qname),
                                                              contextID=(f1.contextID),
                                                              attribute=attrValue,
                                                              element=eltTag,
                                                              error=err)

                                            checkedGraphicsFiles.add(attrValue)

                            if eltTag == 'table' and any(a is not None for a in elt.iterancestors('table')):
                                modelXbrl.error('EFM.6.05.16.nestedTable', (_('Fact %(fact)s of context %(contextID)s has nested <table> elements.')),
                                  modelObject=f1,
                                  fact=(f1.qname),
                                  contextID=(f1.contextID))

                except (XMLSyntaxError,
                 UnicodeDecodeError) as err:
                    modelXbrl.error(('EFM.6.05.15', 'GFM.1.02.14'), (_('Fact %(fact)s contextID %(contextID)s has text which causes the XML error %(error)s')),
                      modelObject=f1,
                      fact=(f1.qname),
                      contextID=(f1.contextID),
                      error=err)

                checkedGraphicsFiles.clear()


def copyHtml(sourceXml, targetHtml):
    for sourceChild in sourceXml.iterchildren():
        targetChild = SubElement(targetHtml, sourceChild.localName if sourceChild.namespaceURI == xhtml else sourceChild.tag)
        for attrTag, attrValue in sourceChild.items():
            targetChild.set('lang' if attrTag == '{http://www.w3.org/XML/1998/namespace}lang' else attrTag, attrValue)

        copyHtml(sourceChild, targetChild)


def validateFootnote(modelXbrl, footnote):
    loadDTD(modelXbrl)
    validatedObjectLabel = _('Footnote {}').format(footnote.get('{http://www.w3.org/1999/xlink}label'))
    try:
        footnoteHtml = XML('<body/>')
        copyHtml(footnote, footnoteHtml)
        if not edbodyDTD.validate(footnoteHtml):
            modelXbrl.error('EFM.6.05.34.dtdError', (_('%(validatedObjectLabel)s causes the XML error %(error)s')),
              modelObject=footnote,
              validatedObjectLabel=validatedObjectLabel,
              error=(', '.join(e.message for e in edbodyDTD.error_log.filter_from_errors())))
        validateHtmlContent(modelXbrl, footnote, footnoteHtml, validatedObjectLabel, 'EFM.6.05.34.')
    except (XMLSyntaxError, UnicodeDecodeError) as err:
        modelXbrl.error('EFM.6.05.34', (_('%(validatedObjectLabel)s causes the XML error %(error)s')),
          modelObject=footnote,
          validatedObjectLabel=validatedObjectLabel,
          error=(edbodyDTD.error_log.filter_from_errors()))


def validateHtmlContent(modelXbrl, referenceElt, htmlEltTree, validatedObjectLabel, messageCodePrefix, isInline=False):
    checkedGraphicsFiles = set()
    _xhtmlNs = '{{{}}}'.format(xhtml)
    _xhtmlNsLen = len(_xhtmlNs)
    _tableTags = ('table', _xhtmlNs + 'table')
    _anchorAncestorTags = set(_xhtmlNs + tag for tag in ('html', 'body', 'div'))
    for elt in htmlEltTree.iter():
        if isinstance(elt, ModelObject):
            if elt.namespaceURI == xhtml:
                eltTag = elt.localName
            else:
                if isinstance(elt, (_ElementTree, _Comment, _ProcessingInstruction)):
                    continue
                else:
                    eltTag = elt.tag
                if eltTag.startswith(_xhtmlNs):
                    eltTag = eltTag[_xhtmlNsLen:]
            if isInline:
                if eltTag in efmBlockedInlineHtmlElements:
                    modelXbrl.error('EFM.5.02.05.disallowedElement', (_('%(validatedObjectLabel)s has disallowed element <%(element)s>')),
                      modelObject=elt,
                      validatedObjectLabel=validatedObjectLabel,
                      element=eltTag)
                if eltTag == 'a' and 'href' not in elt.keys() and any(a.tag not in _anchorAncestorTags for a in elt.iterancestors()):
                    modelXbrl.warning('EFM.5.02.05.anchorElementPosition', (_('If element <a> does not have attribute @href, it should not have any ancestors other than html, body, or div.  Disallowed ancestors: %(disallowedAncestors)s')),
                      modelObject=elt,
                      disallowedAncestors=(', '.join(a.tag.rpartition('}')[2] for a in elt.iterancestors() if a.tag not in _anchorAncestorTags)))
            for attrTag, attrValue in elt.items():
                if isInline:
                    if attrTag in efmBlockedInlineHtmlElementAttributes.get(eltTag, ()):
                        modelXbrl.error('EFM.5.02.05.disallowedAttribute', (_('%(validatedObjectLabel)s has disallowed attribute on element <%(element)s>: %(attribute)s="%(value)s"')),
                          modelObject=elt,
                          validatedObjectLabel=validatedObjectLabel,
                          element=eltTag,
                          attribute=attrTag,
                          value=attrValue)
                    else:
                        if attrTag == '{http://www.w3.org/XML/1998/namespace}base':
                            modelXbrl.error('EFM.5.02.05.xmlBaseDisallowed', (_('%(validatedObjectLabel)s has disallowed attribute on element <%(element)s>: xml:base="%(value)s"')),
                              modelObject=elt,
                              validatedObjectLabel=validatedObjectLabel,
                              element=eltTag,
                              value=attrValue)
                        else:
                            if attrTag == '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation':
                                modelXbrl.warning('EFM.5.02.05.schemaLocationDisallowed', (_('%(validatedObjectLabel)s has disallowed attribute on element <%(element)s>: xsi:schemaLocation="%(value)s"')),
                                  modelObject=elt,
                                  validatedObjectLabel=validatedObjectLabel,
                                  element=eltTag,
                                  value=attrValue)
                    if attrTag == 'href' and eltTag == 'a' or attrTag == 'src' and eltTag == 'img':
                        if 'javascript:' in attrValue:
                            modelXbrl.error((messageCodePrefix + 'activeContent'), (_("%(validatedObjectLabel)s has javascript in '%(attribute)s' for <%(element)s>")),
                              modelObject=elt,
                              validatedObjectLabel=validatedObjectLabel,
                              attribute=attrTag,
                              element=eltTag,
                              messageCodes=('EFM.6.05.34.activeContent', 'EFM.5.02.05.activeContent'))
                        elif attrValue.startswith('http://www.sec.gov/Archives/edgar/data/'):
                            if eltTag == 'a':
                                pass
                        else:
                            if scheme(attrValue) in ('http', 'https', 'ftp'):
                                modelXbrl.error((messageCodePrefix + 'externalReference'), (_("%(validatedObjectLabel)s has an invalid external reference in '%(attribute)s' for <%(element)s>: %(value)s")),
                                  modelObject=elt,
                                  validatedObjectLabel=validatedObjectLabel,
                                  attribute=attrTag,
                                  element=eltTag,
                                  value=attrValue,
                                  messageCodes=('EFM.6.05.34.externalReference', 'EFM.5.02.05.externalReference'))
                            if attrTag == 'src':
                                if attrValue not in checkedGraphicsFiles:
                                    if scheme(attrValue) == 'data':
                                        modelXbrl.error((messageCodePrefix + 'graphicDataUrl'), (_("%(validatedObjectLabel)s references a graphics data URL which isn't accepted '%(attribute)s' for <%(element)s>")),
                                          modelObject=elt,
                                          validatedObjectLabel=validatedObjectLabel,
                                          attribute=(attrValue[:32]),
                                          element=eltTag)
                                    else:
                                        if attrValue.lower()[-4:] not in ('.jpg', '.gif'):
                                            modelXbrl.error((messageCodePrefix + 'graphicFileType'), (_("%(validatedObjectLabel)s references a graphics file which isn't .gif or .jpg '%(attribute)s' for <%(element)s>")),
                                              modelObject=elt,
                                              validatedObjectLabel=validatedObjectLabel,
                                              attribute=attrValue,
                                              element=eltTag,
                                              messageCodes=('EFM.6.05.34.graphicFileType',
                                                            'EFM.5.02.05.graphicFileType'))
                                        else:
                                            try:
                                                if validateGraphicFile(referenceElt, attrValue) != attrValue.lower()[-3:]:
                                                    modelXbrl.error((messageCodePrefix + 'graphicFileContent'), (_("%(validatedObjectLabel)s references a graphics file which doesn't have expected content '%(attribute)s' for <%(element)s>")),
                                                      modelObject=elt,
                                                      validatedObjectLabel=validatedObjectLabel,
                                                      attribute=attrValue,
                                                      element=eltTag,
                                                      messageCodes=('EFM.6.05.34.graphicFileContent',
                                                                    'EFM.5.02.05.graphicFileContent'))
                                            except IOError as err:
                                                modelXbrl.error((messageCodePrefix + 'graphicFileError'), (_("%(validatedObjectLabel)s references a graphics file which isn't openable '%(attribute)s' for <%(element)s>, error: %(error)s")),
                                                  modelObject=elt,
                                                  validatedObjectLabel=validatedObjectLabel,
                                                  attribute=attrValue,
                                                  element=eltTag,
                                                  error=err,
                                                  messageCodes=('EFM.6.05.34.graphicFileError',
                                                                'EFM.5.02.05.graphicFileError'))

                                    checkedGraphicsFiles.add(attrValue)
                    if eltTag == 'meta' and attrTag == 'content' and not attrValue.startswith('text/html'):
                        modelXbrl.error((messageCodePrefix + 'disallowedMetaContent'), (_('%(validatedObjectLabel)s <meta> content is "%(metaContent)s" but must be "text/html"')),
                          modelObject=elt,
                          validatedObjectLabel=validatedObjectLabel,
                          metaContent=attrValue,
                          messageCodes=('EFM.6.05.34.disallowedMetaContent', 'EFM.5.02.05.disallowedMetaContent'))

            if eltTag == 'table' and any(a.tag in _tableTags for a in elt.iterancestors()):
                modelXbrl.error((messageCodePrefix + 'nestedTable'), (_('%(validatedObjectLabel)s has nested <table> elements.')),
                  modelObject=elt,
                  validatedObjectLabel=validatedObjectLabel,
                  messageCodes=('EFM.6.05.34.nestedTable', 'EFM.5.02.05.nestedTable'))


def validateGraphicFile(elt, graphicFile):
    base = elt.modelDocument.baseForElement(elt)
    normalizedUri = elt.modelXbrl.modelManager.cntlr.webCache.normalizeUrl(graphicFile, base)
    if not elt.modelXbrl.fileSource.isInArchive(normalizedUri):
        normalizedUri = elt.modelXbrl.modelManager.cntlr.webCache.getfilename(normalizedUri)
    with elt.modelXbrl.fileSource.file(normalizedUri, binary=True)[0] as (fh):
        data = fh.read(11)
        if data[:4] == b'\xff\xd8\xff\xe0':
            if data[6:] == b'JFIF\x00':
                return 'jpg'
        if data[:3] == b'GIF':
            if data[3:6] in (b'89a', b'89b', b'87a'):
                return 'gif'


def referencedFiles(modelXbrl, localFilesOnly=True):
    _parser = XMLParser(resolve_entities=False, remove_comments=True, remove_pis=True, recover=True)
    referencedFiles = set()

    def addReferencedFile(docElt, elt):
        if elt.tag in ('a', 'img', '{http://www.w3.org/1999/xhtml}a', '{http://www.w3.org/1999/xhtml}img'):
            for attrTag, attrValue in elt.items():
                if attrTag in ('href', 'src'):
                    if scheme(attrValue) not in ('data', 'javascript'):
                        if not localFilesOnly or not isHttpUrl(attrValue) and not os.path.isabs(attrValue):
                            attrValue = attrValue.partition('#')[0]
                            if attrValue:
                                base = docElt.modelDocument.baseForElement(docElt)
                                normalizedUri = docElt.modelXbrl.modelManager.cntlr.webCache.normalizeUrl(attrValue, base)
                                normalizedUri = docElt.modelXbrl.fileSource.isInArchive(normalizedUri) or docElt.modelXbrl.modelManager.cntlr.webCache.getfilename(normalizedUri)
                    if modelXbrl.fileSource.isInArchive(normalizedUri, checkExistence=True) or os.path.exists(normalizedUri):
                        referencedFiles.add(attrValue)

    for fact in modelXbrl.facts:
        if fact.concept is not None and fact.isItem and fact.concept.isTextBlock:
            text = fact.textValue
            for xmltext in [text] + CDATApattern.findall(text):
                try:
                    for elt in XML(('<body>\n{0}\n</body>\n'.format(xmltext)), parser=_parser).iter():
                        addReferencedFile(fact, elt)

                except (XMLSyntaxError, UnicodeDecodeError):
                    pass

    for elt in modelXbrl.modelDocument.xmlRootElement.iter('{http://www.w3.org/1999/xhtml}a', '{http://www.w3.org/1999/xhtml}img'):
        addReferencedFile(elt, elt)

    return referencedFiles