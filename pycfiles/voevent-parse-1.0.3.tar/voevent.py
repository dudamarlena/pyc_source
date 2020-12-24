# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/staley/code/voevent/voevent-parse/src/voeventparse/voevent.py
# Compiled at: 2017-02-22 06:35:44
"""Routines for handling etrees representing VOEvent packets."""
from __future__ import absolute_import
from __future__ import unicode_literals
from six import string_types
from lxml import objectify, etree
import collections, pytz, voeventparse.definitions
voevent_v2_0_schema = etree.XMLSchema(etree.fromstring(voeventparse.definitions.v2_0_schema_str))
from ._version import get_versions
__version__ = get_versions()[b'version']

def Voevent(stream, stream_id, role):
    """Create a new VOEvent element tree, with specified IVORN and role.

    Args:

        stream (string): used to construct the IVORN like so::

                ivorn = 'ivo://' + stream + '#' + stream_id

            (N.B. ``stream_id`` is converted to string if required.)
            So, e.g. we might set::

                stream='voevent.soton.ac.uk/super_exciting_events'
                stream_id=77

        stream_id (string): See above.

        role (string): role as defined in VOEvent spec.
            (See also  :py:class:`.definitions.roles`)

    Returns:
        Root-node of the VOEvent, as represented by an lxml.objectify element
        tree ('etree'). See also
        http://lxml.de/objectify.html#the-lxml-objectify-api
    """
    parser = objectify.makeparser(remove_blank_text=True)
    v = objectify.fromstring(voeventparse.definitions.v2_0_skeleton_str, parser=parser)
    _remove_root_tag_prefix(v)
    if not isinstance(stream_id, string_types):
        stream_id = repr(stream_id)
    v.attrib[b'ivorn'] = (b'').join((b'ivo://', stream, b'#', stream_id))
    v.attrib[b'role'] = role
    etree.SubElement(v, b'Who')
    etree.SubElement(v, b'What')
    etree.SubElement(v, b'WhereWhen')
    v.Who.Description = (b'VOEvent created with voevent-parse, version {}. See https://github.com/timstaley/voevent-parse for details.').format(__version__)
    return v


def loads(s, check_version=True):
    """
    Load VOEvent from bytes.

    This parses a VOEvent XML packet string, taking care of some subtleties.
    For Python 3 users, ``s`` should be a bytes object - see also
    http://lxml.de/FAQ.html,
    "Why can't lxml parse my XML from unicode strings?"
    (Python 2 users can stick with old-school ``str`` type if preferred)

    By default, will raise an exception if the VOEvent is not of version
    2.0. This can be disabled but voevent-parse routines are untested with
    other versions.

    Args:
        s (bytes): Bytes containing raw XML.
        check_version (bool): (Default=True) Checks that the VOEvent is of a
            supported schema version - currently only v2.0 is supported.
    Returns:
        :py:class:`Voevent`: Root-node of the  etree.
    Raises:
        exceptions.ValueError: If passed a VOEvent of wrong schema version
            (i.e. schema 1.1)

    """
    v = objectify.fromstring(s)
    _remove_root_tag_prefix(v)
    if check_version:
        version = v.attrib[b'version']
        if not version == b'2.0':
            raise ValueError(b'Unsupported VOEvent schema version:' + version)
    return v


def load(file, check_version=True):
    """Load VOEvent from file object.

    A simple wrapper to read a file before passing the contents to
    :py:func:`.loads`. Use with an open file object, e.g.::

        with open('/path/to/voevent.xml', 'rb') as f:
            v = vp.load(f)

    Args:
        file (file): An open file object (binary mode preferred), see also
            http://lxml.de/FAQ.html :
            "Can lxml parse from file objects opened in unicode/text mode?"

        check_version (bool): (Default=True) Checks that the VOEvent is of a
            supported schema version - currently only v2.0 is supported.
    Returns:
        :py:class:`Voevent`: Root-node of the  etree.
    """
    s = file.read()
    return loads(s, check_version)


def dumps(voevent, pretty_print=False, xml_declaration=True, encoding=b'UTF-8'):
    """Converts voevent to string.

    .. note:: Default encoding is UTF-8, in line with VOE2.0 schema.
        Declaring the encoding can cause diffs with the original loaded VOEvent,
        but I think it's probably the right thing to do (and lxml doesn't
        really give you a choice anyway).

    Args:
        voevent (:class:`Voevent`): Root node of the VOevent etree.
        pretty_print (bool): indent the output for improved human-legibility
            when possible. See also:
            http://lxml.de/FAQ.html#why-doesn-t-the-pretty-print-option-reformat-my-xml-output
        xml_declaration (bool): Prepends a doctype tag to the string output,
            i.e. something like ``<?xml version='1.0' encoding='UTF-8'?>``
    Returns:
        bytes: Bytestring containing raw XML representation of VOEvent.

    """
    _return_to_standard_xml(voevent)
    s = etree.tostring(voevent, pretty_print=pretty_print, xml_declaration=xml_declaration, encoding=encoding)
    _remove_root_tag_prefix(voevent)
    return s


