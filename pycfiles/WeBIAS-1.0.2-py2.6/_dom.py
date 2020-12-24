# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/parsers/_dom.py
# Compiled at: 2015-04-13 16:10:46
from gnosis.xml.pickle.util import subnodes, _EmptyClass, unsafe_string, unsafe_content, safe_eval, obj_from_name, unpickle_function, get_class_from_name
from gnosis.util.introspect import attr_update
from types import *
import gnosis.xml.pickle.ext as mutate
from xml.dom import minidom
from gnosis.util.XtoY import to_number
import gnosis.pyconfig as pyconfig
try:
    from Numeric import *
    array_type = 'NumPy_array'
except ImportError:
    from array import *
    array_type = 'array'

XMLPicklingError = 'gnosis.xml.pickle.XMLPicklingError'
XMLUnpicklingError = 'gnosis.xml.pickle.XMLUnpicklingError'
if pyconfig.Have_TrueFalse():
    TRUE_VALUE = True
    FALSE_VALUE = False
else:
    TRUE_VALUE = 1
    FALSE_VALUE = 0

def thing_from_dom(fh, paranoia=1):
    global visited
    visited = {}
    return _thing_from_dom(minidom.parse(fh), None, paranoia)


def _save_obj_with_id(node, obj):
    id = node.getAttribute('id')
    if len(id):
        visited[id] = obj


def unpickle_instance(node, paranoia):
    """Take a <PyObject> or <.. type="PyObject"> DOM node and unpickle the object."""
    pyobj = obj_from_node(node, paranoia)
    _save_obj_with_id(node, pyobj)
    raw = _thing_from_dom(node, _EmptyClass(), paranoia)
    try:
        args = raw.__getinitargs__
        delattr(raw, '__getinitargs__')
        apply(pyobj.__init__, args)
    except:
        pass

    if hasattr(raw, '__getstate__'):
        stuff = raw.__getstate__
    else:
        stuff = raw.__dict__
    if hasattr(pyobj, '__setstate__'):
        pyobj.__setstate__(stuff)
    elif type(stuff) is DictType:
        attr_update(pyobj, stuff)
    else:
        raise XMLUnpicklingError, 'Non-DictType without setstate violates pickle protocol.' + '(PARANOIA setting may be too high)'
    return pyobj


def obj_from_node(node, paranoia=1):
    """Given a <PyObject> node, return an object of that type.
    __init__ is NOT called on the new object, since the caller may want
    to do some additional work first.
    """
    classname = node.getAttribute('class')
    try:
        modname = node.getAttribute('module')
    except:
        modname = None

    return obj_from_name(classname, modname, paranoia)


def get_node_valuetext(node):
    """Get text from node, whether in value=, or in element body."""
    if node._attrs.has_key('value'):
        ttext = node.getAttribute('value')
        return unsafe_string(ttext)
    else:
        node.normalize()
        try:
            btext = node.childNodes[0].nodeValue
        except:
            btext = ''

        return unsafe_content(btext)


def _fix_family(family, typename):
    """
    If family is None or empty, guess family based on typename.
    (We can only guess for builtins, of course.)
    """
    if family and len(family):
        return family
    if typename == 'None':
        return 'none'
    if typename == 'dict':
        return 'map'
    if typename == 'list':
        return 'seq'
    if typename == 'tuple':
        return 'seq'
    if typename == 'numeric':
        return 'atom'
    if typename == 'string':
        return 'atom'
    if typename == 'PyObject':
        return 'obj'
    if typename == 'function':
        return 'lang'
    if typename == 'class':
        return 'lang'
    if typename == 'True':
        return 'uniq'
    if typename == 'False':
        return 'uniq'
    raise XMLUnpicklingError, 'family= must be given for unknown type %s' % typename


def _thing_from_dom(dom_node, container=None, paranoia=1):
    """Converts an [xml_pickle] DOM tree to a 'native' Python object"""
    for node in subnodes(dom_node):
        if node.nodeName == 'PyObject':
            container = unpickle_instance(node, paranoia)
            if node.getAttribute('type'):
                klass = node.getAttribute('type')
                if mutate.can_unmutate(klass, container):
                    container = mutate.unmutate(klass, container, paranoia, None)
            try:
                id = node.getAttribute('id')
                visited[id] = container
            except KeyError:
                pass

        elif node.nodeName in ('attr', 'item', 'key', 'val'):
            node_family = node.getAttribute('family')
            node_type = node.getAttribute('type')
            node_name = node.getAttribute('name')
            ref_id = node.getAttribute('refid')
            if len(ref_id):
                if node.nodeName == 'attr':
                    setattr(container, node_name, visited[ref_id])
                else:
                    container.append(visited[ref_id])
                continue
            node_family = _fix_family(node_family, node_type)
            node_valuetext = get_node_valuetext(node)
            if node_family == 'none':
                node_val = None
            elif node_family == 'atom':
                node_val = node_valuetext
            elif node_family == 'seq':
                seq = []
                _save_obj_with_id(node, seq)
                node_val = _thing_from_dom(node, seq, paranoia)
            elif node_family == 'map':
                map = {}
                _save_obj_with_id(node, map)
                node_val = _thing_from_dom(node, map, paranoia)
            elif node_family == 'obj':
                node_val = unpickle_instance(node, paranoia)
            elif node_family == 'lang':
                if node_type == 'function':
                    node_val = unpickle_function(node.getAttribute('module'), node.getAttribute('class'), paranoia)
                elif node_type == 'class':
                    node_val = get_class_from_name(node.getAttribute('class'), node.getAttribute('module'), paranoia)
                else:
                    raise XMLUnpicklingError, 'Unknown lang type %s' % node_type
            elif node_family == 'uniq':
                if node_type == 'function':
                    node_val = unpickle_function(node.getAttribute('module'), node.getAttribute('class'), paranoia)
                elif node_type == 'class':
                    node_val = get_class_from_name(node.getAttribute('class'), node.getAttribute('module'), paranoia)
                elif node_type == 'True':
                    node_val = TRUE_VALUE
                elif node_type == 'False':
                    node_val = FALSE_VALUE
                else:
                    raise XMLUnpicklingError, 'Unknown uniq type %s' % node_type
            else:
                raise XMLUnpicklingError, 'UNKNOWN family %s,%s,%s' % (node_family, node_type, node_name)
            if node_type == 'None':
                node_val = None
            elif node_type == 'numeric':
                node_val = to_number(node_val)
            elif node_type == 'string':
                node_val = node_val
            elif node_type == 'list':
                node_val = node_val
            elif node_type == 'tuple':
                node_val = tuple(node_val)
            elif node_type == 'dict':
                node_val = node_val
            elif node_type == 'function':
                node_val = node_val
            elif node_type == 'class':
                node_val = node_val
            elif node_type == 'True':
                node_val = node_val
            elif node_type == 'False':
                node_val = node_val
            elif mutate.can_unmutate(node_type, node_val):
                mextra = node.getAttribute('extra')
                node_val = mutate.unmutate(node_type, node_val, paranoia, mextra)
            elif node_type == 'PyObject':
                node_val = node_val
            else:
                raise XMLUnpicklingError, 'Unknown type %s,%s' % (node, node_type)
            if node.nodeName == 'attr':
                setattr(container, node_name, node_val)
            else:
                container.append(node_val)
            _save_obj_with_id(node, node_val)
        elif node.nodeName == 'entry':
            keyval = _thing_from_dom(node, [], paranoia)
            key, val = keyval[0], keyval[1]
            container[key] = val
        else:
            raise XMLUnpicklingError, 'element %s is not in PyObjects.dtd' % node.nodeName

    return container