# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jsonstruct/unpickler.py
# Compiled at: 2013-08-09 10:47:32
import operator, sys, jsonstruct.util as util, jsonstruct.tags as tags, jsonstruct.handlers as handlers
from jsonstruct.compat import set

class Unpickler(object):

    def __init__(self):
        self._depth = 0
        self._namedict = {}
        self._namestack = []
        self._obj_to_idx = {}
        self._objs = []

    def _reset(self):
        """Resets the object's internal state.
        """
        self._namedict = {}
        self._namestack = []
        self._obj_to_idx = {}
        self._objs = []

    def _push(self):
        """Steps down one level in the namespace.
        """
        self._depth += 1

    def _pop(self, value):
        """Step up one level in the namespace and return the value.
        If we're at the root, reset the unpickler's state.
        """
        self._depth -= 1
        if self._depth == 0:
            self._reset()
        return value

    def restore(self, obj, cls_def=None):
        """Restores a flattened object to its original python state.

        Simply returns any of the basic builtin types

        >>> u = Unpickler()
        >>> u.restore('hello world')
        'hello world'
        >>> u.restore({'key': 'value'})
        {'key': 'value'}

        cls_def could be either a type or an instance. In case of instance, it
        will be used to define types inside a list or dict. eg. [Test()] means
        a list of Test.
        """
        self._push()
        if has_tag(obj, tags.ID):
            return self._pop(self._objs[obj[tags.ID]])
        else:
            if has_tag(obj, tags.REF):
                return self._pop(self._namedict.get(obj[tags.REF]))
            if has_tag(obj, tags.TYPE):
                typeref = loadclass(obj[tags.TYPE])
                if not typeref:
                    return self._pop(obj)
                return self._pop(typeref)
            if has_tag(obj, tags.REPR):
                obj = loadrepr(obj[tags.REPR])
                return self._pop(self._mkref(obj))
            if util.is_type(cls_def):
                if not util.is_dictionary(obj):
                    return self._pop(None)
                HandlerClass = handlers.BaseHandler._registry.get(cls_def)
                if HandlerClass:
                    handler = HandlerClass(self)
                    instance = handler.restore(obj)
                    return self._pop(self._mkref(instance))
                factory = loadfactory(obj)
                args = getargs(obj, cls_def)
                if args:
                    args = self.restore(args)
                try:
                    if hasattr(cls_def, '__new__'):
                        if factory:
                            instance = cls_def.__new__(cls_def, factory, *args)
                            instance.default_factory = factory
                        else:
                            instance = cls_def.__new__(cls_def, *args)
                    else:
                        instance = object.__new__(cls_def)
                except TypeError:
                    try:
                        instance = cls_def()
                    except TypeError:
                        return self._pop(self._mkref(obj))

                self._mkref(instance)
                if isinstance(instance, tuple):
                    return self._pop(instance)
                if hasattr(instance, '__setstate__') and has_tag(obj, tags.STATE):
                    state = self.restore(obj[tags.STATE])
                    instance.__setstate__(state)
                    return self._pop(instance)
                for k in util.get_public_variables(cls_def):
                    if k in obj:
                        v = obj[k]
                        if k in tags.RESERVED:
                            continue
                        self._namestack.append(k)
                        value = self.restore(v, get_attr_cls_def(cls_def, k))
                        if util.is_noncomplex(instance) or util.is_dictionary(instance):
                            instance[k] = value
                        else:
                            setattr(instance, k, value)
                        self._namestack.pop()
                    else:
                        setattr(instance, k, None)

                if has_tag(obj, tags.SEQ):
                    if hasattr(instance, 'append'):
                        for v in obj[tags.SEQ]:
                            instance.append(self.restore(v))

                    if hasattr(instance, 'add'):
                        for v in obj[tags.SEQ]:
                            instance.add(self.restore(v))

                return self._pop(instance)
            if util.is_list(obj):
                if util.is_collection(cls_def):
                    parent = type(cls_def)()
                else:
                    parent = []
                self._mkref(parent)
                item_type = get_collection_item_type(cls_def)
                is_set = type(parent) is set
                for v in obj:
                    restored_v = self.restore(v, item_type)
                    if is_set:
                        parent.add(restored_v)
                    else:
                        parent.append(restored_v)

                return self._pop(parent)
            if has_tag(obj, tags.TUPLE):
                return self._pop(tuple([ self.restore(v) for v in obj[tags.TUPLE]
                                       ]))
            if has_tag(obj, tags.SET):
                return self._pop(set([ self.restore(v) for v in obj[tags.SET]
                                     ]))
            if util.is_dictionary(obj):
                if util.is_dictionary(cls_def):
                    data = type(cls_def)()
                else:
                    data = {}
                k_type, v_type = get_dictionary_item_type(cls_def)
                for k, v in sorted(obj.items(), key=operator.itemgetter(0)):
                    self._namestack.append(k)
                    data[self.restore(k, k_type)] = self.restore(v, v_type)
                    self._namestack.pop()

                return self._pop(data)
            return self._pop(obj)

    def _refname(self):
        """Calculates the name of the current location in the JSON stack.

        This is called as jsonstruct traverses the object structure to
        create references to previously-traversed objects.  This allows
        cyclical data structures such as doubly-linked lists.
        jsonstruct ensures that duplicate python references to the same
        object results in only a single JSON object definition and
        special reference tags to represent each reference.

        >>> u = Unpickler()
        >>> u._namestack = []
        >>> u._refname()
        '/'

        >>> u._namestack = ['a']
        >>> u._refname()
        '/a'

        >>> u._namestack = ['a', 'b']
        >>> u._refname()
        '/a/b'

        """
        return '/' + ('/').join(self._namestack)

    def _mkref(self, obj):
        """
        >>> from jsonstruct._samples import Thing
        >>> thing = Thing('referenced-thing')
        >>> u = Unpickler()
        >>> u._mkref(thing)
        Thing("referenced-thing")

        >>> u._objs[0]
        Thing("referenced-thing")

        """
        obj_id = id(obj)
        try:
            self._obj_to_idx[obj_id]
        except KeyError:
            self._obj_to_idx[obj_id] = len(self._objs)
            self._objs.append(obj)
            self._namedict[self._refname()] = obj

        return obj


