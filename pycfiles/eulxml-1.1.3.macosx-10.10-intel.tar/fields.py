# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rsutton/workarea/env/eulxml/lib/python2.7/site-packages/eulxml/xmlmap/fields.py
# Compiled at: 2016-02-19 17:15:24
from __future__ import unicode_literals
from copy import deepcopy
from datetime import datetime, date
import logging
from lxml import etree
from lxml.builder import ElementMaker
import six
from eulxml.utils.compat import u
from eulxml.xpath import ast, parse, serialize
__all__ = [
 b'StringField', b'StringListField',
 b'IntegerField', b'IntegerListField',
 b'NodeField', b'NodeListField',
 b'ItemField', b'SimpleBooleanField',
 b'DateTimeField', b'DateTimeListField',
 b'DateField', b'DateListField',
 b'SchemaField', b'FloatField', b'FloatListField']
logger = logging.getLogger(__name__)

class Field(object):
    """Base class for all xmlmap fields.

    Takes an optional ``required`` value to indicate that the field is required
    or not required in the XML.  By default, required is ``None``, which indicates
    that it is unknown whether the field is required or not.  The required value
    for an xmlmap field should not conflict with the schema or DTD for that xml,
    if there is one.
    """
    creation_counter = 0

    def __init__(self, xpath, manager, mapper, required=None, verbose_name=None, help_text=None):
        etree.XPath(xpath)
        self.xpath = xpath
        self.manager = manager
        self.mapper = mapper
        self.required = required
        self.verbose_name = verbose_name
        self.help_text = help_text
        self.parsed_xpath = parse(xpath)
        self.creation_counter = Field.creation_counter
        Field.creation_counter += 1

    def get_for_node(self, node, context):
        return self.manager.get(self.xpath, node, context, self.mapper, self.parsed_xpath)

    def set_for_node(self, node, context, value):
        return self.manager.set(self.xpath, self.parsed_xpath, node, context, self.mapper, value)

    def delete_for_node(self, node, context):
        return self.manager.delete(self.xpath, self.parsed_xpath, node, context, self.mapper)

    def __repr__(self):
        """
        Displays the module, class and name of the field.
        """
        return b'<%s.%s>' % (self.__class__.__module__, self.__class__.__name__)


class Mapper(object):

    def to_xml(self, value):
        if value is None:
            return value
        else:
            return u(value)
            return


class StringMapper(Mapper):
    XPATH = etree.XPath(b'string()')

    def __init__(self, normalize=False):
        if normalize:
            self.XPATH = etree.XPath(b'normalize-space(string())')

    def to_python(self, node):
        if node is None:
            return
        else:
            if isinstance(node, six.string_types):
                return node
            return self.XPATH(node)


class IntegerMapper(Mapper):
    XPATH = etree.XPath(b'number()')

    def to_python(self, node):
        if node is None:
            return
        else:
            try:
                if isinstance(node, six.string_types) or isinstance(node, float):
                    return int(node)
                else:
                    return int(self.XPATH(node))

            except ValueError:
                return

            return


class FloatMapper(Mapper):
    XPATH = etree.XPath(b'number()')

    def to_python(self, node):
        if node is None:
            return
        else:
            try:
                if isinstance(node, six.string_types):
                    return float(node)
                else:
                    return float(self.XPATH(node))

            except ValueError:
                return

            return


class SimpleBooleanMapper(Mapper):
    XPATH = etree.XPath(b'string()')

    def __init__(self, true, false):
        self.true = true
        self.false = false

    def to_python(self, node):
        if node is None:
            if self.false is None:
                return False
            else:
                return

        if isinstance(node, six.string_types):
            value = node
        else:
            value = self.XPATH(node)
        if value == str(self.true):
            return True
        else:
            if self.false is not None and value == str(self.false):
                return False
            raise Exception(b"Boolean field value '%s' is neither '%s' nor '%s'" % (value, self.true, self.false))
            return

    def to_xml(self, value):
        if value:
            return str(self.true)
        else:
            if self.false is not None:
                return str(self.false)
            else:
                return

            return


