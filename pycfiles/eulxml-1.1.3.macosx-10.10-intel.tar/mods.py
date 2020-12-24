# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/xmlmap/mods.py
# Compiled at: 2016-02-19 17:15:24
"""
:mod:`eulxml.xmlmap` classes for dealing with the
`MODS <http://www.loc.gov/standards/mods/>`_ metadata format
(Metadata Object Description Schema).
"""
from __future__ import unicode_literals
import six
from eulxml import xmlmap
MODS_NAMESPACE = b'http://www.loc.gov/mods/v3'
MODS_SCHEMA = b'http://www.loc.gov/standards/mods/mods.xsd'
MODSv34_SCHEMA = b'http://www.loc.gov/standards/mods/v3/mods-3-4.xsd'

class Common(xmlmap.XmlObject):
    """MODS class with namespace declaration common to all MODS
    XmlObjects.  Defines the MODS schema (e.g., for use with
    :class:`xmlmap.SchemaField`), but by sets ``schema_validate`` to
    False.
    """
    ROOT_NS = MODS_NAMESPACE
    ROOT_NAMESPACES = {b'mods': MODS_NAMESPACE}
    XSD_SCHEMA = MODSv34_SCHEMA
    schema_validate = False


@six.python_2_unicode_compatible
class Date(Common):
    """:class:`~eulxml.xmlmap.XmlObject` for MODS date element (common fields
    for the dates under mods:originInfo)."""
    date = xmlmap.StringField(b'text()')
    key_date = xmlmap.SimpleBooleanField(b'@keyDate', b'yes', false=None)
    encoding = xmlmap.SchemaField(b'@encoding', b'dateEncodingAttributeDefinition')
    point = xmlmap.SchemaField(b'@point', b'datePointAttributeDefinition')
    qualifier = xmlmap.SchemaField(b'@qualifier', b'dateQualifierAttributeDefinition')

    def is_empty(self):
        """Returns False if no date value is set; returns True if any date value
        is set.  Attributes are ignored for determining whether or not the
        date should be considered empty, as they are only meaningful in
        reference to a date value."""
        return not self.node.text

    def __str__(self):
        return self.date


class DateCreated(Date):
    ROOT_NAME = b'dateCreated'


class DateIssued(Date):
    ROOT_NAME = b'dateIssued'


class DateCaptured(Date):
    ROOT_NAME = b'dateCaptured'


class DateValid(Date):
    ROOT_NAME = b'dateValid'


class DateModified(Date):
    ROOT_NAME = b'dateModified'


class CopyrightDate(Date):
    ROOT_NAME = b'copyrightDate'


class DateOther(Date):
    ROOT_NAME = b'dateOther'
    type = xmlmap.StringField(b'@type')


class OriginInfo(Common):
    """:class:`~eulxml.xmlmap.XmlObject` for MODS originInfo element (incomplete)"""
    ROOT_NAME = b'originInfo'
    created = xmlmap.NodeListField(b'mods:dateCreated', DateCreated, verbose_name=b'Date Created', help_text=b'Date the resource was first created (e.g., date of recording,' + b' photograph taken, or letter written)')
    issued = xmlmap.NodeListField(b'mods:dateIssued', DateIssued, verbose_name=b'Date Issued', help_text=b'Date the resource was published, released, or issued')
    captured = xmlmap.NodeListField(b'mods:dateCaptured', DateCaptured, verbose_name=b'Date Captured', help_text=b'Date on which the resource was digitized or a subsequent snapshot was taken')
    valid = xmlmap.NodeListField(b'mods:dateValid', DateValid, verbose_name=b'Date Valid', help_text=b'Date in which the content of a resource is valid')
    modified = xmlmap.NodeListField(b'mods:dateModified', DateModified, verbose_name=b'Date Modified', help_text=b'Date in which a resource is modified or changed')
    copyright = xmlmap.NodeListField(b'mods:copyrightDate', CopyrightDate, verbose_name=b'Copyright Date', help_text=b'Date in which a resource is copyrighted')
    other = xmlmap.NodeListField(b'mods:dateOther', DateOther, verbose_name=b'Other Date', help_text=b'Date that does not fall into another category but is important to record')
    publisher = xmlmap.StringField(b'mods:publisher')

    def is_empty(self):
        """Returns True if all child date elements present are empty
        and other nodes are not set.  Returns False if any child date
        elements are not empty or other nodes are set."""
        return all(date.is_empty() for date in [self.created, self.issued]) and not self.publisher


class RecordInfo(Common):
    ROOT_NAME = b'recordInfo'
    record_id = xmlmap.StringField(b'mods:recordIdentifier')
    record_origin = xmlmap.StringField(b'mods:recordOrigin')
    creation_date = xmlmap.StringField(b'mods:recordCreationDate[@encoding="w3cdtf"]')
    change_date = xmlmap.StringField(b'mods:recordChangeDate[@encoding="w3cdtf"]')