def dump(voevent, file, pretty_print=True, xml_declaration=True):
    """Writes the voevent to the file object.

    e.g.::

        with open('/tmp/myvoevent.xml','wb') as f:
            voeventparse.dump(v, f)

    Args:
        voevent(:class:`Voevent`): Root node of the VOevent etree.
        file (file): An open (binary mode) file object for writing.
        pretty_print
        pretty_print(bool): See :func:`dumps`
        xml_declaration(bool): See :func:`dumps`
    """
    file.write(dumps(voevent, pretty_print, xml_declaration))


def valid_as_v2_0(voevent):
    """Tests if a voevent conforms to the schema.

    Args:
        voevent(:class:`Voevent`): Root node of a VOEvent etree.
    Returns:
        bool: Whether VOEvent is valid
    """
    _return_to_standard_xml(voevent)
    valid_bool = voevent_v2_0_schema.validate(voevent)
    _remove_root_tag_prefix(voevent)
    return valid_bool


def assert_valid_as_v2_0(voevent):
    """
    Raises :py:obj:`lxml.etree.DocumentInvalid` if voevent is invalid.

    Especially useful for debugging,
    since the stack trace contains a reason for the invalidation.

    Args:
        voevent(:class:`Voevent`): Root node of a VOEvent etree.
    Raises:
         :py:obj:`lxml.etree.DocumentInvalid`: if VOEvent does not conform to
            schema.
    """
    _return_to_standard_xml(voevent)
    voevent_v2_0_schema.assertValid(voevent)
    _remove_root_tag_prefix(voevent)


def set_who(voevent, date=None, author_ivorn=None):
    """Sets the minimal 'Who' attributes:  date of authoring, AuthorIVORN.

    Args:
        voevent(:class:`Voevent`): Root node of a VOEvent etree.
        date(datetime.datetime): Date of authoring.
            NB Microseconds are ignored, as per the VOEvent spec.
        author_ivorn(string): Short author identifier,
            e.g. ``voevent.4pisky.org/ALARRM``.
            Note that the prefix ``ivo://`` will be prepended internally.

    """
    if author_ivorn is not None:
        voevent.Who.AuthorIVORN = (b'').join((b'ivo://', author_ivorn))
    if date is not None:
        voevent.Who.Date = date.replace(microsecond=0).isoformat()
    return


def set_author(voevent, title=None, shortName=None, logoURL=None, contactName=None, contactEmail=None, contactPhone=None, contributor=None):
    """For setting fields in the detailed author description.

    This can optionally be neglected if a well defined AuthorIVORN is supplied.

    .. note:: Unusually for this library,
        the args here use CamelCase naming convention,
        since there's a direct mapping to the ``Author.*``
        attributes to which they will be assigned.

    Args:
        voevent(:class:`Voevent`): Root node of a VOEvent etree.
            The rest of the arguments are strings corresponding to child elements.
    """
    AuthChildren = locals()
    AuthChildren.pop(b'voevent')
    if not voevent.xpath(b'Who/Author'):
        etree.SubElement(voevent.Who, b'Author')
    for k, v in AuthChildren.items():
        if v is not None:
            voevent.Who.Author[k] = v

    return


def add_where_when(voevent, coords, obs_time, observatory_location, allow_tz_naive_datetime=False):
    """
    Add details of an observation to the WhereWhen section.

    We

    Args:
        voevent(:class:`Voevent`): Root node of a VOEvent etree.
        coords(:class:`.Position2D`): Sky co-ordinates of event.
        obs_time(datetime.datetime): Nominal DateTime of the observation. Must
            either be timezone-aware, or should be carefully verified as
            representing UTC and then set parameter
            ``allow_tz_naive_datetime=True``.
        observatory_location(string): Telescope locale, e.g. 'La Palma'.
            May be a generic location as listed under
            :class:`voeventparse.definitions.observatory_location`.
        allow_tz_naive_datetime (bool): (Default False). Accept timezone-naive
            datetime-timestamps. See comments for ``obs_time``.

    """
    if obs_time.tzinfo is not None:
        utc_naive_obs_time = obs_time.astimezone(pytz.utc).replace(tzinfo=None)
    elif not allow_tz_naive_datetime:
        raise ValueError(b"Datetime passed without tzinfo, cannot be sure if it is really a UTC timestamp. Please verify function call and either add tzinfo or pass parameter 'allow_tz_naive_obstime=True', as appropriate")
    else:
        utc_naive_obs_time = obs_time
    obs_data = etree.SubElement(voevent.WhereWhen, b'ObsDataLocation')
    etree.SubElement(obs_data, b'ObservatoryLocation', id=observatory_location)
    ol = etree.SubElement(obs_data, b'ObservationLocation')
    etree.SubElement(ol, b'AstroCoordSystem', id=coords.system)
    ac = etree.SubElement(ol, b'AstroCoords', coord_system_id=coords.system)
    time = etree.SubElement(ac, b'Time', unit=b's')
    instant = etree.SubElement(time, b'TimeInstant')
    instant.ISOTime = utc_naive_obs_time.isoformat()
    pos2d = etree.SubElement(ac, b'Position2D', unit=coords.units)
    pos2d.Name1 = b'RA'
    pos2d.Name2 = b'Dec'
    pos2d_val = etree.SubElement(pos2d, b'Value2')
    pos2d_val.C1 = coords.ra
    pos2d_val.C2 = coords.dec
    pos2d.Error2Radius = coords.err
    return


