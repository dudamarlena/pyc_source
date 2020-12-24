# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/synxml.py
# Compiled at: 2011-08-30 21:43:45
""" Interface for extending language support through the use of xml files

@summary: EditraXml Implementation

"""
xml_spec = '\n<editra version="1">\n   <syntax language="Python" lexer="STC_LEX_PYTHON" id="ID_LANG_PYTHON">\n\n      <associations value="py pyw"/>\n\n      <keywordlist>\n         <keywords value="0">\n             if else elif for while in\n         </keywords>\n         <keywords value="1">\n             str len setattr getattr\n         </keywords>\n      </keywordlist>\n\n      <syntaxspeclist>\n         <syntaxspec value="STC_P_DEFAULT" tag="default_style"/>\n         <syntaxspec value="STC_P_WORD" tag="keyword_style"/>\n      </syntaxspeclist>\n\n      <propertylist>\n         <property value="fold" enable="1"/>\n         <property value="tab.timmy.whinge.level" enable="1"/>\n      </propertylist>\n\n      <commentpattern value="#"/>\n\n      <featurelist>\n         <feature method="AutoIndenter" source="myextension.py"/>\n         <!-- <feature method="StyleText" source="myextension.py"/> -->\n      </featurelist>\n\n   </syntax>\n\n</editra>\n\n'
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: synxml.py 68814 2011-08-21 17:10:03Z CJP $'
__revision__ = '$Revision: 68814 $'
import os
from xml import sax
try:
    import wx.stc as stc
except ImportError:
    pass

EXML_START = 'editra'
EXML_SYNTAX = 'syntax'
EXML_KEYWORDLIST = 'keywordlist'
EXML_KEYWORDS = 'keywords'
EXML_SYNSPECLIST = 'syntaxspeclist'
EXML_SYNTAXSPEC = 'syntaxspec'
EXML_PROPERTYLIST = 'propertylist'
EXML_PROPERTY = 'property'
EXML_COMMENTPAT = 'commentpattern'
EXML_FEATURELIST = 'featurelist'
EXML_FEATURE = 'feature'
EXML_ASSOCIATIONS = 'associations'
EXML_ENABLE = 'enable'
EXML_LANG = 'language'
EXML_LEXER = 'lexer'
EXML_METHOD = 'method'
EXML_SOURCE = 'source'
EXML_TAG = 'tag'
EXML_VALUE = 'value'
EXML_VERSION = 'version'
EXML_NAME = 'name'
EXML_ID = 'id'

class EditraXml(sax.ContentHandler):
    """Base class for all Editra syntax xml objects"""

    def __init__(self, path=None):
        sax.ContentHandler.__init__(self)
        self.name = ''
        self.level = 0
        self.indent = 3
        self.path = path
        self._ok = False
        self._context = None
        self._reg_handler = dict()
        return

    def __eq__(self, other):
        return self.GetXml() == other.GetXml()

    def __str__(self):
        return self.GetXml()

    def startElement(self, name, attrs):
        if self._context is not None:
            self._context.startElement(name, attrs)
        elif name in self._reg_handler:
            self._context = self._reg_handler.get(name)
            self._context.startElement(name, attrs)
        return

    def endElement(self, name):
        if self._context is not None:
            if self._context.Name == name:
                self._context = None
            else:
                self._context.endElement(name)
        return

    def characters(self, chars):
        if not chars.isspace():
            if self._context is not None:
                self._context.characters(chars)
        return

    def GetXml(self):
        """Get the xml representation of this object
        @return: string

        """
        ident = self.GetIndentationStr()
        xml = ident + self.GetStartTag()
        xml += self.GetSubElements() + os.linesep
        xml += ident + self.GetEndTag()
        return xml

    def GetSubElements(self):
        """Get the sub elements
        @return: string

        """
        xml = ''
        for handler in self.GetHandlers():
            handler.SetLevel(self.Level + 1)
            xml += os.linesep + handler.GetXml()

        return xml

    def GetStartTag(self):
        """Get the opening tag
        @return: string

        """
        return '<%s>' % self.name

    def GetEndTag(self):
        """Get the closing tag
        @return: string

        """
        return '</%s>' % self.name

    def LoadFromDisk(self):
        """Load the object from from disk
        @precondition: path has been set
        @return: bool
        @todo: set error state on failed loads

        """
        assert self.path is not None, 'Must SetPath before calling Load'
        try:
            sax.parse(self.path, self)
        except (sax.SAXException, OSError, IOError, UnicodeDecodeError):
            self._ok = False
            return False

        self._ok = True
        return True
        return

    def LoadFromString(self, txt):
        """Load and initialize the object from an xml string
        @param txt: string

        """
        sax.parseString(txt, self)

    @property
    def Context(self):
        return self._context

    @property
    def Indentation(self):
        return self.indent

    @property
    def Level(self):
        return self.level

    @property
    def Name(self):
        return self.name

    @property
    def Ok(self):
        return self.IsOk()

    def GetHandler(self, tag):
        """Get the handler associated with the given tag
        @param tag: string
        @return: EditraXml object or None

        """
        return self._reg_handler.get(tag, None)

    def GetHandlers(self):
        """Get all the handlers registered with this element
        @return: list of EditraXml objects

        """
        return self._reg_handler.values()

    def GetIndentation(self):
        """Get the indentation string
        @return: int

        """
        return self.indent

    def GetIndentationStr(self):
        """Get the indentation string taking level into consideration
        @return: string

        """
        return self.indent * ' ' * self.level

    def GetLevel(self):
        """Get the level of this element
        @return: int

        """
        return self.level

    def GetName(self):
        """Get the tag name for the handler
        @return: string

        """
        return self.name

    def GetPath(self):
        """Get the xml files path
        @return: string

        """
        return self.path

    def IsOk(self):
        """Did the object load from file correctly?
        return: bool

        """
        return self._ok

    def RegisterHandler(self, handler):
        """Register a handler for a tag. Parsing will be delegated to the
        the registered handler until its end tag is encountered.
        @param handler: EditraXml instance

        """
        tag = handler.GetName()
        assert tag not in self._reg_handler, '%s already registered!' % tag
        handler.SetLevel(self.Level + 1)
        self._reg_handler[tag] = handler

    def SetIndentation(self, indent):
        """Set the indentation level
        @param indent: int

        """
        self.indent = indent

    def SetLevel(self, level):
        """Set the level of this element
        @param level: int

        """
        self.level = level

    def SetName(self, tag):
        """Set this handlers tag name used for identifying the open and
        end tags.
        @param tag: string

        """
        self.name = tag

    def SetPath(self, path):
        """Set the path to load this element from
        @param path: path

        """
        self.path = path


