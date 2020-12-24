# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/golem/helpers/dict.py
# Compiled at: 2008-09-08 11:14:55
from lxml import etree
import golem, sys, random, md5
from xml.sax.saxutils import quoteattr

class ConfigError(Exception):
    __module__ = __name__


class input_dict(dict):
    __module__ = __name__

    def __init__(self, *args, **kwargs):
        super(dict, self).__init__(*args, **kwargs)

    def read_config(self, filename):
        """ Parse an 'input config' file, generating the entries needed to make 
            the dictionary being compiled be able to generate input for this code."""
        for line in open(filename, 'r'):
            frags = line.split()
            if len(frags) == 4:
                self[frags[0]] = input_obj(*frags)
            if len(frags) == 8:
                idetc = frags[0:4]
                remainder = frags[4:]
                for x in range(len(remainder)):
                    if remainder[x] == 'None':
                        remainder[x] = None
                    else:
                        remainder[x] = remainder[x].split(',')

                args = idetc + remainder
                self[args[0]] = input_obj(*args)

        return


class input_obj(object):
    __module__ = __name__

    def __init__(self, inpd, keyword, format, type, bounds=None, shape=None, name=None, options=None):
        """ A concept from an 'input config' file. See input_dict for more details."""
        self.written = False
        if name != None:
            self.name = name[0]
        else:
            self.name = None
        self.id = inpd
        self.keyword = keyword
        if format == 'block':
            self.block = True
            self.symmetric = False
        elif format == 'sblock':
            self.block = True
            self.symmetric = True
        elif format == 'inline':
            self.block = False
        else:
            raise ConfigError('Invalid input configuration file: block syntax')
        if type is 'int' or 'float' or 'string':
            self.type = type
        else:
            raise ConfigError('Invalid input configuration file: unknown type')
        if bounds != None:
            try:
                if bounds[0] != 'None':
                    self.min = float(bounds[0])
                else:
                    self.min = None
                if bounds[1] != 'None':
                    self.max = float(bounds[1])
                else:
                    self.max = None
            except TypeError:
                raise ConfigError('Invalid input configuration file: invalid bounds')
            except IndexError:
                raise ConfigError('Invalid input configuration file: malformed bounds')

        else:
            self.min = None
            self.max = None
        if shape != None:
            try:
                self.xdim = int(shape[0])
                self.ydim = int(shape[1])
            except IndexError:
                raise ConfigError('Invalid input configuration file: malformed shape')
            except TypeError:
                raise ConfigError('Invalid input configuration file: invalid shape')

        else:
            self.xdim = 1
            self.ydim = 1
        if options:
            self.options = options
        else:
            self.options = None
        return

    def toggleWritten(self):
        if self.written == False:
            self.written = True
        elif self.written == True:
            self.written = False

    def generate_xml_castep(self):
        self.toggleWritten()
        gxsl = '\n    <golem:template role="arb_to_input" binding="input" input="external">\n      <xsl:stylesheet version=\'1.0\' \n                      xmlns:xsl=\'http://www.w3.org/1999/XSL/Transform\'\n                      xmlns:cml=\'http://www.xml-cml.org/schema\'>\n        <xsl:strip-space elements="*" />\n        <xsl:output method="text" />'
        size = 1 * self.xdim * self.ydim
        params = [ 'p' + str(x + 1) for x in range(size) ]
        for p in params:
            gxsl += '\n        <xsl:param name="%s" />' % p

        gxsl += '\n        <xsl:template match="/">'
        if self.block:
            gxsl += '\n        <xsl:text>%%BLOCK %s </xsl:text>\n        ' % self.keyword
            for i in range(self.ydim):
                for j in range(self.xdim):
                    param = params.pop(0)
                    gxsl += "<xsl:value-of select='$%s' /><xsl:text> </xsl:text>" % param

                gxsl += '<xsl:text>\n</xsl:text>'

            gxsl += '<xsl:text>%%ENDBLOCK %s</xsl:text>' % self.keyword
        else:
            gxsl += '\n          <xsl:text>%s </xsl:text><xsl:value-of select="$%s" />' % (self.keyword, params[0])
        gxsl += '        </xsl:template>\n      </xsl:stylesheet>\n    </golem:template>'
        return gxsl

    def generate_bounds_and_type(self):
        if hasattr(self, 'type'):
            if self.block:
                if self.symmetric:
                    symm = 'true'
                else:
                    symm = 'false'
                bounds_str = '<golem:possibleValues type="matrix">\n    <golem:matrix dimensionx="%s" dimensiony="%s" type="%s" symmetric="%s"/>\n' % (self.xdim, self.ydim, self.type, symm)
            elif self.xdim != self.ydim and self.xdim != 1:
                raise ConfigError('Malformed matrix; inconsistent with                                       block format')
            else:
                bounds_str = '<golem:possibleValues type="%s">\n' % self.type
            if self.min or self.max:
                bounds_str += '      <golem:range>\n'
                if self.min:
                    bounds_str += '        <golem:min>%s</golem:min>\n' % self.min
                if self.max:
                    bounds_str += '        <golem:max>%s</golem:max>\n' % self.max
                bounds_str += '      </golem:range>\n'
            elif self.options:
                bounds_str += '      <golem:enumeration>\n'
                for option in self.options:
                    bounds_str += '        <golem:value>%s</golem:value>\n' % option

                bounds_str += '      </golem:enumeration>\n'
            bounds_str += '    </golem:possibleValues>\n'
            return bounds_str
        else:
            return ''


class concept(dict):
    """ Abstract representation of a 'concept' within a corpus of XML data; ie, a 
    common structure used to denote a semantically-meaningful unit within a collection
    of semi-structured documents."""
    __module__ = __name__

    def __init__(self, keys, parentConcept):
        dict.__init__(self, keys)
        self.parentConcept = [parentConcept]

    def __eq__(self, other):
        if self is None and other is None:
            return True
        elif self is None or other is None:
            return False
        elif dict.__eq__(self, other):
            return True
        else:
            return False
        return


