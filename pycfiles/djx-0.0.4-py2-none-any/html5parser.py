# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/html5lib/html5parser.py
# Compiled at: 2019-02-14 00:35:07
from __future__ import absolute_import, division, unicode_literals
from pip._vendor.six import with_metaclass, viewkeys
import types
from collections import OrderedDict
from . import _inputstream
from . import _tokenizer
from . import treebuilders
from .treebuilders.base import Marker
from . import _utils
from .constants import spaceCharacters, asciiUpper2Lower, specialElements, headingElements, cdataElements, rcdataElements, tokenTypes, tagTokenTypes, namespaces, htmlIntegrationPointElements, mathmlTextIntegrationPointElements, adjustForeignAttributes as adjustForeignAttributesMap, adjustMathMLAttributes, adjustSVGAttributes, E, _ReparseException

def parse(doc, treebuilder=b'etree', namespaceHTMLElements=True, **kwargs):
    """Parse an HTML document as a string or file-like object into a tree

    :arg doc: the document to parse as a string or file-like object

    :arg treebuilder: the treebuilder to use when parsing

    :arg namespaceHTMLElements: whether or not to namespace HTML elements

    :returns: parsed tree

    Example:

    >>> from html5lib.html5parser import parse
    >>> parse('<html><body><p>This is a doc</p></body></html>')
    <Element u'{http://www.w3.org/1999/xhtml}html' at 0x7feac4909db0>

    """
    tb = treebuilders.getTreeBuilder(treebuilder)
    p = HTMLParser(tb, namespaceHTMLElements=namespaceHTMLElements)
    return p.parse(doc, **kwargs)


def parseFragment(doc, container=b'div', treebuilder=b'etree', namespaceHTMLElements=True, **kwargs):
    """Parse an HTML fragment as a string or file-like object into a tree

    :arg doc: the fragment to parse as a string or file-like object

    :arg container: the container context to parse the fragment in

    :arg treebuilder: the treebuilder to use when parsing

    :arg namespaceHTMLElements: whether or not to namespace HTML elements

    :returns: parsed tree

    Example:

    >>> from html5lib.html5libparser import parseFragment
    >>> parseFragment('<b>this is a fragment</b>')
    <Element u'DOCUMENT_FRAGMENT' at 0x7feac484b090>

    """
    tb = treebuilders.getTreeBuilder(treebuilder)
    p = HTMLParser(tb, namespaceHTMLElements=namespaceHTMLElements)
    return p.parseFragment(doc, container=container, **kwargs)


def method_decorator_metaclass(function):

    class Decorated(type):

        def __new__(meta, classname, bases, classDict):
            for attributeName, attribute in classDict.items():
                if isinstance(attribute, types.FunctionType):
                    attribute = function(attribute)
                classDict[attributeName] = attribute

            return type.__new__(meta, classname, bases, classDict)

    return Decorated


class HTMLParser(object):
    """HTML parser

    Generates a tree structure from a stream of (possibly malformed) HTML.

    """

    def __init__(self, tree=None, strict=False, namespaceHTMLElements=True, debug=False):
        """
        :arg tree: a treebuilder class controlling the type of tree that will be
            returned. Built in treebuilders can be accessed through
            html5lib.treebuilders.getTreeBuilder(treeType)

        :arg strict: raise an exception when a parse error is encountered

        :arg namespaceHTMLElements: whether or not to namespace HTML elements

        :arg debug: whether or not to enable debug mode which logs things

        Example:

        >>> from html5lib.html5parser import HTMLParser
        >>> parser = HTMLParser()                     # generates parser with etree builder
        >>> parser = HTMLParser('lxml', strict=True)  # generates parser with lxml builder which is strict

        """
        self.strict = strict
        if tree is None:
            tree = treebuilders.getTreeBuilder(b'etree')
        self.tree = tree(namespaceHTMLElements)
        self.errors = []
        self.phases = dict([ (name, cls(self, self.tree)) for name, cls in getPhases(debug).items()
                           ])
        return

    def _parse(self, stream, innerHTML=False, container=b'div', scripting=False, **kwargs):
        self.innerHTMLMode = innerHTML
        self.container = container
        self.scripting = scripting
        self.tokenizer = _tokenizer.HTMLTokenizer(stream, parser=self, **kwargs)
        self.reset()
        try:
            self.mainLoop()
        except _ReparseException:
            self.reset()
            self.mainLoop()

    def reset(self):
        self.tree.reset()
        self.firstStartTag = False
        self.errors = []
        self.log = []
        self.compatMode = b'no quirks'
        if self.innerHTMLMode:
            self.innerHTML = self.container.lower()
            if self.innerHTML in cdataElements:
                self.tokenizer.state = self.tokenizer.rcdataState
            elif self.innerHTML in rcdataElements:
                self.tokenizer.state = self.tokenizer.rawtextState
            elif self.innerHTML == b'plaintext':
                self.tokenizer.state = self.tokenizer.plaintextState
            self.phase = self.phases[b'beforeHtml']
            self.phase.insertHtmlElement()
            self.resetInsertionMode()
        else:
            self.innerHTML = False
            self.phase = self.phases[b'initial']
        self.lastPhase = None
        self.beforeRCDataPhase = None
        self.framesetOK = True
        return

    @property
    def documentEncoding(self):
        """Name of the character encoding that was used to decode the input stream, or
        :obj:`None` if that is not determined yet

        """
        if not hasattr(self, b'tokenizer'):
            return None
        else:
            return self.tokenizer.stream.charEncoding[0].name

    def isHTMLIntegrationPoint(self, element):
        if element.name == b'annotation-xml' and element.namespace == namespaces[b'mathml']:
            return b'encoding' in element.attributes and element.attributes[b'encoding'].translate(asciiUpper2Lower) in ('text/html',
                                                                                                                         'application/xhtml+xml')
        else:
            return (
             element.namespace, element.name) in htmlIntegrationPointElements

    def isMathMLTextIntegrationPoint(self, element):
        return (element.namespace, element.name) in mathmlTextIntegrationPointElements

    def mainLoop(self):
        CharactersToken = tokenTypes[b'Characters']
        SpaceCharactersToken = tokenTypes[b'SpaceCharacters']
        StartTagToken = tokenTypes[b'StartTag']
        EndTagToken = tokenTypes[b'EndTag']
        CommentToken = tokenTypes[b'Comment']
        DoctypeToken = tokenTypes[b'Doctype']
        ParseErrorToken = tokenTypes[b'ParseError']
        for token in self.normalizedTokens():
            prev_token = None
            new_token = token
            while new_token is not None:
                prev_token = new_token
                currentNode = self.tree.openElements[(-1)] if self.tree.openElements else None
                currentNodeNamespace = currentNode.namespace if currentNode else None
                currentNodeName = currentNode.name if currentNode else None
                type = new_token[b'type']
                if type == ParseErrorToken:
                    self.parseError(new_token[b'data'], new_token.get(b'datavars', {}))
                    new_token = None
                else:
                    if len(self.tree.openElements) == 0 or currentNodeNamespace == self.tree.defaultNamespace or self.isMathMLTextIntegrationPoint(currentNode) and (type == StartTagToken and token[b'name'] not in frozenset([b'mglyph', b'malignmark']) or type in (CharactersToken, SpaceCharactersToken)) or currentNodeNamespace == namespaces[b'mathml'] and currentNodeName == b'annotation-xml' and type == StartTagToken and token[b'name'] == b'svg' or self.isHTMLIntegrationPoint(currentNode) and type in (StartTagToken, CharactersToken, SpaceCharactersToken):
                        phase = self.phase
                    else:
                        phase = self.phases[b'inForeignContent']
                    if type == CharactersToken:
                        new_token = phase.processCharacters(new_token)
                    elif type == SpaceCharactersToken:
                        new_token = phase.processSpaceCharacters(new_token)
                    elif type == StartTagToken:
                        new_token = phase.processStartTag(new_token)
                    elif type == EndTagToken:
                        new_token = phase.processEndTag(new_token)
                    elif type == CommentToken:
                        new_token = phase.processComment(new_token)
                    elif type == DoctypeToken:
                        new_token = phase.processDoctype(new_token)

            if type == StartTagToken and prev_token[b'selfClosing'] and not prev_token[b'selfClosingAcknowledged']:
                self.parseError(b'non-void-element-with-trailing-solidus', {b'name': prev_token[b'name']})

        reprocess = True
        phases = []
        while reprocess:
            phases.append(self.phase)
            reprocess = self.phase.processEOF()
            if reprocess:
                assert self.phase not in phases

        return

    def normalizedTokens(self):
        for token in self.tokenizer:
            yield self.normalizeToken(token)

    def parse(self, stream, *args, **kwargs):
        """Parse a HTML document into a well-formed tree

        :arg stream: a file-like object or string containing the HTML to be parsed

            The optional encoding parameter must be a string that indicates
            the encoding.  If specified, that encoding will be used,
            regardless of any BOM or later declaration (such as in a meta
            element).

        :arg scripting: treat noscript elements as if JavaScript was turned on

        :returns: parsed tree

        Example:

        >>> from html5lib.html5parser import HTMLParser
        >>> parser = HTMLParser()
        >>> parser.parse('<html><body><p>This is a doc</p></body></html>')
        <Element u'{http://www.w3.org/1999/xhtml}html' at 0x7feac4909db0>

        """
        self._parse(stream, False, None, *args, **kwargs)
        return self.tree.getDocument()

    def parseFragment(self, stream, *args, **kwargs):
        """Parse a HTML fragment into a well-formed tree fragment

        :arg container: name of the element we're setting the innerHTML
            property if set to None, default to 'div'

        :arg stream: a file-like object or string containing the HTML to be parsed

            The optional encoding parameter must be a string that indicates
            the encoding.  If specified, that encoding will be used,
            regardless of any BOM or later declaration (such as in a meta
            element)

        :arg scripting: treat noscript elements as if JavaScript was turned on

        :returns: parsed tree

        Example:

        >>> from html5lib.html5libparser import HTMLParser
        >>> parser = HTMLParser()
        >>> parser.parseFragment('<b>this is a fragment</b>')
        <Element u'DOCUMENT_FRAGMENT' at 0x7feac484b090>

        """
        self._parse(stream, True, *args, **kwargs)
        return self.tree.getFragment()

    def parseError(self, errorcode=b'XXX-undefined-error', datavars=None):
        if datavars is None:
            datavars = {}
        self.errors.append((self.tokenizer.stream.position(), errorcode, datavars))
        if self.strict:
            raise ParseError(E[errorcode] % datavars)
        return

    def normalizeToken(self, token):
        if token[b'type'] == tokenTypes[b'StartTag']:
            raw = token[b'data']
            token[b'data'] = OrderedDict(raw)
            if len(raw) > len(token[b'data']):
                token[b'data'].update(raw[::-1])
        return token

    def adjustMathMLAttributes(self, token):
        adjust_attributes(token, adjustMathMLAttributes)

    def adjustSVGAttributes(self, token):
        adjust_attributes(token, adjustSVGAttributes)

    def adjustForeignAttributes(self, token):
        adjust_attributes(token, adjustForeignAttributesMap)

    def reparseTokenNormal(self, token):
        self.parser.phase()

    def resetInsertionMode(self):
        last = False
        newModes = {b'select': b'inSelect', 
           b'td': b'inCell', 
           b'th': b'inCell', 
           b'tr': b'inRow', 
           b'tbody': b'inTableBody', 
           b'thead': b'inTableBody', 
           b'tfoot': b'inTableBody', 
           b'caption': b'inCaption', 
           b'colgroup': b'inColumnGroup', 
           b'table': b'inTable', 
           b'head': b'inBody', 
           b'body': b'inBody', 
           b'frameset': b'inFrameset', 
           b'html': b'beforeHead'}
        for node in self.tree.openElements[::-1]:
            nodeName = node.name
            new_phase = None
            if node == self.tree.openElements[0]:
                if not self.innerHTML:
                    raise AssertionError
                    last = True
                    nodeName = self.innerHTML
                assert nodeName in ('select', 'colgroup', 'head', 'html') and self.innerHTML
            if not last and node.namespace != self.tree.defaultNamespace:
                continue
            if nodeName in newModes:
                new_phase = self.phases[newModes[nodeName]]
                break
            elif last:
                new_phase = self.phases[b'inBody']
                break

        self.phase = new_phase
        return

    def parseRCDataRawtext(self, token, contentType):
        assert contentType in ('RAWTEXT', 'RCDATA')
        self.tree.insertElement(token)
        if contentType == b'RAWTEXT':
            self.tokenizer.state = self.tokenizer.rawtextState
        else:
            self.tokenizer.state = self.tokenizer.rcdataState
        self.originalPhase = self.phase
        self.phase = self.phases[b'text']


