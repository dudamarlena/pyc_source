# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/doapfiend_html.py
# Compiled at: 2008-05-21 11:52:29
"""

doapfiend_html
==============

This is a plugin for formatting DOAP as HTML.

"""
import logging
from cStringIO import StringIO
from lxml import etree
from doapfiend.plugins.base import Plugin
__docformat__ = 'epytext'
LOG = logging.getLogger(__name__)

def make_html(doap_xml):
    """
    Create HTML page from DOAP profile

    @param doap_xml: DOAP in RDF/XML serialization
    @type doap_xml: string

    @rtype: string
    @returns: DOAP in HTML

    """
    transform = etree.XSLT(etree.fromstring(HDOAP_XSL))
    doc = etree.fromstring(doap_xml)
    result_tree = transform(doc)
    out = StringIO()
    out.write('')
    try:
        result_tree.write(out)
    except AssertionError:
        LOG.error('Invalid RDF')
        return

    text = out.getvalue()
    out.close()
    return text


class HtmlPlugin(Plugin):
    """Class for formatting DOAP output"""
    name = 'html'
    enabled = False
    enable_opt = None

    def __init__(self):
        """Setup HtmlPlugin class"""
        super(HtmlPlugin, self).__init__()

    def add_options(self, parser, output, search):
        """Add plugin's options to doapfiend's opt parser"""
        output.add_option('--%s' % self.name, action='store_true', dest=self.enable_opt, help='Display DOAP as HTML')
        return (parser, output, search)

    def serialize(self, doap_xml, color=False):
        """
        Serialize DOAP as HTML

        @param doap_xml: DOAP in RDF/XML serialization
        @type doap_xml: string

        @param color: Does nothing, could toggle CSS
        @type color: boolean 

        @rtype: unicode
        @returns: DOAP as HTML

        """
        return make_html(doap_xml)