class cmlconcept(concept):
    """
    Concept extracted from a corpus of CML data.
    
    When analysing a corpus of CML data in order to produce a dictionary, every dictRef
    encountered is mapped to an instance of this class; therefore, this class contains
    helper methods to output 
    """
    __module__ = __name__

    def __init__(self, keys, parentConcept):
        concept.__init__(self, keys, parentConcept)
        self.payload = None
        self.relative = None
        return

    def prettyprint(self):
        if self['tag'].startswith('{http://www.xml-cml.org/schema}'):
            tag = self['tag'].split('}')[1]
        else:
            tag = self['tag']
        pstr = '<%s' % tag
        if self['id'] is not None:
            pstr += ' id=' + quoteattr(self['id'])
        if self['dictRef'] is not None:
            pstr += ' dictRef=' + quoteattr(self['dictRef'])
        if self['title'] is not None:
            pstr += ' title=' + quoteattr(self['title'])
        if self['name'] is not None:
            pstr += ' name=' + quoteattr(self['name'])
        pstr += '>'
        return pstr

    def xpathfragment(self, id=True, title=True):
        """ Calculate an XPath expression which identifies an XML node corresponding to
        the current concept.
        
        This XPath expression ignores the document context in which the concept was
        found - ie, "//%%s" %% (xpath) would find all instances of this concept within
        a given XML document."""
        if self['tag'].startswith('{http://www.xml-cml.org/schema}'):
            tag = 'cml:' + self['tag'].split('}')[1]
        else:
            tag = self['tag']
        pstr = '%s' % tag
        if self['dictRef'] is not None:
            (ns, suffix) = self['dictRef'][1:].split('}')
            addition = "[(substring-after(@dictRef, ':')='%s' and @dictRef[../namespace::*[name()=substring-before(../@dictRef,':')]='%s']) or (@dictRef='%s' and namespace::*[name()='']='%s')]" % (suffix, ns, suffix, ns)
            pstr += addition
        elif self['name'] is not None:
            (ns, suffix) = self['name'][1:].split('}')
            addition = "[(substring-after(@name, ':')='%s' and @name[../namespace::*[name()=substring-before(../@name,':')]='%s']) or (@name='%s' and namespace::*[name()='']='%s')]" % (suffix, ns, suffix, ns)
            pstr += addition
        elif self['id'] is not None and id:
            pstr += '[@id=' + quoteattr(self['id']) + ']'
        elif self['title'] is not None and title:
            pstr += '[@title=' + quoteattr(self['title']) + ']'
        return pstr

    def setPayload(self, payloadtype):
        """ Set the payload of this concept - the type of data, if any, it contains. """
        self.payload = payloadtype

    def setRelative(self):
        """ State that this concept is relatively, not absolutely, positioned. 
        
        A relatively-positioned concept occurs in more than one location within
        the documents in this corpus (as distinguished by XPath expressions); 
        an absolutely-positioned concept always occurs in the same place. """
        self.relative = True

    def isRelative(self):
        """ Is this concept relatively-positioned? """
        return self.relative

    def hasPayload(self):
        """ Does this concept have a payload (is self.payload not None)?"""
        if self.payload:
            return True


class conceptset(dict):
    """ A collection of the concepts found in a corpus of documents we're analysing. """
    __module__ = __name__

    def __init__(self, keys):
        dict.__init__(self, {})
        self.keys = keys

    def addconcept(self, concept):
        """ Add a concept to this conceptset. """
        try:
            tk = ''
            for k in range(1, len(self.keys)):
                if concept[self.keys[k]] is not None:
                    tk = str(k) + '_' + concept[self.keys[k]]
                    break

            if len(tk) == 0:
                if len(concept.parentConcept) == 1 and concept.parentConcept[0] is not None:
                    tk = 'childOf_' + concept.parentConcept[0][self.keys[0]]
                else:
                    if concept['tag'] == '{http://www.xml-cml.org/cml}cml':
                        raise KeyError
                    tk = md5.md5(str(random.random())).hexdigest()
            keys = concept[self.keys[0]] + tk
            existing_concept = self[keys]
            if concept.parentConcept[0] not in existing_concept.parentConcept:
                existing_concept.parentConcept.extend(concept.parentConcept)
        except KeyError:
            self[keys] = concept

        return concept


def get_namespaced_attribute(element, attribute_name):
    att_raw = element.get(attribute_name)
    try:
        (prefix, suffix) = att_raw.split(':')
    except ValueError:
        prefix, suffix = None, att_raw
    except AttributeError:
        return

    try:
        namespace = element.nsmap[prefix]
    except KeyError:
        namespace = element.nsmap[None]

    nse = '{%s}%s' % (namespace, suffix)
    return nse


def parsecmlelement(element, parent):
    """ Parse a chunk of CML representing a concept to an instance of ``cmlconcept``."""
    tag = element.tag
    if isinstance(tag, basestring):
        if tag != '{http://www.xml-cml.org/schema}metadata':
            name = None
            id = element.get('id')
            dictRef = get_namespaced_attribute(element, 'dictRef')
            title = element.get('title')
        else:
            dictRef = None
            name = get_namespaced_attribute(element, 'name')
            id = None
            title = None
        return cmlconcept({'tag': tag, 'name': name, 'dictRef': dictRef, 'id': id, 'title': title}, parent)
    else:
        return
    return


def parsecmltree(element, conceptset, parent=None):
    """ Parse an entire CML tree, recursively, parsing any concepts found and adding
    them to the supplied ``conceptset``."""
    for e in element.getchildren():
        elem = parsecmlelement(e, parent)
        if elem is not None:
            concept = conceptset.addconcept(elem)
            parsecmltree(e, conceptset, parent=concept)

    return conceptset


def print_tree(concepttree):
    """ Dump a tree of concepts found in a corpus of documents as a GraphViz .dot file."""
    print 'digraph elements {'
    for k in concepts:
        for y in [ x.parentConcept for x in concepts[k] ]:
            rstr = '{rank = same; ' + (';').join([ '"%s"' % p.prettyprint() for p in y if p is not None if isinstance(p['tag'], basestring) ]) + '}'
            print rstr
            for z in y:
                for alpha in concepts[k]:
                    if z is not None and alpha is not None:
                        if isinstance(z['tag'], basestring) and isinstance(alpha['tag'], basestring):
                            print '"%s"->"%s"' % (z.prettyprint(), alpha.prettyprint())

    print '}'
    return


def xpath_concept(c, concepts, id=True, title=True):
    """ Calculate the XPath for a given concept in a given corpus of documents,
    by backtracking over its parents to determine the longest common
    - ie, most specific - path which captures all instances of it within the corpus."""
    if c['id'] == None and c['dictRef'] == None and c['title'] == None and c['tag'] != '{http://www.xml-cml.org/schema}metadata':
        return
    elif isinstance(c['tag'], basestring):
        terminated = False
        xpath = c.xpathfragment(id=id, title=title)
        backtrack = [c]
        while True:
            if len(backtrack) == 1 and len(backtrack[0].parentConcept) == 1:
                if backtrack[0].parentConcept[0] is not None and isinstance(backtrack[0].parentConcept[0]['tag'], basestring):
                    xpath = backtrack[0].parentConcept[0].xpathfragment(id=id, title=title) + '/' + xpath
                    backtrack = backtrack[0].parentConcept
                else:
                    terminated = True
                    xpath = '/' + xpath
                    break
            else:
                pcs = []
                for conc in backtrack:
                    if conc is not None:
                        pcs.extend(conc.parentConcept)

                if len(pcs) == 0:
                    terminated = True
                    xpath = '/' + xpath
                    break
                xpf = []
                breakflag = False
                if len(pcs) != 1:
                    c.setRelative()
                for concept in pcs:
                    if concept is not None:
                        xpf.append(concept.xpathfragment(id=id, title=title))
                    else:
                        breakflag = True

                if breakflag:
                    break
                for frag in xpf:
                    if frag != xpf[0]:
                        breakflag = True

                if breakflag:
                    break
                xpath = xpf[0] + '/' + xpath
                backtrack = pcs

        if not terminated:
            if xpath.startswith('cml:cml/'):
                xpath = '/' + xpath
            else:
                xpath = './/' + xpath
                c.setRelative()
        return xpath
    return


def print_xpaths(concepts):
    for k in concepts:
        c = concepts[k]
        if c.hasPayload():
            xpath = xpath_concept(c, concepts)
            if xpath is not None:
                print xpath

    return


