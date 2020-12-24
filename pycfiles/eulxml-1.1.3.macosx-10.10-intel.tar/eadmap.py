# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/xmlmap/eadmap.py
# Compiled at: 2016-05-23 17:04:57
from __future__ import unicode_literals
from copy import deepcopy
import six
from eulxml import xmlmap
EAD_NAMESPACE = b'urn:isbn:1-931666-22-9'
XLINK_NAMESPACE = b'http://www.w3.org/1999/xlink'

class _EadBase(xmlmap.XmlObject):
    """Common EAD namespace declarations, for use by all EAD XmlObject instances."""
    ROOT_NS = EAD_NAMESPACE
    ROOT_NAME = b'ead'
    ROOT_NAMESPACES = {b'e': ROOT_NS, 
       b'xlink': XLINK_NAMESPACE, 
       b'exist': b'http://exist.sourceforge.net/NS/exist'}
    match_count = xmlmap.IntegerField(b'count(.//exist:match)')


class Note(_EadBase):
    """EAD note."""
    ROOT_NAME = b'note'
    content = xmlmap.NodeListField(b'e:p', xmlmap.XmlObject)


class Section(_EadBase):
    """Generic EAD section.  Currently only has mappings for head, paragraph, and note."""
    head = xmlmap.NodeField(b'e:head', xmlmap.XmlObject)
    content = xmlmap.NodeListField(b'e:p', xmlmap.XmlObject)
    note = xmlmap.NodeField(b'e:note', Note)


@six.python_2_unicode_compatible
class Heading(_EadBase):
    """Generic xml object for headings used under `controlaccess`"""
    source = xmlmap.StringField(b'@source')
    value = xmlmap.StringField(b'.', normalize=True)

    def __str__(self):
        return self.value


class ControlledAccessHeadings(Section):
    """
    Controlled access headings, such as subject terms, family and corporate
    names, etc.

    Expected node element passed to constructor: `contolaccess`.
    """
    person_name = xmlmap.NodeListField(b'e:persname', Heading)
    family_name = xmlmap.NodeListField(b'e:famname', Heading)
    corporate_name = xmlmap.NodeListField(b'e:corpname', Heading)
    subject = xmlmap.NodeListField(b'e:subject', Heading)
    geographic_name = xmlmap.NodeListField(b'e:geogname', Heading)
    genre_form = xmlmap.NodeListField(b'e:genreform', Heading)
    occupation = xmlmap.NodeListField(b'e:occupation', Heading)
    function = xmlmap.NodeListField(b'e:function', Heading)
    title = xmlmap.NodeListField(b'e:title', Heading)
    terms = xmlmap.NodeListField(b'e:corpname|e:famname|e:function|e:genreform|e:geogname|e:occupation|e:persname|e:subject|e:title', Heading)
    controlaccess = xmlmap.NodeListField(b'e:controlaccess', b'self')


@six.python_2_unicode_compatible
class Container(_EadBase):
    """
    Container - :class:`DescriptiveIdentification` subelement for locating materials.

    Expected node element passed to constructor: `did/container`.
    """
    type = xmlmap.StringField(b'@type')
    value = xmlmap.StringField(b'.')

    def __str__(self):
        return self.value


@six.python_2_unicode_compatible
class DateField(_EadBase):
    """
    DateField - for access to date and unitdate elements value and attributes.
    When converted to unicode, will be the non-normalized version of the date
    in the text content of the element.
    """
    normalized = xmlmap.StringField(b'@normal')
    calendar = xmlmap.StringField(b'@calendar')
    era = xmlmap.StringField(b'@era')
    value = xmlmap.StringField(b'.')

    def __str__(self):
        return self.value


class Unitid(_EadBase):
    """Unitid element"""
    ROOT_NAME = b'unitid'
    identifier = xmlmap.IntegerField(b'@identifier')
    country_code = xmlmap.StringField(b'@countrycode')
    repository_code = xmlmap.StringField(b'@repositorycode')
    value = xmlmap.StringField(b'.')