def add_how(voevent, descriptions=None, references=None):
    """Add descriptions or references to the How section.

    Args:
        voevent(:class:`Voevent`): Root node of a VOEvent etree.
        descriptions(string): Description string, or list of description
            strings.
        references(:py:class:`voeventparse.misc.Reference`): A reference element
            (or list thereof).
    """
    if not voevent.xpath(b'How'):
        etree.SubElement(voevent, b'How')
    if descriptions is not None:
        for desc in _listify(descriptions):
            etree.SubElement(voevent.How, b'Description')
            voevent.How.Description[-1] = desc

    if references is not None:
        voevent.How.extend(_listify(references))
    return


def add_why(voevent, importance=None, expires=None, inferences=None):
    """Add Inferences, or set importance / expires attributes of the Why section.

    .. note::

        ``importance`` / ``expires`` are 'Why' attributes, therefore setting them
        will overwrite previous values.
        ``inferences``, on the other hand,  are appended to the list.

    Args:
        voevent(:class:`Voevent`): Root node of a VOEvent etree.
        importance(float): Value from 0.0 to 1.0
        expires(datetime.datetime): Expiration date given inferred reason
            (See voevent spec).
        inferences(:class:`voeventparse.misc.Inference`): Inference or list of
            inferences, denoting probable identifications or associations, etc.
    """
    if not voevent.xpath(b'Why'):
        etree.SubElement(voevent, b'Why')
    if importance is not None:
        voevent.Why.attrib[b'importance'] = str(importance)
    if expires is not None:
        voevent.Why.attrib[b'expires'] = expires.replace(microsecond=0).isoformat()
    if inferences is not None:
        voevent.Why.extend(_listify(inferences))
    return


def add_citations(voevent, event_ivorns):
    """Add citations to other voevents.

    The schema mandates that the 'Citations' section must either be entirely
    absent, or non-empty - hence we require this wrapper function for its
    creation prior to listing the first citation.

    Args:
        voevent(:class:`Voevent`): Root node of a VOEvent etree.
        event_ivorns (:class:`voeventparse.misc.EventIvorn`): List of EventIvorn
            elements to add to citation list.

    """
    if not voevent.xpath(b'Citations'):
        etree.SubElement(voevent, b'Citations')
    voevent.Citations.extend(_listify(event_ivorns))


def _remove_root_tag_prefix(v):
    """
    Removes 'voe' namespace prefix from root tag.

    When we load in a VOEvent, the root element has a tag prefixed by
     the VOE namespace, e.g. {http://www.ivoa.net/xml/VOEvent/v2.0}VOEvent
    Because objectify expects child elements to have the same namespace as
    their parent, this breaks the python-attribute style access mechanism.
    We can get around it without altering root, via e.g
     who = v['{}Who']

    Alternatively, we can temporarily ditch the namespace altogether.
    This makes access to elements easier, but requires care to reinsert
    the namespace upon output.

    I've gone for the latter option.
    """
    if v.prefix:
        etree.SubElement(v, b'original_prefix')
        v[b'{}original_prefix'][0] = v.prefix
        v.tag = v.tag.replace((b'').join((b'{', v.nsmap[v.prefix], b'}')), b'')


def _reinsert_root_tag_prefix(v):
    """
    Returns namespace prefix to root tag, if it had one.
    """
    if hasattr(v, b'original_prefix'):
        original_prefix = v.original_prefix
        del v.original_prefix
        v.tag = (b'').join((b'{', v.nsmap[original_prefix], b'}VOEvent'))


def _return_to_standard_xml(v):
    objectify.deannotate(v)
    _reinsert_root_tag_prefix(v)
    etree.cleanup_namespaces(v)


def _listify(x):
    """Ensure x is iterable; if not then enclose it in a list and return it."""
    if isinstance(x, string_types):
        return [x]
    else:
        if isinstance(x, collections.Iterable):
            return x
        return [x]