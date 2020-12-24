# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Lib\HtmlPrinter.py
# Compiled at: 2005-02-09 04:12:06
__doc__ = '\nThis module supports document serialization in HTML syntax.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import re
from Ft.Xml import EMPTY_NAMESPACE
import cStreamWriter
from XmlPrinter import XmlPrinter

class HtmlPrinter(XmlPrinter):
    """
    An HtmlPrinter instance provides functions for serializing an XML
    or XML-like document to a stream, based on SAX-like event calls
    initiated by an instance of Ft.Xml.Lib.Print.PrintVisitor.

    The methods in this subclass of XmlPrinter attempt to emit a
    document conformant to the HTML 4.01 syntax, with no extra
    whitespace added for visual formatting. The degree of correctness
    of the output depends on the data supplied in the event calls; no
    checks are done for conditions that would result in syntax errors,
    such as two attributes with the same name, "--" in a comment, etc.
    """
    __module__ = __name__

    def __init__(self, stream, encoding):
        """
        Creates an HtmlPrinter instance.

        stream must be a file-like object open for writing binary
        data. encoding specifies the encoding which is to be used for
        writing to the stream.
        """
        XmlPrinter.__init__(self, stream, encoding)
        self.disableOutputEscaping = 0
        return

    def startDocument(self, version='4.0', standalone=None):
        """
        Handles a startDocument event.

        Differs from the overridden method in that no XML declaration
        is written.
        """
        if version not in self._versionedEntities:
            version = '4.0'
        (self.textEntities, self.attrEntitiesQuot, self.attrEntitiesApos) = self._versionedEntities[version]
        return

    def doctype(self, name, publicId, systemId):
        """
        Handles a doctype event.

        Extends the overridden method by adding support for the case
        when there is a publicId and no systemId, which is allowed in
        HTML but not in XML.
        """
        if publicId and not systemId:
            self.writeAscii('<!DOCTYPE ')
            self.writeEncode(name, 'document type name')
            self.writeAscii(' PUBLIC "')
            self.writeEncode(publicId, 'document type public-id')
            self.writeAscii('">\n')
        else:
            XmlPrinter.doctype(self, name, publicId, systemId)
        return

    def startElement(self, namespaceUri, tagName, namespaces, attributes):
        """
        Handles a startElement event.

        Extends the overridden method by disabling output escaping for
        the content of certain elements (SCRIPT and STYLE).
        """
        if namespaceUri is not EMPTY_NAMESPACE:
            XmlPrinter.startElement(self, namespaceUri, tagName, namespaces, attributes)
            return
        if tagName.lower() in self.noEscapeElements:
            self.disableOutputEscaping += 1
        XmlPrinter.startElement(self, namespaceUri, tagName, namespaces, attributes)
        self.writeAscii('>')
        self._inElement = False
        return

    def endElement(self, namespaceUri, tagName):
        """
        Handles an endElement event.

        Differs from the overridden method in that an end tag is not
        generated for certain elements.
        """
        if namespaceUri is not EMPTY_NAMESPACE:
            XmlPrinter.endElement(self, namespaceUri, tagName)
            return
        element = tagName.lower()
        if element not in self.forbiddenEndElements:
            self.writeAscii('</')
            self.writeEncode(tagName, 'element name')
            self.writeAscii('>')
        if element in self.noEscapeElements:
            self.disableOutputEscaping -= 1
        return

    def attribute(self, elementUri, elementName, name, value):
        """
        Handles an attribute event.

        Extends the overridden method by writing boolean attributes in
        minimized form.
        """
        if elementUri is not EMPTY_NAMESPACE:
            XmlPrinter.attribute(self, elementUri, elementName, name, value)
            return
        element = elementName.lower()
        attribute = name.lower()
        if element in self.booleanAttributes.get(attribute, []) and attribute == value.lower():
            self.writeAscii(' ')
            self.writeEncode(name, 'attribute name')
        elif element in self.uriAttributes.get(attribute, []):
            value = unicode(re.sub(b'[\x80-\xff]', lambda match: '%%%02X' % ord(match.group()), value.encode('UTF-8')))
            XmlPrinter.attribute(self, elementUri, elementName, name, value)
        else:
            XmlPrinter.attribute(self, elementUri, elementName, name, value)
        return

    def text(self, data, disableEscaping=0):
        """
        Handles a text event.

        Extends the overridden method by disabling output escaping if
        in the content of certain elements like SCRIPT or STYLE.
        """
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        disableEscaping = disableEscaping or self.disableOutputEscaping
        XmlPrinter.text(self, data, disableEscaping)
        return

    def processingInstruction(self, target, data):
        """
        Handles a processingInstruction event.

        Differs from the overridden method by writing the tag with
        no "?" at the end.
        """
        if self._inElement:
            self.writeAscii('>')
            self._inElement = False
        self.writeAscii('<?')
        self.writeEncode(target, 'processing-instruction target')
        if data:
            self.writeAscii(' ')
            self.writeEncode(data, 'processing-instruction data')
        self.writeAscii('>')
        return

    forbiddenEndElements = {}
    for name in ['area', 'base', 'basefont', 'br', 'col', 'frame', 'hr', 'img', 'input', 'isindex', 'link', 'meta', 'param']:
        forbiddenEndElements[name] = True

    del name
    noEscapeElements = {'script': True, 'style': True}
    booleanAttributes = {'checked': ['input'], 'compact': ['dl', 'ol', 'ul', 'dir', 'menu', 'li'], 'declare': ['object'], 'defer': ['script'], 'disabled': ['input', 'select', 'optgroup', 'option', 'textarea', 'button'], 'ismap': ['img', 'input'], 'multiple': ['select'], 'nohref': ['area'], 'noresize': ['frame'], 'noshade': ['hr'], 'nowrap': ['th', 'td'], 'readonly': ['input', 'textarea'], 'selected': ['option']}
    uriAttributes = {'action': ['form'], 'background': ['body'], 'cite': ['blockquote', 'del', 'ins', 'q'], 'classid': ['object'], 'codebase': ['applet', 'object'], 'data': ['object'], 'href': ['a', 'area', 'base', 'link'], 'longdesc': ['frame', 'iframe', 'img'], 'profile': ['head'], 'src': ['frame', 'iframe', 'img', 'input', 'script'], 'usemap': ['img', 'input', 'object']}
    entities_3_2 = {'\xa0': '&nbsp;', '¡': '&iexcl;', '¢': '&cent;', '£': '&pound;', '¤': '&curren;', '¥': '&yen;', '¦': '&brvbar;', '§': '&sect;', '¨': '&uml;', '©': '&copy;', 'ª': '&ordf;', '«': '&laquo;', '¬': '&not;', '\xad': '&shy;', '®': '&reg;', '¯': '&macr;', '°': '&deg;', '±': '&plusmn;', '²': '&sup2;', '³': '&sup3;', '´': '&acute;', 'µ': '&micro;', '¶': '&para;', '·': '&middot;', '¸': '&cedil;', '¹': '&sup1;', 'º': '&ordm;', '»': '&raquo;', '¼': '&frac14;', '½': '&frac12;', '¾': '&frac34;', '¿': '&iquest;', 'À': '&Agrave;', 'Á': '&Aacute;', 'Â': '&Acirc;', 'Ã': '&Atilde;', 'Ä': '&Auml;', 'Å': '&Aring;', 'Æ': '&AElig;', 'Ç': '&Ccedil;', 'È': '&Egrave;', 'É': '&Eacute;', 'Ê': '&Ecirc;', 'Ë': '&Euml;', 'Ì': '&Igrave;', 'Í': '&Iacute;', 'Î': '&Icirc;', 'Ï': '&Iuml;', 'Ð': '&ETH;', 'Ñ': '&Ntilde;', 'Ò': '&Ograve;', 'Ó': '&Oacute;', 'Ô': '&Ocirc;', 'Õ': '&Otilde;', 'Ö': '&Ouml;', '×': '&times;', 'Ø': '&Oslash;', 'Ù': '&Ugrave;', 'Ú': '&Uacute;', 'Û': '&Ucirc;', 'Ü': '&Uuml;', 'Ý': '&Yacute;', 'Þ': '&THORN;', 'ß': '&szlig;', 'à': '&agrave;', 'á': '&aacute;', 'â': '&acirc;', 'ã': '&atilde;', 'ä': '&auml;', 'å': '&aring;', 'æ': '&aelig;', 'ç': '&ccedil;', 'è': '&egrave;', 'é': '&eacute;', 'ê': '&ecirc;', 'ë': '&euml;', 'ì': '&igrave;', 'í': '&iacute;', 'î': '&icirc;', 'ï': '&iuml;', 'ð': '&eth;', 'ñ': '&ntilde;', 'ò': '&ograve;', 'ó': '&oacute;', 'ô': '&ocirc;', 'õ': '&otilde;', 'ö': '&ouml;', '÷': '&divide;', 'ø': '&oslash;', 'ù': '&ugrave;', 'ú': '&uacute;', 'û': '&ucirc;', 'ü': '&uuml;', 'ý': '&yacute;', 'þ': '&thorn;', 'ÿ': '&yuml;'}
    entities_4_0 = {'ƒ': '&fnof;', 'Α': '&Alpha;', 'Β': '&Beta;', 'Γ': '&Gamma;', 'Δ': '&Delta;', 'Ε': '&Epsilon;', 'Ζ': '&Zeta;', 'Η': '&Eta;', 'Θ': '&Theta;', 'Ι': '&Iota;', 'Κ': '&Kappa;', 'Λ': '&Lambda;', 'Μ': '&Mu;', 'Ν': '&Nu;', 'Ξ': '&Xi;', 'Ο': '&Omicron;', 'Π': '&Pi;', 'Ρ': '&Rho;', 'Σ': '&Sigma;', 'Τ': '&Tau;', 'Υ': '&Upsilon;', 'Φ': '&Phi;', 'Χ': '&Chi;', 'Ψ': '&Psi;', 'Ω': '&Omega;', 'α': '&alpha;', 'β': '&beta;', 'γ': '&gamma;', 'δ': '&delta;', 'ε': '&epsilon;', 'ζ': '&zeta;', 'η': '&eta;', 'θ': '&theta;', 'ι': '&iota;', 'κ': '&kappa;', 'λ': '&lambda;', 'μ': '&mu;', 'ν': '&nu;', 'ξ': '&xi;', 'ο': '&omicron;', 'π': '&pi;', 'ρ': '&rho;', 'ς': '&sigmaf;', 'σ': '&sigma;', 'τ': '&tau;', 'υ': '&upsilon;', 'φ': '&phi;', 'χ': '&chi;', 'ψ': '&psi;', 'ω': '&omega;', 'ϑ': '&thetasym;', 'ϒ': '&upsih;', 'ϖ': '&piv;', '•': '&bull;', '…': '&hellip;', '′': '&prime;', '″': '&Prime;', '‾': '&oline;', '›': '&frasl;', '℘': '&weierp;', 'ℑ': '&image;', 'ℜ': '&real;', '™': '&trade;', 'ℵ': '&alefsym;', '←': '&larr;', '↑': '&uarr;', '→': '&rarr;', '↓': '&darr;', '↔': '&harr;', '↵': '&crarr;', '⇐': '&lArr;', '⇑': '&uArr;', '⇒': '&rArr;', '⇓': '&dArr;', '⇔': '&hArr;', '∀': '&forall;', '∂': '&part;', '∃': '&exist;', '∅': '&empty;', '∇': '&nabla;', '∈': '&isin;', '∉': '&notin;', '∋': '&ni;', '∏': '&prod;', '∑': '&sum;', '−': '&minus;', '∗': '&lowast;', '√': '&radic;', '∝': '&prop;', '∞': '&infin;', '∠': '&ang;', '∧': '&and;', '∨': '&or;', '∩': '&cap;', '∪': '&cup;', '∫': '&int;', '∴': '&there4;', '∼': '&sim;', '≅': '&cong;', '≈': '&asymp;', '≠': '&ne;', '≡': '&equiv;', '≤': '&le;', '≥': '&ge;', '⊂': '&sub;', '⊃': '&sup;', '⊄': '&nsub;', '⊆': '&sube;', '⊇': '&supe;', '⊕': '&oplus;', '⊗': '&otimes;', '⊥': '&perp;', '⋅': '&sdot;', '⌈': '&lceil;', '⌉': '&rceil;', '⌊': '&lfloor;', '⌋': '&rfloor;', '〈': '&lang;', '〉': '&rang;', '◊': '&loz;', '♠': '&spades;', '♣': '&clubs;', '♥': '&hearts;', '♦': '&diams;', 'Œ': '&OElig;', 'œ': '&oelig;', 'Š': '&Scaron;', 'š': '&scaron;', 'Ÿ': '&Yuml;', 'ˆ': '&circ;', '˜': '&tidle;', '\u2002': '&ensp;', '\u2003': '&emsp;', '\u2009': '&thinsp;', '\u200c': '&zwnj;', '\u200d': '&zwj;', '\u200e': '&lrm;', '\u200f': '&rlm;', '–': '&ndash;', '—': '&mdash;', '‘': '&lsquo;', '’': '&rsquo;', '‚': '&sbquo;', '“': '&ldquo;', '”': '&rdquo;', '„': '&bdquo;', '†': '&dagger;', '‡': '&Dagger;', '‰': '&permil;', '‹': '&lsaquo;', '›': '&rsaquo;', '€': '&euro;'}
    _versionedEntities = {'3.2': [], '4.0': []}
    textEntities = {'<': '&lt;', '>': '&gt;', '&': '&amp;', '\r': '&#13;'}
    textEntities.update(entities_3_2)
    _versionedEntities['3.2'].append(cStreamWriter.EntityMap(textEntities))
    textEntities.update(entities_4_0)
    textEntities = cStreamWriter.EntityMap(textEntities)
    _versionedEntities['4.0'].append(textEntities)

    def attr_amp_escape(string, offset):
        if string.startswith('&{', offset):
            return '&'
        else:
            return '&amp;'

    attrEntitiesQuot = {'&': attr_amp_escape, '\t': '&#9;', '\n': '&#10;', '\r': '&#13;', '"': '&quot;'}
    attrEntitiesQuot.update(entities_3_2)
    _versionedEntities['3.2'].append(cStreamWriter.EntityMap(attrEntitiesQuot))
    attrEntitiesQuot.update(entities_4_0)
    attrEntitiesQuot = cStreamWriter.EntityMap(attrEntitiesQuot)
    _versionedEntities['4.0'].append(attrEntitiesQuot)
    attrEntitiesApos = {'&': attr_amp_escape, '\t': '&#9;', '\n': '&#10;', '\r': '&#13;', "'": '&#39;'}
    attrEntitiesApos.update(entities_3_2)
    _versionedEntities['3.2'].append(cStreamWriter.EntityMap(attrEntitiesApos))
    attrEntitiesApos.update(entities_4_0)
    attrEntitiesApos = cStreamWriter.EntityMap(attrEntitiesApos)
    _versionedEntities['4.0'].append(attrEntitiesApos)
    del entities_3_2
    del entities_4_0
    del attr_amp_escape