class DateTimeMapper(object):
    XPATH = etree.XPath(b'string()')

    def __init__(self, format=None, normalize=False):
        self.format = format
        if normalize:
            self.XPATH = etree.XPath(b'normalize-space(string())')

    def to_python(self, node):
        if node is None:
            return
        else:
            if isinstance(node, six.string_types):
                rep = node
            else:
                rep = self.XPATH(node)
            if rep.endswith(b'Z'):
                rep = rep[:-1]
            if rep[(-6)] in b'+-':
                rep = rep[:-6]
            if self.format is not None:
                dt = datetime.strptime(rep, self.format)
            else:
                try:
                    dt = datetime.strptime(rep, b'%Y-%m-%dT%H:%M:%S')
                except ValueError:
                    dt = datetime.strptime(rep, b'%Y-%m-%dT%H:%M:%S.%f')

            return dt

    def to_xml(self, dt):
        val = None
        if self.format is not None:
            val = u(dt.strftime(self.format))
        else:
            val = u(dt.isoformat())
        return val


class DateMapper(DateTimeMapper):

    def __init__(self, format=None, normalize=False):
        if format is None:
            format = b'%Y-%m-%d'
        super(DateMapper, self).__init__(format=format, normalize=normalize)
        return

    def to_python(self, node):
        if node is None:
            return
        else:
            if isinstance(node, six.string_types):
                rep = node
            elif hasattr(node, b'text'):
                rep = node.text
            dt = datetime.strptime(rep, self.format)
            return date(dt.year, dt.month, dt.day)


class NullMapper(object):

    def to_python(self, node):
        return node


class NodeMapper(object):

    def __init__(self, node_class):
        self.node_class = node_class

    def to_python(self, node):
        if node is None:
            return
        else:
            return self.node_class(node)

    def to_xml(self, xmlobject):
        if xmlobject:
            return xmlobject.node


def _find_terminal_step(xast):
    if isinstance(xast, ast.Step):
        return xast
    else:
        if isinstance(xast, ast.BinaryExpression):
            if xast.op in ('/', '//'):
                return _find_terminal_step(xast.right)
        return


def _find_xml_node(xpath, node, context):
    matches = node.xpath(xpath, **context)
    if matches and isinstance(matches, list):
        return matches[0]
    if matches:
        return matches


def _create_xml_node(xast, node, context, insert_index=None):
    if isinstance(xast, ast.Step):
        if isinstance(xast.node_test, ast.NameTest):
            for pred in xast.predicates:
                if not _predicate_is_constructible(pred):
                    msg = (b"Missing element for '%s', and node creation is " + b'supported only for simple child and attribute ' + b'nodes with simple predicates.') % (serialize(xast),)
                    raise Exception(msg)

            if xast.axis in (None, 'child'):
                new_node = _create_child_node(node, context, xast, insert_index)
            else:
                if xast.axis in ('@', 'attribute'):
                    new_node = _create_attribute_node(node, context, xast)
                for pred in xast.predicates:
                    _construct_predicate(pred, new_node, context)

                return new_node
            if _is_text_nodetest(xast):
                return node
        elif isinstance(xast, ast.BinaryExpression) and xast.op == b'/':
            left_xpath = serialize(xast.left)
            left_node = _find_xml_node(left_xpath, node, context)
            if left_node is None:
                left_node = _create_xml_node(xast.left, node, context)
            return _create_xml_node(xast.right, left_node, context)
    msg = (b"Missing element for '%s', and node creation is supported " + b'only for simple child and attribute nodes.') % (serialize(xast),)
    raise Exception(msg)
    return


def _create_child_node(node, context, step, insert_index=None):
    opts = {}
    ns_uri = None
    if b'namespaces' in context:
        opts[b'nsmap'] = context[b'namespaces']
        if step.node_test.prefix:
            ns_uri = context[b'namespaces'][step.node_test.prefix]
    E = ElementMaker(namespace=ns_uri, **opts)
    new_node = E(step.node_test.name)
    if insert_index is not None:
        node.insert(insert_index, new_node)
    else:
        node.append(new_node)
    return new_node


def _create_attribute_node(node, context, step):
    node_name, node_xpath, nsmap = _get_attribute_name(step, context)
    node.set(node_name, b'')
    result = node.xpath(node_xpath, namespaces=nsmap)
    return result[0]


