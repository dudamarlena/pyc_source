# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/glopes/Projects/RoboticsLanguage/RoboticsLanguage/Tools/DictionaryToXML.py
# Compiled at: 2019-09-27 03:30:17
"""
Converts a Python dictionary or other native data type into a valid XML string.

Supports item (`int`, `float`, `long`, `decimal.Decimal`, `bool`, `str`, `unicode`, `datetime`, `none` and other number-like objects) and collection (`list`, `set`, `tuple` and `dict`, as well as iterable and dict-like objects) data types, with arbitrary nesting for the collections. Items with a `datetime` type are converted to ISO format strings. Items with a `None` type become empty XML elements.

This module works with both Python 2 and 3.
"""
from __future__ import unicode_literals
__version__ = b'1.7.4'
version = __version__
from random import randint
import collections, numbers, logging
from xml.dom.minidom import parseString
LOG = logging.getLogger(b'dicttoxml')
try:
    unicode
except:
    unicode = str

try:
    long
except:
    long = int

def set_debug(debug=True, filename=b'dicttoxml.log'):
    if debug:
        import datetime
        print b'Debug mode is on. Events are logged at: %s' % filename
        logging.basicConfig(filename=filename, level=logging.INFO)
        LOG.info(b'\nLogging session starts: %s' % str(datetime.datetime.today()))
    else:
        logging.basicConfig(level=logging.WARNING)
        print b'Debug mode is off.'


def unicode_me(something):
    """Converts strings with non-ASCII characters to unicode for LOG.
    Python 3 doesn't have a `unicode()` function, so `unicode()` is an alias
    for `str()`, but `str()` doesn't take a second argument, hence this kludge.
    """
    try:
        return unicode(something, b'utf-8')
    except:
        return unicode(something)


ids = []

def make_id(element, start=100000, end=999999):
    """Returns a random integer"""
    return b'%s_%s' % (element, randint(start, end))


def get_unique_id(element):
    """Returns a unique id for a given element"""
    this_id = make_id(element)
    dup = True
    while dup:
        if this_id not in ids:
            dup = False
            ids.append(this_id)
        else:
            this_id = make_id(element)

    return ids[(-1)]


def get_xml_type(val):
    """Returns the data type for the xml type attribute"""
    if type(val).__name__ in ('str', 'unicode'):
        return b'str'
    if type(val).__name__ in ('int', 'long'):
        return b'int'
    if type(val).__name__ == b'float':
        return b'float'
    if type(val).__name__ == b'bool':
        return b'bool'
    if isinstance(val, numbers.Number):
        return b'number'
    if type(val).__name__ == b'NoneType':
        return b'null'
    if isinstance(val, dict):
        return b'dict'
    if isinstance(val, collections.Iterable):
        return b'list'
    return type(val).__name__


def escape_xml(s):
    if type(s) in (str, unicode):
        s = unicode_me(s)
        s = s.replace(b'&', b'&amp;')
        s = s.replace(b'"', b'&quot;')
        s = s.replace(b"'", b'&apos;')
        s = s.replace(b'<', b'&lt;')
        s = s.replace(b'>', b'&gt;')
    return s


def make_attrstring(attr):
    """Returns an attribute string in the form key="val" """
    attrstring = (b' ').join([ b'%s="%s"' % (k, v) for k, v in attr.items() ])
    return b'%s%s' % (b' ' if attrstring != b'' else b'', attrstring)


def key_is_valid_xml(key):
    """Checks that a key is a valid XML name"""
    LOG.info(b'Inside key_is_valid_xml(). Testing "%s"' % unicode_me(key))
    test_xml = b'<?xml version="1.0" encoding="UTF-8" ?><%s>foo</%s>' % (key, key)
    try:
        parseString(test_xml)
        return True
    except Exception:
        return False


def make_valid_xml_name(key, attr):
    """Tests an XML name and fixes it if invalid"""
    LOG.info(b'Inside make_valid_xml_name(). Testing key "%s" with attr "%s"' % (
     unicode_me(key), unicode_me(attr)))
    key = escape_xml(key)
    attr = escape_xml(attr)
    if key_is_valid_xml(key):
        return (key, attr)
    if key.isdigit():
        return (b'n%s' % key, attr)
    if key_is_valid_xml(key.replace(b' ', b'_')):
        return (key.replace(b' ', b'_'), attr)
    attr[b'name'] = key
    key = b'key'
    return (key, attr)


def wrap_cdata(s):
    """Wraps a string into CDATA sections"""
    s = unicode_me(s).replace(b']]>', b']]]]><![CDATA[>')
    return b'<![CDATA[' + s + b']]>'


