# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redlink/format.py
# Compiled at: 2015-11-07 07:42:52


class FormatDef:
    """
    Format (internal) definition
    """

    def __init__(self, name, mimetype, rdflibMapping=None):
        self.name = name
        self.mimetype = mimetype
        self.rdflibMapping = rdflibMapping

    def __str__(self):
        return '%s[%s]' % (self.name, self.mimetype)

    def __cmp__(self, other):
        if other is None:
            return -1
        else:
            if isinstance(other, FormatDef):
                return -1 * int(not self.mimetype == other.mimetype)
            if '/' in other:
                if ';' in other:
                    return -1 * int(not self.mimetype == other.split(';')[0])
                else:
                    return -1 * int(not self.mimetype == other)

            else:
                return -1 * int(not self.name == other)
            return

    def __eq__(self, other):
        if other is None:
            return -1
        else:
            if isinstance(other, FormatDef):
                return self.mimetype == other.mimetype
            if '/' in other:
                if ';' in other:
                    return self.mimetype == other.split(';')[0]
                else:
                    return self.mimetype == other

            else:
                return self.name == other
            return


class Format:
    """
    Redlink formats
    """
    TEXT = FormatDef('text', 'text/plain')
    PDF = FormatDef('pdf', 'application/pdf')
    HTML = FormatDef('html', 'text/html')
    OFFICE = FormatDef('office', 'application/doc')
    OCTETSTREAM = FormatDef('octetstream', 'application/octet-stream')
    JSON = FormatDef('json', 'application/json')
    XML = FormatDef('xml', 'application/xml')
    REDLINKJSON = FormatDef('redlinkjson', 'application/redlink-analysis+json')
    REDLINKXML = FormatDef('redlinkxml', 'application/redlink-analysis+xml')
    JSONLD = FormatDef('jsonld', 'application/ld+json', 'json-ld')
    RDFXML = FormatDef('rdfxml', 'application/rdf+xml', 'xml')
    RDFJSON = FormatDef('rdfjson', 'application/rdf+json')
    TURTLE = FormatDef('turtle', 'text/turtle', 'turtle')
    NT = FormatDef('nt', 'text/rdf+n3', 'n3')


def from_mimetype(mimetype):
    """
    Returns a C{FormatDef} representing the passed mimetype

    @type mimetype: str
    @param mimetype: format mimetype
    @return: format
    """
    for name, format in Format.__dict__.items():
        if isinstance(format, FormatDef):
            if format == mimetype:
                return format

    return