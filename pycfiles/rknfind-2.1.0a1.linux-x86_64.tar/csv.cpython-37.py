# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scpketer/Dev/rknfind/.env/lib/python3.7/site-packages/rknfind/rkn/csv.py
# Compiled at: 2019-09-20 13:36:22
# Size of source mod 2**32: 5457 bytes
from os import linesep as lsep
LIST_ELEMENT_SEPARATOR = ' | '

class RknBlockEntry(object):

    def __init__(self, addr, domain, url, issuer, decree, date):
        """Initialize new RknBlockEntry with its data.

        Parameters
        ----------
        addr : str
            String of IP-addresses, separated by LIST_ELEMENT_SEPARATOR.
        domain : str
            String of domains, separated by LIST_ELEMENT_SEPARATOR.
        url : str
            String of URLs, separated by LIST_ELEMENT_SEPARATOR.
        decree:
            String of block entry decree.
        date:
            String of DD-MM-YYYY formatted block entry date.
        """
        self.addr = addr
        self.decree = decree
        self.date = date
        self.issuer = issuer
        self.domain = domain
        self.url = url
        if type(addr) is str:
            self.addr = addr.split(LIST_ELEMENT_SEPARATOR)
        else:
            if addr is None:
                self.addr = []
        if type(domain) is str:
            self.domain = domain.split(LIST_ELEMENT_SEPARATOR)
        else:
            if domain is None:
                self.domain = []
            elif type(url) is str:
                self.url = url.split(LIST_ELEMENT_SEPARATOR)
            else:
                if url is None:
                    self.url = []

    def __repr__(self):
        """Returns object representations as string.

        Returns
        ------
        str
            String representation of an object.
        """
        return 'RknBlockEntry(address={address!r}; domain={domains!r}; url={url!r}; issuer={issuer!r}; decree={decree!r}; date={date!r})'.format(address=(self.addr),
          issuer=(self.issuer),
          decree=(self.decree),
          date=(self.date),
          domains=(self.domain),
          url=(self.url))

    def __json__(self):
        """Returns object serialized in JSON.

        Returns
        ------
        str
            JSON-serialized object.
        """
        from json import dumps
        return dumps({k:v for k, v in vars(self).items() if not k.startswith('_') if not callable(v) if not callable(v)})

    def match(self, field, occurence, glob=False, regexp=False):
        """Matches entry's field against occurence.

        Parameters
        ----------
        field : str
            Field to match entry against. May be None, in this case any field
            will be used to match against.
        occurence : str
            Occurence to match in field.
        glob : bool
            Threat occurence as a glob expression if True.
            Cannot be True if regexp=True.
        regexp : bool
            Thread occurence as a regular expression if True.
            Cannot be True if glob=True.

        Returns
        -------
        bool
            True if entry is matching against occurence specified for field.
        """
        import re
        from fnmatch import fnmatch
        attrs = [attr for attr, value in vars(self).items() if not attr.startswith('_') if not callable(value)]
        if glob:
            if regexp:
                raise ValueError('glob and regexp are mutually exclusive')
        if field is not None:
            if field not in attrs:
                return False
                value = getattr(self, field)
                if not isinstance(value, list):
                    value = repr(value)
                    if glob:
                        return fnmatch(value, occurence)
                    if regexp:
                        return re.match(occurence, value)
                    return occurence in value
            else:
                for item in value:
                    item = repr(item)
                    if glob:
                        return fnmatch(item, occurence)
                    if regexp:
                        return re.match(occurence, item)
                    return occurence in item

        else:
            for attr in attrs:
                if self.match(attr, occurence, glob, regexp):
                    return True


def entries(fd, readbuf=1024):
    """Generator function to iterate over Rkn CSV dump file.

    Parameters
    ----------
    fd : TextIO
        File or file-like object to read from.
    readbuf : int
        File reading buffer.

    Yields
    ------
    RknBlockEntry
        Block entry read from Rkn dump file.
    """
    field_id = None
    in_field = False
    quoted = False
    while 1:
        buffer = fd.read(readbuf)
        if not buffer:
            return
            for ch in buffer:
                if field_id is None:
                    entry = ['' for _ in range(6)]
                    field_id = 0
                    field = str()
                if ch == '"':
                    if not field or in_field:
                        in_field = not in_field
                if ch == ';':
                    if (in_field or len(field)) > 0:
                        entry[field_id] = field
                    else:
                        entry[field_id] = None
                    field_id += 1
                    field = str()
                elif ch == '\n':
                    entry[field_id] = in_field or field
                    field_id = None
                    yield RknBlockEntry(*entry)
                else:
                    field += ch