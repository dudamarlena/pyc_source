# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\zinspect\inspect.py
# Compiled at: 2007-06-26 13:15:06
"""
the inspect module is used to inspect an object and make sure it conforms
to a specific interface declaration.
For this the object must declare that is implements the interface, but we
will also make sure the object really provides the attributes and methods
that the interface requires.
"""
import new, zope.interface
from zope.interface import Attribute, Interface, implements
from zinspect import MissingAttribute, MissingMethod, DoesNotProvide, DoesNotImplement
__all__ = [
 'conforms']
reference_class = new.classobj('u', (), dict())
reference_newclass = new.classobj('u', (object,), dict())
T_CLASS = type(reference_class)
T_NEWCLASS = type(reference_newclass)
T_INSTANCE = type(reference_class())
instance_method = new.instancemethod(lambda x: '', None, reference_class)
T_INSTANCE_METHOD = type(instance_method)

def conforms(obj, interface):
    """
    this function will inspect the given obj and return True if it conforms
    to the interface declaration interface given as the second argument.

    @param obj: an object to inspect, can be a class or an instance of a class
    @type obj: class or instance

    @param interface: an interface class that will be used to test if the
    given object is really implementing it
    @type obj: Interface Class
    """
    assert type(interface) == type(Interface), 'interface must be of type zope.interface.Interface'
    if type(obj) == T_INSTANCE:
        if not interface.providedBy(obj):
            msg = 'object %s does not declare to provide interface %s' % (
             obj, interface)
            raise DoesNotProvide(msg)
    elif type(obj) == T_CLASS or type(obj) == T_NEWCLASS:
        if not interface.implementedBy(obj):
            msg = 'class %s does not declare to implement interface %s' % (
             obj, interface)
            raise DoesNotImplement(msg)
    else:
        msg = 'Unknown type for obj: %s' % type(obj)
        raise TypeError(msg)
    inames = interface.names()
    for name in inames:
        missing_attrs = list()
        req_type = type(interface.get(name))
        try:
            req_attr = getattr(obj, name)
        except:
            msg = '%s does not contain the required attribute: %s' % (
             obj, name)
            missing_attrs.append(name)

        if req_type == zope.interface.interface.Method:
            if not type(req_attr) == T_INSTANCE_METHOD:
                msg = 'Attribute %s is not of the required type:'
                msg += 'instancemethod'
                msg = msg % name
                raise MissingMethod(msg)
        try:
            f_init = obj.__dict__['__init__']
            init_code = f_init.func_code
            for mattr in missing_attrs:
                if mattr in init_code.co_names:
                    missing_attrs.remove(mattr)

        except KeyError:
            pass

        if len(missing_attrs) > 0:
            msg = 'Missing attributes: %s' % missing_attrs
            raise MissingAttribute(msg)

    return True