class SyntaxModeHandler(EditraXml):
    """Main Xml interface to extending filetype handling support"""

    def __init__(self, path=None):
        EditraXml.__init__(self, path)
        self._start = False
        self._version = 0
        self.syntax = Syntax()
        self.SetName(EXML_START)
        self.SetIndentation(3)
        self.RegisterHandler(self.syntax)

    def startElement(self, name, attrs):
        if self._start:
            EditraXml.startElement(self, name, attrs)
        elif name == EXML_START:
            self._version = int(attrs.get(EXML_VERSION, 0))
            self._start = True

    def endElement(self, name):
        if name == EXML_START:
            self._start = False
        else:
            EditraXml.endElement(self, name)

    def GetStartTag(self):
        return '<%s version="%s">' % (self.GetName(), self.Version)

    @property
    def CommentPattern(self):
        return self.GetCommentPattern()

    @property
    def FileExtensions(self):
        return self.GetFileExtensions()

    @property
    def Keywords(self):
        return self.GetKeywords()

    @property
    def LangId(self):
        return self.GetLangId()

    @property
    def Lexer(self):
        return self.GetLexer()

    @property
    def Properties(self):
        return self.GetProperties()

    @property
    def SyntaxSpec(self):
        return self.GetSyntaxSpec()

    @property
    def Version(self):
        return self._version

    def GetCommentPattern(self):
        """Get the comment pattern list
        @return: list of strings

        """
        return self.syntax.GetCommentPattern()

    def GetFileExtensions(self):
        """Get the list of associated file extensions
        @return: list of strings

        """
        return self.syntax.GetFileExtensions()

    def GetKeywords(self):
        """Get the keyword list
        @return: list of tuples [(idx, ['word', 'word2',]),]

        """
        kwxml = self.syntax.GetKeywordXml()
        return kwxml.GetKeywords()

    def GetFeatureFromXml(self, fet):
        """Get the callable associated with the given feature
        @param fet: string
        @return: string

        """
        fetxml = self.syntax.GetFeatureXml()
        return fetxml.GetFeature(fet)

    def GetSyntaxSpec(self):
        """Get the syntax spec
        @return: list of tuples [(style_id, "style_tag")]

        """
        spxml = self.syntax.GetSyntaxSpecXml()
        return spxml.GetStyleSpecs()

    def GetLangId(self):
        """Get the language id string
        @return: str "ID_LANG_"

        """
        return self.syntax.GetLangId()

    def GetLanguage(self):
        """Get the language name string
        @return: string

        """
        return self.syntax.GetLanguage()

    def GetLexer(self):
        """Get the lexer id
        @return: wx.stc.STC_LEX_

        """
        return self.syntax.GetLexer()

    def GetProperties(self):
        """Get the property defs
        @return: list of tuples [("fold", "1"),]

        """
        propxml = self.syntax.GetPropertiesXml()
        return propxml.GetProperties()