class UnitTitle(_EadBase):
    ROOT_NAME = b'unittitle'
    unitdate = xmlmap.NodeField(b'e:unitdate', DateField)
    text = xmlmap.StringField(b'text()')

    @property
    def short(self):
        """Short-form of the unit title, excluding any unit date, as an instance
        of :class:`~eulxml.xmlmap.eadmap.UnitTitle` . Can be used with formatting
        anywhere the full form of the unittitle can be used."""
        if not self.unitdate:
            return self
        ut = UnitTitle(node=deepcopy(self.node))
        ut.node.remove(ut.unitdate.node)
        return ut


class DigitalArchivalObject(_EadBase):
    """Digital Archival Object (`dao` element)"""
    ROOT_NAME = b'dao'
    audience = xmlmap.StringField(b'@audience')
    id = xmlmap.StringField(b'@id')
    title = xmlmap.StringField(b'@xlink:title')
    href = xmlmap.StringField(b'@xlink:href')
    show = xmlmap.StringField(b'@xlink:show')


class DescriptiveIdentification(_EadBase):
    """Descriptive Information (`did` element) for materials in a component"""
    ROOT_NAME = b'did'
    unitid = xmlmap.NodeField(b'e:unitid', Unitid)
    unittitle = xmlmap.NodeField(b'e:unittitle', UnitTitle)
    unitdate = xmlmap.NodeField(b'.//e:unitdate', DateField)
    physdesc = xmlmap.StringField(b'e:physdesc')
    abstract = xmlmap.NodeField(b'e:abstract', xmlmap.XmlObject)
    langmaterial = xmlmap.StringField(b'e:langmaterial')
    origination = xmlmap.StringField(b'e:origination', normalize=True)
    location = xmlmap.StringField(b'e:physloc')
    container = xmlmap.NodeListField(b'e:container', Container)
    dao_list = xmlmap.NodeListField(b'e:dao', DigitalArchivalObject)


class Component(_EadBase):
    """Generic component `cN` (`c1`-`c12`) element - a subordinate component of the materials"""
    level = xmlmap.StringField(b'@level')
    id = xmlmap.StringField(b'@id')
    did = xmlmap.NodeField(b'e:did', DescriptiveIdentification)
    use_restriction = xmlmap.NodeField(b'e:userestrict', Section)
    alternate_form = xmlmap.NodeField(b'e:altformavail', Section)
    originals_location = xmlmap.NodeField(b'e:originalsloc', Section)
    related_material = xmlmap.NodeField(b'e:relatedmaterial', Section)
    separated_material = xmlmap.NodeField(b'e:separatedmaterial', Section)
    acquisition_info = xmlmap.NodeField(b'e:acqinfo', Section)
    custodial_history = xmlmap.NodeField(b'e:custodhist', Section)
    preferred_citation = xmlmap.NodeField(b'e:prefercite', Section)
    biography_history = xmlmap.NodeField(b'e:bioghist', Section)
    bibliography = xmlmap.NodeField(b'e:bibliography', Section)
    scope_content = xmlmap.NodeField(b'e:scopecontent', Section)
    process_info = xmlmap.NodeField(b'e:processinfo', Section)
    arrangement = xmlmap.NodeField(b'e:arrangement', Section)
    other = xmlmap.NodeField(b'e:otherfindaid', Section)
    use_restriction = xmlmap.NodeField(b'e:userestrict', Section)
    access_restriction = xmlmap.NodeField(b'e:accessrestrict', Section)
    dao_list = xmlmap.NodeListField(b'e:dao', DigitalArchivalObject)
    c = xmlmap.NodeListField(b'e:c02|e:c03|e:c04|e:c05|e:c06|e:c07|e:c08|e:c09|e:c10|e:c11|e:c12', b'self')

    def hasSubseries(self):
        """Check if this component has subseries or not.

           Determined based on level of first subcomponent (series or subseries)
           or if first component has subcomponents present.

            :rtype: boolean
        """
        if self.c and self.c[0] and (self.c[0].level in ('series', 'subseries') or self.c[0].c and self.c[0].c[0]):
            return True
        return False


