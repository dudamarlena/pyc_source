# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sdmpy/mime.py
# Compiled at: 2018-04-11 18:01:28
from __future__ import print_function, division, absolute_import, unicode_literals
from builtins import bytes, chr, dict, object, range, map, input, str
from future.utils import itervalues, viewitems, iteritems, listvalues, listitems
from io import open
import os.path
from collections import OrderedDict

class MIMEHeader(OrderedDict):

    @property
    def boundary(self):
        if self[b'Content-Type'][0].startswith(b'multipart/'):
            for v in self[b'Content-Type']:
                if v.startswith(b'boundary='):
                    return v[v.index(b'=') + 1:]

        return

    def addline(self, line):
        """
        Given a single line from a mime header, split it into key/val and
        add it to the dict.
        """
        if line.startswith(b'\t'):
            key = list(self.keys())[(-1)]
            vals = [ ll.strip() for ll in line[1].split(b';') ]
            self[key].extend(vals)
        else:
            idx = line.index(b':')
            key = line[:idx]
            vals = [ ll.strip() for ll in line[idx + 1:].split(b';') ]
            self[key] = vals

    @staticmethod
    def _asline(key, val):
        """Convert given key and value list to MIME header line."""
        return key + b': ' + (b'; ').join(val) + b'\n'

    def tostring(self, key=None):
        """
        Return contents as in MIME-header format.  If key is given, only
        the line corresponding to the requested key will be returned,
        otherwise the full header will be returned.
        """
        if key is not None:
            return self._asline(key, self[key])
        else:
            out = b''
            for k in list(self.keys()):
                out += self._asline(k, self[k])

            return out
            return

    def __str__(self):
        return self.tostring()


def basename_noext(path):
    return os.path.basename(os.path.splitext(path)[0])


class MIMEPart(object):
    """
    Class for representing one part of a MIME message.
    Has two member variable:

      hdr  = Dict of MIME header key/value pairs
      body = Body of message.  In our usage, can be a file offset in bytes
             (for binary parts), a string (for text) or a list of MIMEPart
             objects (for multipart).

    The loc property is a shortcut for the Content-Location header
    parameter.

    The type property is a shortcut for Content-Type
    """

    def __init__(self, fp, boundary=None, recurse=False, binary_size=None):
        """
        Read a MIME content part starting at the current file location.
        Return value is a MIMEPart object, which has elements:

            hdr    dict of MIME header key / value pairs

            body   string if Content-Type was 'text/xml', offset into
                   the file if 'application/octet-stream', or list of
                   other MIMEParts for a 'multipart/*'.

        If recurse is True, will read/return the contents of a multipart
        (and any multiparts found at lower levels).  Otherwise will read
        one header/body unit and pointer will be left at the start of
        the next one (or first sub-part for multiparts).

        binary_size is a dict of sizes of binary components by type.
        For each binary part found, if Content-Location agrees with type,
        the binary data will be skipped over rather than read (this is
        for reading BDF files).  If binary_size is not given, or if an
        unknown type is found, the data must be read to determine its
        size, however this last part is not implemented yet.
        """
        self.hdr = MIMEHeader({})
        self.body = None
        in_hdr = True
        binary_type = False
        multipart_type = False
        while True:
            line = fp.readline().decode(b'utf-8').replace(b'\r', b'')
            if line == b'':
                return
            if boundary is not None:
                if in_hdr:
                    if line == b'--' + boundary + b'\n':
                        continue
                    elif line == b'--' + boundary + b'--\n':
                        self.hdr = MIMEHeader({})
                        self.body = None
                        return
                elif line.startswith(b'--' + boundary):
                    fp.seek(-len(line), 1)
                    return
            if line == b'\n':
                in_hdr = False
                if binary_type:
                    try:
                        bin_name = basename_noext(self.hdr[b'Content-Location'][0])
                    except KeyError:
                        bin_name = None

                    self.body = fp.tell()
                    if binary_size is None or bin_name not in list(binary_size.keys()):
                        bl = len(boundary) + 2
                        bs = 1048576
                        gotit = False
                        while not gotit:
                            junk = fp.read(bs)
                            bloc = junk.find(bytes(b'--' + boundary, b'utf-8'))
                            br = len(junk)
                            eof = br < bs
                            if bloc < 0:
                                if eof:
                                    raise RuntimeError(b"Missing boundary string '%s'" % boundary)
                                else:
                                    fp.seek(-bl, 1)
                            else:
                                gotit = True
                                fp.seek(-br + bloc, 1)

                    else:
                        fp.seek(binary_size[bin_name] + 1, 1)
                    self.size = fp.tell() - self.body
                elif multipart_type:
                    if recurse:
                        while True:
                            pmime = MIMEPart(fp, boundary=boundary, recurse=True, binary_size=binary_size)
                            if pmime.hdr == {}:
                                return
                            self.body.append(pmime)

                continue
            if in_hdr:
                self.hdr.addline(line)
                if b'Content-Type' in line:
                    vals = self.hdr[b'Content-Type']
                    if vals[0].startswith(b'multipart/'):
                        multipart_type = True
                        boundary = self.hdr.boundary
                        self.body = []
                    elif vals[0] == b'application/octet-stream' or vals[0] == b'binary/octet-stream':
                        binary_type = True
            elif not binary_type:
                if self.body is None:
                    self.body = line
                else:
                    self.body += line
            else:
                raise RuntimeError(b'MIME parsing failure')

        return

    @property
    def loc(self):
        try:
            return self.hdr[b'Content-Location'][0]
        except KeyError:
            return

        return

    @property
    def type(self):
        try:
            return self.hdr[b'Content-Type'][0]
        except KeyError:
            return

        return