HDOAP_XSL = '\n<!-- \n\nAuthor: Danny Ayers\nhttp://dannyayers.com:88/xmlns/hdoap/profile/index.xhtml\n\nModified by Rob Cakebread <rob <@> doapspace.org>:\n\n 09-13-2007 Added:\n\tfile-release\n\told-homepage\n\tscreenshots\n\tprogramming-language\n\twiki\n\tbug-database\n\tos\n\thelper\n\tdeveloper\n\tdocumenter\n\ttranslator\n\ttester\n 04-23-2008\n    shortname\n-->\n<xsl:stylesheet version="1.0" \n\t\t\t\txmlns:xsl="http://www.w3.org/1999/XSL/Transform"\n\t\t\t\txmlns="http://www.w3.org/1999/xhtml"\n\t\t\t\txmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n\t\t\t\txmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"\n\t\t\t\txmlns:dc="http://purl.org/dc/elements/1.1/"\n\t\t\t\txmlns:foaf="http://xmlns.com/foaf/0.1/"\n\t\t\t\txmlns:doap="http://usefulinc.com/ns/doap#"\n\t\t\t\t>\n  \n  <xsl:output method="xml" indent="yes" encoding="utf-8" />\n  \n  <xsl:template match="/"> \n\t<xsl:apply-templates select="/rdf:RDF/doap:Project|/doap:Project" />\n  </xsl:template> \n  \n  <xsl:template match="/rdf:RDF/doap:Project|/doap:Project"> \n\t<html>\n\t  <head profile="http://purl.org/stuff/hdoap/profile">\n\t\t<title><xsl:value-of select="doap:name/text()"/></title>\n\t\t<link rel="transformation" href="http://purl.org/stuff/hdoap/hdoap2doap.xsl" />  \n\t\t<link href="/static/css/hdoap.css" rel="stylesheet" type="text/css" />\t  \n\t  </head>\n\t  <body>\n\t\t<div class="Project">\n\t\t  <h1>Project: <xsl:value-of select="doap:name/text()"/></h1>\n\t\t  <div class="project-details">\n\t\t\t<xsl:apply-templates select="*[count(*)=0]" />\n\t\t  </div>\n\t\t  <xsl:apply-templates select="doap:release"/>\n\t\t  <xsl:apply-templates select="doap:repository" />\n\t\t  <xsl:apply-templates select="doap:maintainer" />\n\t\t  <xsl:apply-templates select="doap:developer" />\n\t\t  <xsl:apply-templates select="doap:documenter" />\n\t\t  <xsl:apply-templates select="doap:translator" />\n\t\t  <xsl:apply-templates select="doap:tester" />\n\t\t  <xsl:apply-templates select="doap:helper" />\n\t\t</div>\n\t\t<xsl:apply-templates select="/rdf:RDF/rdf:Description" /> \n\t  </body>\n\t</html>\n  </xsl:template>\n  \n  <!--  Properties with Literal subjects -->\n  <xsl:template match="doap:name|doap:shortname|doap:created|doap:programming-language|doap:shortdesc|doap:description|doap:revision|foaf:name|foaf:mbox_sha1sum|doap:anon-root|doap:module|doap:os">\n\t<p>\n\t  <span class="literal-label"><xsl:value-of select="local-name()" /></span> :  \n\t  <span class="literal-value">\n\t\t<xsl:attribute name="class"><xsl:value-of select="local-name()" /></xsl:attribute>\n\t\t<xsl:if test="@xml:lang">\n\t\t  <xsl:attribute name="xml:lang"><xsl:value-of select="@xml:lang" /></xsl:attribute>\n\t\t</xsl:if> \n\t\t<xsl:value-of select="text()" />\n\t  </span>\n\t</p>\n  </xsl:template>\n  \n  <!-- Properties with Resource subjects -->\n  <xsl:template match="doap:homepage|doap:old-homepage|doap:file-release|doap:mailing-list|doap:download-page|doap:download-mirror|doap:bug-database|doap:category|doap:license|rdfs:seeAlso|doap:location|doap:browse|foaf:mbox|foaf:homepage|doap:wiki|doap:screenshots">\n\t<p>\n\t  <span class="resource-label"><xsl:value-of select="local-name()" /></span> :  \n\t  <span class="resource-value">\n\t  <a>\n\t\t<xsl:attribute name="class"><xsl:value-of select="local-name()" /></xsl:attribute>\n\t\t<xsl:attribute name="href"><xsl:value-of select="@rdf:resource" /></xsl:attribute>\n\t\t<xsl:value-of select="@rdf:resource" />  \n\t  </a>\n\t  </span>\n\t</p>\n  </xsl:template>\n  \n  <!-- Release subsection -->\n  <xsl:template match="doap:release">\n\t<div class="release">\n\t  <h2>Release</h2>\n\t  <div class="Version">\n\t\t<xsl:apply-templates select="./doap:Version/*" />\n\t  </div>\n\t</div>\n  </xsl:template>\n  \n  <!-- Maintainer subsection -->\n  <xsl:template match="doap:maintainer">\n\t<div class="maintainer">\n\t  <h2>Maintainer</h2>\n\t  <div class="Person">\n\t\t<xsl:apply-templates select="./foaf:Person/*" />\n\t  </div>\n\t</div>\n  </xsl:template>\n  \n  <!-- Developer subsection -->\n  <xsl:template match="doap:developer">\n\t<div class="developer">\n\t  <h2>Developer</h2>\n\t  <div class="Person">\n\t\t<xsl:apply-templates select="./foaf:Person/*" />\n\t  </div>\n\t</div>\n  </xsl:template>\n  \n  <!-- Documenter subsection -->\n  <xsl:template match="doap:documenter">\n\t<div class="documenter">\n\t  <h2>Documenter</h2>\n\t  <div class="Person">\n\t\t<xsl:apply-templates select="./foaf:Person/*" />\n\t  </div>\n\t</div>\n  </xsl:template>\n  \n  <!-- Translator subsection -->\n  <xsl:template match="doap:translator">\n\t<div class="translator">\n\t  <h2>Translator</h2>\n\t  <div class="Person">\n\t\t<xsl:apply-templates select="./foaf:Person/*" />\n\t  </div>\n\t</div>\n  </xsl:template>\n\n  <!-- Tester subsection -->\n  <xsl:template match="doap:tester">\n\t<div class="tester">\n\t  <h2>Tester</h2>\n\t  <div class="Person">\n\t\t<xsl:apply-templates select="./foaf:Person/*" />\n\t  </div>\n\t</div>\n  </xsl:template>\n  \n  <!-- Helper subsection -->\n  <xsl:template match="doap:helper">\n\t<div class="helper">\n\t  <h2>Helper</h2>\n\t  <div class="Person">\n\t\t<xsl:apply-templates select="./foaf:Person/*" />\n\t  </div>\n\t</div>\n  </xsl:template>\n\n  <!-- Repository subsection -->\n  <xsl:template match="doap:repository">\n\t<div class="repository">\n\t  <h2>Repository</h2>\n\t  <div>\n\t\t<xsl:attribute name="class"><xsl:value-of select="local-name(./*)"/></xsl:attribute>\n\t\t<xsl:apply-templates select="./*/*" />\n\t  </div>\n\t</div>\n  </xsl:template>\n  \n  <!-- Maker subsection -->\n  <xsl:template match="/rdf:RDF/rdf:Description/foaf:maker">\n\t<div class="maker">\n\t  <h3>Maker of DOAP Profile</h3>\n\t  <div class="Person">\n\t\t<xsl:apply-templates select="./foaf:Person/*" />\n\t  </div>\n\t</div>\n  </xsl:template>\n  \n</xsl:stylesheet>\n'