class SubordinateComponents(Section):
    """Description of Subordinate Components (dsc element); container lists and series.

       Expected node element passed to constructor: `ead/archdesc/dsc`.
    """
    ROOT_NAME = b'dsc'
    type = xmlmap.StringField(b'@type')
    c = xmlmap.NodeListField(b'e:c01', Component)

    def hasSeries(self):
        """Check if this finding aid has series/subseries.

           Determined based on level of first component (series) or if first
           component has subcomponents present.

           :rtype: boolean
        """
        if len(self.c) and (self.c[0].level == b'series' or self.c[0].c and self.c[0].c[0]):
            return True
        return False


@six.python_2_unicode_compatible
class Reference(_EadBase):
    """Internal linking element that may contain text.

    Expected node element passed to constructor: `ref`.
    """
    ROOT_NAME = b'ref'
    type = xmlmap.StringField(b'@xlink:type')
    target = xmlmap.StringField(b'@target')
    value = xmlmap.NodeField(b'.', xmlmap.XmlObject)

    def __str__(self):
        return self.value


class PointerGroup(_EadBase):
    """Group of pointer or reference elements in an index entry

    Expected node element passed to constructor: `ptrgrp`.
    """
    ROOT_NAME = b'ptrgrp'
    ref = xmlmap.NodeListField(b'e:ref', Reference)


class IndexEntry(_EadBase):
    """Index entry in an archival description index."""
    ROOT_NAME = b'indexentry'
    name = xmlmap.NodeField(b'e:corpname|e:famname|e:function|e:genreform|e:geogname|e:name|e:namegrp|e:occupation|e:persname|e:title|e:subject', xmlmap.XmlObject)
    ptrgroup = xmlmap.NodeField(b'e:ptrgrp', PointerGroup)


class Index(Section):
    """Index (index element); list of key terms and reference information.

       Expected node element passed to constructor: `ead/archdesc/index`.
    """
    ROOT_NAME = b'index'
    entry = xmlmap.NodeListField(b'e:indexentry', IndexEntry)
    id = xmlmap.StringField(b'@id')
    note = xmlmap.NodeField(b'e:note', Note)


class ArchivalDescription(_EadBase):
    """Archival description, contains the bulk of the information in an EAD document.

      Expected node element passed to constructor: `ead/archdesc`.
      """
    ROOT_NAME = b'archdesc'
    did = xmlmap.NodeField(b'e:did', DescriptiveIdentification)
    origination = xmlmap.StringField(b'e:did/e:origination', normalize=True)
    unitid = xmlmap.NodeField(b'e:did/e:unitid', Unitid)
    extent = xmlmap.StringListField(b'e:did/e:physdesc/e:extent')
    langmaterial = xmlmap.StringField(b'e:did/e:langmaterial')
    location = xmlmap.StringField(b'e:did/e:physloc')
    access_restriction = xmlmap.NodeField(b'e:accessrestrict', Section)
    use_restriction = xmlmap.NodeField(b'e:userestrict', Section)
    alternate_form = xmlmap.NodeField(b'e:altformavail', Section)
    originals_location = xmlmap.NodeField(b'e:originalsloc', Section)
    related_material = xmlmap.NodeField(b'e:relatedmaterial', Section)
    separated_material = xmlmap.NodeField(b'e:separatedmaterial', Section)
    acquisition_info = xmlmap.NodeField(b'e:acqinfo', Section)
    custodial_history = xmlmap.NodeField(b'e:custodhist', Section)
    preferred_citation = xmlmap.NodeField(b'e:prefercite', Section)
    biography_history = xmlmap.NodeField(b'e:bioghist', Section)
    bibliography = xmlmap.NodeField(b'e:bibliography', Section)
    scope_content = xmlmap.NodeField(b'e:scopecontent', Section)
    process_info = xmlmap.NodeField(b'e:archdesc/e:processinfo', Section)
    arrangement = xmlmap.NodeField(b'e:arrangement', Section)
    other = xmlmap.NodeField(b'e:otherfindaid', Section)
    controlaccess = xmlmap.NodeField(b'e:controlaccess', ControlledAccessHeadings)
    index = xmlmap.NodeListField(b'e:index', Index)
    dao_list = xmlmap.NodeListField(b'e:dao', DigitalArchivalObject)


