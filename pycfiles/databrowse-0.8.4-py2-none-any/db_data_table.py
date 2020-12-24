# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Files\Research\databrowse\databrowse\plugins\db_data_table\db_data_table.py
# Compiled at: 2018-06-29 17:51:46
""" plugins/renderers/db_data_table - Plugin for Data Table Display """
import sys, os, glob, zipfile, tempfile
from lxml import etree
from databrowse.support.renderer_support import renderer_class

class db_data_table(renderer_class):
    """ Data Table Plugin Renderer """
    _namespace_uri = 'http://thermal.cnde.iastate.edu/databrowse/datatable'
    _namespace_local = 'dt'
    _default_content_mode = 'full'
    _default_style_mode = 'view_table'
    _default_recursion_depth = 2
    _table_transform = '<?xml version="1.0" encoding="utf-8"?>\n<xsl:stylesheet xmlns="http://thermal.cnde.iastate.edu/databrowse/datatable" xmlns:dt="http://thermal.cnde.iastate.edu/databrowse/datatable" %s xmlns:my="http://thermal.cnde.iastate.edu/databrowse/datatable/functions" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:dyn="http://exslt.org/dynamic" extension-element-prefixes="dyn my" version="1.0" exclude-result-prefixes="my">\n    <xsl:output method=\'xml\' indent=\'yes\' omit-xml-declaration="no" version="1.0" media-type="application/xml" encoding="UTF-8"/>\n    <xsl:variable name="siteurl" select="string(\'%s\')" />\n    <xsl:template match="table">\n        <dt:datatable sourcefile="%s">\n            <xsl:variable name="files" select="@filenamematch" />\n            <xsl:variable name="rowmatch" select="rowmatch/@select" />\n            <xsl:variable name="data" select="my:data($files)" />\n            <xsl:variable name="assert" select="assert" />\n            <xsl:variable name="cols" select="colspec"/>\n            <xsl:attribute name="title">\n                <xsl:choose>\n                    <xsl:when test="@title"><xsl:value-of select="@title" /></xsl:when>\n                    <xsl:otherwise>%s</xsl:otherwise>\n                </xsl:choose>\n            </xsl:attribute>\n            <xsl:if test="description">\n                <dt:description><xsl:copy-of select="description/node()"/></dt:description>\n            </xsl:if>\n            <dt:header>\n                <xsl:for-each select="$cols">\n                    <dt:coldef>\n                        <xsl:if test="@tooltip">\n                            <xsl:attribute name="tooltip"><xsl:value-of select="@tooltip" /></xsl:attribute>\n                        </xsl:if>\n                        <xsl:choose>\n                            <xsl:when test="@label">\n                                <xsl:value-of select="@label"/>\n                            </xsl:when>\n                            <xsl:otherwise>\n                                <xsl:value-of select="@select"/>\n                            </xsl:otherwise>\n                        </xsl:choose>\n                    </dt:coldef>\n                </xsl:for-each>\n            </dt:header>\n            <xsl:apply-templates select="$data" mode="data">\n                <xsl:with-param name="cols" select="$cols" />\n                <xsl:with-param name="rowmatch" select="$rowmatch" />\n                <xsl:with-param name="assert" select="$assert" />\n            </xsl:apply-templates>\n        </dt:datatable>\n    </xsl:template>\n    <xsl:template match="*" mode="data">\n        <xsl:param name="cols" />\n        <xsl:param name="rowmatch" />\n        <xsl:param name="assert" />\n        <xsl:for-each select="dyn:evaluate($rowmatch)">\n            <xsl:variable name="data" select="." />\n            <xsl:for-each select="$assert">\n                <xsl:apply-templates mode="assert" select="$data">\n                    <xsl:with-param name="assert" select="$assert/@select"/>\n                </xsl:apply-templates>\n            </xsl:for-each>\n            <dt:row>\n                <xsl:for-each select="$cols">\n                    <dt:data><xsl:if test="@type"><xsl:attribute name="type"><xsl:value-of select="@type"/></xsl:attribute></xsl:if><xsl:if test="@url"><xsl:attribute name="url"><xsl:apply-templates mode="value" select="$data"><xsl:with-param name="select" select="@url"/></xsl:apply-templates></xsl:attribute></xsl:if><xsl:apply-templates mode="value" select="$data"><xsl:with-param name="select" select="@select"/></xsl:apply-templates></dt:data>\n                </xsl:for-each>\n            </dt:row>\n        </xsl:for-each>\n    </xsl:template>\n    <xsl:template match="*" mode="value">\n        <xsl:param name="select"/>\n        <xsl:value-of select="dyn:evaluate($select)"/>\n    </xsl:template>\n    <xsl:template match="*" mode="url">\n        <xsl:param name="select"/>\n        <xsl:value-of select="dyn:evaluate($select)"/>\n    </xsl:template>\n    <xsl:template match="*" mode="assert">\n        <xsl:param name="assert"/>\n        <xsl:if test="not(dyn:evaluate($assert))">\n            <xsl:if test="my:xmlassert($assert)"/>\n        </xsl:if>\n    </xsl:template>\n</xsl:stylesheet>\n'
    _ods_transform = '<?xml version="1.0" encoding="utf-8"?>\n<xsl:stylesheet xmlns:dt="http://thermal.cnde.iastate.edu/databrowse/datatable" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0" xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0" xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0" xmlns:dom="http://www.w3.org/2001/xml-events" xmlns:xforms="http://www.w3.org/2002/xforms" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0">\n    <xsl:output method=\'xml\' indent=\'yes\'/>  \n    <xsl:template match=\'dt:datatable\'>\n        <!-- Opendocument boilerplate -->\n        <office:document-content office:version="1.0">  <!-- for ODF 1.2 conformance, change "1.0" to "1.2" -->\n            <office:scripts/>\n            <office:automatic-styles>\n                <style:style style:name="co1" style:family="table-column">\n                    <style:table-column-properties fo:break-before="auto" style:column-width="0.8925in"/>\n                </style:style>\n                <style:style style:name="ro1" style:family="table-row">\n                    <style:table-row-properties style:row-height="0.1681in" fo:break-before="auto" style:use-optimal-row-height="true"/>\n                </style:style>\n                <style:style style:name="ta1" style:family="table" style:master-page-name="Default">\n                    <style:table-properties table:display="true" style:writing-mode="lr-tb"/>\n                </style:style>\n            </office:automatic-styles>\n            <office:body>\n                <office:spreadsheet>\n                    <table:table>\n                        <xsl:attribute name="table:name">\n                            <xsl:value-of select="@title"/>\n                        </xsl:attribute>\n                        <xsl:attribute name="table:style-name">ta1</xsl:attribute>\n                        <xsl:attribute name="table:print">false</xsl:attribute>\n                        <table:table-column table:style-name="co1" table:default-cell-style-name="Default"/>\n                        <table:table-row table:style-name="ro1">\n                            <xsl:for-each select="dt:header/dt:coldef">\n                                <table:table-cell office:value-type="string">\n                                    <text:p><xsl:value-of select="." /></text:p>\n                                </table:table-cell>\n                            </xsl:for-each>\n                        </table:table-row>\n                        <xsl:for-each select="dt:row">\n                            <table:table-row table:style-name="ro1">\n                                <xsl:for-each select="dt:data">\n                                    <table:table-cell>\n                                        <xsl:choose>\n                                            <xsl:when test="@type=\'numeric\'">\n                                                <xsl:attribute name="office:value-type">float</xsl:attribute>\n                                                <xsl:attribute name="office:value"><xsl:value-of select="normalize-space(.)"/></xsl:attribute>\n                                            </xsl:when>\n                                            <xsl:otherwise>\n                                                <xsl:attribute name="office:value-type">string</xsl:attribute>\n                                            </xsl:otherwise>\n                                        </xsl:choose>\n                                        <text:p>\n                                            <xsl:choose>\n                                                <xsl:when test="@url">\n                                                    <text:a xlink:type="simple">\n                                                        <xsl:attribute name="xlink:href"><xsl:value-of select="@url"/></xsl:attribute>\n                                                        <xsl:value-of select="normalize-space(.)" />    \n                                                    </text:a>                                                    \n                                                </xsl:when>\n                                                <xsl:otherwise>\n                                                    <xsl:value-of select="normalize-space(.)" />\n                                                </xsl:otherwise>\n                                            </xsl:choose>\n                                        </text:p>\n                                    </table:table-cell>\n                                </xsl:for-each>\n                            </table:table-row>\n                        </xsl:for-each>  \n                    </table:table>                  \n                </office:spreadsheet>\n            </office:body>\n        </office:document-content>\n    </xsl:template>\n</xsl:stylesheet>\n'

    class MyExt:
        _fullpath = '/'
        _namespaces = {'dc': 'http://thermal.cnde.iastate.edu/datacollect', 'dcv': 'http://thermal.cnde.iastate.edu/dcvalue'}

        class AssertionException(Exception):
            pass

        def __init__(self, fullpath):
            self._fullpath = fullpath

        def data(self, _, files):
            cwd = os.getcwd()
            os.chdir(os.path.dirname(self._fullpath))
            filelist = glob.glob(files[0])
            output = []
            p = etree.XMLParser(huge_tree=True)
            for filename in filelist:
                e = etree.parse(filename, parser=p).getroot()
                output.append(e)

            os.chdir(cwd)
            return output

        def xmlassert(self, _, assertstatement):
            raise self.AssertionException('Assertion "%s" failed' % str(assertstatement[0]))

    def getContent(self):
        if self._caller != 'databrowse':
            return
        else:
            if self._content_mode == 'full':
                xml = etree.parse(self._fullpath)
                namespaces = (' ').join([ 'xmlns:' + str(item) + '="' + str(value) + '"' for item, value in xml.getroot().nsmap.iteritems() ])
                ext_module = self.MyExt(self._fullpath)
                extensions = etree.Extension(ext_module, ('data', 'xmlassert'), ns='http://thermal.cnde.iastate.edu/databrowse/datatable/functions')
                return xml.xslt(etree.XML(self._table_transform % (namespaces, self._web_support.siteurl, self.getURL(self._relpath), os.path.basename(self._fullpath))), extensions=extensions).getroot()
            if self._content_mode == 'raw' and 'filetype' in self._web_support.req.form and self._web_support.req.form['filetype'].value == 'ods':
                xml = etree.parse(self._fullpath)
                namespaces = (' ').join([ 'xmlns:' + str(item) + '="' + str(value) + '"' for item, value in xml.getroot().nsmap.iteritems() ])
                ext_module = self.MyExt(self._fullpath)
                extensions = etree.Extension(ext_module, ('data', 'xmlassert'), ns='http://thermal.cnde.iastate.edu/databrowse/datatable/functions')
                base = xml.xslt(etree.XML(self._table_transform % (namespaces, self._web_support.siteurl, self.getURL(self._relpath), os.path.basename(self._fullpath))), extensions=extensions)
                result = etree.tostring(base.xslt(etree.XML(self._ods_transform)))
                filename = str(base.xpath('//@title')[0])
                f = tempfile.TemporaryFile()
                if sys.version_info[0] <= 2 and sys.version_info[1] < 7:
                    zipfile_compression = zipfile.ZIP_STORED
                else:
                    zipfile_compression = zipfile.ZIP_DEFLATED
                zf = zipfile.ZipFile(f, 'w', zipfile_compression)
                if sys.version_info[0] <= 2 and sys.version_info[1] < 7:
                    zf.writestr('mimetype', 'application/vnd.oasis.opendocument.spreadsheet')
                else:
                    zf.writestr('mimetype', 'application/vnd.oasis.opendocument.spreadsheet', compress_type=zipfile.ZIP_STORED)
                zf.writestr('META-INF/manifest.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">\n    <manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.spreadsheet" manifest:full-path="/"/>\n    <manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>\n    <!-- manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/-->\n    <!-- manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml"/-->\n    <!-- manifest:file-entry manifest:media-type="text/xml" manifest:full-path="settings.xml"/-->\n</manifest:manifest>\n')
                zf.writestr('content.xml', result)
                zf.close()
                self._web_support.req.response_headers['Content-Type'] = 'application/vnd.oasis.opendocument.spreadsheet'
                self._web_support.req.response_headers['Content-Length'] = str(f.tell())
                f.seek(0, 0)
                self._web_support.req.response_headers['Content-Disposition'] = 'attachment; filename=' + filename + '.ods'
                self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                self._web_support.req.output_done = True
                if 'wsgi.file_wrapper' in self._web_support.req.environ:
                    return self._web_support.req.environ['wsgi.file_wrapper'](f, 1024)
                return iter(lambda : f.read(1024), '')
            elif self._content_mode == 'raw' and 'filetype' in self._web_support.req.form and self._web_support.req.form['filetype'].value == 'csv':
                xml = etree.parse(self._fullpath)
                namespaces = (' ').join([ 'xmlns:' + str(item) + '="' + str(value) + '"' for item, value in xml.getroot().nsmap.iteritems() ])
                ext_module = self.MyExt(self._fullpath)
                extensions = etree.Extension(ext_module, ('data', 'xmlassert'), ns='http://thermal.cnde.iastate.edu/databrowse/datatable/functions')
                base = xml.xslt(etree.XML(self._table_transform % (namespaces, self._web_support.siteurl, self.getURL(self._relpath), os.path.basename(self._fullpath))), extensions=extensions)
                f = tempfile.TemporaryFile()
                filename = str(base.xpath('//@title')[0])
                coldef = base.xpath('dt:header/dt:coldef', namespaces={'dt': 'http://thermal.cnde.iastate.edu/databrowse/datatable'})
                f.write((',').join([ x.text for x in coldef ]) + '\n')
                for row in base.xpath('dt:row', namespaces={'dt': 'http://thermal.cnde.iastate.edu/databrowse/datatable'}):
                    datadef = row.xpath('dt:data/.', namespaces={'dt': 'http://thermal.cnde.iastate.edu/databrowse/datatable'})
                    f.write((',').join([ x.text if x.text is not None else '' for x in datadef ]) + '\n')

                f.flush()
                f.seek(0, 2)
                self._web_support.req.response_headers['Content-Type'] = 'text/csv'
                self._web_support.req.response_headers['Content-Length'] = str(f.tell())
                f.seek(0, 0)
                self._web_support.req.response_headers['Content-Disposition'] = 'attachment; filename=' + filename + '.csv'
                self._web_support.req.start_response(self._web_support.req.status, self._web_support.req.response_headers.items())
                self._web_support.req.output_done = True
                if 'wsgi.file_wrapper' in self._web_support.req.environ:
                    return self._web_support.req.environ['wsgi.file_wrapper'](f, 1024)
                return iter(lambda : f.read(1024), '')
            else:
                raise self.RendererException('Invalid Content Mode')
            return