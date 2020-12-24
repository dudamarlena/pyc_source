# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/xmlmap/premis.py
# Compiled at: 2016-02-19 17:15:24
"""
:mod:`eulxml.xmlmap` classes for dealing with the `PREMIS
<http://www.loc.gov/standards/premis/>`_ metadata format for
preservation metadata.

-----
"""
from __future__ import unicode_literals
from eulxml import xmlmap
PREMIS_NAMESPACE = b'info:lc/xmlns/premis-v2'
PREMIS_SCHEMA = b'http://www.loc.gov/standards/premis/v2/premis-v2-1.xsd'

class BasePremis(xmlmap.XmlObject):
    """Base PREMIS class with namespace declaration common to all PREMIS
    XmlObjects.

    .. Note::

       This class is intended mostly for internal use, but could be
       useful when extending or adding additional PREMIS
       :class:`~eulxml.xmlmap.XmlObject` classes.  The
       :attr:`PREMIS_NAMESPACE` is mapped to the prefix **p**.
    """
    ROOT_NS = PREMIS_NAMESPACE
    ROOT_NAMESPACES = {b'p': PREMIS_NAMESPACE, 
       b'xsi': b'http://www.w3.org/2001/XMLSchema-instance'}


class PremisRoot(BasePremis):
    """Base class with a schema declaration for any of the
    root/stand-alone PREMIS elements:

     * ``<premis>`` - :class:`Premis`
     * ``<object>`` - :class:`Object`
     * ``<event>``  - :class:`Event`
     * ``<agent>``
     * ``<rights>``

    """
    XSD_SCHEMA = PREMIS_SCHEMA


class Object(PremisRoot):
    """Preliminary :class:`~eulxml.xmlmap.XmlObject` for a PREMIS
    object.

    Curently only includes the minimal required fields.
    """
    ROOT_NAME = b'object'
    type = xmlmap.StringField(b'@xsi:type')
    id_type = xmlmap.StringField(b'p:objectIdentifier/p:objectIdentifierType')
    id = xmlmap.StringField(b'p:objectIdentifier/p:objectIdentifierValue')


class Event(PremisRoot):
    """Preliminary :class:`~eulxml.xmlmap.XmlObject` for a PREMIS
    event.

    .. Note::

      The PREMIS schema requires that elements occur in a specified
      order, which :mod:`eulxml` does not currently handle or manage.
      As a work-around, when creating a new :class:`Event` from
      scratch, you should set the following required fields in this
      order: identifier (:attr:`id` and :attr:`ad_type`

    """
    ROOT_NAME = b'event'
    type = xmlmap.StringField(b'p:eventType')
    id_type = xmlmap.StringField(b'p:eventIdentifier/p:eventIdentifierType')
    id = xmlmap.StringField(b'p:eventIdentifier/p:eventIdentifierValue')
    date = xmlmap.StringField(b'p:eventDateTime')
    detail = xmlmap.StringField(b'p:eventDetail', required=False)
    outcome = xmlmap.StringField(b'p:eventOutcomeInformation/p:eventOutcome', required=False)
    agent_type = xmlmap.StringField(b'p:linkingAgentIdentifier/p:linkingAgentIdentifierType')
    agent_id = xmlmap.StringField(b'p:linkingAgentIdentifier/p:linkingAgentIdentifierValue')
    object_type = xmlmap.StringField(b'p:linkingObjectIdentifier/p:linkingObjectIdentifierType')
    object_id = xmlmap.StringField(b'p:linkingObjectIdentifier/p:linkingObjectIdentifierValue')


class Premis(PremisRoot):
    """Preliminary :class:`~eulxml.xmlmap.XmlObject` for a PREMIS
    container element that can contain any of the other top-level
    PREMIS elements.

    Curently only includes mappings for a single object and list of
    events.
    """
    ROOT_NAME = b'premis'
    version = xmlmap.StringField(b'@version')
    object = xmlmap.NodeField(b'p:object', Object)
    events = xmlmap.NodeListField(b'p:event', Event)

    def __init__(self, *args, **kwargs):
        if b'version' not in kwargs:
            kwargs[b'version'] = b'2.1'
        super(Premis, self).__init__(*args, **kwargs)