class Note(Common):
    """:class:`~eulxml.xmlmap.XmlObject` for MODS note element"""
    ROOT_NAME = b'note'
    label = xmlmap.StringField(b'@displayLabel')
    type = xmlmap.StringField(b'@type')
    text = xmlmap.StringField(b'text()')


class TypedNote(Note):
    """Extends :class:`Note` to modify :meth:`is_empty` behavior-- considered
    empty when a type attribute is set without any text."""

    def is_empty(self):
        """Returns True if the root node contains no child elements, no text,
        and no attributes other than **type**. Returns False if any are present."""
        non_type_attributes = [ attr for attr in self.node.attrib.keys() if attr != b'type' ]
        return len(self.node) == 0 and len(non_type_attributes) == 0 and not self.node.text and not self.node.tail


class Identifier(Common):
    """:class:`~eulxml.xmlmap.XmlObject` for MODS identifier"""
    ROOT_NAME = b'identifier'
    type = xmlmap.StringField(b'@type')
    text = xmlmap.StringField(b'text()')
    label = xmlmap.StringField(b'@displayLabel')


class AccessCondition(Common):
    """:class:`~eulxml.xmlmap.XmlObject` for MODS accessCondition"""
    ROOT_NAME = b'accessCondition'
    type = xmlmap.StringField(b'@type', choices=[
     b'restrictions on access', b'use and reproduction'])
    text = xmlmap.StringField(b'text()')


class NamePart(Common):
    """:class:`~eulxml.xmlmap.XmlObject` for MODS namePart"""
    ROOT_NAME = b'namePart'
    type = xmlmap.SchemaField(b'@type', b'namePartTypeAttributeDefinition', required=False)
    text = xmlmap.StringField(b'text()')


class Role(Common):
    """:class:`~eulxml.xmlmap.XmlObject` for MODS role"""
    ROOT_NAME = b'role'
    type = xmlmap.StringField(b'mods:roleTerm/@type')
    authority = xmlmap.StringField(b'mods:roleTerm/@authority', choices=[b'', b'marcrelator', b'local'])
    text = xmlmap.StringField(b'mods:roleTerm')


class Name(Common):
    """:class:`~eulxml.xmlmap.XmlObject` for MODS name"""
    ROOT_NAME = b'name'
    type = xmlmap.SchemaField(b'@type', b'nameTypeAttributeDefinition', required=False)
    authority = xmlmap.StringField(b'@authority', choices=[b'', b'local', b'naf'], required=False)
    id = xmlmap.StringField(b'@ID', required=False)
    name_parts = xmlmap.NodeListField(b'mods:namePart', NamePart)
    display_form = xmlmap.StringField(b'mods:displayForm')
    affiliation = xmlmap.StringField(b'mods:affiliation')
    roles = xmlmap.NodeListField(b'mods:role', Role)

    def __unicode__(self):
        return (b' ').join([ unicode(part) for part in self.name_parts ])


class Genre(Common):
    ROOT_NAME = b'genre'
    authority = xmlmap.StringField(b'@authority')
    text = xmlmap.StringField(b'text()')


class LanguageTerm(Common):
    ROOT_NAME = b'languageTerm'
    type = xmlmap.StringField(b'@type')
    authority = xmlmap.StringField(b'@authority')
    text = xmlmap.StringField(b'text()')


class Language(Common):
    ROOT_NAME = b'language'
    terms = xmlmap.NodeListField(b'mods:languageTerm', LanguageTerm)


class Location(Common):
    ROOT_NAME = b'location'
    physical = xmlmap.StringField(b'mods:physicalLocation')
    url = xmlmap.StringField(b'mods:url')


class Subject(Common):
    ROOT_NAME = b'subject'
    authority = xmlmap.StringField(b'@authority')
    id = xmlmap.StringField(b'@ID')
    geographic = xmlmap.StringField(b'mods:geographic')
    name = xmlmap.NodeField(b'mods:name', Name)
    topic = xmlmap.StringField(b'mods:topic')
    title = xmlmap.StringField(b'mods:titleInfo/mods:title')


class TitleInfo(Common):
    ROOT_NAME = b'titleInfo'
    title = xmlmap.StringField(b'mods:title')
    subtitle = xmlmap.StringField(b'mods:subTitle')
    part_number = xmlmap.StringField(b'mods:partNumber')
    part_name = xmlmap.StringField(b'mods:partName')
    non_sort = xmlmap.StringField(b'mods:nonSort')
    type = xmlmap.SchemaField(b'@type', b'titleInfoTypeAttributeDefinition')
    label = xmlmap.StringField(b'@displayLabel')

    def is_empty(self):
        """Returns True if all titleInfo subfields are not set or
        empty; returns False if any of the fields are not empty."""
        return not bool(self.title or self.subtitle or self.part_number or self.part_name or self.non_sort or self.type)


