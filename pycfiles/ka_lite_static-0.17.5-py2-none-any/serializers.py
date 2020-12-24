# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-tastypie-legacy/tastypie/serializers.py
# Compiled at: 2018-07-11 18:15:32
from __future__ import unicode_literals
import datetime, json, re
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.encoding import force_text, smart_bytes
from django.core.serializers import json as djangojson
from tastypie.bundle import Bundle
from tastypie.exceptions import BadRequest, UnsupportedFormat
from tastypie.utils import format_datetime, format_date, format_time, make_naive
try:
    import defusedxml.lxml as lxml
    from defusedxml.common import DefusedXmlException
    from defusedxml.lxml import parse as parse_xml
    from lxml.etree import Element, tostring, LxmlError
except ImportError:
    lxml = None

try:
    import yaml
except ImportError:
    yaml = None

try:
    import biplist
except ImportError:
    biplist = None

XML_ENCODING = re.compile(b'<\\?xml.*?\\?>', re.IGNORECASE)
if yaml is not None:
    from yaml.constructor import SafeConstructor
    from yaml.loader import Reader, Scanner, Parser, Composer, Resolver

    class TastypieConstructor(SafeConstructor):

        def construct_yaml_unicode_dammit(self, node):
            value = self.construct_scalar(node)
            try:
                return value.encode(b'ascii')
            except UnicodeEncodeError:
                return value


    TastypieConstructor.add_constructor(b'tag:yaml.org,2002:python/unicode', TastypieConstructor.construct_yaml_unicode_dammit)

    class TastypieLoader(Reader, Scanner, Parser, Composer, TastypieConstructor, Resolver):

        def __init__(self, stream):
            Reader.__init__(self, stream)
            Scanner.__init__(self)
            Parser.__init__(self)
            Composer.__init__(self)
            TastypieConstructor.__init__(self)
            Resolver.__init__(self)


_NUM = 0
_DICT = 1
_LIST = 2
_STR = 3
_BUNDLE = 4
_DATETIME = 5
_DATE = 6
_TIME = 7
_SIMPLETYPES = {float: _NUM, 
   bool: _NUM, 
   dict: _DICT, 
   list: _LIST, 
   tuple: _LIST, 
   Bundle: _BUNDLE, 
   datetime.datetime: _DATETIME, 
   datetime.date: _DATE, 
   datetime.time: _TIME}
for integer_type in six.integer_types:
    _SIMPLETYPES[integer_type] = _NUM

for string_type in six.string_types:
    _SIMPLETYPES[string_type] = _STR