def _predicate_is_constructible(pred):
    if isinstance(pred, ast.Step):
        if pred.axis not in (None, 'child', '@', 'attribute'):
            return False
        if not isinstance(pred.node_test, ast.NameTest):
            return False
        if any(not _predicate_is_constructible(sub_pred) for sub_pred in pred.predicates):
            return False
    elif isinstance(pred, ast.BinaryExpression):
        if pred.op == b'/':
            if not _predicate_is_constructible(pred.left):
                return False
            if not _predicate_is_constructible(pred.right):
                return False
        elif pred.op == b'=':
            if not _predicate_is_constructible(pred.left):
                return False
            if not isinstance(pred.right, (
             six.integer_types, six.string_types, ast.VariableReference)):
                return False
    return True


def _construct_predicate(xast, node, context):
    if isinstance(xast, ast.Step):
        return _create_xml_node(xast, node, context)
    else:
        if isinstance(xast, ast.BinaryExpression):
            if xast.op == b'/':
                left_leaf = _construct_predicate(xast.left, node, context)
                right_node = _construct_predicate(xast.right, left_leaf, context)
                return right_node
            if xast.op == b'=':
                left_leaf = _construct_predicate(xast.left, node, context)
                step = _find_terminal_step(xast.left)
                if isinstance(xast.right, ast.VariableReference):
                    name = xast.right.name
                    ctxval = context.get(name, None)
                    if ctxval is None:
                        ctxval = context[name[1]]
                    xvalue = str(ctxval)
                else:
                    xvalue = str(xast.right)
                _set_in_xml(left_leaf, xvalue, context, step)
                return left_leaf
        return


def _set_in_xml(node, val, context, step):
    if isinstance(node, etree._Element):
        if isinstance(val, etree._Element):
            node.clear()
            node.text = val.text
            for child in val:
                node.append(child)

            for name, val in val.attrib.iteritems():
                node.set(name, val)

        elif not list(node):
            node.text = val
        else:
            raise Exception(b'Cannot set string value - not a text node!')
    elif hasattr(node, b'getparent'):
        if _is_text_nodetest(step):
            node.getparent().text = val
        else:
            attribute, node_xpath, nsmap = _get_attribute_name(step, context)
            node.getparent().set(attribute, val)


def _remove_xml(xast, node, context, if_empty=False):
    """Remove a node or attribute.  For multipart XPaths that are
    constructible by :mod:`eulxml.xmlmap`, the corresponding nodes
    will be removed if they are empty (other than predicates specified
    in the XPath).

    :param xast: parsed xpath (xpath abstract syntax tree) from
        :mod:`eulxml.xpath`
    :param node: lxml node relative to which xast should be removed
    :param context: any context required for the xpath (e.g.,
        namespace definitions)
    :param if_empty: optional boolean; only remove a node if it is
        empty (no attributes and no child nodes); defaults to False

    :returns: True if something was deleted
    """
    if isinstance(xast, ast.Step):
        if isinstance(xast.node_test, ast.NameTest):
            if xast.axis in (None, 'child'):
                return _remove_child_node(node, context, xast, if_empty=if_empty)
            if xast.axis in ('@', 'attribute'):
                return _remove_attribute_node(node, context, xast)
        elif _is_text_nodetest(xast):
            node.text = b''
            return True
    elif isinstance(xast, ast.BinaryExpression):
        if xast.op == b'/':
            left_xpath = serialize(xast.left)
            left_node = _find_xml_node(left_xpath, node, context)
            if left_node is not None:
                removed = _remove_xml(xast.right, left_node, context, if_empty=if_empty)
                if removed and _predicate_is_constructible(left_xpath):
                    _remove_xml(xast.left, node, context, if_empty=True)
                return removed
    return False


def _remove_child_node(node, context, xast, if_empty=False):
    """Remove a child node based on the specified xpath.

    :param node: lxml element relative to which the xpath will be
        interpreted
    :param context: any context required for the xpath (e.g.,
        namespace definitions)
    :param xast: parsed xpath (xpath abstract syntax tree) from
        :mod:`eulxml.xpath`
    :param if_empty: optional boolean; only remove a node if it is
        empty (no attributes and no child nodes); defaults to False

    :returns: True if a node was deleted
    """
    xpath = serialize(xast)
    child = _find_xml_node(xpath, node, context)
    if child is not None:
        if if_empty is True and not _empty_except_predicates(xast, child, context):
            return False
        node.remove(child)
        return True
    else:
        return