class Abstract(Common):
    ROOT_NAME = b'abstract'
    text = xmlmap.StringField(b'text()')
    type = xmlmap.StringField(b'@type')
    label = xmlmap.StringField(b'@displayLabel')


class PhysicalDescription(Common):
    ROOT_NAME = b'physicalDescription'
    media_type = xmlmap.StringField(b'mods:internetMediaType')
    extent = xmlmap.StringField(b'mods:extent')


class PartDetail(Common):
    ROOT_NAME = b'detail'
    type = xmlmap.StringField(b'@type')
    number = xmlmap.StringField(b'mods:number')

    def is_empty(self):
        """Returns False if no number value is set; returns True if
        any number value is set.  Type attribute is ignored for
        determining whether or not this node should be considered
        empty."""
        return not self.number


class PartExtent(Common):
    ROOT_NAME = b'extent'
    unit = xmlmap.StringField(b'@unit')
    start = xmlmap.StringField(b'mods:start')
    end = xmlmap.StringField(b'mods:end')
    total = xmlmap.StringField(b'mods:total')

    def is_empty(self):
        """Returns False if no extent value is set; returns True if
        any extent value is set.  Unit attribute is ignored for
        determining whether or not this node should be considered
        empty."""
        return not bool(self.start or self.end or self.total)


class Part(Common):
    ROOT_NAME = b'part'
    type = xmlmap.StringField(b'@type')
    details = xmlmap.NodeListField(b'mods:detail', PartDetail)
    extent = xmlmap.NodeField(b'mods:extent', PartExtent)

    def is_empty(self):
        """Returns True if details, extent, and type are not set or
        return True for ``is_empty``; returns False if any of the
        fields are not empty."""
        return all(field.is_empty() for field in [self.details, self.extent] if field is not None) and not self.type


class BaseMods(Common):
    """:class:`~eulxml.xmlmap.XmlObject` with common field declarations for all
    top-level MODS elements; base class for :class:`MODS` and :class:`RelatedItem`."""
    schema_validate = True
    id = xmlmap.StringField(b'@ID')
    title = xmlmap.StringField(b'mods:titleInfo/mods:title')
    title_info = xmlmap.NodeField(b'mods:titleInfo', TitleInfo)
    title_info_list = xmlmap.NodeListField(b'mods:titleInfo', TitleInfo)
    resource_type = xmlmap.SchemaField(b'mods:typeOfResource', b'resourceTypeDefinition')
    name = xmlmap.NodeField(b'mods:name', Name)
    names = xmlmap.NodeListField(b'mods:name', Name)
    note = xmlmap.NodeField(b'mods:note', Note)
    notes = xmlmap.NodeListField(b'mods:note', Note)
    origin_info = xmlmap.NodeField(b'mods:originInfo', OriginInfo)
    record_info = xmlmap.NodeField(b'mods:recordInfo', RecordInfo)
    identifiers = xmlmap.NodeListField(b'mods:identifier', Identifier)
    access_conditions = xmlmap.NodeListField(b'mods:accessCondition', AccessCondition)
    genres = xmlmap.NodeListField(b'mods:genre', Genre)
    languages = xmlmap.NodeListField(b'mods:language', Language)
    location = xmlmap.StringField(b'mods:location/mods:physicalLocation', required=False)
    locations = xmlmap.NodeListField(b'mods:location', Location)
    subjects = xmlmap.NodeListField(b'mods:subject', Subject)
    physical_description = xmlmap.NodeField(b'mods:physicalDescription', PhysicalDescription)
    abstract = xmlmap.NodeField(b'mods:abstract', Abstract)
    parts = xmlmap.NodeListField(b'mods:part', Part)


class RelatedItem(BaseMods):
    """:class:`~eulxml.xmlmap.XmlObject` for MODS relatedItem: contains all the
    top-level MODS fields defined by :class:`BaseMods`, plus a type attribute."""
    ROOT_NAME = b'relatedItem'
    type = xmlmap.SchemaField(b'@type', b'relatedItemTypeAttributeDefinition')
    label = xmlmap.StringField(b'@displayLabel')


class MODS(BaseMods):
    """Top-level :class:`~eulxml.xmlmap.XmlObject` for a MODS metadata record.
    Inherits all standard top-level MODS fields from :class:`BaseMods` and adds
    a mapping for :class:`RelatedItem`.
    """
    ROOT_NAME = b'mods'
    related_items = xmlmap.NodeListField(b'mods:relatedItem', RelatedItem)


class MODSv34(MODS):
    """:class:`~eulxml.xmlmap.XmlObject` for MODS version 3.4.  Currently
    consists of all the same fields as :class:`MODS`, but loads the MODS version
    3.4 schema for validation.
    """
    XSD_SCHEMA = MODSv34_SCHEMA