def print_dictheader(ns, prefix, title):
    """ Return the common header for a CML/Golem dictionary with given namespace,
    short name, and title."""
    header = '<?xml version="1.0"?>\n<dictionary \n  namespace="%s"\n  dictionaryPrefix="%s" \n  title="%s"\n  xmlns="http://www.xml-cml.org/schema"\n  xmlns:h="http://www.w3.org/1999/xhtml/"\n  xmlns:cml="http://www.xml-cml.org/schema"\n  xmlns:xsd="http://www.w3.org/2001/XMLSchema"\n  xmlns:golem="http://www.lexical.org.uk/golem"\n  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n\n  <metadataList>\n    <metadata name="dc:creator" content="golem-kiln" />\n  </metadataList>\n\n  <!-- This dictionary created using pyGolem -->\n' % (ns, prefix, title)
    return header


def print_dictfooter():
    """ Return the common footer - including data-parsing XSLT stylesheets - for a
    CML/Golem dictionary. """
    footer = '\n\n\n   <!-- pyGolem Internals. DO NOT EDIT BEYOND THIS POINT UNLESS YOU\n        KNOW WHAT YOU ARE DOING - or things will probably stop working. -->\n        \n   <!--\n     XSLT found in this dictionary is licensed according to the following\n     terms:\n     \n     Copyright (c) 2005-2008 Toby White <tow21@cam.ac.uk>\n               (c) 2007-2008 Andrew Walkingshaw <andrew@lexical.org.uk>\n               \n     Permission is hereby granted, free of charge, to any person obtaining \n     a copy of this software and associated documentation files (the \n     "Software"), to deal in the Software without restriction, including \n     without limitation the rights to use, copy, modify, merge, publish, \n     distribute, sublicense, and/or sell copies of the Software, and to \n     permit persons to whom the Software is furnished to do so, subject to \n     the following conditions:\n\n     The above copyright notice and this permission notice shall be \n      included in all copies or substantial portions of the Software.\n\n     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS \n     OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF \n     MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. \n     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY \n     CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, \n     TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE \n     SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n   -->\n\n  <entry id="gwtsystem" term="INTERNAL ENTRY for golem web tool use">\n    <definition/>\n    <description/>\n    <metadataList/>\n    <golem:seealso>gwtsystem</golem:seealso>\n  </entry>\n\n  <entry id="absolute" term="Absolutely-positioned concept">\n    <definition>Concept which only occurs once in a document</definition>\n    <description>\n      <h:p>Absolutely-positioned concepts occur exactly once in a document,\n           and therefore do not need to be located by specifying a given \n           grouping concept (or chain of grouping concepts).\n      </h:p>\n    </description>\n    <metadataList>\n      <metadata name="dc:author" content="golem-kiln" />\n    </metadataList>\n    <golem:seealso>gwtsystem</golem:seealso>\n  </entry>\n\n  <entry id="relative" term="Relatively-positioned concept">\n    <definition>Concept which may occur many times in a document</definition>\n    <description>\n      <h:p>Relatively-positioned concepts can occur more than once in a \n           document, and therefore need to be located by specifying a given \n           grouping concept (or chain of grouping concepts).\n      </h:p>\n    </description>\n    <metadataList>\n      <metadata name="dc:author" content="golem-kiln" />\n    </metadataList>\n    <golem:seealso>gwtsystem</golem:seealso>\n  </entry>\n\n  <entry id="grouping" term="Grouping concept">\n    <definition>Concept acting as a container for other concepts</definition>\n    <description>\n      <h:p>\n      Grouping concepts do not directly contain values; instead, they contain\n      other, relatively positioned, concepts, which themselves may or may not\n      contain values.\n      </h:p>\n    </description>          \n    <metadataList>\n      <metadata name="dc:author" content="golem-kiln" />\n    </metadataList>\n    <golem:seealso>gwtsystem</golem:seealso>\n  </entry>\n\n  <entry id="value" term="Value-bearing concept">\n    <definition>Concept with a direct payload of data</definition>\n    <description>\n      <h:p>\n        Value-bearing concepts directly contain observables -\n        data with a value we can extract and evaluate.\n      </h:p>\n    </description>\n    <metadataList>\n      <metadata name="dc:author" content="golem-kiln" />\n    </metadataList>\n    <golem:seealso>gwtsystem</golem:seealso>\n  </entry>\n\n  <entry id="parameterInInput" term="Input parameter">\n    <definition>User-specified input parameters for the simulation.</definition>\n    <description>\n      <h:p>\n      </h:p>\n    </description>\n    <metadataList>\n      <metadata name="dc:author" content="golem-kiln" />\n    </metadataList>\n    <golem:seealso>gwtsystem</golem:seealso>\n  </entry>\n\n  <entry id="convertibleToInput" term="Input parameter">\n    <definition>User-specified input parameters with defined transforms to\n    code-native input.</definition>\n    <description>\n      <h:p>\n      </h:p>\n    </description>\n    <metadataList>\n      <metadata name="dc:author" content="golem-kiln" />\n    </metadataList>\n    <golem:seealso>gwtsystem</golem:seealso>\n  </entry>\n  \n  <entry id="inFinalProperties" term="Final property">\n    <definition>A concept appearing the final properties of a task.</definition>\n    <description>\n    </description>\n    <metadataList>\n      <metadata name="dc:author" content="golem-kiln" />\n    </metadataList>\n    <golem:seealso>gwtsystem</golem:seealso>\n  </entry>\n\n  <entry id="atomArray" term="FoX Atom array parser">\n    <annotation />\n    <definition />\n    <description />\n    <metadataList />\n    <golem:template role="getvalue" binding="pygolem_serialization">\n      <xsl:stylesheet version=\'1.0\' \n\t\txmlns:xsl=\'http://www.w3.org/1999/XSL/Transform\'\n\t\txmlns:cml=\'http://www.xml-cml.org/schema\'\n\t\txmlns:str="http://exslt.org/strings"\n\t\textension-element-prefixes="str"\n\t\t>\n      <xsl:output method="text" />\n      <xsl:template match="/">\n        <xsl:apply-templates />\n      </xsl:template>\n      <xsl:template match="cml:atomArray">\n        <xsl:text>[[</xsl:text>\n        <xsl:for-each select="cml:atom">\n          <xsl:text>["</xsl:text><xsl:value-of select="@elementType" /><xsl:text>"</xsl:text>\n          <xsl:text>,</xsl:text>\n          <xsl:value-of select="@xFract" />\n          <xsl:text>,</xsl:text>\n          <xsl:value-of select="@yFract" />\n          <xsl:text>,</xsl:text>\n          <xsl:value-of select="@zFract" />\n          <xsl:text>,</xsl:text>\n          <xsl:choose>\n            <xsl:when test="@occupancy">\n              <xsl:value-of select="@occupancy" />\n            </xsl:when>\n            <xsl:otherwise>\n              <xsl:text>1</xsl:text>\n            </xsl:otherwise>\n          </xsl:choose>\n          <xsl:text>,</xsl:text>\n          <xsl:choose>\n\t    <xsl:when test="@id">\n\t      <xsl:text>"</xsl:text><xsl:value-of select="@id" /><xsl:text>"</xsl:text>\n\t    </xsl:when>\n\t    <xsl:otherwise>\n\t      <xsl:text>"Unspecified"</xsl:text>\n\t    </xsl:otherwise>\n          </xsl:choose>\n          <xsl:choose>\n\t    <xsl:when test="position() != last()">\n\t      <xsl:text>],</xsl:text>\n\t    </xsl:when>\n\t    <xsl:otherwise>\n\t      <xsl:text>]</xsl:text>\n\t    </xsl:otherwise>\n          </xsl:choose>\n        </xsl:for-each>\n        <xsl:text>], ""]</xsl:text>\n      </xsl:template>\n      </xsl:stylesheet>\n    </golem:template>\n    <golem:xpath>.//cml:atomArray</golem:xpath>\n  </entry>\n  \n  <entry id="lattice" term="Set of lattice vectors - generic read">\n    <annotation />\n    <definition />\n    <description />\n    <metadataList />\n    <golem:template role="getvalue" binding="pygolem_serialization">\n\n      <xsl:stylesheet version=\'1.0\' \n\t\t      xmlns:xsl=\'http://www.w3.org/1999/XSL/Transform\'\n\t\t      xmlns:cml=\'http://www.xml-cml.org/schema\'\n\t\t      xmlns:str="http://exslt.org/strings"\n\t\t      extension-element-prefixes="str"\n\t\t      >\n\t<xsl:output method="text" />\n\n\t<xsl:template match="/">\n\t  <xsl:apply-templates />\n\t</xsl:template>\n\t\n\t<xsl:template match="cml:lattice">\n\t  <xsl:text>[</xsl:text>\n\t  <xsl:for-each select="cml:latticeVector">\n\t    <xsl:text>[</xsl:text> \n\t    <xsl:for-each select="str:tokenize(string(.), \' \')" >\n\t      <xsl:choose>\n\t\t<xsl:when test="position() != last()">\n\t\t  <xsl:value-of select="." /><xsl:text>,</xsl:text>\n\t\t</xsl:when>\n\t\t<xsl:otherwise>\n\t\t  <xsl:value-of select="." />\n\t\t</xsl:otherwise>\n\t      </xsl:choose>\n\t    </xsl:for-each>\n\t    <xsl:choose>\n\t      <xsl:when test="position() != last()">\n\t\t<xsl:text>],</xsl:text>\n\t      </xsl:when>\n\t      <xsl:otherwise>\n\t\t<xsl:text>]</xsl:text>\n\t      </xsl:otherwise>\n\t    </xsl:choose>\n\t  </xsl:for-each>\n\t  <xsl:text>]</xsl:text>\n\t</xsl:template>\n      </xsl:stylesheet>\n    </golem:template>\n    <golem:xpath>.//cml:lattice</golem:xpath>\n    <golem:possibleValues type="matrix">\n      <golem:matrix dimensionx="3" dimensiony="3" type="float" symmetric="false"/>\n      <golem:range>\n\t<golem:minimum>0</golem:minimum>\n      </golem:range>\n    </golem:possibleValues>\n  </entry>\n  \n  <entry id="metadata" term="Metadata default call">\n    <annotation />\n    <definition />\n    <description />\n    <metadataList />\n    <golem:template role="getvalue" binding="pygolem_serialization">\n        <xsl:stylesheet version=\'1.0\' \n                xmlns:xsl=\'http://www.w3.org/1999/XSL/Transform\'\n\t\txmlns:cml=\'http://www.xml-cml.org/schema\'\n\t\txmlns:str="http://exslt.org/strings"\n\t\txmlns:func="http://exslt.org/functions"\n\t\txmlns:exsl="http://exslt.org/common"\n\t\txmlns:tohw="http://www.uszla.me.uk/xsl/1.0/functions"\n\t\textension-element-prefixes="func exsl tohw str"\n\t\texclude-result-prefixes="exsl func tohw xsl str">\n        <xsl:output method="text" />\n        <xsl:template match="/">\n          <xsl:apply-templates />\n        </xsl:template>    \n\t<xsl:template match="cml:metadata">\n\t  <xsl:text>["</xsl:text><xsl:value-of select="@content" /><xsl:text>", "golem:metadata"]</xsl:text>\n\t</xsl:template>\n      </xsl:stylesheet>\n    </golem:template>\n  </entry>\n  \n  <entry id="matrix" term="Matrix default call">\n    <annotation />\n    <definition />\n    <description />\n    <metadataList />\n    <golem:template role="getvalue" binding="pygolem_serialization">\n        <xsl:stylesheet version=\'1.0\' \n                xmlns:xsl=\'http://www.w3.org/1999/XSL/Transform\'\n\t\txmlns:cml=\'http://www.xml-cml.org/schema\'\n\t\txmlns:str="http://exslt.org/strings"\n\t\txmlns:func="http://exslt.org/functions"\n\t\txmlns:exsl="http://exslt.org/common"\n\t\txmlns:tohw="http://www.uszla.me.uk/xsl/1.0/functions"\n\t\textension-element-prefixes="func exsl tohw str"\n\t\texclude-result-prefixes="exsl func tohw xsl str">\n        <xsl:output method="text" />\n  \n  <func:function name="tohw:isAListOfDigits">\n    <!-- look only for [0-9]+ -->\n    <xsl:param name="x_"/>\n    <xsl:variable name="x" select="normalize-space($x_)"/>\n    <xsl:choose>\n      <xsl:when test="string-length($x)=0">\n        <func:result select="false()"/>\n      </xsl:when>\n      <xsl:when test="substring($x, 1, 1)=\'0\' or\n                      substring($x, 1, 1)=\'1\' or\n                      substring($x, 1, 1)=\'2\' or\n                      substring($x, 1, 1)=\'3\' or\n                      substring($x, 1, 1)=\'4\' or\n                      substring($x, 1, 1)=\'5\' or\n                      substring($x, 1, 1)=\'6\' or\n                      substring($x, 1, 1)=\'7\' or\n                      substring($x, 1, 1)=\'8\' or\n                      substring($x, 1, 1)=\'9\'">\n        <xsl:choose>\n          <xsl:when test="string-length($x)=1">\n            <func:result select="true()"/>\n          </xsl:when>\n          <xsl:otherwise>\n            <func:result select="tohw:isAListOfDigits(substring($x, 2))"/>\n          </xsl:otherwise>\n        </xsl:choose>\n      </xsl:when>\n      <xsl:otherwise>\n        <func:result select="false()"/>\n      </xsl:otherwise>\n    </xsl:choose>\n  </func:function>\n\n  <func:function name="tohw:isAnInteger">\n    <!-- numbers fitting [\\+-][0-9]+ -->\n    <xsl:param name="x_"/>\n    <xsl:variable name="x" select="normalize-space($x_)"/>\n    <xsl:variable name="try">\n      <xsl:choose>\n        <xsl:when test="starts-with($x, \'+\')">\n          <xsl:value-of select="substring($x,2)"/>\n        </xsl:when>\n        <xsl:when test="starts-with($x, \'-\')">\n          <xsl:value-of select="substring($x,2)"/>\n        </xsl:when>\n        <xsl:otherwise>\n          <xsl:value-of select="$x"/>\n        </xsl:otherwise>\n      </xsl:choose>\n    </xsl:variable>\n    <func:result select="tohw:isAListOfDigits($try)"/>\n  </func:function>\n\n  <func:function name="tohw:isANumberWithoutExponent">\n    <!-- numbers fitting [\\+-][0-9]+(\\.[0-9]*) -->\n    <xsl:param name="x"/>\n    <xsl:choose>\n      <xsl:when test="contains($x, \'.\')">\n        <func:result select="tohw:isAnInteger(substring-before($x, \'.\')) and\n                             tohw:isAListOfDigits(substring-after($x, \'.\'))"/>\n      </xsl:when>\n      <xsl:otherwise>\n        <func:result select="tohw:isAnInteger($x)"/>\n      </xsl:otherwise>\n    </xsl:choose>\n  </func:function>\n\n  <func:function name="tohw:isAnFPNumber">\n    <!-- Try and interpret a string as an exponential number -->\n    <!-- should only recognise strings of the form: [\\+-][0-9]*\\.[0-9]*([DdEe][\\+-][0-9]+)? -->\n    <xsl:param name="x"/>\n    <xsl:choose>\n      <xsl:when test="contains($x, \'d\')">\n        <func:result select="tohw:isANumberWithoutExponent(substring-before($x, \'d\')) and\n                             tohw:isAnInteger(substring-after($x, \'d\'))"/>\n      </xsl:when>\n      <xsl:when test="contains($x, \'D\')">\n        <func:result select="tohw:isANumberWithoutExponent(substring-before($x, \'D\')) and\n                             tohw:isAnInteger(substring-after($x, \'D\'))"/>\n      </xsl:when>\n      <xsl:when test="contains($x, \'e\')">\n        <func:result select="tohw:isANumberWithoutExponent(substring-before($x, \'e\')) and\n                             tohw:isAnInteger(substring-after($x, \'e\'))"/>\n      </xsl:when>\n      <xsl:when test="contains($x, \'E\')">\n        <func:result select="tohw:isANumberWithoutExponent(substring-before($x, \'E\')) and\n                             tohw:isAnInteger(substring-after($x, \'E\'))"/>\n      </xsl:when>\n      <xsl:otherwise>\n         <func:result select="tohw:isANumberWithoutExponent($x)"/>\n      </xsl:otherwise>\n    </xsl:choose>\n  </func:function>\n  \n      <xsl:output method="text" />\n  \n      <xsl:template match="/">\n        <xsl:apply-templates />\n      </xsl:template>\n    \n      <xsl:template match="cml:matrix">\n        <xsl:param name="rowlength">\n          <xsl:value-of select="@columns" />\n        </xsl:param>\n        <xsl:text>[[[</xsl:text>\n        <xsl:for-each select="str:tokenize(string(.), \' \')" >\n          <xsl:choose>\n            <xsl:when test="position() = last()">\n              <xsl:choose>\n                <xsl:when test="tohw:isAnFPNumber(.)">\n                  <xsl:value-of select="." /><xsl:text>]</xsl:text>\n                </xsl:when>\n                <xsl:otherwise>\n                  <xsl:text>"</xsl:text><xsl:value-of select="." /><xsl:text>"]</xsl:text>\n                </xsl:otherwise>\n              </xsl:choose>\n            </xsl:when>\n            <xsl:when test="position() mod $rowlength = 0">\n              <xsl:choose>\n                <xsl:when test="tohw:isAnFPNumber(.)">\n                  <xsl:value-of select="." /><xsl:text>],[</xsl:text>\n                </xsl:when>\n                <xsl:otherwise>\n                  <xsl:text>"</xsl:text><xsl:value-of select="." /><xsl:text>"],[</xsl:text>\n                </xsl:otherwise>\n              </xsl:choose>\n            </xsl:when>\n            <xsl:otherwise>\n              <xsl:choose>\n                <xsl:when test="tohw:isAnFPNumber(.)">\n                  <xsl:value-of select="." /><xsl:text>,</xsl:text>\n                </xsl:when>\n                <xsl:otherwise>\n                  <xsl:text>"</xsl:text><xsl:value-of select="." /><xsl:text>",</xsl:text>\n                </xsl:otherwise>\n              </xsl:choose>\n            </xsl:otherwise>\n          </xsl:choose>\n        </xsl:for-each>\n        <xsl:text>],</xsl:text>\n        <xsl:choose>\n          <xsl:when test="@units">\n            <xsl:text>"</xsl:text><xsl:value-of select="@units" /><xsl:text>"</xsl:text>\n          </xsl:when>\n          <xsl:otherwise>\n            <xsl:text>""</xsl:text>\n          </xsl:otherwise>\n        </xsl:choose>\n        <xsl:text>]</xsl:text>\n      </xsl:template>\n      </xsl:stylesheet>\n    </golem:template>\n    <golem:seealso>gwtsystem</golem:seealso>\n  </entry>\n\n  <entry id="cellParameter" term="Cell parameter default call">\n    <annotation />\n    <definition />\n    <description />\n    <metadataList />\n    <golem:template role="getvalue" binding="pygolem_serialization">\n      <xsl:stylesheet version=\'1.0\' \n                      xmlns:xsl=\'http://www.w3.org/1999/XSL/Transform\'\n                      xmlns:cml=\'http://www.xml-cml.org/schema\'\n                      xmlns:str="http://exslt.org/strings"\n                      extension-element-prefixes="str"\n                      >\n        <xsl:output method="text" />\n        \n        <xsl:template match="/">\n          <xsl:apply-templates />\n        </xsl:template>\n    \n        <xsl:template match="cml:cellParameter[@parameterType=\'length\']">\n          <xsl:text>[[[</xsl:text>\n          <xsl:for-each select="str:tokenize(string(.), \' \')" >\n            <xsl:choose>\n              <xsl:when test="position() = last()">\n                <xsl:value-of select="." />\n              </xsl:when>\n              <xsl:otherwise>\n                <xsl:value-of select="." /><xsl:text>,</xsl:text>\n              </xsl:otherwise>\n            </xsl:choose>\n          </xsl:for-each>\n          <xsl:text>],</xsl:text>\n          <xsl:choose>\n            <xsl:when test="@units">\n              <xsl:text>"</xsl:text><xsl:value-of select="@units" /><xsl:text>"</xsl:text>\n            </xsl:when>\n            <xsl:otherwise>\n              <xsl:text>""</xsl:text>\n            </xsl:otherwise>\n          </xsl:choose>\n          <xsl:text>],[[</xsl:text>\n        </xsl:template>\n        \n        <xsl:template match="cml:cellParameter[@parameterType=\'angle\']">\n          <xsl:for-each select="str:tokenize(string(.), \' \')" >\n            <xsl:choose>\n              <xsl:when test="position() = last()">\n                <xsl:value-of select="." />\n              </xsl:when>\n              <xsl:otherwise>\n                <xsl:value-of select="." /><xsl:text>,</xsl:text>\n              </xsl:otherwise>\n            </xsl:choose>\n          </xsl:for-each>\n          <xsl:text>],</xsl:text>\n          <xsl:choose>\n            <xsl:when test="@units">\n              <xsl:text>"</xsl:text><xsl:value-of select="@units" /><xsl:text>"</xsl:text>\n            </xsl:when>\n            <xsl:otherwise>\n              <xsl:text>""</xsl:text>\n            </xsl:otherwise>\n          </xsl:choose>\n          <xsl:text>]]</xsl:text>\n        </xsl:template>\n      </xsl:stylesheet>\n    </golem:template>\n    <golem:seealso>gwtsystem</golem:seealso>\n  </entry>\n\n  <entry id="array" term="Array default call">\n    <annotation />\n    <definition />\n    <description />\n    <metadataList />\n    <golem:template role="getvalue" binding="pygolem_serialization">\n        <xsl:stylesheet version=\'1.0\' \n                xmlns:xsl=\'http://www.w3.org/1999/XSL/Transform\'\n\t\txmlns:cml=\'http://www.xml-cml.org/schema\'\n\t\txmlns:str="http://exslt.org/strings"\n\t\txmlns:func="http://exslt.org/functions"\n\t\txmlns:exsl="http://exslt.org/common"\n\t\txmlns:tohw="http://www.uszla.me.uk/xsl/1.0/functions"\n\t\textension-element-prefixes="func exsl tohw str"\n\t\texclude-result-prefixes="exsl func tohw xsl str">\n        <xsl:output method="text" />\n    \n  <func:function name="golemxsl:escape">\n    <xsl:param name="text"/>\n    <func:result select=\'str:replace($text, "&apos;", "\\&apos;")\'/>\n  </func:function>\n  \n  <func:function name="tohw:isAListOfDigits">\n    <!-- look only for [0-9]+ -->\n    <xsl:param name="x_"/>\n    <xsl:variable name="x" select="normalize-space($x_)"/>\n    <xsl:choose>\n      <xsl:when test="string-length($x)=0">\n        <func:result select="false()"/>\n      </xsl:when>\n      <xsl:when test="substring($x, 1, 1)=\'0\' or\n                      substring($x, 1, 1)=\'1\' or\n                      substring($x, 1, 1)=\'2\' or\n                      substring($x, 1, 1)=\'3\' or\n                      substring($x, 1, 1)=\'4\' or\n                      substring($x, 1, 1)=\'5\' or\n                      substring($x, 1, 1)=\'6\' or\n                      substring($x, 1, 1)=\'7\' or\n                      substring($x, 1, 1)=\'8\' or\n                      substring($x, 1, 1)=\'9\'">\n        <xsl:choose>\n          <xsl:when test="string-length($x)=1">\n            <func:result select="true()"/>\n          </xsl:when>\n          <xsl:otherwise>\n            <func:result select="tohw:isAListOfDigits(substring($x, 2))"/>\n          </xsl:otherwise>\n        </xsl:choose>\n      </xsl:when>\n      <xsl:otherwise>\n        <func:result select="false()"/>\n      </xsl:otherwise>\n    </xsl:choose>\n  </func:function>\n\n  <func:function name="tohw:isAnInteger">\n    <!-- numbers fitting [\\+-][0-9]+ -->\n    <xsl:param name="x_"/>\n    <xsl:variable name="x" select="normalize-space($x_)"/>\n    <xsl:variable name="try">\n      <xsl:choose>\n        <xsl:when test="starts-with($x, \'+\')">\n          <xsl:value-of select="substring($x,2)"/>\n        </xsl:when>\n        <xsl:when test="starts-with($x, \'-\')">\n          <xsl:value-of select="substring($x,2)"/>\n        </xsl:when>\n        <xsl:otherwise>\n          <xsl:value-of select="$x"/>\n        </xsl:otherwise>\n      </xsl:choose>\n    </xsl:variable>\n    <func:result select="tohw:isAListOfDigits($try)"/>\n  </func:function>\n\n  <func:function name="tohw:isANumberWithoutExponent">\n    <!-- numbers fitting [\\+-][0-9]+(\\.[0-9]*) -->\n    <xsl:param name="x"/>\n    <xsl:choose>\n      <xsl:when test="contains($x, \'.\')">\n        <func:result select="tohw:isAnInteger(substring-before($x, \'.\')) and\n                             tohw:isAListOfDigits(substring-after($x, \'.\'))"/>\n      </xsl:when>\n      <xsl:otherwise>\n        <func:result select="tohw:isAnInteger($x)"/>\n      </xsl:otherwise>\n    </xsl:choose>\n  </func:function>\n\n  <func:function name="tohw:isAnFPNumber">\n    <!-- Try and interpret a string as an exponential number -->\n    <!-- should only recognise strings of the form: [\\+-][0-9]*\\.[0-9]*([DdEe][\\+-][0-9]+)? -->\n    <xsl:param name="x"/>\n    <xsl:choose>\n      <xsl:when test="contains($x, \'d\')">\n        <func:result select="tohw:isANumberWithoutExponent(substring-before($x, \'d\')) and\n                             tohw:isAnInteger(substring-after($x, \'d\'))"/>\n      </xsl:when>\n      <xsl:when test="contains($x, \'D\')">\n        <func:result select="tohw:isANumberWithoutExponent(substring-before($x, \'D\')) and\n                             tohw:isAnInteger(substring-after($x, \'D\'))"/>\n      </xsl:when>\n      <xsl:when test="contains($x, \'e\')">\n        <func:result select="tohw:isANumberWithoutExponent(substring-before($x, \'e\')) and\n                             tohw:isAnInteger(substring-after($x, \'e\'))"/>\n      </xsl:when>\n      <xsl:when test="contains($x, \'E\')">\n        <func:result select="tohw:isANumberWithoutExponent(substring-before($x, \'E\')) and\n                             tohw:isAnInteger(substring-after($x, \'E\'))"/>\n      </xsl:when>\n      <xsl:otherwise>\n         <func:result select="tohw:isANumberWithoutExponent($x)"/>\n      </xsl:otherwise>\n    </xsl:choose>\n  </func:function>\n  \n        <xsl:template match="/">\n          <xsl:apply-templates />\n        </xsl:template>\n\n        <xsl:template match="cml:array">\n          <xsl:variable name="delim">\n            <xsl:choose>\n               <xsl:when test="@delimiter">\n                 <xsl:value-of select="@delimiter" />\n               </xsl:when> \n               <xsl:otherwise>\n                 <xsl:text> </xsl:text>\n               </xsl:otherwise>\n            </xsl:choose>\n          </xsl:variable>\n          <xsl:text>[[</xsl:text>\n            <xsl:for-each select="str:tokenize(string(.), $delim)" >\n              <xsl:choose>\n                <xsl:when test="tohw:isAnFPNumber(.)">\n                  <xsl:value-of select="." />\n                </xsl:when>\n                <xsl:otherwise>\n                  <xsl:text>"</xsl:text><xsl:value-of select="." /><xsl:text>"</xsl:text>\n                </xsl:otherwise>\n              </xsl:choose>\n              <xsl:if test="position() != last()">\n                <xsl:text>,</xsl:text>\n              </xsl:if>\n            </xsl:for-each>\n          <xsl:text>],</xsl:text>\n          <xsl:choose>\n            <xsl:when test="@units">\n              <xsl:text>"</xsl:text><xsl:value-of select="@units" /><xsl:text>"</xsl:text>\n            </xsl:when>\n            <xsl:otherwise>\n              <xsl:text>""</xsl:text>\n            </xsl:otherwise>\n          </xsl:choose>\n          <xsl:text>]</xsl:text>\n        </xsl:template>\n      </xsl:stylesheet>\n    </golem:template>\n    <golem:seealso>gwtsystem</golem:seealso>\n  </entry>\n\n  <entry id="scalar" term="Scalar default call">\n    <annotation />\n    <definition />\n    <description />\n    <metadataList />\n    <golem:template role="getvalue" binding="pygolem_serialization">\n        <xsl:stylesheet version=\'1.0\' \n                xmlns:xsl=\'http://www.w3.org/1999/XSL/Transform\'\n\t\txmlns:cml=\'http://www.xml-cml.org/schema\'\n\t\txmlns:str="http://exslt.org/strings"\n\t\txmlns:func="http://exslt.org/functions"\n\t\txmlns:exsl="http://exslt.org/common"\n\t\txmlns:tohw="http://www.uszla.me.uk/xsl/1.0/functions"\n\t\textension-element-prefixes="func exsl tohw str"\n\t\texclude-result-prefixes="exsl func tohw xsl str">\n        <xsl:output method="text" />\n  \n  \n  <func:function name="tohw:isAListOfDigits">\n    <!-- look only for [0-9]+ -->\n    <xsl:param name="x_"/>\n    <xsl:variable name="x" select="normalize-space($x_)"/>\n    <xsl:choose>\n      <xsl:when test="string-length($x)=0">\n        <func:result select="false()"/>\n      </xsl:when>\n      <xsl:when test="substring($x, 1, 1)=\'0\' or\n                      substring($x, 1, 1)=\'1\' or\n                      substring($x, 1, 1)=\'2\' or\n                      substring($x, 1, 1)=\'3\' or\n                      substring($x, 1, 1)=\'4\' or\n                      substring($x, 1, 1)=\'5\' or\n                      substring($x, 1, 1)=\'6\' or\n                      substring($x, 1, 1)=\'7\' or\n                      substring($x, 1, 1)=\'8\' or\n                      substring($x, 1, 1)=\'9\'">\n        <xsl:choose>\n          <xsl:when test="string-length($x)=1">\n            <func:result select="true()"/>\n          </xsl:when>\n          <xsl:otherwise>\n            <func:result select="tohw:isAListOfDigits(substring($x, 2))"/>\n          </xsl:otherwise>\n        </xsl:choose>\n      </xsl:when>\n      <xsl:otherwise>\n        <func:result select="false()"/>\n      </xsl:otherwise>\n    </xsl:choose>\n  </func:function>\n\n  <func:function name="tohw:isAnInteger">\n    <!-- numbers fitting [\\+-][0-9]+ -->\n    <xsl:param name="x_"/>\n    <xsl:variable name="x" select="normalize-space($x_)"/>\n    <xsl:variable name="try">\n      <xsl:choose>\n        <xsl:when test="starts-with($x, \'+\')">\n          <xsl:value-of select="substring($x,2)"/>\n        </xsl:when>\n        <xsl:when test="starts-with($x, \'-\')">\n          <xsl:value-of select="substring($x,2)"/>\n        </xsl:when>\n        <xsl:otherwise>\n          <xsl:value-of select="$x"/>\n        </xsl:otherwise>\n      </xsl:choose>\n    </xsl:variable>\n    <func:result select="tohw:isAListOfDigits($try)"/>\n  </func:function>\n\n  <func:function name="tohw:isANumberWithoutExponent">\n    <!-- numbers fitting [\\+-][0-9]+(\\.[0-9]*) -->\n    <xsl:param name="x"/>\n    <xsl:choose>\n      <xsl:when test="contains($x, \'.\')">\n        <func:result select="tohw:isAnInteger(substring-before($x, \'.\')) and\n                             tohw:isAListOfDigits(substring-after($x, \'.\'))"/>\n      </xsl:when>\n      <xsl:otherwise>\n        <func:result select="tohw:isAnInteger($x)"/>\n      </xsl:otherwise>\n    </xsl:choose>\n  </func:function>\n\n  <func:function name="tohw:isAnFPNumber">\n    <!-- Try and interpret a string as an exponential number -->\n    <!-- should only recognise strings of the form: [\\+-][0-9]*\\.[0-9]*([DdEe][\\+-][0-9]+)? -->\n    <xsl:param name="x"/>\n    <xsl:choose>\n      <xsl:when test="contains($x, \'d\')">\n        <func:result select="tohw:isANumberWithoutExponent(substring-before($x, \'d\')) and\n                             tohw:isAnInteger(substring-after($x, \'d\'))"/>\n      </xsl:when>\n      <xsl:when test="contains($x, \'D\')">\n        <func:result select="tohw:isANumberWithoutExponent(substring-before($x, \'D\')) and\n                             tohw:isAnInteger(substring-after($x, \'D\'))"/>\n      </xsl:when>\n      <xsl:when test="contains($x, \'e\')">\n        <func:result select="tohw:isANumberWithoutExponent(substring-before($x, \'e\')) and\n                             tohw:isAnInteger(substring-after($x, \'e\'))"/>\n      </xsl:when>\n      <xsl:when test="contains($x, \'E\')">\n        <func:result select="tohw:isANumberWithoutExponent(substring-before($x, \'E\')) and\n                             tohw:isAnInteger(substring-after($x, \'E\'))"/>\n      </xsl:when>\n      <xsl:otherwise>\n         <func:result select="tohw:isANumberWithoutExponent($x)"/>\n      </xsl:otherwise>\n    </xsl:choose>\n  </func:function>\n        \n  <xsl:template match="/">\n    <xsl:apply-templates />\n  </xsl:template>\n  \n  <xsl:template match="cml:scalar">\n    <xsl:variable name="value">\n      <xsl:choose>\n\t<xsl:when test="tohw:isAnFPNumber(.)">\n          <xsl:value-of select="." />\n\t</xsl:when>\n\t<xsl:otherwise>\n          <xsl:text>"</xsl:text><xsl:value-of select="." /><xsl:text>"</xsl:text>\n\t</xsl:otherwise>\n      </xsl:choose>\n    </xsl:variable>\n    <xsl:variable name="units">\n      <xsl:choose>\n\t<xsl:when test="@units">\n\t  <xsl:text>"</xsl:text><xsl:value-of select="@units" /><xsl:text>"</xsl:text>\n\t</xsl:when>\n\t<xsl:otherwise>\n\t  <xsl:text>""</xsl:text>\n\t</xsl:otherwise>\n      </xsl:choose>\n    </xsl:variable>\n    <xsl:text>[</xsl:text><xsl:value-of select="$value"/><xsl:text>,</xsl:text><xsl:value-of select="$units" /><xsl:text>]</xsl:text>\n  </xsl:template>\n</xsl:stylesheet>\n    </golem:template>\n\n    <golem:template role="defaultoutput">\n      <xsl:stylesheet version=\'1.0\' \n                      xmlns:xsl=\'http://www.w3.org/1999/XSL/Transform\'\n                      xmlns:cml=\'http://www.xml-cml.org/schema\'\n                      xmlns:str="http://exslt.org/strings"\n                      extension-element-prefixes="str"\n                      >\n        <xsl:output method="text" />\n        <xsl:param name="name" />\n        <xsl:param name="value" />\n        <xsl:template match="/">\n          <xsl:value-of select=\'$name\' /><xsl:value-of select=\'$value\' />\n        </xsl:template>\n      </xsl:stylesheet>\n    </golem:template>\n    <golem:seealso>gwtsystem</golem:seealso>\n  </entry>\n</dictionary>\n'
    return footer