class Syntax(EditraXml):
    """Syntax definition for initializing a Scintilla Lexer"""

    def __init__(self):
        EditraXml.__init__(self)
        self.language = 'Plain Text'
        self.langid = 'ID_LANG_TXT'
        self.lexstr = 'STC_LEX_NULL'
        self.lexer = stc.STC_LEX_NULL
        self.file_ext = list()
        self.keywords = KeywordList()
        self.synspec = SyntaxSpecList()
        self.props = PropertyList()
        self.features = FeatureList()
        self.comment = list()
        self.SetName(EXML_SYNTAX)
        self.RegisterHandler(self.keywords)
        self.RegisterHandler(self.synspec)
        self.RegisterHandler(self.props)
        self.RegisterHandler(self.features)

    def startElement(self, name, attrs):
        """Parse the Syntax Xml"""
        if name == EXML_COMMENTPAT:
            val = attrs.get(EXML_VALUE, '')
            tmp = val.split()
            if len(tmp) == 1:
                comment = [
                 val]
            else:
                comment = tmp
            self.comment = comment
        elif name == EXML_ASSOCIATIONS:
            self.file_ext = attrs.get(EXML_VALUE, '').split()
        elif name == self.Name:
            lang = attrs.get(EXML_LANG, 'Plain Text')
            langid = attrs.get(EXML_ID, 'ID_LANG_TXT')
            assert langid.startswith('ID_LANG_'), 'id must start with ID_LANG_'
            lexer = attrs.get(EXML_LEXER, 'STC_LEX_NULL')
            lexval = getattr(stc, lexer, None)
            assert lexval is not None, 'Invalid Lexer: %s' % lexer
            self.language = lang
            self.langid = langid
            self.lexstr = lexer
            self.lexer = lexval
        else:
            EditraXml.startElement(self, name, attrs)
        return

    def GetStartTag(self):
        """Get the syntax opening tag and attributes"""
        return '<%s %s="%s" %s="%s" %s="%s">' % (self.Name, EXML_LANG,
         self.language, EXML_LEXER,
         self.lexstr, EXML_ID,
         self.langid)

    def GetSubElements(self):
        """Get the SubElements xml string
        @return: string

        """
        xml = EditraXml.GetSubElements(self)
        ident = self.GetIndentationStr() + self.Indentation * ' '
        xml += os.linesep
        cpat = (' ').join(self.GetCommentPattern())
        comment = '<%s %s="%s"/>' % (EXML_COMMENTPAT, EXML_VALUE, cpat.strip())
        xml += os.linesep
        xml += ident + comment
        xml += os.linesep
        fileext = '<%s %s="%s"/>' % (EXML_ASSOCIATIONS, EXML_VALUE, (' ').join(self.file_ext))
        xml += ident + fileext
        return xml

    def GetCommentPattern(self):
        """Get the comment pattern
        @return: list of strings ["/*", "*/"]

        """
        return self.comment

    def GetFeatureXml(self):
        """Get the FeatureList xml object"""
        return self.features

    def GetFileExtensions(self):
        """Get the list of associated file extensions"""
        return self.file_ext

    def GetKeywordXml(self):
        """Get the Keyword Xml object"""
        return self.keywords

    def GetLanguage(self):
        """Get the language description/name
        @return: string

        """
        return self.language

    def GetLangId(self):
        """Get the language id
        @return: string

        """
        return self.langid

    def GetLexer(self):
        """Get the lexer to use for this language
        @return: stc.STC_LEX_FOO

        """
        return self.lexer

    def GetSyntaxSpecXml(self):
        """Get the Syntax Spec Xml object"""
        return self.synspec

    def GetPropertiesXml(self):
        """Get the properties xml object"""
        return self.props


class KeywordList(EditraXml):
    """Container object for all keyword sets"""

    def __init__(self):
        EditraXml.__init__(self)
        self._current = None
        self._keywords = dict()
        self.SetName(EXML_KEYWORDLIST)
        return

    def startElement(self, name, attrs):
        if name == EXML_KEYWORDS:
            idx = attrs.get(EXML_VALUE, None)
            assert idx is not None, 'value attribute not set'
            idx = int(idx)
            assert idx not in self._keywords, 'Duplicate index set %d' % idx
            self._keywords[idx] = list()
            self._current = self._keywords[idx]
        return

    def endElement(self, name):
        if name == EXML_KEYWORDS:
            self._current = None
        return

    def characters(self, chars):
        chars = chars.strip().split()
        if self._current is not None:
            if len(chars):
                self._current.extend(chars)
        return

    def GetSubElements(self):
        """Get the keyword list elements"""
        xml = ''
        tag = '<%s %s=' % (EXML_KEYWORDS, EXML_VALUE)
        tag += '"%s">'
        end = '</%s>' % EXML_KEYWORDS
        ident = self.GetIndentationStr() + self.Indentation * ' '
        for key in sorted(self._keywords.keys()):
            xml += os.linesep + ident
            xml += tag % key
            xml += os.linesep + ident
            words = self.Indentation * ' ' + (' ').join(self._keywords[key])
            xml += words
            xml += os.linesep + ident
            xml += end

        return xml

    def GetKeywords(self):
        """Get the list of keyword strings
        @return: sorted list of tuples [(kw_idx, [word1, word2,])]

        """
        keys = sorted(self._keywords.keys())
        keywords = [ (idx, self._keywords[idx]) for idx in keys ]
        keywords.sort(key=lambda x: x[0])
        return keywords

    def GetKeywordList(self, idx):
        """Get the list of keywords associated with the given index
        @return: list of strings

        """
        return self._keywords.get(idx, None)