def loadclass(module_and_name):
    """Loads the module and returns the class.

    >>> loadclass('jsonstruct._samples.Thing')
    <class 'jsonstruct._samples.Thing'>

    >>> loadclass('example.module.does.not.exist.Missing')

    >>> loadclass('samples.MissingThing')

    """
    try:
        module, name = module_and_name.rsplit('.', 1)
        __import__(module)
        return getattr(sys.modules[module], name)
    except:
        return

    return


def loadfactory(obj):
    if not util.is_dictionary(obj):
        return
    else:
        try:
            default_factory = obj['default_factory']
        except KeyError:
            return

        try:
            type_tag = default_factory[tags.TYPE]
        except:
            return

        typeref = loadclass(type_tag)
        if typeref:
            del obj['default_factory']
            return typeref
        return


def getargs(obj, cls):
    if not cls or tags.SEQ not in obj:
        return []
    seq_list = obj[tags.SEQ]
    if hasattr(cls, '_fields'):
        if len(cls._fields) == len(seq_list):
            return seq_list
    return []


def loadrepr(reprstr):
    """Returns an instance of the object from the object's repr() string.
    It involves the dynamic specification of code.

    >>> loadrepr('jsonstruct._samples/jsonstruct._samples.Thing("json")')
    Thing("json")

    """
    module, evalstr = reprstr.split('/')
    mylocals = locals()
    localname = module
    if '.' in localname:
        localname = module.split('.', 1)[0]
    mylocals[localname] = __import__(module)
    return eval(evalstr)


def has_tag(obj, tag):
    """Helper class that tests to see if the obj is a dictionary
    and contains a particular key/tag.

    >>> obj = {'test': 1}
    >>> has_tag(obj, 'test')
    True
    >>> has_tag(obj, 'fail')
    False

    >>> has_tag(42, 'fail')
    False

    """
    return type(obj) is dict and tag in obj


def get_attr_cls_def(cls_def, k):
    if not cls_def or not k:
        return None
    attr = getattr(cls_def, k)
    return get_obj_cls_def(attr)


def get_obj_cls_def(obj):
    if not obj or util.is_function(obj):
        return
    if util.is_container(obj):
        return obj
    else:
        if not util.is_primitive(obj):
            return type(obj)
        return


def get_collection_item_type(cls_def):
    if cls_def and util.is_collection(cls_def):
        return get_obj_cls_def(cls_def.__iter__().next())
    else:
        return


def get_dictionary_item_type(cls_def):
    if cls_def and util.is_dictionary(cls_def):
        k, v = cls_def.iteritems().next()
        return (
         get_obj_cls_def(k), get_obj_cls_def(v))
    else:
        return (None, None)