def print_dictionary(ns, prefix, title, concepts, groupings, model=None, inputdict=None, use_id=True, use_title=True):
    """ Write out a CML/Golem dictionary, using ``model`` as a source of 
    definitions, descriptions and terms, containing definitions for the
    entries in ``concepts`` and the relationships between concepts defined
    in ``groupings``.
    
    ``prefix`` is the short name to be used in the namespace declaration; the 
    namespace is ``ns``, and the dictionary will be entitled ``title``."""
    entries = print_dictheader(ns, prefix, title)
    for k in concepts:
        c = concepts[k]
        entries += print_entry(ns, prefix, c, concepts, groupings, model=model, inputdict=inputdict, use_id=use_id, use_title=use_title)

    if inputdict:
        for key in inputdict:
            if not inputdict[key].written:
                print >> sys.stderr, 'Writing %s' % inputdict[key].id
                thisentry = '\n  <entry id=%s term="">\n    <annotation />\n    <definition />\n    <description />\n    <metadataList>\n      <metadata name="dc:author" content="golem-kiln" />\n    </metadataList>\n    %s\n    %s\n  </entry>\n' % (quoteattr(inputdict[key].id), inputdict[key].generate_xml_castep(), inputdict[key].generate_bounds_and_type())
                entries += thisentry

    entries += print_dictfooter()
    return entries