class SyntaxSpecList(EditraXml):
    """Container element for holding the syntax specification elements"""

    def __init__(self):
        EditraXml.__init__(self)
        self._specs = list()
        self.SetName(EXML_SYNSPECLIST)

    def startElement(self, name, attrs):
        """Parse all syntaxspec elements in the list"""
        if name == EXML_SYNTAXSPEC:
            lid = attrs.get(EXML_VALUE, '')
            assert len(lid), 'Style Id not specified'
            if lid.isdigit():
                style_id = int(lid)
            else:
                style_id = getattr(stc, lid, None)
                assert style_id is not None, 'Invalid STC Value: %s' % lid
                assert isinstance(style_id, int), 'Invalid ID: %s' % lid
            self._specs.append((style_id, attrs.get(EXML_TAG, 'default_style')))
        return

    def GetSubElements(self):
        """Get the xml for all the syntax spec elements"""
        xml = ''
        tag = '<%s %s=' % (EXML_SYNTAXSPEC, EXML_VALUE)
        tag += '"%s" ' + EXML_TAG + '="%s"/>'
        ident = self.GetIndentationStr() + self.Indentation * ' '
        for spec in self._specs:
            xml += os.linesep + ident
            xml += tag % spec

        return xml

    def GetStyleSpecs(self):
        """Get the list of keyword strings
        @return: list of tuples [(style_id, "style_tag"),]

        """
        return self._specs


class PropertyList(EditraXml):
    """Container class for the syntax properties"""

    def __init__(self):
        EditraXml.__init__(self)
        self.properties = list()
        self.SetName(EXML_PROPERTYLIST)

    def startElement(self, name, attrs):
        if name == EXML_PROPERTY:
            prop = attrs.get(EXML_VALUE, '')
            if prop:
                enable = attrs.get(EXML_ENABLE, '0')
                self.properties.append((prop, enable))

    def GetSubElements(self):
        xml = ''
        tag = '<%s %s=' % (EXML_PROPERTY, EXML_VALUE)
        tag += '"%s" ' + EXML_ENABLE + '="%s"/>'
        ident = self.GetIndentationStr() + self.Indentation * ' '
        for prop in self.properties:
            xml += os.linesep + ident
            xml += tag % prop

        return xml

    def GetProperties(self):
        """Get the list of properties
        @return: list of tuples [("property", "1")]

        """
        return self.properties


class FeatureList(EditraXml):
    """Container for all other misc syntax features.
    Currently Available Features:
      - AutoIndent
      - StyleText

    """

    def __init__(self):
        EditraXml.__init__(self)
        self._features = dict()
        self.SetName(EXML_FEATURELIST)

    def startElement(self, name, attrs):
        if name == EXML_FEATURE:
            meth = attrs.get(EXML_METHOD, None)
            assert meth is not None, 'method not defined'
            mod = attrs.get(EXML_SOURCE, None)
            assert mod is not None, 'source not defined'
            self._features[meth] = mod
        else:
            EditraXml.startElement(self, name, attrs)
        return

    def GetSubElements(self):
        xml = ''
        tag = '<%s %s=' % (EXML_FEATURE, EXML_METHOD)
        tag += '"%s" ' + EXML_SOURCE + '="%s"/>'
        ident = self.GetIndentationStr() + self.Indentation * ' '
        for feature in self._features.iteritems():
            xml += os.linesep + ident
            xml += tag % feature

        return xml

    def GetFeature(self, fet):
        """Get the callable feature by name
        @param fet: string (module name)

        """
        feature = None
        src = self._features.get(fet, None)
        if src is not None:
            feature = src
        return feature


def LoadHandler(path):
    """Load and initialize a SyntaxModeHandler from an on disk xml config file
    @param path: path to an EditraXml file to load a handler from
    @return: SyntaxModeHandler instance

    """
    synmode = SyntaxModeHandler(path)
    synmode.LoadFromDisk()
    return synmode