def _remove_attribute_node(node, context, xast):
    node_name, node_xpath, nsmap = _get_attribute_name(xast, context)
    del node.attrib[node_name]
    return True


def _remove_predicates(xast, node, context):
    """Remove any constructible predicates specified in the xpath
    relative to the specified node.

    :param xast: parsed xpath (xpath abstract syntax tree) from
        :mod:`eulxml.xpath`
    :param node: lxml element which predicates will be removed from
    :param context: any context required for the xpath (e.g.,
        namespace definitions)

    :returns: updated a copy of the xast without the predicates that
        were successfully removed
    """
    xast_c = deepcopy(xast)
    for pred in list(xast_c.predicates):
        if not _predicate_is_constructible(pred):
            continue
        if isinstance(pred, ast.BinaryExpression):
            if pred.op == b'=' and node.xpath(serialize(pred), **context) is True:
                if isinstance(pred.left, ast.Step):
                    if pred.left.axis in ('@', 'attribute'):
                        if _remove_attribute_node(node, context, pred.left):
                            xast_c.predicates.remove(pred)
                    elif pred.left.axis in (None, 'child'):
                        if _remove_child_node(node, context, pred.left, if_empty=True):
                            xast_c.predicates.remove(pred)
                elif isinstance(pred.left, ast.BinaryExpression):
                    _remove_xml(pred.left, node, context, if_empty=True)

    return xast_c


def _empty_except_predicates(xast, node, context):
    """Check if a node is empty (no child nodes or attributes) except
    for any predicates defined in the specified xpath.

    :param xast: parsed xpath (xpath abstract syntax tree) from
        :mod:`eulxml.xpath`
    :param node: lxml element to check
    :param context: any context required for the xpath (e.g.,
        namespace definitions)

    :returns: boolean indicating if the element is empty or not
    """
    node_c = deepcopy(node)
    _remove_predicates(xast, node_c, context)
    return bool(len(node_c) == 0 and len(node_c.attrib) == 0)


def _get_attribute_name(step, context):
    if not step.node_test.prefix:
        nsmap = {}
        ns_uri = None
        node_name = step.node_test.name
        node_xpath = b'@%s' % node_name
    else:
        if b'namespaces' in context and step.node_test.prefix in context[b'namespaces']:
            ns_uri = context[b'namespaces'][step.node_test.prefix]
        else:
            ns_uri = None
        node_xpath = b'@%s:%s' % (step.node_test.prefix, step.node_test.name)
        node_name = b'{%s}%s' % (ns_uri, step.node_test.name)
        nsmap = {step.node_test.prefix: ns_uri}
    return (node_name, node_xpath, nsmap)


def _is_text_nodetest(step):
    """Fields selected with an xpath of text() need special handling; Check if
    a xpath step is a text() node test. """
    try:
        return step.node_test.name == b'text'
    except:
        pass

    return False


class SingleNodeManager(object):

    def __init__(self, instantiate_on_get=False):
        self.instantiate_on_get = instantiate_on_get

    def get(self, xpath, node, context, mapper, xast):
        match = _find_xml_node(xpath, node, context)
        if match is None and self.instantiate_on_get:
            return mapper.to_python(_create_xml_node(xast, node, context))
        else:
            return mapper.to_python(match)

    def set(self, xpath, xast, node, context, mapper, value):
        xvalue = mapper.to_xml(value)
        match = _find_xml_node(xpath, node, context)
        if xvalue is None:
            if match is not None:
                removed = _remove_xml(xast, node, context)
                if not removed:
                    logger.warn(b"Could not remove xml for '%s' from %r" % (
                     serialize(xast), node))
        else:
            if match is None:
                match = _create_xml_node(xast, node, context)
            step = _find_terminal_step(xast)
            _set_in_xml(match, xvalue, context, step)
        return

    def create(self, xpath, xast, node, context):
        match = _find_xml_node(xpath, node, context)
        if match is not None:
            return match
        else:
            return _create_xml_node(xast, node, context)

    def delete(self, xpath, xast, node, context, mapper):
        match = _find_xml_node(xpath, node, context)
        if match is not None:
            _remove_xml(xast, node, context)
        return


