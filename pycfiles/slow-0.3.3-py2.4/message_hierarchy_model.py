# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slow/model/message_hierarchy_model.py
# Compiled at: 2006-03-22 06:36:28
from itertools import chain
from lxml import etree
from xpathmodel import XPathModel
from model import NamedObject
MSG_NAMESPACE_URI = 'http://www.dvs1.informatik.tu-darmstadt.de/research/OverML/himdel'

def buildMessageElement(parent, node_type, **kwargs):
    tag = '{%s}%s' % (MSG_NAMESPACE_URI, node_type)
    return etree.SubElement(parent, tag, **kwargs)


class MessageHierarchyBaseClass(XPathModel):
    __module__ = __name__
    DEFAULT_NAMESPACE = MSG_NAMESPACE_URI


class MessageHierarchyRoot(MessageHierarchyBaseClass):
    __module__ = __name__
    TYPE_NAME = 'message_hierarchy'
    _get_containers = './{%(DEFAULT_NAMESPACE)s}container'
    _get_protocols = './{%(DEFAULT_NAMESPACE)s}protocol'
    _get_headers = './{%(DEFAULT_NAMESPACE)s}header'
    _get_access_names = './*/@access_name'
    _get_type_names = './*/@type_name'
    _get_message_names = './/{%(DEFAULT_NAMESPACE)s}message/@type_name'


class AccessibleMixin(object):
    __module__ = __name__
    _val_access_name = NamedObject._val_name
    _attr_access_name = './@access_name'


class MessageFieldBase(MessageHierarchyBaseClass):
    __module__ = __name__
    _val_type_name = NamedObject._val_name
    _attr_type_name = './@type_name'
    _attr_readable_name = './@readable_name'


class MessageFieldHierarchy(MessageFieldBase):
    __module__ = __name__
    _get_access_names = './*/@access_name'


class LinkModel(MessageFieldBase):
    __module__ = __name__


class MessageLinkModel(LinkModel):
    __module__ = __name__
    TYPE_NAME = 'message-ref'


class ContainerLinkModel(LinkModel, AccessibleMixin):
    __module__ = __name__
    TYPE_NAME = 'container-ref'


class ContentModel(MessageFieldBase, AccessibleMixin):
    __module__ = __name__
    TYPE_NAME = 'content'


class AttributeModel(MessageFieldBase, AccessibleMixin):
    __module__ = __name__
    TYPE_NAME = 'attribute'


class ViewDataModel(MessageFieldBase, AccessibleMixin):
    __module__ = __name__
    TYPE_NAME = 'viewdata'
    _attr_structured = 'bool#./@structured'
    _attr_bucket = 'bool#./@single_bucket'
    _attr_list = 'bool#./@list'


class ContainerModel(MessageFieldHierarchy, AccessibleMixin):
    __module__ = __name__
    TYPE_NAME = 'container'
    _attr_list = 'bool#./@list'


class HeaderModel(MessageFieldHierarchy, AccessibleMixin):
    __module__ = __name__
    TYPE_NAME = 'header'


class IPProtocolModel(MessageFieldHierarchy, AccessibleMixin):
    __module__ = __name__
    TYPE_NAME = 'protocol'


class MessageModel(MessageFieldHierarchy):
    __module__ = __name__
    TYPE_NAME = 'message'


ns = etree.Namespace(MSG_NAMESPACE_URI)
ns.update(chain(((cls.TYPE_NAME, cls) for cls in globals().itervalues() if hasattr(cls, 'TYPE_NAME')), [
 (
  None, MessageHierarchyBaseClass)]))