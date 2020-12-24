# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/catalog.py
# Compiled at: 2016-06-01 14:16:48
"""
Logic for downloading local copies of schemas and generating an
`XML catalog <http://lxml.de/resolvers.html#xml-catalogs`_ for use in
resolving schemas locally instead of downloading them every time validation
is required.

Catalog generation is available via the setup.py custom command xmlcatalog,
and a generated catalog and corresponding schema files should be included
in packaged releases of eulxml.

For more information about setting up and testing XML catalogs, see the
`libxml2 documentation <http://xmlsoft.org/catalog.html>`_.
"""
import os, logging
from datetime import date
from lxml import etree
import sys
from eulxml import xmlmap, __version__, XMLCATALOG_DIR, XMLCATALOG_FILE
try:
    import requests
except ImportError:
    requests = None

logger = logging.getLogger(__name__)
req_requests_msg = 'Please install requests to download schemas ' + '(pip install requests)\n'
XSD_SCHEMAS = [
 'http://www.loc.gov/standards/mods/mods.xsd',
 'http://www.loc.gov/standards/mods/v3/mods-3-4.xsd',
 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
 'http://www.loc.gov/standards/xlink/xlink.xsd',
 'http://www.loc.gov/standards/premis/premis.xsd',
 'http://www.loc.gov/standards/premis/v2/premis-v2-1.xsd',
 'http://www.tei-c.org/release/xml/tei/custom/schema/xsd/tei_all.xsd',
 'http://www.history.ncdcr.gov/SHRAB/ar/emailpreservation/mail-account/mail-account.xsd',
 'http://www.loc.gov/ead/ead.xsd']

class Uri(xmlmap.XmlObject):
    """:class:`xmlmap.XmlObject` class for Catalog URIs"""
    ROOT_NAME = 'uri'
    ROOT_NS = 'urn:oasis:names:tc:entity:xmlns:xml:catalog'
    name = xmlmap.StringField('@name')
    uri = xmlmap.StringField('@uri')


class Catalog(xmlmap.XmlObject):
    """:class:`xmlmap.XmlObject` class to for generating XML Catalogs"""
    ROOT_NAME = 'catalog'
    ROOT_NS = 'urn:oasis:names:tc:entity:xmlns:xml:catalog'
    ROOT_NAMESPACES = {'c': ROOT_NS}
    uri_list = xmlmap.NodeListField('c:uri', Uri)


def download_schema(uri, path, comment=None):
    """Download a schema from a specified URI and save it locally.

    :param uri: url where the schema should be downloaded
    :param path: local file path where the schema should be saved
    :param comment: optional comment; if specified, will be added to
        the downloaded schema
    :returns: true on success, false if there was an error and the
        schema failed to download
    """
    if requests is None:
        sys.stderr.write(req_requests_msg)
        return
    else:
        schema = os.path.basename(uri)
        try:
            req = requests.get(uri, stream=True)
            req.raise_for_status()
            with open(path, 'wb') as (schema_download):
                for chunk in req.iter_content(chunk_size=1024):
                    if chunk:
                        schema_download.write(chunk)

            if comment is not None:
                tree = etree.parse(path)
                tree.getroot().append(etree.Comment(comment))
                with open(path, 'wb') as (xml_catalog):
                    xml_catalog.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
                logger.debug('Downloaded schema %s', schema)
            return True
        except requests.exceptions.HTTPError as err:
            msg = 'Failed to download schema %s' % schema
            msg += '(error codes %s)' % err.response.status_code
            logger.warn(msg)
            return False

        return


def generate_catalog(xsd_schemas=None, xmlcatalog_dir=None, xmlcatalog_file=None):
    """Generating an XML catalog for use in resolving schemas

    Creates the XML Catalog directory if it doesn't already exist.
    Uses :meth:`download_schema` to save local copies of schemas,
    adding a comment indicating the date downloaded by eulxml.

    Generates a new catalog.xml file, with entries for all schemas
    that downloaded successfully.  If no schemas downloaded, the catalog
    is not generated.

    .. Note::

        Currently this method overwites any existing schema and catalog
        files, without checking if they are present or need to be
        updated.

    """
    if requests is None:
        sys.stderr.write(req_requests_msg)
        return
    else:
        logger.debug('Generating a new XML catalog')
        if xsd_schemas is None:
            xsd_schemas = XSD_SCHEMAS
        if xmlcatalog_file is None:
            xmlcatalog_file = XMLCATALOG_FILE
        if xmlcatalog_dir is None:
            xmlcatalog_dir = XMLCATALOG_DIR
        if not os.path.isdir(xmlcatalog_dir):
            os.mkdir(xmlcatalog_dir)
        catalog = Catalog()
        comment = 'Downloaded by eulxml %s on %s' % (
         __version__, date.today().isoformat())
        for schema_uri in xsd_schemas:
            filename = os.path.basename(schema_uri)
            schema_path = os.path.join(xmlcatalog_dir, filename)
            saved = download_schema(schema_uri, schema_path, comment)
            if saved:
                catalog.uri_list.append(Uri(name=schema_uri, uri=filename))

        if catalog.uri_list:
            with open(xmlcatalog_file, 'wb') as (xml_catalog):
                catalog.serializeDocument(xml_catalog, pretty=True)
        return catalog