class NodeList(object):
    """Custom List-like object to handle ListFields like :class:`IntegerListField`,
    :class:`StringListField`, and :class:`NodeListField`, which allows for getting,
    setting, and deleting list members.  :class:`NodeList` should **not** be
    initialized directly, but instead should only be accessed as the return type
    from a ListField.

    Supports common list functions and operators, including the following: len();
    **in**; equal and not equal comparison to standard python Lists.  Items can
    be retrieved, set, and deleted by index, but slice indexing is not supported.
    Supports the methods that Python documentation indicates should be provided
    by Mutable sequences, with the exceptions of reverse and sort; in the
    particular case of :class:`NodeListField`, it is unclear how a list of
    :class:`~eulxml.xmlmap.XmlObject` should be sorted, or whether or not such
    a thing would be useful or meaningful for XML content.

    When a new element is appended to a :class:`~eulxml.xmlmap.fields.NodeList`,
    it will be added to the XML immediately after the last element in the list.
    In the case of an empty list, the new content will be appended at the end of
    the appropriate XML parent node.  For XML content where element order is important
    for schema validity, extra care may be required when constructing content.
    """

    def __init__(self, xpath, node, context, mapper, xast):
        self.xpath = xpath
        self.node = node
        self.context = context
        self.mapper = mapper
        self.xast = xast

    @property
    def matches(self):
        return self.node.xpath(self.xpath, **self.context)

    def is_empty(self):
        """Parallel to :meth:`eulxml.xmlmap.XmlObject.is_empty`.  A
        NodeList is considered to be empty if every element in the
        list is empty."""
        return all(n.is_empty() for n in self)

    @property
    def data(self):
        return [ self.mapper.to_python(match) for match in self.matches ]

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data

    def __iter__(self):
        for item in self.matches:
            yield self.mapper.to_python(item)

    def __eq__(self, other):
        return self.data == other

    def __ne__(self, other):
        return self.data != other

    def _check_key_type(self, key):
        if not isinstance(key, (slice, six.integer_types)):
            raise TypeError
        assert not isinstance(key, slice), b'Slice indexing is not supported'

    def __getitem__(self, key):
        self._check_key_type(key)
        return self.mapper.to_python(self.matches[key])

    def __setitem__(self, key, value):
        self._check_key_type(key)
        if key == len(self.matches):
            if len(self.matches):
                last_item = self.matches[(-1)]
                position = last_item.getparent().index(last_item)
                insert_index = position + 1
            else:
                insert_index = None
            match = _create_xml_node(self.xast, self.node, self.context, insert_index)
        elif key > len(self.matches):
            raise IndexError(b"Can't set at index %d - out of range" % key)
        else:
            match = self.matches[key]
        if isinstance(self.mapper, NodeMapper):
            match.getparent().replace(match, value.node)
        else:
            step = _find_terminal_step(self.xast)
            _set_in_xml(match, self.mapper.to_xml(value), self.context, step)
        return

    def __delitem__(self, key):
        self._check_key_type(key)
        if key >= len(self.matches):
            raise IndexError(b"Can't delete at index %d - out of range" % key)
        match = self.matches[key]
        match.getparent().remove(match)

    def count(self, x):
        """Return the number of times x appears in the list."""
        return self.data.count(x)

    def append(self, x):
        """Add an item to the end of the list."""
        self[len(self)] = x

    def index(self, x):
        """Return the index in the list of the first item whose value is x,
        or error if there is no such item."""
        return self.data.index(x)

    def remove(self, x):
        """Remove the first item from the list whose value is x,
        or error if there is no such item."""
        del self[self.index(x)]

    def pop(self, i=None):
        """Remove the item at the given position in the list, and return it.
        If no index is specified, removes and returns the last item in the list."""
        if i is None:
            i = len(self) - 1
        val = self[i]
        del self[i]
        return val

    def extend(self, list):
        """Extend the list by appending all the items in the given list."""
        for item in list:
            self.append(item)

    def insert(self, i, x):
        """Insert an item (x) at a given position (i)."""
        if i == len(self):
            self.append(x)
        elif len(self.matches) > i:
            insert_index = self.matches[i].getparent().index(self.matches[i])
            _create_xml_node(self.xast, self.node, self.context, insert_index)
            self[i] = x
        else:
            raise IndexError(b"Can't insert '%s' at index %d - list length is only %d" % (
             x, i, len(self)))