class Address(_EadBase):
    """Address information.

      Expected node element passed to constructor: `address`.
    """
    ROOT_NAME = b'address'
    lines = xmlmap.StringListField(b'e:addressline')


class PublicationStatement(_EadBase):
    """Publication information for an EAD document.

    Expected node element passed to constructor: `ead/eadheader/filedesc/publicationstmt`.
    """
    ROOT_NAME = b'publicationstmt'
    date = xmlmap.NodeField(b'e:date', DateField)
    publisher = xmlmap.StringField(b'e:publisher')
    address = xmlmap.NodeField(b'e:address', Address)


class ProfileDescription(_EadBase):
    """Profile Descriptor for an EAD document.
       Expected node element passed to constructor: 'ead/eadheader/profiledesc'.
    """
    ROOT_NAME = b'profiledesc'
    date = xmlmap.NodeField(b'e:creation/e:date', DateField)
    languages = xmlmap.StringListField(b'e:langusage/e:language')
    language_codes = xmlmap.StringListField(b'e:langusage/e:language/@langcode')


class FileDescription(_EadBase):
    """Bibliographic information about this EAD document.

      Expected node element passed to constructor: `ead/eadheader/filedesc`.
    """
    ROOT_NAME = b'filedesc'
    publication = xmlmap.NodeField(b'e:publicationstmt', PublicationStatement)


class EadId(_EadBase):
    """EAD identifier for a single EAD finding aid document.

    Expected element passed to constructor: `ead/eadheader/eadid`.
    """
    ROOT_NAME = b'eadid'
    country = xmlmap.StringField(b'@countrycode')
    maintenance_agency = xmlmap.StringField(b'@mainagencycode')
    url = xmlmap.StringField(b'@url')
    identifier = xmlmap.StringField(b'@identifier')
    value = xmlmap.StringField(b'.', normalize=True)


class EncodedArchivalDescription(_EadBase):
    """:class:`~eulxml.xmlmap.XmlObject` for an Encoded Archival Description
    (EAD) Finding Aid (Schema-based).  All XPaths use the EAD namespace; this
    class can not be used with non-namespaced, DTD-based EAD.

    Expects node passed to constructor to be top-level `ead` element.
    """
    XSD_SCHEMA = b'http://www.loc.gov/ead/ead.xsd'
    id = xmlmap.StringField(b'@id')
    eadid = xmlmap.NodeField(b'e:eadheader/e:eadid', EadId)
    title = xmlmap.NodeField(b'e:eadheader/e:filedesc/e:titlestmt/e:titleproper', xmlmap.XmlObject)
    author = xmlmap.StringField(b'e:eadheader/e:filedesc/e:titlestmt/e:author')
    unittitle = xmlmap.NodeField(b'e:archdesc[@level="collection"]/e:did/e:unittitle', UnitTitle)
    physical_desc = xmlmap.StringField(b'e:archdesc[@level="collection"]/e:did/e:physdesc')
    abstract = xmlmap.NodeField(b'e:archdesc[@level="collection"]/e:did/e:abstract', xmlmap.XmlObject)
    archdesc = xmlmap.NodeField(b'e:archdesc', ArchivalDescription)
    dsc = xmlmap.NodeField(b'e:archdesc/e:dsc', SubordinateComponents)
    file_desc = xmlmap.NodeField(b'e:eadheader/e:filedesc', FileDescription)
    profiledesc = xmlmap.NodeField(b'e:eadheader/e:profiledesc', ProfileDescription)