@_utils.memoize
def getPhases(debug):

    def log(function):
        """Logger that records which phase processes each token"""
        type_names = dict((value, key) for key, value in tokenTypes.items())

        def wrapped(self, *args, **kwargs):
            if function.__name__.startswith(b'process') and len(args) > 0:
                token = args[0]
                try:
                    info = {b'type': type_names[token[b'type']]}
                except:
                    raise

                if token[b'type'] in tagTokenTypes:
                    info[b'name'] = token[b'name']
                self.parser.log.append((self.parser.tokenizer.state.__name__,
                 self.parser.phase.__class__.__name__,
                 self.__class__.__name__,
                 function.__name__,
                 info))
                return function(self, *args, **kwargs)
            else:
                return function(self, *args, **kwargs)

        return wrapped

    def getMetaclass(use_metaclass, metaclass_func):
        if use_metaclass:
            return method_decorator_metaclass(metaclass_func)
        else:
            return type

    class Phase(with_metaclass(getMetaclass(debug, log))):
        """Base class for helper object that implements each phase of processing
        """

        def __init__(self, parser, tree):
            self.parser = parser
            self.tree = tree

        def processEOF(self):
            raise NotImplementedError

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.openElements[(-1)])

        def processDoctype(self, token):
            self.parser.parseError(b'unexpected-doctype')

        def processCharacters(self, token):
            self.tree.insertText(token[b'data'])

        def processSpaceCharacters(self, token):
            self.tree.insertText(token[b'data'])

        def processStartTag(self, token):
            return self.startTagHandler[token[b'name']](token)

        def startTagHtml(self, token):
            if not self.parser.firstStartTag and token[b'name'] == b'html':
                self.parser.parseError(b'non-html-root')
            for attr, value in token[b'data'].items():
                if attr not in self.tree.openElements[0].attributes:
                    self.tree.openElements[0].attributes[attr] = value

            self.parser.firstStartTag = False

        def processEndTag(self, token):
            return self.endTagHandler[token[b'name']](token)

    class InitialPhase(Phase):

        def processSpaceCharacters(self, token):
            pass

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.document)

        def processDoctype(self, token):
            name = token[b'name']
            publicId = token[b'publicId']
            systemId = token[b'systemId']
            correct = token[b'correct']
            if name != b'html' or publicId is not None or systemId is not None and systemId != b'about:legacy-compat':
                self.parser.parseError(b'unknown-doctype')
            if publicId is None:
                publicId = b''
            self.tree.insertDoctype(token)
            if publicId != b'':
                publicId = publicId.translate(asciiUpper2Lower)
            if not correct or token[b'name'] != b'html' or publicId.startswith(('+//silmaril//dtd html pro v0r11 19970101//',
                                                                                '-//advasoft ltd//dtd html 3.0 aswedit + extensions//',
                                                                                '-//as//dtd html 3.0 aswedit + extensions//',
                                                                                '-//ietf//dtd html 2.0 level 1//',
                                                                                '-//ietf//dtd html 2.0 level 2//',
                                                                                '-//ietf//dtd html 2.0 strict level 1//',
                                                                                '-//ietf//dtd html 2.0 strict level 2//',
                                                                                '-//ietf//dtd html 2.0 strict//',
                                                                                '-//ietf//dtd html 2.0//',
                                                                                '-//ietf//dtd html 2.1e//',
                                                                                '-//ietf//dtd html 3.0//',
                                                                                '-//ietf//dtd html 3.2 final//',
                                                                                '-//ietf//dtd html 3.2//',
                                                                                '-//ietf//dtd html 3//',
                                                                                '-//ietf//dtd html level 0//',
                                                                                '-//ietf//dtd html level 1//',
                                                                                '-//ietf//dtd html level 2//',
                                                                                '-//ietf//dtd html level 3//',
                                                                                '-//ietf//dtd html strict level 0//',
                                                                                '-//ietf//dtd html strict level 1//',
                                                                                '-//ietf//dtd html strict level 2//',
                                                                                '-//ietf//dtd html strict level 3//',
                                                                                '-//ietf//dtd html strict//',
                                                                                '-//ietf//dtd html//',
                                                                                '-//metrius//dtd metrius presentational//',
                                                                                '-//microsoft//dtd internet explorer 2.0 html strict//',
                                                                                '-//microsoft//dtd internet explorer 2.0 html//',
                                                                                '-//microsoft//dtd internet explorer 2.0 tables//',
                                                                                '-//microsoft//dtd internet explorer 3.0 html strict//',
                                                                                '-//microsoft//dtd internet explorer 3.0 html//',
                                                                                '-//microsoft//dtd internet explorer 3.0 tables//',
                                                                                '-//netscape comm. corp.//dtd html//',
                                                                                '-//netscape comm. corp.//dtd strict html//',
                                                                                "-//o'reilly and associates//dtd html 2.0//",
                                                                                "-//o'reilly and associates//dtd html extended 1.0//",
                                                                                "-//o'reilly and associates//dtd html extended relaxed 1.0//",
                                                                                '-//softquad software//dtd hotmetal pro 6.0::19990601::extensions to html 4.0//',
                                                                                '-//softquad//dtd hotmetal pro 4.0::19971010::extensions to html 4.0//',
                                                                                '-//spyglass//dtd html 2.0 extended//',
                                                                                '-//sq//dtd html 2.0 hotmetal + extensions//',
                                                                                '-//sun microsystems corp.//dtd hotjava html//',
                                                                                '-//sun microsystems corp.//dtd hotjava strict html//',
                                                                                '-//w3c//dtd html 3 1995-03-24//',
                                                                                '-//w3c//dtd html 3.2 draft//',
                                                                                '-//w3c//dtd html 3.2 final//',
                                                                                '-//w3c//dtd html 3.2//',
                                                                                '-//w3c//dtd html 3.2s draft//',
                                                                                '-//w3c//dtd html 4.0 frameset//',
                                                                                '-//w3c//dtd html 4.0 transitional//',
                                                                                '-//w3c//dtd html experimental 19960712//',
                                                                                '-//w3c//dtd html experimental 970421//',
                                                                                '-//w3c//dtd w3 html//',
                                                                                '-//w3o//dtd w3 html 3.0//',
                                                                                '-//webtechs//dtd mozilla html 2.0//',
                                                                                '-//webtechs//dtd mozilla html//')) or publicId in ('-//w3o//dtd w3 html strict 3.0//en//',
                                                                                                                                    '-/w3c/dtd html 4.0 transitional/en',
                                                                                                                                    'html') or publicId.startswith(('-//w3c//dtd html 4.01 frameset//',
                                                                                                                                                                    '-//w3c//dtd html 4.01 transitional//')) and systemId is None or systemId and systemId.lower() == b'http://www.ibm.com/data/dtd/v11/ibmxhtml1-transitional.dtd':
                self.parser.compatMode = b'quirks'
            elif publicId.startswith(('-//w3c//dtd xhtml 1.0 frameset//', '-//w3c//dtd xhtml 1.0 transitional//')) or publicId.startswith(('-//w3c//dtd html 4.01 frameset//',
                                                                                                                                           '-//w3c//dtd html 4.01 transitional//')) and systemId is not None:
                self.parser.compatMode = b'limited quirks'
            self.parser.phase = self.parser.phases[b'beforeHtml']
            return

        def anythingElse(self):
            self.parser.compatMode = b'quirks'
            self.parser.phase = self.parser.phases[b'beforeHtml']

        def processCharacters(self, token):
            self.parser.parseError(b'expected-doctype-but-got-chars')
            self.anythingElse()
            return token

        def processStartTag(self, token):
            self.parser.parseError(b'expected-doctype-but-got-start-tag', {b'name': token[b'name']})
            self.anythingElse()
            return token

        def processEndTag(self, token):
            self.parser.parseError(b'expected-doctype-but-got-end-tag', {b'name': token[b'name']})
            self.anythingElse()
            return token

        def processEOF(self):
            self.parser.parseError(b'expected-doctype-but-got-eof')
            self.anythingElse()
            return True

    class BeforeHtmlPhase(Phase):

        def insertHtmlElement(self):
            self.tree.insertRoot(impliedTagToken(b'html', b'StartTag'))
            self.parser.phase = self.parser.phases[b'beforeHead']

        def processEOF(self):
            self.insertHtmlElement()
            return True

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.document)

        def processSpaceCharacters(self, token):
            pass

        def processCharacters(self, token):
            self.insertHtmlElement()
            return token

        def processStartTag(self, token):
            if token[b'name'] == b'html':
                self.parser.firstStartTag = True
            self.insertHtmlElement()
            return token

        def processEndTag(self, token):
            if token[b'name'] not in ('head', 'body', 'html', 'br'):
                self.parser.parseError(b'unexpected-end-tag-before-html', {b'name': token[b'name']})
            else:
                self.insertHtmlElement()
                return token

    class BeforeHeadPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              b'head', self.startTagHead)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              ('head', 'body', 'html', 'br'), self.endTagImplyHead)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            self.startTagHead(impliedTagToken(b'head', b'StartTag'))
            return True

        def processSpaceCharacters(self, token):
            pass

        def processCharacters(self, token):
            self.startTagHead(impliedTagToken(b'head', b'StartTag'))
            return token

        def startTagHtml(self, token):
            return self.parser.phases[b'inBody'].processStartTag(token)

        def startTagHead(self, token):
            self.tree.insertElement(token)
            self.tree.headPointer = self.tree.openElements[(-1)]
            self.parser.phase = self.parser.phases[b'inHead']

        def startTagOther(self, token):
            self.startTagHead(impliedTagToken(b'head', b'StartTag'))
            return token

        def endTagImplyHead(self, token):
            self.startTagHead(impliedTagToken(b'head', b'StartTag'))
            return token

        def endTagOther(self, token):
            self.parser.parseError(b'end-tag-after-implied-root', {b'name': token[b'name']})

    class InHeadPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              b'title', self.startTagTitle),
             (
              ('noframes', 'style'), self.startTagNoFramesStyle),
             (
              b'noscript', self.startTagNoscript),
             (
              b'script', self.startTagScript),
             (
              ('base', 'basefont', 'bgsound', 'command', 'link'),
              self.startTagBaseLinkCommand),
             (
              b'meta', self.startTagMeta),
             (
              b'head', self.startTagHead)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              b'head', self.endTagHead),
             (
              ('br', 'html', 'body'), self.endTagHtmlBodyBr)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            self.anythingElse()
            return True

        def processCharacters(self, token):
            self.anythingElse()
            return token

        def startTagHtml(self, token):
            return self.parser.phases[b'inBody'].processStartTag(token)

        def startTagHead(self, token):
            self.parser.parseError(b'two-heads-are-not-better-than-one')

        def startTagBaseLinkCommand(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token[b'selfClosingAcknowledged'] = True

        def startTagMeta(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token[b'selfClosingAcknowledged'] = True
            attributes = token[b'data']
            if self.parser.tokenizer.stream.charEncoding[1] == b'tentative':
                if b'charset' in attributes:
                    self.parser.tokenizer.stream.changeEncoding(attributes[b'charset'])
                elif b'content' in attributes and b'http-equiv' in attributes and attributes[b'http-equiv'].lower() == b'content-type':
                    data = _inputstream.EncodingBytes(attributes[b'content'].encode(b'utf-8'))
                    parser = _inputstream.ContentAttrParser(data)
                    codec = parser.parse()
                    self.parser.tokenizer.stream.changeEncoding(codec)

        def startTagTitle(self, token):
            self.parser.parseRCDataRawtext(token, b'RCDATA')

        def startTagNoFramesStyle(self, token):
            self.parser.parseRCDataRawtext(token, b'RAWTEXT')

        def startTagNoscript(self, token):
            if self.parser.scripting:
                self.parser.parseRCDataRawtext(token, b'RAWTEXT')
            else:
                self.tree.insertElement(token)
                self.parser.phase = self.parser.phases[b'inHeadNoscript']

        def startTagScript(self, token):
            self.tree.insertElement(token)
            self.parser.tokenizer.state = self.parser.tokenizer.scriptDataState
            self.parser.originalPhase = self.parser.phase
            self.parser.phase = self.parser.phases[b'text']

        def startTagOther(self, token):
            self.anythingElse()
            return token

        def endTagHead(self, token):
            node = self.parser.tree.openElements.pop()
            assert node.name == b'head', b'Expected head got %s' % node.name
            self.parser.phase = self.parser.phases[b'afterHead']

        def endTagHtmlBodyBr(self, token):
            self.anythingElse()
            return token

        def endTagOther(self, token):
            self.parser.parseError(b'unexpected-end-tag', {b'name': token[b'name']})

        def anythingElse(self):
            self.endTagHead(impliedTagToken(b'head'))

    class InHeadNoscriptPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              ('basefont', 'bgsound', 'link', 'meta', 'noframes', 'style'), self.startTagBaseLinkCommand),
             (
              ('head', 'noscript'), self.startTagHeadNoscript)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              b'noscript', self.endTagNoscript),
             (
              b'br', self.endTagBr)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            self.parser.parseError(b'eof-in-head-noscript')
            self.anythingElse()
            return True

        def processComment(self, token):
            return self.parser.phases[b'inHead'].processComment(token)

        def processCharacters(self, token):
            self.parser.parseError(b'char-in-head-noscript')
            self.anythingElse()
            return token

        def processSpaceCharacters(self, token):
            return self.parser.phases[b'inHead'].processSpaceCharacters(token)

        def startTagHtml(self, token):
            return self.parser.phases[b'inBody'].processStartTag(token)

        def startTagBaseLinkCommand(self, token):
            return self.parser.phases[b'inHead'].processStartTag(token)

        def startTagHeadNoscript(self, token):
            self.parser.parseError(b'unexpected-start-tag', {b'name': token[b'name']})

        def startTagOther(self, token):
            self.parser.parseError(b'unexpected-inhead-noscript-tag', {b'name': token[b'name']})
            self.anythingElse()
            return token

        def endTagNoscript(self, token):
            node = self.parser.tree.openElements.pop()
            assert node.name == b'noscript', b'Expected noscript got %s' % node.name
            self.parser.phase = self.parser.phases[b'inHead']

        def endTagBr(self, token):
            self.parser.parseError(b'unexpected-inhead-noscript-tag', {b'name': token[b'name']})
            self.anythingElse()
            return token

        def endTagOther(self, token):
            self.parser.parseError(b'unexpected-end-tag', {b'name': token[b'name']})

        def anythingElse(self):
            self.endTagNoscript(impliedTagToken(b'noscript'))

    class AfterHeadPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              b'body', self.startTagBody),
             (
              b'frameset', self.startTagFrameset),
             (
              ('base', 'basefont', 'bgsound', 'link', 'meta', 'noframes', 'script', 'style', 'title'),
              self.startTagFromHead),
             (
              b'head', self.startTagHead)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (('body', 'html', 'br'),
              self.endTagHtmlBodyBr)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            self.anythingElse()
            return True

        def processCharacters(self, token):
            self.anythingElse()
            return token

        def startTagHtml(self, token):
            return self.parser.phases[b'inBody'].processStartTag(token)

        def startTagBody(self, token):
            self.parser.framesetOK = False
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases[b'inBody']

        def startTagFrameset(self, token):
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases[b'inFrameset']

        def startTagFromHead(self, token):
            self.parser.parseError(b'unexpected-start-tag-out-of-my-head', {b'name': token[b'name']})
            self.tree.openElements.append(self.tree.headPointer)
            self.parser.phases[b'inHead'].processStartTag(token)
            for node in self.tree.openElements[::-1]:
                if node.name == b'head':
                    self.tree.openElements.remove(node)
                    break

        def startTagHead(self, token):
            self.parser.parseError(b'unexpected-start-tag', {b'name': token[b'name']})

        def startTagOther(self, token):
            self.anythingElse()
            return token

        def endTagHtmlBodyBr(self, token):
            self.anythingElse()
            return token

        def endTagOther(self, token):
            self.parser.parseError(b'unexpected-end-tag', {b'name': token[b'name']})

        def anythingElse(self):
            self.tree.insertElement(impliedTagToken(b'body', b'StartTag'))
            self.parser.phase = self.parser.phases[b'inBody']
            self.parser.framesetOK = True

    class InBodyPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.processSpaceCharacters = self.processSpaceCharactersNonPre
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              ('base', 'basefont', 'bgsound', 'command', 'link', 'meta', 'script', 'style', 'title'),
              self.startTagProcessInHead),
             (
              b'body', self.startTagBody),
             (
              b'frameset', self.startTagFrameset),
             (
              ('address', 'article', 'aside', 'blockquote', 'center', 'details', 'dir', 'div', 'dl',
 'fieldset', 'figcaption', 'figure', 'footer', 'header', 'hgroup', 'main', 'menu',
 'nav', 'ol', 'p', 'section', 'summary', 'ul'),
              self.startTagCloseP),
             (
              headingElements, self.startTagHeading),
             (
              ('pre', 'listing'), self.startTagPreListing),
             (
              b'form', self.startTagForm),
             (
              ('li', 'dd', 'dt'), self.startTagListItem),
             (
              b'plaintext', self.startTagPlaintext),
             (
              b'a', self.startTagA),
             (
              ('b', 'big', 'code', 'em', 'font', 'i', 's', 'small', 'strike', 'strong', 'tt', 'u'), self.startTagFormatting),
             (
              b'nobr', self.startTagNobr),
             (
              b'button', self.startTagButton),
             (
              ('applet', 'marquee', 'object'), self.startTagAppletMarqueeObject),
             (
              b'xmp', self.startTagXmp),
             (
              b'table', self.startTagTable),
             (
              ('area', 'br', 'embed', 'img', 'keygen', 'wbr'),
              self.startTagVoidFormatting),
             (
              ('param', 'source', 'track'), self.startTagParamSource),
             (
              b'input', self.startTagInput),
             (
              b'hr', self.startTagHr),
             (
              b'image', self.startTagImage),
             (
              b'isindex', self.startTagIsIndex),
             (
              b'textarea', self.startTagTextarea),
             (
              b'iframe', self.startTagIFrame),
             (
              b'noscript', self.startTagNoscript),
             (
              ('noembed', 'noframes'), self.startTagRawtext),
             (
              b'select', self.startTagSelect),
             (
              ('rp', 'rt'), self.startTagRpRt),
             (
              ('option', 'optgroup'), self.startTagOpt),
             (
              b'math', self.startTagMath),
             (
              b'svg', self.startTagSvg),
             (
              ('caption', 'col', 'colgroup', 'frame', 'head', 'tbody', 'td', 'tfoot', 'th', 'thead',
 'tr'), self.startTagMisplaced)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              b'body', self.endTagBody),
             (
              b'html', self.endTagHtml),
             (
              ('address', 'article', 'aside', 'blockquote', 'button', 'center', 'details', 'dialog',
 'dir', 'div', 'dl', 'fieldset', 'figcaption', 'figure', 'footer', 'header', 'hgroup',
 'listing', 'main', 'menu', 'nav', 'ol', 'pre', 'section', 'summary', 'ul'), self.endTagBlock),
             (
              b'form', self.endTagForm),
             (
              b'p', self.endTagP),
             (
              ('dd', 'dt', 'li'), self.endTagListItem),
             (
              headingElements, self.endTagHeading),
             (
              ('a', 'b', 'big', 'code', 'em', 'font', 'i', 'nobr', 's', 'small', 'strike', 'strong',
 'tt', 'u'), self.endTagFormatting),
             (
              ('applet', 'marquee', 'object'), self.endTagAppletMarqueeObject),
             (
              b'br', self.endTagBr)])
            self.endTagHandler.default = self.endTagOther

        def isMatchingFormattingElement(self, node1, node2):
            return node1.name == node2.name and node1.namespace == node2.namespace and node1.attributes == node2.attributes

        def addFormattingElement(self, token):
            self.tree.insertElement(token)
            element = self.tree.openElements[(-1)]
            matchingElements = []
            for node in self.tree.activeFormattingElements[::-1]:
                if node is Marker:
                    break
                elif self.isMatchingFormattingElement(node, element):
                    matchingElements.append(node)

            assert len(matchingElements) <= 3
            if len(matchingElements) == 3:
                self.tree.activeFormattingElements.remove(matchingElements[(-1)])
            self.tree.activeFormattingElements.append(element)

        def processEOF(self):
            allowed_elements = frozenset(('dd', 'dt', 'li', 'p', 'tbody', 'td', 'tfoot',
                                          'th', 'thead', 'tr', 'body', 'html'))
            for node in self.tree.openElements[::-1]:
                if node.name not in allowed_elements:
                    self.parser.parseError(b'expected-closing-tag-but-got-eof')
                    break

        def processSpaceCharactersDropNewline(self, token):
            data = token[b'data']
            self.processSpaceCharacters = self.processSpaceCharactersNonPre
            if data.startswith(b'\n') and self.tree.openElements[(-1)].name in ('pre',
                                                                                'listing',
                                                                                'textarea') and not self.tree.openElements[(-1)].hasContent():
                data = data[1:]
            if data:
                self.tree.reconstructActiveFormattingElements()
                self.tree.insertText(data)

        def processCharacters(self, token):
            if token[b'data'] == b'\x00':
                return
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertText(token[b'data'])
            if self.parser.framesetOK and any([ char not in spaceCharacters for char in token[b'data']
                                              ]):
                self.parser.framesetOK = False

        def processSpaceCharactersNonPre(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertText(token[b'data'])

        def startTagProcessInHead(self, token):
            return self.parser.phases[b'inHead'].processStartTag(token)

        def startTagBody(self, token):
            self.parser.parseError(b'unexpected-start-tag', {b'name': b'body'})
            if len(self.tree.openElements) == 1 or self.tree.openElements[1].name != b'body':
                assert self.parser.innerHTML
            else:
                self.parser.framesetOK = False
                for attr, value in token[b'data'].items():
                    if attr not in self.tree.openElements[1].attributes:
                        self.tree.openElements[1].attributes[attr] = value

        def startTagFrameset(self, token):
            self.parser.parseError(b'unexpected-start-tag', {b'name': b'frameset'})
            if len(self.tree.openElements) == 1 or self.tree.openElements[1].name != b'body':
                assert self.parser.innerHTML
            elif not self.parser.framesetOK:
                pass
            else:
                if self.tree.openElements[1].parent:
                    self.tree.openElements[1].parent.removeChild(self.tree.openElements[1])
                while self.tree.openElements[(-1)].name != b'html':
                    self.tree.openElements.pop()

                self.tree.insertElement(token)
                self.parser.phase = self.parser.phases[b'inFrameset']

        def startTagCloseP(self, token):
            if self.tree.elementInScope(b'p', variant=b'button'):
                self.endTagP(impliedTagToken(b'p'))
            self.tree.insertElement(token)

        def startTagPreListing(self, token):
            if self.tree.elementInScope(b'p', variant=b'button'):
                self.endTagP(impliedTagToken(b'p'))
            self.tree.insertElement(token)
            self.parser.framesetOK = False
            self.processSpaceCharacters = self.processSpaceCharactersDropNewline

        def startTagForm(self, token):
            if self.tree.formPointer:
                self.parser.parseError(b'unexpected-start-tag', {b'name': b'form'})
            else:
                if self.tree.elementInScope(b'p', variant=b'button'):
                    self.endTagP(impliedTagToken(b'p'))
                self.tree.insertElement(token)
                self.tree.formPointer = self.tree.openElements[(-1)]

        def startTagListItem(self, token):
            self.parser.framesetOK = False
            stopNamesMap = {b'li': [b'li'], b'dt': [
                     b'dt', b'dd'], 
               b'dd': [
                     b'dt', b'dd']}
            stopNames = stopNamesMap[token[b'name']]
            for node in reversed(self.tree.openElements):
                if node.name in stopNames:
                    self.parser.phase.processEndTag(impliedTagToken(node.name, b'EndTag'))
                    break
                if node.nameTuple in specialElements and node.name not in ('address',
                                                                           'div',
                                                                           'p'):
                    break

            if self.tree.elementInScope(b'p', variant=b'button'):
                self.parser.phase.processEndTag(impliedTagToken(b'p', b'EndTag'))
            self.tree.insertElement(token)

        def startTagPlaintext(self, token):
            if self.tree.elementInScope(b'p', variant=b'button'):
                self.endTagP(impliedTagToken(b'p'))
            self.tree.insertElement(token)
            self.parser.tokenizer.state = self.parser.tokenizer.plaintextState

        def startTagHeading(self, token):
            if self.tree.elementInScope(b'p', variant=b'button'):
                self.endTagP(impliedTagToken(b'p'))
            if self.tree.openElements[(-1)].name in headingElements:
                self.parser.parseError(b'unexpected-start-tag', {b'name': token[b'name']})
                self.tree.openElements.pop()
            self.tree.insertElement(token)

        def startTagA(self, token):
            afeAElement = self.tree.elementInActiveFormattingElements(b'a')
            if afeAElement:
                self.parser.parseError(b'unexpected-start-tag-implies-end-tag', {b'startName': b'a', b'endName': b'a'})
                self.endTagFormatting(impliedTagToken(b'a'))
                if afeAElement in self.tree.openElements:
                    self.tree.openElements.remove(afeAElement)
                if afeAElement in self.tree.activeFormattingElements:
                    self.tree.activeFormattingElements.remove(afeAElement)
            self.tree.reconstructActiveFormattingElements()
            self.addFormattingElement(token)

        def startTagFormatting(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.addFormattingElement(token)

        def startTagNobr(self, token):
            self.tree.reconstructActiveFormattingElements()
            if self.tree.elementInScope(b'nobr'):
                self.parser.parseError(b'unexpected-start-tag-implies-end-tag', {b'startName': b'nobr', b'endName': b'nobr'})
                self.processEndTag(impliedTagToken(b'nobr'))
                self.tree.reconstructActiveFormattingElements()
            self.addFormattingElement(token)

        def startTagButton(self, token):
            if self.tree.elementInScope(b'button'):
                self.parser.parseError(b'unexpected-start-tag-implies-end-tag', {b'startName': b'button', b'endName': b'button'})
                self.processEndTag(impliedTagToken(b'button'))
                return token
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)
            self.parser.framesetOK = False

        def startTagAppletMarqueeObject(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)
            self.tree.activeFormattingElements.append(Marker)
            self.parser.framesetOK = False

        def startTagXmp(self, token):
            if self.tree.elementInScope(b'p', variant=b'button'):
                self.endTagP(impliedTagToken(b'p'))
            self.tree.reconstructActiveFormattingElements()
            self.parser.framesetOK = False
            self.parser.parseRCDataRawtext(token, b'RAWTEXT')

        def startTagTable(self, token):
            if self.parser.compatMode != b'quirks':
                if self.tree.elementInScope(b'p', variant=b'button'):
                    self.processEndTag(impliedTagToken(b'p'))
            self.tree.insertElement(token)
            self.parser.framesetOK = False
            self.parser.phase = self.parser.phases[b'inTable']

        def startTagVoidFormatting(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token[b'selfClosingAcknowledged'] = True
            self.parser.framesetOK = False

        def startTagInput(self, token):
            framesetOK = self.parser.framesetOK
            self.startTagVoidFormatting(token)
            if b'type' in token[b'data'] and token[b'data'][b'type'].translate(asciiUpper2Lower) == b'hidden':
                self.parser.framesetOK = framesetOK

        def startTagParamSource(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token[b'selfClosingAcknowledged'] = True

        def startTagHr(self, token):
            if self.tree.elementInScope(b'p', variant=b'button'):
                self.endTagP(impliedTagToken(b'p'))
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token[b'selfClosingAcknowledged'] = True
            self.parser.framesetOK = False

        def startTagImage(self, token):
            self.parser.parseError(b'unexpected-start-tag-treated-as', {b'originalName': b'image', b'newName': b'img'})
            self.processStartTag(impliedTagToken(b'img', b'StartTag', attributes=token[b'data'], selfClosing=token[b'selfClosing']))

        def startTagIsIndex(self, token):
            self.parser.parseError(b'deprecated-tag', {b'name': b'isindex'})
            if self.tree.formPointer:
                return
            form_attrs = {}
            if b'action' in token[b'data']:
                form_attrs[b'action'] = token[b'data'][b'action']
            self.processStartTag(impliedTagToken(b'form', b'StartTag', attributes=form_attrs))
            self.processStartTag(impliedTagToken(b'hr', b'StartTag'))
            self.processStartTag(impliedTagToken(b'label', b'StartTag'))
            if b'prompt' in token[b'data']:
                prompt = token[b'data'][b'prompt']
            else:
                prompt = b'This is a searchable index. Enter search keywords: '
            self.processCharacters({b'type': tokenTypes[b'Characters'], b'data': prompt})
            attributes = token[b'data'].copy()
            if b'action' in attributes:
                del attributes[b'action']
            if b'prompt' in attributes:
                del attributes[b'prompt']
            attributes[b'name'] = b'isindex'
            self.processStartTag(impliedTagToken(b'input', b'StartTag', attributes=attributes, selfClosing=token[b'selfClosing']))
            self.processEndTag(impliedTagToken(b'label'))
            self.processStartTag(impliedTagToken(b'hr', b'StartTag'))
            self.processEndTag(impliedTagToken(b'form'))

        def startTagTextarea(self, token):
            self.tree.insertElement(token)
            self.parser.tokenizer.state = self.parser.tokenizer.rcdataState
            self.processSpaceCharacters = self.processSpaceCharactersDropNewline
            self.parser.framesetOK = False

        def startTagIFrame(self, token):
            self.parser.framesetOK = False
            self.startTagRawtext(token)

        def startTagNoscript(self, token):
            if self.parser.scripting:
                self.startTagRawtext(token)
            else:
                self.startTagOther(token)

        def startTagRawtext(self, token):
            """iframe, noembed noframes, noscript(if scripting enabled)"""
            self.parser.parseRCDataRawtext(token, b'RAWTEXT')

        def startTagOpt(self, token):
            if self.tree.openElements[(-1)].name == b'option':
                self.parser.phase.processEndTag(impliedTagToken(b'option'))
            self.tree.reconstructActiveFormattingElements()
            self.parser.tree.insertElement(token)

        def startTagSelect(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)
            self.parser.framesetOK = False
            if self.parser.phase in (self.parser.phases[b'inTable'],
             self.parser.phases[b'inCaption'],
             self.parser.phases[b'inColumnGroup'],
             self.parser.phases[b'inTableBody'],
             self.parser.phases[b'inRow'],
             self.parser.phases[b'inCell']):
                self.parser.phase = self.parser.phases[b'inSelectInTable']
            else:
                self.parser.phase = self.parser.phases[b'inSelect']

        def startTagRpRt(self, token):
            if self.tree.elementInScope(b'ruby'):
                self.tree.generateImpliedEndTags()
                if self.tree.openElements[(-1)].name != b'ruby':
                    self.parser.parseError()
            self.tree.insertElement(token)

        def startTagMath(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.parser.adjustMathMLAttributes(token)
            self.parser.adjustForeignAttributes(token)
            token[b'namespace'] = namespaces[b'mathml']
            self.tree.insertElement(token)
            if token[b'selfClosing']:
                self.tree.openElements.pop()
                token[b'selfClosingAcknowledged'] = True

        def startTagSvg(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.parser.adjustSVGAttributes(token)
            self.parser.adjustForeignAttributes(token)
            token[b'namespace'] = namespaces[b'svg']
            self.tree.insertElement(token)
            if token[b'selfClosing']:
                self.tree.openElements.pop()
                token[b'selfClosingAcknowledged'] = True

        def startTagMisplaced(self, token):
            """ Elements that should be children of other elements that have a
            different insertion mode; here they are ignored
            "caption", "col", "colgroup", "frame", "frameset", "head",
            "option", "optgroup", "tbody", "td", "tfoot", "th", "thead",
            "tr", "noscript"
            """
            self.parser.parseError(b'unexpected-start-tag-ignored', {b'name': token[b'name']})

        def startTagOther(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)

        def endTagP(self, token):
            if not self.tree.elementInScope(b'p', variant=b'button'):
                self.startTagCloseP(impliedTagToken(b'p', b'StartTag'))
                self.parser.parseError(b'unexpected-end-tag', {b'name': b'p'})
                self.endTagP(impliedTagToken(b'p', b'EndTag'))
            else:
                self.tree.generateImpliedEndTags(b'p')
                if self.tree.openElements[(-1)].name != b'p':
                    self.parser.parseError(b'unexpected-end-tag', {b'name': b'p'})
                node = self.tree.openElements.pop()
                while node.name != b'p':
                    node = self.tree.openElements.pop()

        def endTagBody(self, token):
            if not self.tree.elementInScope(b'body'):
                self.parser.parseError()
                return
            if self.tree.openElements[(-1)].name != b'body':
                for node in self.tree.openElements[2:]:
                    if node.name not in frozenset(('dd', 'dt', 'li', 'optgroup', 'option',
                                                   'p', 'rp', 'rt', 'tbody', 'td',
                                                   'tfoot', 'th', 'thead', 'tr',
                                                   'body', 'html')):
                        self.parser.parseError(b'expected-one-end-tag-but-got-another', {b'gotName': b'body', b'expectedName': node.name})
                        break

            self.parser.phase = self.parser.phases[b'afterBody']

        def endTagHtml(self, token):
            if self.tree.elementInScope(b'body'):
                self.endTagBody(impliedTagToken(b'body'))
                return token

        def endTagBlock(self, token):
            if token[b'name'] == b'pre':
                self.processSpaceCharacters = self.processSpaceCharactersNonPre
            inScope = self.tree.elementInScope(token[b'name'])
            if inScope:
                self.tree.generateImpliedEndTags()
            if self.tree.openElements[(-1)].name != token[b'name']:
                self.parser.parseError(b'end-tag-too-early', {b'name': token[b'name']})
            if inScope:
                node = self.tree.openElements.pop()
                while node.name != token[b'name']:
                    node = self.tree.openElements.pop()

        def endTagForm(self, token):
            node = self.tree.formPointer
            self.tree.formPointer = None
            if node is None or not self.tree.elementInScope(node):
                self.parser.parseError(b'unexpected-end-tag', {b'name': b'form'})
            else:
                self.tree.generateImpliedEndTags()
                if self.tree.openElements[(-1)] != node:
                    self.parser.parseError(b'end-tag-too-early-ignored', {b'name': b'form'})
                self.tree.openElements.remove(node)
            return

        def endTagListItem(self, token):
            if token[b'name'] == b'li':
                variant = b'list'
            else:
                variant = None
            if not self.tree.elementInScope(token[b'name'], variant=variant):
                self.parser.parseError(b'unexpected-end-tag', {b'name': token[b'name']})
            else:
                self.tree.generateImpliedEndTags(exclude=token[b'name'])
                if self.tree.openElements[(-1)].name != token[b'name']:
                    self.parser.parseError(b'end-tag-too-early', {b'name': token[b'name']})
                node = self.tree.openElements.pop()
                while node.name != token[b'name']:
                    node = self.tree.openElements.pop()

            return

        def endTagHeading(self, token):
            for item in headingElements:
                if self.tree.elementInScope(item):
                    self.tree.generateImpliedEndTags()
                    break

            if self.tree.openElements[(-1)].name != token[b'name']:
                self.parser.parseError(b'end-tag-too-early', {b'name': token[b'name']})
            for item in headingElements:
                if self.tree.elementInScope(item):
                    item = self.tree.openElements.pop()
                    while item.name not in headingElements:
                        item = self.tree.openElements.pop()

                    break

        def endTagFormatting(self, token):
            """The much-feared adoption agency algorithm"""
            outerLoopCounter = 0
            while outerLoopCounter < 8:
                outerLoopCounter += 1
                formattingElement = self.tree.elementInActiveFormattingElements(token[b'name'])
                if not formattingElement or formattingElement in self.tree.openElements and not self.tree.elementInScope(formattingElement.name):
                    self.endTagOther(token)
                    return
                if formattingElement not in self.tree.openElements:
                    self.parser.parseError(b'adoption-agency-1.2', {b'name': token[b'name']})
                    self.tree.activeFormattingElements.remove(formattingElement)
                    return
                if not self.tree.elementInScope(formattingElement.name):
                    self.parser.parseError(b'adoption-agency-4.4', {b'name': token[b'name']})
                    return
                if formattingElement != self.tree.openElements[(-1)]:
                    self.parser.parseError(b'adoption-agency-1.3', {b'name': token[b'name']})
                afeIndex = self.tree.openElements.index(formattingElement)
                furthestBlock = None
                for element in self.tree.openElements[afeIndex:]:
                    if element.nameTuple in specialElements:
                        furthestBlock = element
                        break

                if furthestBlock is None:
                    element = self.tree.openElements.pop()
                    while element != formattingElement:
                        element = self.tree.openElements.pop()

                    self.tree.activeFormattingElements.remove(element)
                    return
                commonAncestor = self.tree.openElements[(afeIndex - 1)]
                bookmark = self.tree.activeFormattingElements.index(formattingElement)
                lastNode = node = furthestBlock
                innerLoopCounter = 0
                index = self.tree.openElements.index(node)
                while innerLoopCounter < 3:
                    innerLoopCounter += 1
                    index -= 1
                    node = self.tree.openElements[index]
                    if node not in self.tree.activeFormattingElements:
                        self.tree.openElements.remove(node)
                        continue
                    if node == formattingElement:
                        break
                    if lastNode == furthestBlock:
                        bookmark = self.tree.activeFormattingElements.index(node) + 1
                    clone = node.cloneNode()
                    self.tree.activeFormattingElements[self.tree.activeFormattingElements.index(node)] = clone
                    self.tree.openElements[self.tree.openElements.index(node)] = clone
                    node = clone
                    if lastNode.parent:
                        lastNode.parent.removeChild(lastNode)
                    node.appendChild(lastNode)
                    lastNode = node

                if lastNode.parent:
                    lastNode.parent.removeChild(lastNode)
                if commonAncestor.name in frozenset(('table', 'tbody', 'tfoot', 'thead',
                                                     'tr')):
                    parent, insertBefore = self.tree.getTableMisnestedNodePosition()
                    parent.insertBefore(lastNode, insertBefore)
                else:
                    commonAncestor.appendChild(lastNode)
                clone = formattingElement.cloneNode()
                furthestBlock.reparentChildren(clone)
                furthestBlock.appendChild(clone)
                self.tree.activeFormattingElements.remove(formattingElement)
                self.tree.activeFormattingElements.insert(bookmark, clone)
                self.tree.openElements.remove(formattingElement)
                self.tree.openElements.insert(self.tree.openElements.index(furthestBlock) + 1, clone)

            return

        def endTagAppletMarqueeObject(self, token):
            if self.tree.elementInScope(token[b'name']):
                self.tree.generateImpliedEndTags()
            if self.tree.openElements[(-1)].name != token[b'name']:
                self.parser.parseError(b'end-tag-too-early', {b'name': token[b'name']})
            if self.tree.elementInScope(token[b'name']):
                element = self.tree.openElements.pop()
                while element.name != token[b'name']:
                    element = self.tree.openElements.pop()

                self.tree.clearActiveFormattingElements()

        def endTagBr(self, token):
            self.parser.parseError(b'unexpected-end-tag-treated-as', {b'originalName': b'br', b'newName': b'br element'})
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(impliedTagToken(b'br', b'StartTag'))
            self.tree.openElements.pop()

        def endTagOther(self, token):
            for node in self.tree.openElements[::-1]:
                if node.name == token[b'name']:
                    self.tree.generateImpliedEndTags(exclude=token[b'name'])
                    if self.tree.openElements[(-1)].name != token[b'name']:
                        self.parser.parseError(b'unexpected-end-tag', {b'name': token[b'name']})
                    while self.tree.openElements.pop() != node:
                        pass

                    break
                elif node.nameTuple in specialElements:
                    self.parser.parseError(b'unexpected-end-tag', {b'name': token[b'name']})
                    break

    class TextPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              b'script', self.endTagScript)])
            self.endTagHandler.default = self.endTagOther

        def processCharacters(self, token):
            self.tree.insertText(token[b'data'])

        def processEOF(self):
            self.parser.parseError(b'expected-named-closing-tag-but-got-eof', {b'name': self.tree.openElements[(-1)].name})
            self.tree.openElements.pop()
            self.parser.phase = self.parser.originalPhase
            return True

        def startTagOther(self, token):
            assert False, b'Tried to process start tag %s in RCDATA/RAWTEXT mode' % token[b'name']

        def endTagScript(self, token):
            node = self.tree.openElements.pop()
            assert node.name == b'script'
            self.parser.phase = self.parser.originalPhase

        def endTagOther(self, token):
            self.tree.openElements.pop()
            self.parser.phase = self.parser.originalPhase

    class InTablePhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              b'caption', self.startTagCaption),
             (
              b'colgroup', self.startTagColgroup),
             (
              b'col', self.startTagCol),
             (
              ('tbody', 'tfoot', 'thead'), self.startTagRowGroup),
             (
              ('td', 'th', 'tr'), self.startTagImplyTbody),
             (
              b'table', self.startTagTable),
             (
              ('style', 'script'), self.startTagStyleScript),
             (
              b'input', self.startTagInput),
             (
              b'form', self.startTagForm)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              b'table', self.endTagTable),
             (
              ('body', 'caption', 'col', 'colgroup', 'html', 'tbody', 'td', 'tfoot', 'th', 'thead',
 'tr'), self.endTagIgnore)])
            self.endTagHandler.default = self.endTagOther

        def clearStackToTableContext(self):
            while self.tree.openElements[(-1)].name not in ('table', 'html'):
                self.tree.openElements.pop()

        def processEOF(self):
            if self.tree.openElements[(-1)].name != b'html':
                self.parser.parseError(b'eof-in-table')
            else:
                assert self.parser.innerHTML

        def processSpaceCharacters(self, token):
            originalPhase = self.parser.phase
            self.parser.phase = self.parser.phases[b'inTableText']
            self.parser.phase.originalPhase = originalPhase
            self.parser.phase.processSpaceCharacters(token)

        def processCharacters(self, token):
            originalPhase = self.parser.phase
            self.parser.phase = self.parser.phases[b'inTableText']
            self.parser.phase.originalPhase = originalPhase
            self.parser.phase.processCharacters(token)

        def insertText(self, token):
            self.tree.insertFromTable = True
            self.parser.phases[b'inBody'].processCharacters(token)
            self.tree.insertFromTable = False

        def startTagCaption(self, token):
            self.clearStackToTableContext()
            self.tree.activeFormattingElements.append(Marker)
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases[b'inCaption']

        def startTagColgroup(self, token):
            self.clearStackToTableContext()
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases[b'inColumnGroup']

        def startTagCol(self, token):
            self.startTagColgroup(impliedTagToken(b'colgroup', b'StartTag'))
            return token

        def startTagRowGroup(self, token):
            self.clearStackToTableContext()
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases[b'inTableBody']

        def startTagImplyTbody(self, token):
            self.startTagRowGroup(impliedTagToken(b'tbody', b'StartTag'))
            return token

        def startTagTable(self, token):
            self.parser.parseError(b'unexpected-start-tag-implies-end-tag', {b'startName': b'table', b'endName': b'table'})
            self.parser.phase.processEndTag(impliedTagToken(b'table'))
            if not self.parser.innerHTML:
                return token

        def startTagStyleScript(self, token):
            return self.parser.phases[b'inHead'].processStartTag(token)

        def startTagInput(self, token):
            if b'type' in token[b'data'] and token[b'data'][b'type'].translate(asciiUpper2Lower) == b'hidden':
                self.parser.parseError(b'unexpected-hidden-input-in-table')
                self.tree.insertElement(token)
                self.tree.openElements.pop()
            else:
                self.startTagOther(token)

        def startTagForm(self, token):
            self.parser.parseError(b'unexpected-form-in-table')
            if self.tree.formPointer is None:
                self.tree.insertElement(token)
                self.tree.formPointer = self.tree.openElements[(-1)]
                self.tree.openElements.pop()
            return

        def startTagOther(self, token):
            self.parser.parseError(b'unexpected-start-tag-implies-table-voodoo', {b'name': token[b'name']})
            self.tree.insertFromTable = True
            self.parser.phases[b'inBody'].processStartTag(token)
            self.tree.insertFromTable = False

        def endTagTable(self, token):
            if self.tree.elementInScope(b'table', variant=b'table'):
                self.tree.generateImpliedEndTags()
                if self.tree.openElements[(-1)].name != b'table':
                    self.parser.parseError(b'end-tag-too-early-named', {b'gotName': b'table', b'expectedName': self.tree.openElements[(-1)].name})
                while self.tree.openElements[(-1)].name != b'table':
                    self.tree.openElements.pop()

                self.tree.openElements.pop()
                self.parser.resetInsertionMode()
            else:
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagIgnore(self, token):
            self.parser.parseError(b'unexpected-end-tag', {b'name': token[b'name']})

        def endTagOther(self, token):
            self.parser.parseError(b'unexpected-end-tag-implies-table-voodoo', {b'name': token[b'name']})
            self.tree.insertFromTable = True
            self.parser.phases[b'inBody'].processEndTag(token)
            self.tree.insertFromTable = False

    class InTableTextPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.originalPhase = None
            self.characterTokens = []
            return

        def flushCharacters(self):
            data = (b'').join([ item[b'data'] for item in self.characterTokens ])
            if any([ item not in spaceCharacters for item in data ]):
                token = {b'type': tokenTypes[b'Characters'], b'data': data}
                self.parser.phases[b'inTable'].insertText(token)
            elif data:
                self.tree.insertText(data)
            self.characterTokens = []

        def processComment(self, token):
            self.flushCharacters()
            self.parser.phase = self.originalPhase
            return token

        def processEOF(self):
            self.flushCharacters()
            self.parser.phase = self.originalPhase
            return True

        def processCharacters(self, token):
            if token[b'data'] == b'\x00':
                return
            self.characterTokens.append(token)

        def processSpaceCharacters(self, token):
            self.characterTokens.append(token)

        def processStartTag(self, token):
            self.flushCharacters()
            self.parser.phase = self.originalPhase
            return token

        def processEndTag(self, token):
            self.flushCharacters()
            self.parser.phase = self.originalPhase
            return token

    class InCaptionPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              ('caption', 'col', 'colgroup', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr'), self.startTagTableElement)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              b'caption', self.endTagCaption),
             (
              b'table', self.endTagTable),
             (
              ('body', 'col', 'colgroup', 'html', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr'), self.endTagIgnore)])
            self.endTagHandler.default = self.endTagOther

        def ignoreEndTagCaption(self):
            return not self.tree.elementInScope(b'caption', variant=b'table')

        def processEOF(self):
            self.parser.phases[b'inBody'].processEOF()

        def processCharacters(self, token):
            return self.parser.phases[b'inBody'].processCharacters(token)

        def startTagTableElement(self, token):
            self.parser.parseError()
            ignoreEndTag = self.ignoreEndTagCaption()
            self.parser.phase.processEndTag(impliedTagToken(b'caption'))
            if not ignoreEndTag:
                return token

        def startTagOther(self, token):
            return self.parser.phases[b'inBody'].processStartTag(token)

        def endTagCaption(self, token):
            if not self.ignoreEndTagCaption():
                self.tree.generateImpliedEndTags()
                if self.tree.openElements[(-1)].name != b'caption':
                    self.parser.parseError(b'expected-one-end-tag-but-got-another', {b'gotName': b'caption', b'expectedName': self.tree.openElements[(-1)].name})
                while self.tree.openElements[(-1)].name != b'caption':
                    self.tree.openElements.pop()

                self.tree.openElements.pop()
                self.tree.clearActiveFormattingElements()
                self.parser.phase = self.parser.phases[b'inTable']
            else:
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagTable(self, token):
            self.parser.parseError()
            ignoreEndTag = self.ignoreEndTagCaption()
            self.parser.phase.processEndTag(impliedTagToken(b'caption'))
            if not ignoreEndTag:
                return token

        def endTagIgnore(self, token):
            self.parser.parseError(b'unexpected-end-tag', {b'name': token[b'name']})

        def endTagOther(self, token):
            return self.parser.phases[b'inBody'].processEndTag(token)

    class InColumnGroupPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              b'col', self.startTagCol)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              b'colgroup', self.endTagColgroup),
             (
              b'col', self.endTagCol)])
            self.endTagHandler.default = self.endTagOther

        def ignoreEndTagColgroup(self):
            return self.tree.openElements[(-1)].name == b'html'

        def processEOF(self):
            if self.tree.openElements[(-1)].name == b'html':
                if not self.parser.innerHTML:
                    raise AssertionError
                    return
                ignoreEndTag = self.ignoreEndTagColgroup()
                self.endTagColgroup(impliedTagToken(b'colgroup'))
                return ignoreEndTag or True

        def processCharacters(self, token):
            ignoreEndTag = self.ignoreEndTagColgroup()
            self.endTagColgroup(impliedTagToken(b'colgroup'))
            if not ignoreEndTag:
                return token

        def startTagCol(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token[b'selfClosingAcknowledged'] = True

        def startTagOther(self, token):
            ignoreEndTag = self.ignoreEndTagColgroup()
            self.endTagColgroup(impliedTagToken(b'colgroup'))
            if not ignoreEndTag:
                return token

        def endTagColgroup(self, token):
            if self.ignoreEndTagColgroup():
                assert self.parser.innerHTML
                self.parser.parseError()
            else:
                self.tree.openElements.pop()
                self.parser.phase = self.parser.phases[b'inTable']

        def endTagCol(self, token):
            self.parser.parseError(b'no-end-tag', {b'name': b'col'})

        def endTagOther(self, token):
            ignoreEndTag = self.ignoreEndTagColgroup()
            self.endTagColgroup(impliedTagToken(b'colgroup'))
            if not ignoreEndTag:
                return token

    class InTableBodyPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              b'tr', self.startTagTr),
             (
              ('td', 'th'), self.startTagTableCell),
             (
              ('caption', 'col', 'colgroup', 'tbody', 'tfoot', 'thead'),
              self.startTagTableOther)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              ('tbody', 'tfoot', 'thead'), self.endTagTableRowGroup),
             (
              b'table', self.endTagTable),
             (
              ('body', 'caption', 'col', 'colgroup', 'html', 'td', 'th', 'tr'), self.endTagIgnore)])
            self.endTagHandler.default = self.endTagOther

        def clearStackToTableBodyContext(self):
            while self.tree.openElements[(-1)].name not in ('tbody', 'tfoot', 'thead',
                                                            'html'):
                self.tree.openElements.pop()

            assert self.tree.openElements[(-1)].name == b'html' and self.parser.innerHTML

        def processEOF(self):
            self.parser.phases[b'inTable'].processEOF()

        def processSpaceCharacters(self, token):
            return self.parser.phases[b'inTable'].processSpaceCharacters(token)

        def processCharacters(self, token):
            return self.parser.phases[b'inTable'].processCharacters(token)

        def startTagTr(self, token):
            self.clearStackToTableBodyContext()
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases[b'inRow']

        def startTagTableCell(self, token):
            self.parser.parseError(b'unexpected-cell-in-table-body', {b'name': token[b'name']})
            self.startTagTr(impliedTagToken(b'tr', b'StartTag'))
            return token

        def startTagTableOther(self, token):
            if self.tree.elementInScope(b'tbody', variant=b'table') or self.tree.elementInScope(b'thead', variant=b'table') or self.tree.elementInScope(b'tfoot', variant=b'table'):
                self.clearStackToTableBodyContext()
                self.endTagTableRowGroup(impliedTagToken(self.tree.openElements[(-1)].name))
                return token
            assert self.parser.innerHTML
            self.parser.parseError()

        def startTagOther(self, token):
            return self.parser.phases[b'inTable'].processStartTag(token)

        def endTagTableRowGroup(self, token):
            if self.tree.elementInScope(token[b'name'], variant=b'table'):
                self.clearStackToTableBodyContext()
                self.tree.openElements.pop()
                self.parser.phase = self.parser.phases[b'inTable']
            else:
                self.parser.parseError(b'unexpected-end-tag-in-table-body', {b'name': token[b'name']})

        def endTagTable(self, token):
            if self.tree.elementInScope(b'tbody', variant=b'table') or self.tree.elementInScope(b'thead', variant=b'table') or self.tree.elementInScope(b'tfoot', variant=b'table'):
                self.clearStackToTableBodyContext()
                self.endTagTableRowGroup(impliedTagToken(self.tree.openElements[(-1)].name))
                return token
            assert self.parser.innerHTML
            self.parser.parseError()

        def endTagIgnore(self, token):
            self.parser.parseError(b'unexpected-end-tag-in-table-body', {b'name': token[b'name']})

        def endTagOther(self, token):
            return self.parser.phases[b'inTable'].processEndTag(token)

    class InRowPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              ('td', 'th'), self.startTagTableCell),
             (
              ('caption', 'col', 'colgroup', 'tbody', 'tfoot', 'thead', 'tr'), self.startTagTableOther)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              b'tr', self.endTagTr),
             (
              b'table', self.endTagTable),
             (
              ('tbody', 'tfoot', 'thead'), self.endTagTableRowGroup),
             (
              ('body', 'caption', 'col', 'colgroup', 'html', 'td', 'th'),
              self.endTagIgnore)])
            self.endTagHandler.default = self.endTagOther

        def clearStackToTableRowContext(self):
            while self.tree.openElements[(-1)].name not in ('tr', 'html'):
                self.parser.parseError(b'unexpected-implied-end-tag-in-table-row', {b'name': self.tree.openElements[(-1)].name})
                self.tree.openElements.pop()

        def ignoreEndTagTr(self):
            return not self.tree.elementInScope(b'tr', variant=b'table')

        def processEOF(self):
            self.parser.phases[b'inTable'].processEOF()

        def processSpaceCharacters(self, token):
            return self.parser.phases[b'inTable'].processSpaceCharacters(token)

        def processCharacters(self, token):
            return self.parser.phases[b'inTable'].processCharacters(token)

        def startTagTableCell(self, token):
            self.clearStackToTableRowContext()
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases[b'inCell']
            self.tree.activeFormattingElements.append(Marker)

        def startTagTableOther(self, token):
            ignoreEndTag = self.ignoreEndTagTr()
            self.endTagTr(impliedTagToken(b'tr'))
            if not ignoreEndTag:
                return token

        def startTagOther(self, token):
            return self.parser.phases[b'inTable'].processStartTag(token)

        def endTagTr(self, token):
            if not self.ignoreEndTagTr():
                self.clearStackToTableRowContext()
                self.tree.openElements.pop()
                self.parser.phase = self.parser.phases[b'inTableBody']
            else:
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagTable(self, token):
            ignoreEndTag = self.ignoreEndTagTr()
            self.endTagTr(impliedTagToken(b'tr'))
            if not ignoreEndTag:
                return token

        def endTagTableRowGroup(self, token):
            if self.tree.elementInScope(token[b'name'], variant=b'table'):
                self.endTagTr(impliedTagToken(b'tr'))
                return token
            self.parser.parseError()

        def endTagIgnore(self, token):
            self.parser.parseError(b'unexpected-end-tag-in-table-row', {b'name': token[b'name']})

        def endTagOther(self, token):
            return self.parser.phases[b'inTable'].processEndTag(token)

    class InCellPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              ('caption', 'col', 'colgroup', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr'), self.startTagTableOther)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              ('td', 'th'), self.endTagTableCell),
             (
              ('body', 'caption', 'col', 'colgroup', 'html'), self.endTagIgnore),
             (
              ('table', 'tbody', 'tfoot', 'thead', 'tr'), self.endTagImply)])
            self.endTagHandler.default = self.endTagOther

        def closeCell(self):
            if self.tree.elementInScope(b'td', variant=b'table'):
                self.endTagTableCell(impliedTagToken(b'td'))
            elif self.tree.elementInScope(b'th', variant=b'table'):
                self.endTagTableCell(impliedTagToken(b'th'))

        def processEOF(self):
            self.parser.phases[b'inBody'].processEOF()

        def processCharacters(self, token):
            return self.parser.phases[b'inBody'].processCharacters(token)

        def startTagTableOther(self, token):
            if self.tree.elementInScope(b'td', variant=b'table') or self.tree.elementInScope(b'th', variant=b'table'):
                self.closeCell()
                return token
            assert self.parser.innerHTML
            self.parser.parseError()

        def startTagOther(self, token):
            return self.parser.phases[b'inBody'].processStartTag(token)

        def endTagTableCell(self, token):
            if self.tree.elementInScope(token[b'name'], variant=b'table'):
                self.tree.generateImpliedEndTags(token[b'name'])
                if self.tree.openElements[(-1)].name != token[b'name']:
                    self.parser.parseError(b'unexpected-cell-end-tag', {b'name': token[b'name']})
                    while True:
                        node = self.tree.openElements.pop()
                        if node.name == token[b'name']:
                            break

                else:
                    self.tree.openElements.pop()
                self.tree.clearActiveFormattingElements()
                self.parser.phase = self.parser.phases[b'inRow']
            else:
                self.parser.parseError(b'unexpected-end-tag', {b'name': token[b'name']})

        def endTagIgnore(self, token):
            self.parser.parseError(b'unexpected-end-tag', {b'name': token[b'name']})

        def endTagImply(self, token):
            if self.tree.elementInScope(token[b'name'], variant=b'table'):
                self.closeCell()
                return token
            self.parser.parseError()

        def endTagOther(self, token):
            return self.parser.phases[b'inBody'].processEndTag(token)

    class InSelectPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              b'option', self.startTagOption),
             (
              b'optgroup', self.startTagOptgroup),
             (
              b'select', self.startTagSelect),
             (
              ('input', 'keygen', 'textarea'), self.startTagInput),
             (
              b'script', self.startTagScript)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              b'option', self.endTagOption),
             (
              b'optgroup', self.endTagOptgroup),
             (
              b'select', self.endTagSelect)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            if self.tree.openElements[(-1)].name != b'html':
                self.parser.parseError(b'eof-in-select')
            else:
                assert self.parser.innerHTML

        def processCharacters(self, token):
            if token[b'data'] == b'\x00':
                return
            self.tree.insertText(token[b'data'])

        def startTagOption(self, token):
            if self.tree.openElements[(-1)].name == b'option':
                self.tree.openElements.pop()
            self.tree.insertElement(token)

        def startTagOptgroup(self, token):
            if self.tree.openElements[(-1)].name == b'option':
                self.tree.openElements.pop()
            if self.tree.openElements[(-1)].name == b'optgroup':
                self.tree.openElements.pop()
            self.tree.insertElement(token)

        def startTagSelect(self, token):
            self.parser.parseError(b'unexpected-select-in-select')
            self.endTagSelect(impliedTagToken(b'select'))

        def startTagInput(self, token):
            self.parser.parseError(b'unexpected-input-in-select')
            if self.tree.elementInScope(b'select', variant=b'select'):
                self.endTagSelect(impliedTagToken(b'select'))
                return token
            assert self.parser.innerHTML

        def startTagScript(self, token):
            return self.parser.phases[b'inHead'].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError(b'unexpected-start-tag-in-select', {b'name': token[b'name']})

        def endTagOption(self, token):
            if self.tree.openElements[(-1)].name == b'option':
                self.tree.openElements.pop()
            else:
                self.parser.parseError(b'unexpected-end-tag-in-select', {b'name': b'option'})

        def endTagOptgroup(self, token):
            if self.tree.openElements[(-1)].name == b'option' and self.tree.openElements[(-2)].name == b'optgroup':
                self.tree.openElements.pop()
            if self.tree.openElements[(-1)].name == b'optgroup':
                self.tree.openElements.pop()
            else:
                self.parser.parseError(b'unexpected-end-tag-in-select', {b'name': b'optgroup'})

        def endTagSelect(self, token):
            if self.tree.elementInScope(b'select', variant=b'select'):
                node = self.tree.openElements.pop()
                while node.name != b'select':
                    node = self.tree.openElements.pop()

                self.parser.resetInsertionMode()
            else:
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagOther(self, token):
            self.parser.parseError(b'unexpected-end-tag-in-select', {b'name': token[b'name']})

    class InSelectInTablePhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              ('caption', 'table', 'tbody', 'tfoot', 'thead', 'tr', 'td', 'th'),
              self.startTagTable)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              ('caption', 'table', 'tbody', 'tfoot', 'thead', 'tr', 'td', 'th'),
              self.endTagTable)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            self.parser.phases[b'inSelect'].processEOF()

        def processCharacters(self, token):
            return self.parser.phases[b'inSelect'].processCharacters(token)

        def startTagTable(self, token):
            self.parser.parseError(b'unexpected-table-element-start-tag-in-select-in-table', {b'name': token[b'name']})
            self.endTagOther(impliedTagToken(b'select'))
            return token

        def startTagOther(self, token):
            return self.parser.phases[b'inSelect'].processStartTag(token)

        def endTagTable(self, token):
            self.parser.parseError(b'unexpected-table-element-end-tag-in-select-in-table', {b'name': token[b'name']})
            if self.tree.elementInScope(token[b'name'], variant=b'table'):
                self.endTagOther(impliedTagToken(b'select'))
                return token

        def endTagOther(self, token):
            return self.parser.phases[b'inSelect'].processEndTag(token)

    class InForeignContentPhase(Phase):
        breakoutElements = frozenset([b'b', b'big', b'blockquote', b'body', b'br',
         b'center', b'code', b'dd', b'div', b'dl', b'dt',
         b'em', b'embed', b'h1', b'h2', b'h3',
         b'h4', b'h5', b'h6', b'head', b'hr', b'i', b'img',
         b'li', b'listing', b'menu', b'meta', b'nobr',
         b'ol', b'p', b'pre', b'ruby', b's', b'small',
         b'span', b'strong', b'strike', b'sub', b'sup',
         b'table', b'tt', b'u', b'ul', b'var'])

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

        def adjustSVGTagNames(self, token):
            replacements = {b'altglyph': b'altGlyph', b'altglyphdef': b'altGlyphDef', 
               b'altglyphitem': b'altGlyphItem', 
               b'animatecolor': b'animateColor', 
               b'animatemotion': b'animateMotion', 
               b'animatetransform': b'animateTransform', 
               b'clippath': b'clipPath', 
               b'feblend': b'feBlend', 
               b'fecolormatrix': b'feColorMatrix', 
               b'fecomponenttransfer': b'feComponentTransfer', 
               b'fecomposite': b'feComposite', 
               b'feconvolvematrix': b'feConvolveMatrix', 
               b'fediffuselighting': b'feDiffuseLighting', 
               b'fedisplacementmap': b'feDisplacementMap', 
               b'fedistantlight': b'feDistantLight', 
               b'feflood': b'feFlood', 
               b'fefunca': b'feFuncA', 
               b'fefuncb': b'feFuncB', 
               b'fefuncg': b'feFuncG', 
               b'fefuncr': b'feFuncR', 
               b'fegaussianblur': b'feGaussianBlur', 
               b'feimage': b'feImage', 
               b'femerge': b'feMerge', 
               b'femergenode': b'feMergeNode', 
               b'femorphology': b'feMorphology', 
               b'feoffset': b'feOffset', 
               b'fepointlight': b'fePointLight', 
               b'fespecularlighting': b'feSpecularLighting', 
               b'fespotlight': b'feSpotLight', 
               b'fetile': b'feTile', 
               b'feturbulence': b'feTurbulence', 
               b'foreignobject': b'foreignObject', 
               b'glyphref': b'glyphRef', 
               b'lineargradient': b'linearGradient', 
               b'radialgradient': b'radialGradient', 
               b'textpath': b'textPath'}
            if token[b'name'] in replacements:
                token[b'name'] = replacements[token[b'name']]

        def processCharacters(self, token):
            if token[b'data'] == b'\x00':
                token[b'data'] = b'�'
            elif self.parser.framesetOK and any(char not in spaceCharacters for char in token[b'data']):
                self.parser.framesetOK = False
            Phase.processCharacters(self, token)

        def processStartTag(self, token):
            currentNode = self.tree.openElements[(-1)]
            if token[b'name'] in self.breakoutElements or token[b'name'] == b'font' and set(token[b'data'].keys()) & set([b'color', b'face', b'size']):
                self.parser.parseError(b'unexpected-html-element-in-foreign-content', {b'name': token[b'name']})
                while self.tree.openElements[(-1)].namespace != self.tree.defaultNamespace and not self.parser.isHTMLIntegrationPoint(self.tree.openElements[(-1)]) and not self.parser.isMathMLTextIntegrationPoint(self.tree.openElements[(-1)]):
                    self.tree.openElements.pop()

                return token
            if currentNode.namespace == namespaces[b'mathml']:
                self.parser.adjustMathMLAttributes(token)
            elif currentNode.namespace == namespaces[b'svg']:
                self.adjustSVGTagNames(token)
                self.parser.adjustSVGAttributes(token)
            self.parser.adjustForeignAttributes(token)
            token[b'namespace'] = currentNode.namespace
            self.tree.insertElement(token)
            if token[b'selfClosing']:
                self.tree.openElements.pop()
                token[b'selfClosingAcknowledged'] = True

        def processEndTag(self, token):
            nodeIndex = len(self.tree.openElements) - 1
            node = self.tree.openElements[(-1)]
            if node.name.translate(asciiUpper2Lower) != token[b'name']:
                self.parser.parseError(b'unexpected-end-tag', {b'name': token[b'name']})
            while True:
                if node.name.translate(asciiUpper2Lower) == token[b'name']:
                    if self.parser.phase == self.parser.phases[b'inTableText']:
                        self.parser.phase.flushCharacters()
                        self.parser.phase = self.parser.phase.originalPhase
                    while self.tree.openElements.pop() != node:
                        assert self.tree.openElements

                    new_token = None
                    break
                nodeIndex -= 1
                node = self.tree.openElements[nodeIndex]
                if node.namespace != self.tree.defaultNamespace:
                    continue
                else:
                    new_token = self.parser.phase.processEndTag(token)
                    break

            return new_token

    class AfterBodyPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([(b'html', self.endTagHtml)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            pass

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.openElements[0])

        def processCharacters(self, token):
            self.parser.parseError(b'unexpected-char-after-body')
            self.parser.phase = self.parser.phases[b'inBody']
            return token

        def startTagHtml(self, token):
            return self.parser.phases[b'inBody'].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError(b'unexpected-start-tag-after-body', {b'name': token[b'name']})
            self.parser.phase = self.parser.phases[b'inBody']
            return token

        def endTagHtml(self, name):
            if self.parser.innerHTML:
                self.parser.parseError(b'unexpected-end-tag-after-body-innerhtml')
            else:
                self.parser.phase = self.parser.phases[b'afterAfterBody']

        def endTagOther(self, token):
            self.parser.parseError(b'unexpected-end-tag-after-body', {b'name': token[b'name']})
            self.parser.phase = self.parser.phases[b'inBody']
            return token

    class InFramesetPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              b'frameset', self.startTagFrameset),
             (
              b'frame', self.startTagFrame),
             (
              b'noframes', self.startTagNoframes)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              b'frameset', self.endTagFrameset)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            if self.tree.openElements[(-1)].name != b'html':
                self.parser.parseError(b'eof-in-frameset')
            else:
                assert self.parser.innerHTML

        def processCharacters(self, token):
            self.parser.parseError(b'unexpected-char-in-frameset')

        def startTagFrameset(self, token):
            self.tree.insertElement(token)

        def startTagFrame(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()

        def startTagNoframes(self, token):
            return self.parser.phases[b'inBody'].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError(b'unexpected-start-tag-in-frameset', {b'name': token[b'name']})

        def endTagFrameset(self, token):
            if self.tree.openElements[(-1)].name == b'html':
                self.parser.parseError(b'unexpected-frameset-in-frameset-innerhtml')
            else:
                self.tree.openElements.pop()
            if not self.parser.innerHTML and self.tree.openElements[(-1)].name != b'frameset':
                self.parser.phase = self.parser.phases[b'afterFrameset']

        def endTagOther(self, token):
            self.parser.parseError(b'unexpected-end-tag-in-frameset', {b'name': token[b'name']})

    class AfterFramesetPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              b'noframes', self.startTagNoframes)])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.endTagHtml)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            pass

        def processCharacters(self, token):
            self.parser.parseError(b'unexpected-char-after-frameset')

        def startTagNoframes(self, token):
            return self.parser.phases[b'inHead'].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError(b'unexpected-start-tag-after-frameset', {b'name': token[b'name']})

        def endTagHtml(self, token):
            self.parser.phase = self.parser.phases[b'afterAfterFrameset']

        def endTagOther(self, token):
            self.parser.parseError(b'unexpected-end-tag-after-frameset', {b'name': token[b'name']})

    class AfterAfterBodyPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml)])
            self.startTagHandler.default = self.startTagOther

        def processEOF(self):
            pass

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.document)

        def processSpaceCharacters(self, token):
            return self.parser.phases[b'inBody'].processSpaceCharacters(token)

        def processCharacters(self, token):
            self.parser.parseError(b'expected-eof-but-got-char')
            self.parser.phase = self.parser.phases[b'inBody']
            return token

        def startTagHtml(self, token):
            return self.parser.phases[b'inBody'].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError(b'expected-eof-but-got-start-tag', {b'name': token[b'name']})
            self.parser.phase = self.parser.phases[b'inBody']
            return token

        def processEndTag(self, token):
            self.parser.parseError(b'expected-eof-but-got-end-tag', {b'name': token[b'name']})
            self.parser.phase = self.parser.phases[b'inBody']
            return token

    class AfterAfterFramesetPhase(Phase):

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = _utils.MethodDispatcher([
             (
              b'html', self.startTagHtml),
             (
              b'noframes', self.startTagNoFrames)])
            self.startTagHandler.default = self.startTagOther

        def processEOF(self):
            pass

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.document)

        def processSpaceCharacters(self, token):
            return self.parser.phases[b'inBody'].processSpaceCharacters(token)

        def processCharacters(self, token):
            self.parser.parseError(b'expected-eof-but-got-char')

        def startTagHtml(self, token):
            return self.parser.phases[b'inBody'].processStartTag(token)

        def startTagNoFrames(self, token):
            return self.parser.phases[b'inHead'].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError(b'expected-eof-but-got-start-tag', {b'name': token[b'name']})

        def processEndTag(self, token):
            self.parser.parseError(b'expected-eof-but-got-end-tag', {b'name': token[b'name']})

    return {b'initial': InitialPhase, 
       b'beforeHtml': BeforeHtmlPhase, 
       b'beforeHead': BeforeHeadPhase, 
       b'inHead': InHeadPhase, 
       b'inHeadNoscript': InHeadNoscriptPhase, 
       b'afterHead': AfterHeadPhase, 
       b'inBody': InBodyPhase, 
       b'text': TextPhase, 
       b'inTable': InTablePhase, 
       b'inTableText': InTableTextPhase, 
       b'inCaption': InCaptionPhase, 
       b'inColumnGroup': InColumnGroupPhase, 
       b'inTableBody': InTableBodyPhase, 
       b'inRow': InRowPhase, 
       b'inCell': InCellPhase, 
       b'inSelect': InSelectPhase, 
       b'inSelectInTable': InSelectInTablePhase, 
       b'inForeignContent': InForeignContentPhase, 
       b'afterBody': AfterBodyPhase, 
       b'inFrameset': InFramesetPhase, 
       b'afterFrameset': AfterFramesetPhase, 
       b'afterAfterBody': AfterAfterBodyPhase, 
       b'afterAfterFrameset': AfterAfterFramesetPhase}


def adjust_attributes(token, replacements):
    needs_adjustment = viewkeys(token[b'data']) & viewkeys(replacements)
    if needs_adjustment:
        token[b'data'] = OrderedDict((replacements.get(k, k), v) for k, v in token[b'data'].items())


def impliedTagToken(name, type=b'EndTag', attributes=None, selfClosing=False):
    if attributes is None:
        attributes = {}
    return {b'type': tokenTypes[type], b'name': name, b'data': attributes, b'selfClosing': selfClosing}


class ParseError(Exception):
    """Error in parsed document"""
    pass