class NodeListManager(object):

    def get(self, xpath, node, context, mapper, xast):
        return NodeList(xpath, node, context, mapper, xast)

    def delete(self, xpath, xast, node, context, mapper):
        current_list = self.get(xpath, node, context, mapper, xast)
        [ current_list.remove(x) for x in current_list ]

    def set(self, xpath, xast, node, context, mapper, value):
        current_list = self.get(xpath, node, context, mapper, xast)
        for i in range(len(value)):
            current_list[i] = value[i]

        while len(current_list) > len(value):
            current_list.pop()


class StringField(Field):
    """Map an XPath expression to a single Python string. If the XPath
    expression evaluates to an empty NodeList, a StringField evaluates to
    `None`.

    Takes an optional parameter to indicate that the string contents should have
    whitespace normalized.  By default, does not normalize.

    Takes an optional list of choices to restrict possible values.

    Supports setting values for attributes, empty nodes, or text-only nodes.
    """

    def __init__(self, xpath, normalize=False, choices=None, *args, **kwargs):
        self.choices = choices
        super(StringField, self).__init__(xpath, manager=SingleNodeManager(), mapper=StringMapper(normalize=normalize), *args, **kwargs)


class StringListField(Field):
    """Map an XPath expression to a list of Python strings. If the XPath
    expression evaluates to an empty NodeList, a StringListField evaluates to
    an empty list.

    Takes an optional parameter to indicate that the string contents should have
    whitespace normalized.  By default, does not normalize.

    Takes an optional list of choices to restrict possible values.

    Actual return type is :class:`~eulxml.xmlmap.fields.NodeList`, which can be
    treated like a regular Python list, and includes set and delete functionality.
    """

    def __init__(self, xpath, normalize=False, choices=None, *args, **kwargs):
        self.choices = choices
        super(StringListField, self).__init__(xpath, manager=NodeListManager(), mapper=StringMapper(normalize=normalize), *args, **kwargs)


class FloatField(Field):
    """Map an XPath expression to a single Python float. If the XPath
    expression evaluates to an empty NodeList, an FloatField evaluates to
    `None`.

    Supports setting values for attributes, empty nodes, or text-only nodes.
    """

    def __init__(self, xpath, *args, **kwargs):
        super(FloatField, self).__init__(xpath, manager=SingleNodeManager(), mapper=FloatMapper(), *args, **kwargs)


class FloatListField(Field):
    """Map an XPath expression to a list of Python floats. If the XPath
    expression evaluates to an empty NodeList, an IntegerListField evaluates to
    an empty list.

    Actual return type is :class:`~eulxml.xmlmap.fields.NodeList`, which can be
    treated like a regular Python list, and includes set and delete functionality.
    """

    def __init__(self, xpath, *args, **kwargs):
        super(FloatListField, self).__init__(xpath, manager=NodeListManager(), mapper=FloatMapper(), *args, **kwargs)


class IntegerField(Field):
    """Map an XPath expression to a single Python integer. If the XPath
    expression evaluates to an empty NodeList, an IntegerField evaluates to
    `None`.

    Supports setting values for attributes, empty nodes, or text-only nodes.
    """

    def __init__(self, xpath, *args, **kwargs):
        super(IntegerField, self).__init__(xpath, manager=SingleNodeManager(), mapper=IntegerMapper(), *args, **kwargs)


class IntegerListField(Field):
    """Map an XPath expression to a list of Python integers. If the XPath
    expression evaluates to an empty NodeList, an IntegerListField evaluates to
    an empty list.

    Actual return type is :class:`~eulxml.xmlmap.fields.NodeList`, which can be
    treated like a regular Python list, and includes set and delete functionality.
    """

    def __init__(self, xpath, *args, **kwargs):
        super(IntegerListField, self).__init__(xpath, manager=NodeListManager(), mapper=IntegerMapper(), *args, **kwargs)


class SimpleBooleanField(Field):
    """Map an XPath expression to a Python boolean.  Constructor takes additional
    parameter of true, false values for comparison and setting in xml.  This only
    handles simple boolean that can be read and set via string comparison.

    Supports setting values for attributes, empty nodes, or text-only nodes.
    """

    def __init__(self, xpath, true, false, *args, **kwargs):
        super(SimpleBooleanField, self).__init__(xpath, manager=SingleNodeManager(), mapper=SimpleBooleanMapper(true, false), *args, **kwargs)


