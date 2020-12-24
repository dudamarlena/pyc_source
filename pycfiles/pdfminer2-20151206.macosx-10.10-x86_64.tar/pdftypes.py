# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chris/Projects/chris/various/pdfminer/venv/lib/python2.7/site-packages/pdfminer/pdftypes.py
# Compiled at: 2015-11-01 16:27:53
import zlib
from .lzw import lzwdecode
from .ascii85 import ascii85decode
from .ascii85 import asciihexdecode
from .runlength import rldecode
from .ccitt import ccittfaxdecode
from .psparser import PSException
from .psparser import PSObject
from .psparser import LIT
from .settings import STRICT
from .utils import apply_png_predictor
from .utils import isnumber
import six
LITERAL_CRYPT = LIT('Crypt')
LITERALS_FLATE_DECODE = (
 LIT('FlateDecode'), LIT('Fl'))
LITERALS_LZW_DECODE = (LIT('LZWDecode'), LIT('LZW'))
LITERALS_ASCII85_DECODE = (LIT('ASCII85Decode'), LIT('A85'))
LITERALS_ASCIIHEX_DECODE = (LIT('ASCIIHexDecode'), LIT('AHx'))
LITERALS_RUNLENGTH_DECODE = (LIT('RunLengthDecode'), LIT('RL'))
LITERALS_CCITTFAX_DECODE = (LIT('CCITTFaxDecode'), LIT('CCF'))
LITERALS_DCT_DECODE = (LIT('DCTDecode'), LIT('DCT'))

class PDFObject(PSObject):
    pass


class PDFException(PSException):
    pass


class PDFTypeError(PDFException):
    pass


class PDFValueError(PDFException):
    pass


class PDFObjectNotFound(PDFException):
    pass


class PDFNotImplementedError(PDFException):
    pass


class PDFObjRef(PDFObject):

    def __init__(self, doc, objid, _):
        if objid == 0:
            if STRICT:
                raise PDFValueError('PDF object id cannot be 0.')
        self.doc = doc
        self.objid = objid

    def __repr__(self):
        return '<PDFObjRef:%d>' % self.objid

    def resolve(self, default=None):
        try:
            return self.doc.getobj(self.objid)
        except PDFObjectNotFound:
            return default


def resolve1(x, default=None):
    """Resolves an object.

    If this is an array or dictionary, it may still contains
    some indirect objects inside.
    """
    while isinstance(x, PDFObjRef):
        x = x.resolve(default=default)

    return x


def resolve_all(x, default=None):
    """Recursively resolves the given object and all the internals.

    Make sure there is no indirect reference within the nested object.
    This procedure might be slow.
    """
    while isinstance(x, PDFObjRef):
        x = x.resolve(default=default)

    if isinstance(x, list):
        x = [ resolve_all(v, default=default) for v in x ]
    elif isinstance(x, dict):
        for k, v in x.iteritems():
            x[k] = resolve_all(v, default=default)

    return x


def decipher_all(decipher, objid, genno, x):
    """Recursively deciphers the given object.
    """
    if isinstance(x, bytes):
        return decipher(objid, genno, x)
    if isinstance(x, list):
        x = [ decipher_all(decipher, objid, genno, v) for v in x ]
    elif isinstance(x, dict):
        for k, v in six.iteritems(x):
            x[k] = decipher_all(decipher, objid, genno, v)

    return x


def int_value(x):
    x = resolve1(x)
    if not isinstance(x, int):
        if STRICT:
            raise PDFTypeError('Integer required: %r' % x)
        return 0
    return x


def float_value(x):
    x = resolve1(x)
    if not isinstance(x, float):
        if STRICT:
            raise PDFTypeError('Float required: %r' % x)
        return 0.0
    return x


def num_value(x):
    x = resolve1(x)
    if not isnumber(x):
        if STRICT:
            raise PDFTypeError('Int or Float required: %r' % x)
        return 0
    return x


def str_value(x):
    x = resolve1(x)
    if not isinstance(x, six.binary_type):
        if STRICT:
            raise PDFTypeError('String required: %r' % x)
        return ''
    return x


