# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\model\AttributeMapper.py
# Compiled at: 2018-01-18 12:27:33
# Size of source mod 2**32: 8053 bytes
import importlib, logging
from .exceptions import *
from .Mapper import Mapper
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AttributeMapper(Mapper):
    __doc__ = "\n        Decorator to map xml elements to model children\n\n        **kwargs**\n\n        namespace\n            The xml namespace to match. It can also be * to match any namespace.\n            If not specified, it defaults to the parent element's namespace.\n        local_name\n            Required. The local name of the xml attribute we're matching. It can\n            also be * to match any local name.\n        into\n            The python attribute to store the value of the attribute into.\n            Defaults to the local_name if not specified.\n\n        type\n            The type of the expected value. Types are stored directly as data,\n            no enclosed in a model class. Types usually restrict the domain\n            values.\n        enum\n            Enumeration the attribute's value must be from\n        pattern\n            Pattern which the value of the attribute must match.\n\n        required\n            True or False (default). Specifies if the attribute is required.\n        default\n            The default value of an attribute if it isn't specified. The\n            (implicit) default is None or the first item of an *enum*.\n\n        min\n            The minimum value of the attribute. Can be numeric or None (the\n            default).\n        max\n            The maximum value of the attribute. Can be numeric or None (the\n            default).\n\n        prohibited\n            The attribute should not appear in the element.\n    "

    def __init__(self, **kwargs):
        if 'local_name' not in kwargs:
            raise DecoratorException('Attributes need at least local_name defined')
        (super().__init__)(**kwargs)

    def get_attr_name(self):
        if 'into' in self._kwargs:
            return self._kwargs['into']
        else:
            return self._kwargs['local_name'].replace('-', '_')

    def initialize(self, model):
        attr_name = self.get_attr_name()
        if 'default' in self._kwargs:
            default_value = self._kwargs['default']
        else:
            default_value = None
        setattr(model, attr_name, default_value)
        logger.debug('Initialized ' + str(model) + ' attribute ' + attr_name + ' to default ' + str(default_value))

    def get_namespace(self):
        if 'namespace' in self._kwargs:
            return self._kwargs['namespace']
        else:
            return

    def get_local_name(self):
        return self._kwargs['local_name']

    def matches(self, attr, model):
        from .Model import Model
        matches = (
         self.get_namespace(), self.get_local_name()) in (
         (
          attr.namespace, attr.local_name),
         (
          None, attr.local_name),
         (
          attr.namespace, Model.ANY_LOCAL_NAME),
         (
          Model.ANY_NAMESPACE, Model.ANY_LOCAL_NAME))
        if matches:
            logger.debug('AttributeMapper matches ' + str(attr))
        else:
            logger.debug('AttributeMapper does not match ' + str(attr))
        return matches

    def parse_in(self, model, attr):
        logger.debug('Parsing attribute ' + attr.name + ' using kwargs: ' + str(self._kwargs))
        name = self.get_attr_name()
        value = attr.value
        if 'enum' in self._kwargs:
            if value not in self._kwargs['enum']:
                raise EnumerationException(name + ' attribute must be one of ' + str(self._kwargs['enum']) + ': ' + str(value))
        if 'type' in self._kwargs:
            logger.debug('Parsing ' + str(value) + ' as ' + str(self._kwargs['type']))
            type_ = self._kwargs['type']
            if isinstance(type_, tuple):
                mod = importlib.import_module(type_[0])
                type_ = getattr(mod, type_[1])
            value = type_().parse_value(value)
        logger.debug('Parsed attribute ' + name + ' = ' + str(value))
        setattr(model, name, value)

    def validate(self, model):
        name = self.get_attr_name()
        logger.debug('Validating attribute ' + str(self._kwargs))
        name = self._kwargs['local_name']
        if 'required' in self._kwargs:
            if self._kwargs['required']:
                if not hasattr(model, name) or getattr(model, name) is None:
                    raise RequiredAttributeException(str(model) + ' must define ' + name + ' attribute')
        if 'prohibited' in self._kwargs:
            if self._kwargs['prohibited']:
                if hasattr(model, name):
                    raise ProhibitedAttributeException(str(model) + ' must not define ' + name + ' attribute')

    def produce_in(self, el, model):
        from .Model import Model
        from .xs.StringType import StringType
        if 'prohibited' in self._kwargs:
            if self._kwargs['prohibited']:
                return
        name = self.get_attr_name()
        value = getattr(model, name)
        if value is None:
            return
        else:
            if 'default' in self._kwargs:
                if value == self._kwargs['default']:
                    return
            else:
                logger.debug(str(self) + ' producing ' + str(model) + ' attribute ' + name + ' according to ' + str(self._kwargs))
                if 'namespace' in self._kwargs:
                    namespace = self._kwargs['namespace']
                else:
                    namespace = el.namespace
            prefix = el.namespace_to_prefix(namespace)
            if self._kwargs['local_name'] == Model.ANY_LOCAL_NAME:
                return
            local_name = self._kwargs['local_name']
            if 'namespace' in self._kwargs and self._kwargs['namespace'] != el.namespace:
                attr_name = prefix + ':' + local_name
            else:
                attr_name = local_name
        if 'type' in self._kwargs:
            logger.debug(str(model) + ' Producing ' + str(value) + ' as ' + str(self._kwargs['type']) + ' type')
            type_ = self._kwargs['type']()
            v = type_.produce_value(value)
            el.attributes[attr_name] = v
        else:
            if 'enum' in self._kwargs:
                if value not in self._kwargs['enum']:
                    raise EnumerationException(str(model) + '.' + name + ' attribute must be one of ' + str(self._kwargs['enum']) + ': ' + str(value))
                el.attributes[attr_name] = value
            else:
                logger.debug(str(model) + ' Producing ' + str(value) + ' as String type')
                type_ = StringType()
                v = type_.produce_value(value)
                el.attributes[attr_name] = v