def default_item_func(parent):
    return b'item'


def convert(obj, ids, attr_type, item_func, cdata, parent=b'root', namespace=b''):
    """Routes the elements of an object to the right function to convert them
    based on their data type"""
    LOG.info(b'Inside convert(). obj type is: "%s", obj="%s"' % (type(obj).__name__, unicode_me(obj)))
    item_name = item_func(parent)
    if isinstance(obj, numbers.Number) or type(obj) in (str, unicode):
        return convert_kv(item_name, obj, attr_type, cdata, namespace=namespace)
    else:
        if hasattr(obj, b'isoformat'):
            return convert_kv(item_name, obj.isoformat(), attr_type, cdata, namespace=namespace)
        if type(obj) == bool:
            return convert_bool(item_name, obj, attr_type, cdata, namespace=namespace)
        if obj is None:
            return convert_none(item_name, b'', attr_type, cdata, namespace=namespace)
        if isinstance(obj, dict):
            return convert_dict(obj, ids, parent, attr_type, item_func, cdata, namespace=namespace)
        if isinstance(obj, collections.Iterable):
            return convert_list(obj, ids, parent, attr_type, item_func, cdata, namespace=namespace)
        raise TypeError(b'Unsupported data type: %s (%s)' % (obj, type(obj).__name__))
        return


def convert_dict(obj, ids, parent, attr_type, item_func, cdata, namespace=b''):
    """Converts a dict into an XML string."""
    LOG.info(b'Inside convert_dict(): obj type is: "%s", obj="%s"' % (
     type(obj).__name__, unicode_me(obj)))
    output = []
    addline = output.append
    item_name = item_func(parent)
    for key, val in obj.items():
        LOG.info(b'Looping inside convert_dict(): key="%s%s", val="%s", type(val)="%s"' % (
         unicode_me(namespace), unicode_me(key), unicode_me(val), type(val).__name__))
        attr = {} if not ids else {b'id': b'%s' % get_unique_id(parent)}
        key, attr = make_valid_xml_name(key, attr)
        if isinstance(val, numbers.Number) or type(val) in (str, unicode):
            addline(convert_kv(key, val, attr_type, attr, cdata, namespace=namespace))
        elif hasattr(val, b'isoformat'):
            addline(convert_kv(key, val.isoformat(), attr_type, attr, cdata, namespace=namespace))
        elif type(val) == bool:
            addline(convert_bool(key, val, attr_type, attr, cdata, namespace=namespace))
        elif isinstance(val, dict):
            if attr_type:
                attr[b'type'] = get_xml_type(val)
            addline(b'<%s%s%s>%s</%s%s>' % (
             namespace, key, make_attrstring(attr),
             convert_dict(val, ids, key, attr_type, item_func, cdata, namespace=namespace),
             namespace, key))
        elif isinstance(val, collections.Iterable):
            if attr_type:
                attr[b'type'] = get_xml_type(val)
            addline(b'<%s%s%s>%s</%s%s>' % (
             namespace, key,
             make_attrstring(attr),
             convert_list(val, ids, key, attr_type, item_func, cdata, namespace=namespace),
             namespace, key))
        elif val is None:
            addline(convert_none(key, val, attr_type, attr, cdata, namespace=namespace))
        else:
            raise TypeError(b'Unsupported data type: %s (%s)' % (
             val, type(val).__name__))

    return (b'').join(output)


