# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/traversing.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 10619 bytes
"""PyAMS_utils.traversing module

This module provides a custom Pyramid "namespace" traverser: using "++name++" URLs allows
to traverse URLs based on custom traversing adapters.

It also provides a "get_parent" function, which returns a parent object of given object providing
a given interface.
"""
from pyramid.compat import decode_path_info, is_nonstr_iter
from pyramid.exceptions import NotFound, URLDecodeError
from pyramid.interfaces import VH_ROOT_KEY
from pyramid.location import lineage
from pyramid.threadlocal import get_current_registry
from pyramid.traversal import ResourceTreeTraverser, empty, slash, split_path_info
from zope.interface import Interface
from zope.intid.interfaces import IIntIds
from zope.location import ILocation
from zope.location.interfaces import IContained
from zope.traversing.interfaces import BeforeTraverseEvent, ITraversable
from pyams_utils.adapter import ContextAdapter, adapter_config
from pyams_utils.interfaces.traversing import IPathElements
from pyams_utils.registry import query_utility
__docformat__ = 'restructuredtext'

class NamespaceTraverser(ResourceTreeTraverser):
    __doc__ = 'Custom traverser handling views and namespaces\n\n    This is an upgraded version of native Pyramid traverser.\n    It adds:\n    - a new BeforeTraverseEvent before traversing each object in the path\n    - support for namespaces with "++" notation\n    '
    PLUS_SELECTOR = '+'
    NAMESPACE_SELECTOR = PLUS_SELECTOR * 2

    def __call__(self, request):
        environ = request.environ
        matchdict = request.matchdict
        if matchdict is not None:
            path = matchdict.get('traverse', slash) or slash
            if is_nonstr_iter(path):
                path = '/' + slash.join(path) or slash
            subpath = matchdict.get('subpath', ())
            if not is_nonstr_iter(subpath):
                subpath = split_path_info(subpath)
        else:
            subpath = ()
            try:
                path = request.path_info or slash
            except KeyError:
                path = slash
            except UnicodeDecodeError as exc:
                raise URLDecodeError(exc.encoding, exc.object, exc.start, exc.end, exc.reason)

            if VH_ROOT_KEY in environ:
                vroot_path = decode_path_info(environ[VH_ROOT_KEY])
                vroot_tuple = split_path_info(vroot_path)
                vpath = vroot_path + path
                vroot_idx = len(vroot_tuple) - 1
            else:
                vroot_tuple = ()
                vpath = path
                vroot_idx = -1
            root = self.root
            obj = vroot = root
            request.registry.notify(BeforeTraverseEvent(root, request))
            if vpath == slash:
                vpath_tuple = ()
            else:
                i = 0
                plus_selector = self.PLUS_SELECTOR
                ns_selector = self.NAMESPACE_SELECTOR
                view_selector = self.VIEW_SELECTOR
                vpath_tuple = split_path_info(vpath)
                for segment in vpath_tuple:
                    if obj is not root:
                        request.registry.notify(BeforeTraverseEvent(obj, request))
                    if segment == plus_selector:
                        registry = get_current_registry()
                        traverser = registry.queryMultiAdapter((obj, request), ITraversable, '+')
                        if traverser is None:
                            raise NotFound()
                        try:
                            obj = traverser.traverse(vpath_tuple[(vroot_idx + i + 2)], vpath_tuple[vroot_idx + i + 3:])
                        except IndexError:
                            raise NotFound()
                        else:
                            i += 1
                            return {'context': obj, 
                             'view_name': ''.join(vpath_tuple[vroot_idx + i + 2:]), 
                             'subpath': vpath_tuple[i + 2:], 
                             'traversed': vpath_tuple[:vroot_idx + i + 2], 
                             'virtual_root': vroot, 
                             'virtual_root_path': vroot_tuple, 
                             'root': root}
                    else:
                        if segment[:2] == ns_selector:
                            nss, name = segment[2:].split(ns_selector, 1)
                            registry = get_current_registry()
                            traverser = registry.queryMultiAdapter((obj, request), ITraversable, nss)
                            if traverser is None:
                                traverser = registry.queryAdapter(obj, ITraversable, nss)
                            if traverser is None:
                                raise NotFound()
                            obj = traverser.traverse(name, vpath_tuple[vroot_idx + i + 1:])
                            i += 1
                            continue
                        elif segment[:2] == view_selector:
                            return {'context': obj, 
                             'view_name': segment[2:], 
                             'subpath': vpath_tuple[i + 1:], 
                             'traversed': vpath_tuple[:vroot_idx + i + 1], 
                             'virtual_root': vroot, 
                             'virtual_root_path': vroot_tuple, 
                             'root': root}
                        try:
                            getitem = obj.__getitem__
                        except AttributeError:
                            return {'context': obj, 
                             'view_name': segment, 
                             'subpath': vpath_tuple[i + 1:], 
                             'traversed': vpath_tuple[:vroot_idx + i + 1], 
                             'virtual_root': vroot, 
                             'virtual_root_path': vroot_tuple, 
                             'root': root}

                        try:
                            next_item = getitem(segment)
                        except KeyError:
                            return {'context': obj, 
                             'view_name': segment, 
                             'subpath': vpath_tuple[i + 1:], 
                             'traversed': vpath_tuple[:vroot_idx + i + 1], 
                             'virtual_root': vroot, 
                             'virtual_root_path': vroot_tuple, 
                             'root': root}

                        if i == vroot_idx:
                            vroot = next_item
                    obj = next_item
                    i += 1

        if obj is not root:
            request.registry.notify(BeforeTraverseEvent(obj, request))
        return {'context': obj, 
         'view_name': empty, 
         'subpath': subpath, 
         'traversed': vpath_tuple, 
         'virtual_root': vroot, 
         'virtual_root_path': vroot_tuple, 
         'root': root}


def get_name(context):
    """Get context name"""
    return ILocation(context).__name__


def get_parent(context, interface=Interface, allow_context=True, condition=None):
    """Get first parent of the context that implements given interface

    :param object context: base element
    :param Interface interface: the interface that parend should implement
    :param boolean allow_context: if 'True' (the default), traversing is done starting with
        context; otherwise, traversing is done starting from context's parent
    :param callable condition: an optional function that should return a 'True' result when
        called with parent as first argument
    """
    if allow_context:
        parent = context
    else:
        parent = getattr(context, '__parent__', None)
    while parent is not None:
        if interface.providedBy(parent):
            target = interface(parent)
            if not condition or condition(target):
                pass
            return target
        parent = getattr(parent, '__parent__', None)


@adapter_config(context=IContained, provides=IPathElements)
class PathElementsAdapter(ContextAdapter):
    __doc__ = 'Contained object path elements adapter\n\n    This interface is intended to be used inside a keyword index to\n    be able to search object based on a given parent\n    '

    @property
    def parents(self):
        """Get list of parents OIDs"""
        intids = query_utility(IIntIds)
        if intids is None:
            return []
        return [intids.register(parent) for parent in lineage(self.context)]