def id_for_concept(concept, prefix, use_id=True, use_title=True):
    if concept['dictRef'] == None:
        if concept['name'] == None:
            if use_id:
                if concept['id'] == None:
                    if use_title:
                        if concept['title'] == None:
                            return
                        else:
                            return 'title_' + concept['title']
                    else:
                        return
                else:
                    return 'id_' + concept['id']
            elif use_title:
                if concept['title'] == None:
                    return
                else:
                    return 'title_' + concept['title']
            else:
                return
        else:
            return concept['name'].split('}')[1]
    return concept['dictRef'].split('}')[1]


def getParents(concept, prefix, use_id=True, use_title=True):
    res = []
    for c in concept.parentConcept:
        if c is None:
            return res
        else:
            dr = id_for_concept(c, prefix, use_id, use_title)
            if dr is not None:
                res += [dr]
            else:
                res += getParents(c, prefix, use_id, use_title)

    return res


def print_entry(ns, prefix, c, concepts, groupings, model=None, inputdict=None, use_id=True, use_title=True):
    """ Dump a given concept in CML/Golem dictionary format. """
    entry_str = ''
    implements_str = ''
    payload_str = ''
    xpath_str = ''
    xpath = xpath_concept(c, concepts, id=use_id, title=use_title)
    if xpath is not None:
        parents_str = ''
        parents = getParents(c, prefix, use_title, use_id)
        for x in set(parents):
            parents_str += '    <golem:childOf>%s</golem:childOf>\n' % x

        xpath_str = '    <golem:xpath>%s</golem:xpath>\n' % xpath
        for key in groupings:
            if key in xpath:
                implements_str += '    <golem:implements>%s</golem:implements>\n' % groupings[key]

        dictRef = id_for_concept(c, prefix, use_id, use_title)
        if dictRef == None:
            return ''
        inputxsl = ''
        if inputdict:
            print 'checking %s' % dictRef
            if dictRef in inputdict:
                print 'found %s' % dictRef
                inputxsl = inputdict[dictRef].generate_xml_castep()
                implements_str += '    <golem:implements>convertibleToInput</golem:implements>\n'
        term = None
        if model:
            try:
                entry = model[('{%s}%s' % (ns, dictRef))]
                term = entry.term
            except KeyError:
                pass

        if term is None and c['title'] is not None:
            term = c['title']
        elif term is None:
            term = ''
        dictRef = dictRef.replace(' ', '_')
        entry_str = '  <entry id=%s term=%s>\n' % (quoteattr(dictRef), quoteattr(term))
        if c.hasPayload() and isinstance(c.payload, basestring):
            if c.payload.startswith('{http://www.xml-cml.org/schema}'):
                payload = c.payload.split('}')[1]
            else:
                payload = c.payload
            if payload in ['scalar', 'matrix', 'array', 'cellParameter', 'lattice']:
                payload_str = '    <golem:template call="%s" role="getvalue" binding="pygolem_serialization" />\n' % payload
                implements_str += '    <golem:implements>value</golem:implements>\n'
            else:
                implements_str += '    <golem:implements>grouping</golem:implements>\n'
        elif c['tag'].startswith('{http://www.xml-cml.org/schema}') and c['tag'].split('}')[1] in ['scalar', 'matrix', 'array', 'cellParameter', 'metadata', 'lattice']:
            payload_str = '    <golem:template call="%s" role="getvalue" binding="pygolem_serialization" />\n' % c['tag'].split('}')[1]
            implements_str += '    <golem:implements>value</golem:implements>\n'
        else:
            implements_str += '    <golem:implements>grouping</golem:implements>\n'
        if c.isRelative():
            implements_str += '    <golem:implements>relative</golem:implements>\n'
        else:
            implements_str += '    <golem:implements>absolute</golem:implements>\n'
        definition_str = '<definition />'
        description_str = '<description />'
        pv_str = ''
        if model:
            try:
                entry = model[('{%s}%s' % (ns, dictRef))]
                definition_str = '<definition>%s</definition>' % entry.definition
                description_str = etree.tostring(entry.description).strip()
                if inputdict:
                    pv_str = inputdict[dictRef].generate_bounds_and_type()
                else:
                    try:
                        pv_str = etree.tostring(entry.pvxml).strip()
                    except AttributeError:
                        pass

                if description_str[(-1)] != '\n':
                    description_str += '\n'
            except KeyError:
                pass

        entry = '\n%s    <annotation />\n    %s\n    %s    \n    <metadataList>\n      <metadata name="dc:author" content="golem-kiln" />\n    </metadataList>\n%s%s\n%s\n%s%s\n    %s\n  </entry>\n' % (entry_str, definition_str, description_str, xpath_str, payload_str, inputxsl, implements_str, parents_str, pv_str)
        return entry
    else:
        return ''
    return