class DateTimeField(Field):
    """
    Map an XPath expression to a single Python
    :class:`datetime.datetime`. If the XPath expression evaluates to
    an empty :class:`NodeList`, a :class:`DateTimeField` evaluates to
    `None`.

    :param format: optional date-time format.  Used with
        :meth:`datetime.datetime.strptime` and
        :meth:`datetime.datetime.strftime` to convert between XML text
        and Python :class:`datetime.datetime` objects.  If no format
        is specified, XML dates are converted from full ISO date time
        format, with or without microseconds, and dates are written
        out to XML in ISO format via
        :meth:`datetime.datetime.isoformat`.

    :param normalize: optional parameter to indicate string contents
        should have whitespace normalized before converting to
        :class:`~datetime.datetime`.  By default, no normalization is
        done.

    For example, given the field definition::

      last_update = DateTimeField('last_update', format="%d-%m-%Y %H:%M:%S",
          normalize=True)

    and the XML::

      <last_update>
          21-04-2012 00:00:00
      </last_update>

    accessing the field would return::

      >>> myobj.last_update
      datetime.datetime(2012, 4, 21, 0, 0)

    """

    def __init__(self, xpath, format=None, normalize=False, *args, **kwargs):
        super(DateTimeField, self).__init__(xpath, manager=SingleNodeManager(), mapper=DateTimeMapper(format=format, normalize=normalize), *args, **kwargs)


class DateTimeListField(Field):
    """
    Map an XPath expression to a list of Python
    :class:`datetime.datetime` objects. If the XPath expression
    evaluates to an empty :class:`NodeList`, a
    :class:`DateTimeListField` evaluates to an empty list.  Date
    formatting is as described in :class:`DateTimeField`.

    Actual return type is :class:`~eulxml.xmlmap.fields.NodeList`, which can be
    treated like a regular Python list, and includes set and delete functionality.

    :param format: optional date-time format.  See
        :class:`DateTimeField` for more details.

    :param normalize: optional parameter to indicate string contents
        should have whitespace normalized before converting to
        :class:`~datetime.datetime`.  By default, no normalization is
        done.

    """

    def __init__(self, xpath, format=None, normalize=False, *args, **kwargs):
        super(DateTimeListField, self).__init__(xpath, manager=NodeListManager(), mapper=DateTimeMapper(format=format, normalize=normalize), *args, **kwargs)


class DateField(Field):
    """
    Map an XPath expression to a single Python :class:`datetime.date`,
    roughly comparable to :class:`DateTimeField`.

    :param format: optional date-time format.  Used to convert between
        XML and Python :class:`datetime.date`; if no format, then
        the ISO format YYYY-MM-DD (%Y-%m-%d) will be used.
    :param normalize: optional parameter to indicate string contents
        should have whitespace normalized before converting to
        :class:`~datetime.date`.  By default, no normalization is
        done.
    """

    def __init__(self, xpath, format=None, normalize=False, *args, **kwargs):
        super(DateField, self).__init__(xpath, manager=SingleNodeManager(), mapper=DateMapper(format=format, normalize=normalize), *args, **kwargs)


class DateListField(Field):
    """
    Map an XPath expression to a list of Python
    :class:`datetime.date` objects. See :class:`DateField` and
    :class:`DateTimeListField` for more details.
    """

    def __init__(self, xpath, format=None, normalize=False, *args, **kwargs):
        super(DateListField, self).__init__(xpath, manager=NodeListManager(), mapper=DateMapper(format=format, normalize=normalize), *args, **kwargs)


