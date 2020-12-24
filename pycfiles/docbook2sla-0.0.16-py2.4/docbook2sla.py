# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/docbook2sla/docbook2sla.py
# Compiled at: 2008-03-14 13:07:50
__author__ = 'Timo Stollenwerk (timo@zmag.de)'
__license__ = 'GNU General Public License (GPL)'
__revision__ = '$Rev: 257 $'
__date__ = '$Date: 2008-03-11 22:00:09 +0100 (Tue, 11 Mar 2008) $'
__URL__ = '$URL: http://svn.zmag.de/svn/python/docbook2sla/trunk/docbook2sla/docbook2sla.py $'
import os, sys
from util import newTempfile, runcmd
from logger import LOG
from lxml import etree
from zope.interface import implements
from interfaces import IDocBook2Sla
dirname = os.path.dirname(__file__)
_debug = 1

class NotValidXmlError(Exception):
    __module__ = __name__


class DocBook2Sla(object):
    """Conversions from DocBook to Scribus. """
    __module__ = __name__
    implements(IDocBook2Sla)

    def __init__(self):
        xsl_generateid = os.path.abspath(os.path.join(dirname, 'xsl', 'generate-id.xsl'))
        if not os.path.exists(xsl_generateid):
            raise IOError('%s does not exist' % xsl_generateid)
        xsl_docbook2pageobject = os.path.abspath(os.path.join(dirname, 'xsl', 'docbook2pageobject.xsl'))
        if not os.path.exists(xsl_docbook2pageobject):
            raise IOError('%s does not exist' % xsl_docbook2pageobject)
        xsl_wrapper = os.path.abspath(os.path.join(dirname, 'xsl', 'wrapper.xsl'))
        if not os.path.exists(xsl_wrapper):
            raise IOError('%s does not exist' % xsl_wrapper)
        self.xsl_generateid = xsl_generateid
        self.xsl_docbook2pageobject = xsl_docbook2pageobject
        self.xsl_wrapper = xsl_wrapper

    def create(self, docbookfn, scribusfn, output_filename=None, validate=False):
        """ Creates a Scribus file from a DocBook source. """
        if _debug:
            LOG.info('create(%s, %s, output_filename=%s, validate=%s' % (docbookfn, scribusfn, output_filename, validate))
        if validate:
            LOG.info('validate docbook: %s' % self.validate(docbookfn))
            LOG.info('validate scribus: %s' % self.validate(scribusfn))
        scribus_pageobjects = self.transform(docbookfn, self.xsl_docbook2pageobject)
        if _debug:
            LOG.info("scribus_pageobjects written to '%s'" % scribus_pageobjects)
        output = self.transform(scribusfn, self.xsl_wrapper, secondinputfn=scribus_pageobjects)
        if _debug:
            LOG.info("output written to '%s'" % output)
        if output_filename:
            open(output_filename, 'w').write(open(output, 'r').read())
            return output_filename
        else:
            return output

    def syncronize(self, docbookfn, scribusfn, output_filename=None, validate=False):
        """ Syncronize changes in a docbook file into a scribus file. """
        LOG.info('syncronize(%s, %s, output_filename=%s, validate=%s' % (docbookfn, scribusfn, output_filename, validate))
        xsl_syncronize = os.path.abspath(os.path.join(dirname, 'xsl', 'syncronize.xsl'))
        if not os.path.exists(xsl_syncronize):
            raise IOError('%s does not exist' % xsl_syncronize)
        if validate:
            try:
                LOG.info('syncronize(): validate docbook: %s' % self.validate(docbookfn))
                LOG.info('syncronize(): validate scribus: %s' % self.validate(scribusfn))
            except:
                print >> sys.stderr, 'syncronize(): Error validating %s and %s' % (docbookfn, scribusfn)
                raise

        output = self.transform(scribusfn, xsl_syncronize, secondinputfn=docbookfn)
        if _debug:
            LOG.info("DEBUG: output written to '%s'" % output)
        if output_filename:
            open(output_filename, 'w').write(open(output, 'r').read())
            return output_filename
        else:
            return output

    def transform(self, xmlfn, stylefn, secondinputfn=None, outputfn=None, validate=False):
        """ Transforms a XML document with a XSL stylesheet. """
        if not outputfn:
            outputfn = newTempfile(suffix='.xml')
        try:
            xmltree = etree.parse(xmlfn)
            styletree = etree.parse(stylefn)
            xslt = etree.XSLT(styletree)
            if secondinputfn:
                pathname = os.path.dirname(stylefn)
                abspath = os.path.abspath(pathname)
                tmpfile = '%s/tmp.xml' % abspath
                self.write(secondinputfn, tmpfile)
                result = xslt(xmltree, secondinput="'tmp.xml'")
                os.remove(tmpfile)
            else:
                result = xslt(xmltree)
            if result != None:
                open(outputfn, 'w').write(etree.tostring(result.getroot()))
        except:
            print >> sys.stderr, 'Error transforming %s (%s) with %s' % (xmlfn, secondinputfn, stylefn)
            raise

        return outputfn

    def validate(self, fname):
        """ Validates XML against DocBook or Scribus XML Schema. """
        fe = os.path.splitext(fname)[1]
        xmltree = etree.parse(fname)
        if fe == '.xml':
            xmlschema_doc = etree.parse('http://www.docbook.org/xsd/4.5/docbook.xsd')
            xmlschema = etree.XMLSchema(xmlschema_doc)
            if xmlschema.validate(xmltree):
                return True
            else:
                raise NotValidXmlError, '%s is no valid %s file.' % (fname, fe)
        elif fe == '.sla':
            xml_schema_scribus = os.path.abspath(os.path.join(dirname, 'schema', 'scribus.xsd'))
            if not os.path.exists(xml_schema_scribus):
                raise IOError('%s does not exist' % xml_schema_scribus)
            xmlschema_doc = etree.parse(xml_schema_scribus)
            xmlschema = etree.XMLSchema(xmlschema_doc)
            if xmlschema.validate(xmltree):
                return True
            else:
                raise NotValidXmlError, '%s is no valid %s file.' % (fname, fe)
        else:
            raise ValueError('Unsupported format: %s' % fe)

    def write(self, tmpfn, outputfn):
        """ Write tempfile into output file. """
        tmpFile = open(tmpfn, 'r')
        outputFile = open(outputfn, 'w')
        outputFile.write(tmpFile.read())
        return outputFile.close()

    def analyseScribusFile(self, scribusfn):
        """ Returns statistical informations about a Scribus file. """
        tree = etree.parse(scribusfn)
        return '# Pageobjects: %s' % len(tree.findall('.//PAGEOBJECT'))

    def analyseDocBookFile(self, docbookfn):
        """ Returns statistival informations about a DocBook file. """
        pass

    def showFile(self, fn):
        """ Returns string representation of a file. """
        tmpFile = open(fn, 'r')
        return tmpFile.read()

    def __call__(self, *args, **kw):
        return self.create(*args, **kw)