def findpayloads(concepts):
    for k in concepts:
        c = concepts[k]
        if c['id'] == None and c['dictRef'] == None and c['title'] == None:
            for parent in c.parentConcept:
                if parent is not None:
                    parent.setPayload(c['tag'])

        elif c['name'] != None and c['tag'] == '{http://www.xml-cml.org/schema}metadata':
            c.setPayload(c['tag'])

    return


def make(filenames, namespace, prefix, title, groupings, model=None, inputfn=None, use_id=True, use_title=True):
    """ Build a dictionary.
    
Arguments:

* ``filenames`` - list of CML files comprising the corpus to be analysed.
* ``namespace`` - namespace of the dictionary
* ``prefix`` - short prefix to be used within the dictionary and namespace declaration
* ``title`` - Title of the dictionary (eg 'CASTEP dictionary')
* ``groupings`` - Extra groupings to be determined for entries. If the XPath for this entry contains the key, then this entry is a <golem:instanceOf> the grouping.
* ``model`` - Optionally, a dictionary to copy definitions/descriptions/terms from.
* ``inputfn`` - Optionally, an input file containing extra dictionary entries, not found in the corpus supplied, which should be added to the dictionary. 
* ``use_id``/``use_title`` - distinguish concepts by unique ID/title as well as dictRef.

    """
    if model:
        modeldict = golem.Dictionary(model, asModel=True)
    else:
        modeldict = None
    concepts = conceptset(['tag', 'name', 'dictRef', 'id', 'title'])
    for filename in filenames:
        xml = etree.parse(filename)
        root = xml.getroot()
        rootconcept = concepts.addconcept(parsecmlelement(root, None))
        parsecmltree(root, concepts, parent=rootconcept)

    findpayloads(concepts)
    if inputfn:
        inpd = input_dict()
        inpd.read_config(inputfn)
    else:
        inpd = None
    return print_dictionary(namespace, prefix, title, concepts, groupings, model=modeldict, inputdict=inpd, use_id=use_id, use_title=use_title)


def ossiatest():
    modeldict_fn = sys.argv[1]
    print make(sys.argv[2:], 'http://www.esc.cam.ac.uk/ossia', 'ossia', 'OSSIA dictionary', {"/cml:cml/cml:parameterList[@dictRef='input']": 'parameterInInput', "/cml:cml/cml:propertyList[@id='finalProperties']": 'inFinalProperties'}, model=modeldict_fn)


if __name__ == '__main__':
    ossiatest()