def list_value(x):
    x = resolve1(x)
    if not isinstance(x, (list, tuple)):
        if STRICT:
            raise PDFTypeError('List required: %r' % x)
        return []
    return x


def dict_value(x):
    x = resolve1(x)
    if not isinstance(x, dict):
        if STRICT:
            import logging
            logging.error('PDFTypeError : Dict required: %r', x)
            raise PDFTypeError('Dict required: %r' % x)
        return {}
    return x


def stream_value(x):
    x = resolve1(x)
    if not isinstance(x, PDFStream):
        if STRICT:
            raise PDFTypeError('PDFStream required: %r' % x)
        return PDFStream({}, '')
    return x


class PDFStream(PDFObject):

    def __init__(self, attrs, rawdata, decipher=None):
        assert isinstance(attrs, dict)
        self.attrs = attrs
        self.rawdata = rawdata
        self.decipher = decipher
        self.data = None
        self.objid = None
        self.genno = None
        return

    def set_objid(self, objid, genno):
        self.objid = objid
        self.genno = genno

    def __repr__(self):
        if self.data is None:
            assert self.rawdata is not None
            return '<PDFStream(%r): raw=%d, %r>' % (self.objid, len(self.rawdata), self.attrs)
        else:
            assert self.data is not None
            return '<PDFStream(%r): len=%d, %r>' % (self.objid, len(self.data), self.attrs)
            return

    def __contains__(self, name):
        return name in self.attrs

    def __getitem__(self, name):
        return self.attrs[name]

    def get(self, name, default=None):
        return self.attrs.get(name, default)

    def get_any(self, names, default=None):
        for name in names:
            if name in self.attrs:
                return self.attrs[name]

        return default

    def get_filters(self):
        filters = self.get_any(('F', 'Filter'))
        params = self.get_any(('DP', 'DecodeParms', 'FDecodeParms'), {})
        if not filters:
            return []
        if not isinstance(filters, list):
            filters = [
             filters]
        if not isinstance(params, list):
            params = [
             params]
        return zip(filters, params)

    def decode(self):
        if not (self.data is None and self.rawdata is not None):
            raise AssertionError
            data = self.rawdata
            if self.decipher:
                data = self.decipher(self.objid, self.genno, data, self.attrs)
            filters = self.get_filters()
            self.data = filters or data
            self.rawdata = None
            return
        else:
            for f, params in filters:
                if f in LITERALS_FLATE_DECODE:
                    try:
                        data = zlib.decompress(data)
                    except zlib.error as e:
                        if STRICT:
                            raise PDFException('Invalid zlib bytes: %r, %r' % (e, data))
                        data = ''

                elif f in LITERALS_LZW_DECODE:
                    data = lzwdecode(data)
                elif f in LITERALS_ASCII85_DECODE:
                    data = ascii85decode(data)
                elif f in LITERALS_ASCIIHEX_DECODE:
                    data = asciihexdecode(data)
                elif f in LITERALS_RUNLENGTH_DECODE:
                    data = rldecode(data)
                elif f in LITERALS_CCITTFAX_DECODE:
                    data = ccittfaxdecode(data, params)
                elif f in LITERALS_DCT_DECODE:
                    pass
                elif f == LITERAL_CRYPT:
                    raise PDFNotImplementedError('/Crypt filter is unsupported')
                else:
                    raise PDFNotImplementedError('Unsupported filter: %r' % f)
                if 'Predictor' in params:
                    pred = int_value(params['Predictor'])
                    if pred == 1:
                        pass
                    elif 10 <= pred:
                        colors = int_value(params.get('Colors', 1))
                        columns = int_value(params.get('Columns', 1))
                        bitspercomponent = int_value(params.get('BitsPerComponent', 8))
                        data = apply_png_predictor(pred, colors, columns, bitspercomponent, data)
                    else:
                        raise PDFNotImplementedError('Unsupported predictor: %r' % pred)

            self.data = data
            self.rawdata = None
            return

    def get_data(self):
        if self.data is None:
            self.decode()
        return self.data

    def get_rawdata(self):
        return self.rawdata