class Serializer(object):
    """
    A swappable class for serialization.

    This handles most types of data as well as the following output formats::

        * json
        * jsonp (Disabled by default)
        * xml
        * yaml
        * plist (see http://explorapp.com/biplist/)

    It was designed to make changing behavior easy, either by overridding the
    various format methods (i.e. ``to_json``), by changing the
    ``formats/content_types`` options or by altering the other hook methods.
    """
    formats = [
     b'json', b'xml', b'yaml', b'plist']
    content_types = {b'json': b'application/json', 
       b'jsonp': b'text/javascript', 
       b'xml': b'application/xml', 
       b'yaml': b'text/yaml', 
       b'plist': b'application/x-plist'}

    def __init__(self, formats=None, content_types=None, datetime_formatting=None):
        if datetime_formatting is not None:
            self.datetime_formatting = datetime_formatting
        else:
            self.datetime_formatting = getattr(settings, b'TASTYPIE_DATETIME_FORMATTING', b'iso-8601')
        self.supported_formats = []
        if content_types is not None:
            self.content_types = content_types
        if formats is not None:
            self.formats = formats
        if self.formats is Serializer.formats and hasattr(settings, b'TASTYPIE_DEFAULT_FORMATS'):
            self.formats = settings.TASTYPIE_DEFAULT_FORMATS
        if not isinstance(self.formats, (list, tuple)):
            raise ImproperlyConfigured(b'Formats should be a list or tuple, not %r' % self.formats)
        for format in self.formats:
            try:
                self.supported_formats.append(self.content_types[format])
            except KeyError:
                raise ImproperlyConfigured(b"Content type for specified type '%s' not found. Please provide it at either the class level or via the arguments." % format)

        self.supported_formats_reversed = list(self.supported_formats)
        self.supported_formats_reversed.reverse()
        self._from_methods = {}
        self._to_methods = {}
        for short_format, long_format in self.content_types.items():
            method = getattr(self, b'from_%s' % short_format, None)
            self._from_methods[long_format] = method
            method = getattr(self, b'to_%s' % short_format, None)
            self._to_methods[long_format] = method

        return

    def get_mime_for_format(self, format):
        """
        Given a format, attempts to determine the correct MIME type.

        If not available on the current ``Serializer``, returns
        ``application/json`` by default.
        """
        try:
            return self.content_types[format]
        except KeyError:
            return b'application/json'

    def format_datetime(self, data):
        """
        A hook to control how datetimes are formatted.

        Can be overridden at the ``Serializer`` level (``datetime_formatting``)
        or globally (via ``settings.TASTYPIE_DATETIME_FORMATTING``).

        Default is ``iso-8601``, which looks like "2010-12-16T03:02:14".
        """
        data = make_naive(data)
        if self.datetime_formatting == b'rfc-2822':
            return format_datetime(data)
        if self.datetime_formatting == b'iso-8601-strict':
            data = data - datetime.timedelta(microseconds=data.microsecond)
        return data.isoformat()

    def format_date(self, data):
        """
        A hook to control how dates are formatted.

        Can be overridden at the ``Serializer`` level (``datetime_formatting``)
        or globally (via ``settings.TASTYPIE_DATETIME_FORMATTING``).

        Default is ``iso-8601``, which looks like "2010-12-16".
        """
        if self.datetime_formatting == b'rfc-2822':
            return format_date(data)
        return data.isoformat()

    def format_time(self, data):
        """
        A hook to control how times are formatted.

        Can be overridden at the ``Serializer`` level (``datetime_formatting``)
        or globally (via ``settings.TASTYPIE_DATETIME_FORMATTING``).

        Default is ``iso-8601``, which looks like "03:02:14".
        """
        if self.datetime_formatting == b'rfc-2822':
            return format_time(data)
        if self.datetime_formatting == b'iso-8601-strict':
            data = (datetime.datetime.combine(datetime.date(1, 1, 1), data) - datetime.timedelta(microseconds=data.microsecond)).time()
        return data.isoformat()

    def serialize(self, bundle, format=b'application/json', options=None):
        """
        Given some data and a format, calls the correct method to serialize
        the data and returns the result.
        """
        method = None
        if options is None:
            options = {}
        method = self._to_methods.get(format)
        if method is None:
            raise UnsupportedFormat(b"The format indicated '%s' had no available serialization method. Please check your ``formats`` and ``content_types`` on your Serializer." % format)
        return method(bundle, options)

    def deserialize(self, content, format=b'application/json'):
        """
        Given some data and a format, calls the correct method to deserialize
        the data and returns the result.
        """
        method = None
        format = format.split(b';')[0]
        method = self._from_methods.get(format)
        if method is None:
            raise UnsupportedFormat(b"The format indicated '%s' had no available deserialization method. Please check your ``formats`` and ``content_types`` on your Serializer." % format)
        if isinstance(content, six.binary_type):
            content = force_text(content)
        return method(content)

    def to_simple(self, data, options):
        """
        For a piece of data, attempts to recognize it and provide a simplified
        form of something complex.

        This brings complex Python data structures down to native types of the
        serialization format(s).
        """
        if data is None:
            return
        else:
            data_type = type(data)
            stype = _STR
            for dt in data_type.__mro__:
                try:
                    stype = _SIMPLETYPES[dt]
                    break
                except KeyError:
                    pass

            if stype == _NUM:
                return data
            if stype == _DICT:
                to_simple = self.to_simple
                return dict([ (key, to_simple(val, options)) for key, val in six.iteritems(data) ])
            if stype == _STR:
                return force_text(data)
            if stype == _LIST:
                to_simple = self.to_simple
                return [ to_simple(item, options) for item in data ]
            if stype == _BUNDLE:
                to_simple = self.to_simple
                return dict([ (key, to_simple(val, options)) for key, val in six.iteritems(data.data) ])
            if stype == _DATETIME:
                return self.format_datetime(data)
            if stype == _DATE:
                return self.format_date(data)
            if stype == _TIME:
                return self.format_time(data)
            return

    def to_etree(self, data, options=None, name=None, depth=0):
        """
        Given some data, converts that data to an ``etree.Element`` suitable
        for use in the XML output.
        """
        if isinstance(data, (list, tuple)):
            element = Element(name or b'objects')
            if name:
                element = Element(name)
                element.set(b'type', b'list')
            else:
                element = Element(b'objects')
            for item in data:
                element.append(self.to_etree(item, options, depth=depth + 1))
                element[:] = sorted(element, key=lambda x: x.tag)

        elif isinstance(data, dict):
            if depth == 0:
                element = Element(name or b'response')
            else:
                element = Element(name or b'object')
                element.set(b'type', b'hash')
            for key, value in data.items():
                element.append(self.to_etree(value, options, name=key, depth=depth + 1))
                element[:] = sorted(element, key=lambda x: x.tag)

        elif isinstance(data, Bundle):
            element = Element(name or b'object')
            for field_name, field_object in data.data.items():
                element.append(self.to_etree(field_object, options, name=field_name, depth=depth + 1))
                element[:] = sorted(element, key=lambda x: x.tag)

        else:
            element = Element(name or b'value')
            simple_data = self.to_simple(data, options)
            data_type = get_type_string(simple_data)
            if data_type != b'string':
                element.set(b'type', get_type_string(simple_data))
            if data_type != b'null':
                if isinstance(simple_data, six.text_type):
                    element.text = simple_data
                else:
                    element.text = force_text(simple_data)
        return element

    def from_etree(self, data):
        """
        Not the smartest deserializer on the planet. At the request level,
        it first tries to output the deserialized subelement called "object"
        or "objects" and falls back to deserializing based on hinted types in
        the XML element attribute "type".
        """
        if data.tag == b'request':
            elements = data.getchildren()
            for element in elements:
                if element.tag in ('object', 'objects'):
                    return self.from_etree(element)

            return dict((element.tag, self.from_etree(element)) for element in elements)
        else:
            if data.tag == b'object' or data.get(b'type') == b'hash':
                return dict((element.tag, self.from_etree(element)) for element in data.getchildren())
            if data.tag == b'objects' or data.get(b'type') == b'list':
                return [ self.from_etree(element) for element in data.getchildren() ]
            type_string = data.get(b'type')
            if type_string in ('string', None):
                return data.text
            if type_string == b'integer':
                return int(data.text)
            if type_string == b'float':
                return float(data.text)
            if type_string == b'boolean':
                if data.text == b'True':
                    return True
                else:
                    return False

            else:
                return
            return

    def to_json(self, data, options=None):
        """
        Given some Python data, produces JSON output.
        """
        options = options or {}
        data = self.to_simple(data, options)
        return djangojson.json.dumps(data, cls=djangojson.DjangoJSONEncoder, sort_keys=True, ensure_ascii=False)

    def from_json(self, content):
        """
        Given some JSON data, returns a Python dictionary of the decoded data.
        """
        try:
            return json.loads(content)
        except ValueError:
            raise BadRequest

    def to_jsonp(self, data, options=None):
        """
        Given some Python data, produces JSON output wrapped in the provided
        callback.

        Due to a difference between JSON and Javascript, two
        newline characters, \u2028 and \u2029, need to be escaped.
        See http://timelessrepo.com/json-isnt-a-javascript-subset for
        details.
        """
        options = options or {}
        jsonstr = self.to_json(data, options).replace(b'\u2028', b'\\u2028').replace(b'\u2029', b'\\u2029')
        return b'%s(%s)' % (options[b'callback'], jsonstr)

    def to_xml(self, data, options=None):
        """
        Given some Python data, produces XML output.
        """
        options = options or {}
        if lxml is None:
            raise ImproperlyConfigured(b'Usage of the XML aspects requires lxml and defusedxml.')
        return tostring(self.to_etree(data, options), xml_declaration=True, encoding=b'utf-8')

    def from_xml(self, content, forbid_dtd=True, forbid_entities=True):
        """
        Given some XML data, returns a Python dictionary of the decoded data.

        By default XML entity declarations and DTDs will raise a BadRequest
        exception content but subclasses may choose to override this if
        necessary.
        """
        if lxml is None:
            raise ImproperlyConfigured(b'Usage of the XML aspects requires lxml and defusedxml.')
        try:
            content = XML_ENCODING.sub(b'', content)
            parsed = parse_xml(six.StringIO(content), forbid_dtd=forbid_dtd, forbid_entities=forbid_entities)
        except (LxmlError, DefusedXmlException):
            raise BadRequest()

        return self.from_etree(parsed.getroot())

    def to_yaml(self, data, options=None):
        """
        Given some Python data, produces YAML output.
        """
        options = options or {}
        if yaml is None:
            raise ImproperlyConfigured(b'Usage of the YAML aspects requires yaml.')
        return yaml.dump(self.to_simple(data, options))

    def from_yaml(self, content):
        """
        Given some YAML data, returns a Python dictionary of the decoded data.
        """
        if yaml is None:
            raise ImproperlyConfigured(b'Usage of the YAML aspects requires yaml.')
        return yaml.load(content, Loader=TastypieLoader)

    def to_plist(self, data, options=None):
        """
        Given some Python data, produces binary plist output.
        """
        options = options or {}
        if biplist is None:
            raise ImproperlyConfigured(b'Usage of the plist aspects requires biplist.')
        return biplist.writePlistToString(self.to_simple(data, options))

    def from_plist(self, content):
        """
        Given some binary plist data, returns a Python dictionary of the
        decoded data.
        """
        if biplist is None:
            raise ImproperlyConfigured(b'Usage of the plist aspects requires biplist.')
        if isinstance(content, six.text_type):
            content = smart_bytes(content)
        return biplist.readPlistFromString(content)


def get_type_string(data):
    """
    Translates a Python data type into a string format.
    """
    data_type = type(data)
    if data_type in six.integer_types:
        return b'integer'
    else:
        if data_type == float:
            return b'float'
        if data_type == bool:
            return b'boolean'
        if data_type in (list, tuple):
            return b'list'
        if data_type == dict:
            return b'hash'
        if data is None:
            return b'null'
        if isinstance(data, six.string_types):
            return b'string'
        return