class NodeField(Field):
    """Map an XPath expression to a single
    :class:`~eulxml.xmlmap.XmlObject` subclass instance. If the XPath
    expression evaluates to an empty NodeList, a NodeField evaluates
    to `None`.

    Normally a ``NodeField``'s ``node_class`` is a class. As a special
    exception, it may be the string ``"self"``, in which case it recursively
    refers to objects of its containing :class:`~eulxml.xmlmap.XmlObject` class.

    If an :class:`~eulxml.xmlmap.XmlObject` contains a NodeField named
    ``foo``, then the object will automatically have a
    ``create_foo()`` method in addition to its ``foo`` property. Code
    can call this ``create_foo()`` method to create the child element
    if it doesn't exist; the method will have no effect if the element
    is already present.

    Deprecated ``instantiate_on_get`` flag: set to True if you need a
    non-existent node to be created when the NodeField is accessed. This
    feature is deprecated: Instead, create your node explicitly with
    ``create_foo()`` as described above.
    """

    def __init__(self, xpath, node_class, instantiate_on_get=False, *args, **kwargs):
        super(NodeField, self).__init__(xpath, manager=SingleNodeManager(instantiate_on_get=instantiate_on_get), mapper=NodeMapper(node_class), *args, **kwargs)

    def _get_node_class(self):
        return self.mapper.node_class

    def _set_node_class(self, val):
        self.mapper.node_class = val

    node_class = property(_get_node_class, _set_node_class)

    def create_for_node(self, node, context):
        return self.manager.create(self.xpath, self.parsed_xpath, node, context)


class NodeListField(Field):
    """Map an XPath expression to a list of
    :class:`~eulxml.xmlmap.XmlObject` subclass instances. If the XPath
    expression evalues to an empty NodeList, a NodeListField evaluates
    to an empty list.

    Normally a ``NodeListField``'s ``node_class`` is a class. As a special
    exception, it may be the string ``"self"``, in which case it recursively
    refers to objects of its containing :class:`~eulxml.xmlmap.XmlObject` class.

    Actual return type is :class:`~eulxml.xmlmap.fields.NodeList`, which can be
    treated like a regular Python list, and includes set and delete functionality.
    """

    def __init__(self, xpath, node_class, *args, **kwargs):
        super(NodeListField, self).__init__(xpath, manager=NodeListManager(), mapper=NodeMapper(node_class), *args, **kwargs)

    def _get_node_class(self):
        return self.mapper.node_class

    def _set_node_class(self, val):
        self.mapper.node_class = val

    node_class = property(_get_node_class, _set_node_class)


class ItemField(Field):
    """Access the results of an XPath expression directly. An ItemField does no
    conversion on the result of evaluating the XPath expression."""

    def __init__(self, xpath, *args, **kwargs):
        super(ItemField, self).__init__(xpath, manager=SingleNodeManager(), mapper=NullMapper(), *args, **kwargs)


class SchemaField(Field):
    """Schema-based field.  At class definition time, a SchemaField will be
    **replaced** with the appropriate :class:`eulxml.xmlmap.fields.Field` type
    based on the schema type definition.

    Takes an xpath (which will be passed on to the real Field init) and a schema
    type definition name.  If the schema type has enumerated restricted values,
    those will be passed as choices to the Field.

    For example, to define a resource type based on the `MODS
    <http://www.loc.gov/standards/mods/>`_ schema,
    ``resourceTypeDefinition`` is a simple type with an enumeration of
    values, so you could add something like this::

        resource_type  = xmlmap.SchemaField("mods:typeOfResource", "resourceTypeDefinition")

    Currently only supports simple string-based schema types.
    """

    def __init__(self, xpath, schema_type, *args, **kwargs):
        self.xpath = xpath
        self.schema_type = schema_type
        super(SchemaField, self).__init__(xpath, manager=None, mapper=None, *args, **kwargs)
        return

    def get_field(self, schema):
        """Get the requested type definition from the schema and return the
        appropriate :class:`~eulxml.xmlmap.fields.Field`.

        :param schema: instance of :class:`eulxml.xmlmap.core.XsdSchema`
        :rtype: :class:`eulxml.xmlmap.fields.Field`
        """
        type = schema.get_type(self.schema_type)
        logger.debug(b'Found schema type %s; base type %s, restricted values %s' % (
         self.schema_type, type.base_type(), type.restricted_values))
        kwargs = {}
        if type.restricted_values:
            choices = []
            choices.extend(type.restricted_values)
            if b'' in choices:
                choices.remove(b'')
            choices.insert(0, b'')
            kwargs[b'choices'] = choices
        basetype = type.base_type()
        if basetype == b'string':
            newfield = StringField(self.xpath, required=self.required, **kwargs)
            newfield.creation_counter = self.creation_counter
            return newfield
        raise Exception(b'basetype %s is not yet supported by SchemaField' % basetype)