def convert_list(items, ids, parent, attr_type, item_func, cdata, namespace=b''):
    """Converts a list into an XML string."""
    LOG.info(b'Inside convert_list()')
    output = []
    addline = output.append
    item_name = item_func(parent)
    if ids:
        this_id = get_unique_id(parent)
    for i, item in enumerate(items):
        LOG.info(b'Looping inside convert_list(): item="%s", item_name="%s", type="%s"' % (
         unicode_me(item), item_name, type(item).__name__))
        attr = {} if not ids else {b'id': b'%s_%s' % (this_id, i + 1)}
        if isinstance(item, numbers.Number) or type(item) in (str, unicode):
            addline(convert_kv(item_name, item, attr_type, attr, cdata, namespace=namespace))
        elif hasattr(item, b'isoformat'):
            addline(convert_kv(item_name, item.isoformat(), attr_type, attr, cdata, namespace=namespace))
        elif type(item) == bool:
            addline(convert_bool(item_name, item, attr_type, attr, cdata, namespace=namespace))
        elif isinstance(item, dict):
            if not attr_type:
                addline(b'<%s%s>%s</%s%s>' % (
                 namespace, item_name,
                 convert_dict(item, ids, parent, attr_type, item_func, cdata, namespace=namespace),
                 namespace, item_name))
            else:
                addline(b'<%s%s type="dict">%s</%s%s>' % (
                 namespace, item_name,
                 convert_dict(item, ids, parent, attr_type, item_func, cdata, namespace=namespace),
                 namespace, item_name))
        elif isinstance(item, collections.Iterable):
            if not attr_type:
                addline(b'<%s%s %s>%s</%s%s>' % (
                 namespace, item_name, make_attrstring(attr),
                 convert_list(item, ids, item_name, attr_type, item_func, cdata, namespace=namespace),
                 namespace, item_name))
            else:
                addline(b'<%s%s type="list"%s>%s</%s%s>' % (
                 namespace, item_name, make_attrstring(attr),
                 convert_list(item, ids, item_name, attr_type, item_func, cdata, namespace=namespace),
                 namespace, item_name))
        elif item is None:
            addline(convert_none(item_name, None, attr_type, attr, cdata, namespace=namespace))
        else:
            raise TypeError(b'Unsupported data type: %s (%s)' % (
             item, type(item).__name__))

    return (b'').join(output)


def convert_kv(key, val, attr_type, attr={}, cdata=False, namespace=b''):
    """Converts a number or string into an XML element"""
    LOG.info(b'Inside convert_kv(): key="%s", val="%s", type(val) is: "%s"' % (
     unicode_me(key), unicode_me(val), type(val).__name__))
    key, attr = make_valid_xml_name(key, attr)
    if attr_type:
        attr[b'type'] = get_xml_type(val)
    attrstring = make_attrstring(attr)
    return b'<%s%s%s>%s</%s%s>' % (
     namespace, key, attrstring,
     wrap_cdata(val) if cdata == True else escape_xml(val),
     namespace, key)


def convert_bool(key, val, attr_type, attr={}, cdata=False, namespace=b''):
    """Converts a boolean into an XML element"""
    LOG.info(b'Inside convert_bool(): key="%s", val="%s", type(val) is: "%s"' % (
     unicode_me(key), unicode_me(val), type(val).__name__))
    key, attr = make_valid_xml_name(key, attr)
    if attr_type:
        attr[b'type'] = get_xml_type(val)
    attrstring = make_attrstring(attr)
    return b'<%s%s%s>%s</%s%s>' % (namespace, key, attrstring, unicode(val).lower(), namespace, key)


def convert_none(key, val, attr_type, attr={}, cdata=False, namespace=b''):
    """Converts a null value into an XML element"""
    LOG.info(b'Inside convert_none(): key="%s"' % unicode_me(key))
    key, attr = make_valid_xml_name(key, attr)
    if attr_type:
        attr[b'type'] = get_xml_type(val)
    attrstring = make_attrstring(attr)
    return b'<%s%s%s></%s%s>' % (namespace, key, attrstring, namespace, key)


def dicttoxml(obj, root=True, custom_root=b'root', ids=False, attr_type=False, item_func=default_item_func, cdata=False, namespace=b''):
    """Converts a python object into XML.
    Arguments:
    - root specifies whether the output is wrapped in an XML root element
      Default is True
    - custom_root allows you to specify a custom root element.
      Default is 'root'
    - ids specifies whether elements get unique ids.
      Default is False
    - attr_type specifies whether elements get a data type attribute.
      Default is True
    - item_func specifies what function should generate the element name for
      items in a list.
      Default is 'item'
    - cdata specifies whether string values should be wrapped in CDATA sections.
      Default is False
    """
    if namespace != b'':
        namespace_attribute = (b' xmlns:{}="{}"').format(namespace, namespace)
        namespace += b':'
        root = True
    else:
        namespace_attribute = b''
    LOG.info(b'Inside dicttoxml(): type(obj) is: "%s", obj="%s"' % (type(obj).__name__, unicode_me(obj)))
    output = []
    addline = output.append
    if root:
        addline(b'<?xml version="1.0" encoding="UTF-8" ?>')
        addline(b'<%s%s%s>%s</%s%s>' % (namespace, custom_root, namespace_attribute,
         convert(obj, ids, attr_type, item_func, cdata, parent=custom_root, namespace=namespace),
         namespace, custom_root))
    else:
        addline(convert(obj, ids, attr_type, item_func, cdata, parent=b'', namespace=namespace))
    return (b'').join(output).encode(b'utf-8')