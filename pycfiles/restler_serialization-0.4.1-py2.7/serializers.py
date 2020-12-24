# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/restler/serializers.py
# Compiled at: 2012-10-25 14:26:05
import copy, datetime, decimal, json, pprint, types, warnings
from xml.etree import ElementTree as ET
from restler import models
import datetime_safe
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DEFAULT_STYLE = {'xml': {'root': lambda thing: ET.Element('result'), 
           'model': lambda el, thing: ET.SubElement(el, thing._restler_serialization_name()), 
           'list': lambda el, thing: None, 
           'list_item': lambda el, thing: ET.SubElement(el, 'item'), 
           'dict': lambda el, thing: None, 
           'dict_item': lambda el, thing: ET.SubElement(el, thing[0]), 
           'null': lambda el, thing: el.set('null', 'true')}, 
   'json': {'flatten': True, 
            'indent': None}}

class SkipField(object):
    """ An empty class to dynamically exclude fields on serialization """
    pass


SKIP = SkipField()

def json_response(response, model_or_query, strategy=None, status_code=200, context={}):
    """ Render json to a webapp response """
    content = to_json(model_or_query, strategy, context=context)
    response.set_status(status_code)
    response.headers['Content-Type'] = 'application/json'
    response.out.write(content)
    return content


def xml_response(response, model_or_query, strategy=None, status_code=200, context={}):
    """ Render xml to a webapp response """
    xml = to_xml(model_or_query, strategy, context=context)
    response.set_status(status_code)
    response.headers['Content-Type'] = 'application/xml'
    response.out.write(xml)


class SerializationStrategy(object):
    """ A container for multiple mappings (shouldn't be used directly)"""

    def __init__(self, mappings={}, style=None):
        if isinstance(mappings, ModelStrategy):
            self.mappings = mappings.to_dict()
        else:
            self.mappings = dict(mappings.items())
        if style is None:
            self.style = copy.deepcopy(DEFAULT_STYLE)
        else:
            self.style = style
        return

    def _new_mapping(self, other_dict):
        """ Creates a new mapping (underlying data structure SerializationStrategy)

        :param other_dict: another mapping
        :returns: a new mapping
        """
        maps = dict(self.mappings.items())
        maps.update(other_dict)
        return self.__class__(maps)

    def __add__(self, mapping):
        """ Adds to a Serialization strategy either from an existing SerializationStrategy,
         ModelStrategy or a mapping (dictionary structure -- not recommended).
        :param mapping: SerializationStrategy, ModelStrategy or dictionary
        :returns: new SerializationStrategy
        """
        if isinstance(mapping, dict):
            return self._new_mapping(mapping)
        if isinstance(mapping, self.__class__):
            return self._new_mapping(mapping.mappings)
        if isinstance(mapping, ModelStrategy):
            return self._new_mapping(mapping.to_dict())
        raise ValueError('Cannot add type: %s' % type(mapping))

    def __sub__(self, mapping):
        """Removes a ModelStrategy from a SerializationStrategy.
        :param mapping: SerializationStrategy, ModelStrategy or dictionary
        :returns: new SerializationStrategy
        """
        if isinstance(mapping, ModelStrategy):
            self._new_mapping(mapping.to_dict())
        else:
            raise ValueError('Not of type ModelStrategy')

    def __repr__(self):
        return pprint.pformat(self.mappings)


class ModelStrategy(object):
    """ Defines how to serialize an AppEngine model i.e. which fields to include,
        exclude or map to a callable.
    """

    def __init__(self, model, include_all_fields=False, output_name=None):
        """
        Initialize the ModelStrategy

        :param model: The App Engine model class to be serialized.
        :param include_all_fields: (False) Creates a strategy with all properties of the Model to be serialized.
        :param output_name: (None) [None|string|callable] The key or tag that surrounds the serialized properties for a Model.
            The default value is the lowercase classname of the Model.
            None flattens the result structure.
                with name:  [{'my_class':{'prop1':'value1'}}, ...]
                without name:  [{'prop1':'value1'}, ...]
        """
        self.model = model
        if include_all_fields:
            self.fields = model._restler_property_map().keys()
        else:
            self.fields = []
        self.name = output_name

    def __name_map(self):
        names = {}
        for prop in self.fields:
            if isinstance(prop, dict):
                names[prop.keys()[0]] = prop
            elif isinstance(prop, tuple):
                names[prop[0]] = prop[1]
            elif isinstance(prop, basestring):
                names[prop] = prop

        return names

    def __add(self, new_fields):
        names = self.__name_map()
        model_strategy = ModelStrategy(self.model, output_name=self.name)
        model_strategy.fields = self.fields[:]
        if isinstance(new_fields, (tuple, list)):
            for name in new_fields:
                if isinstance(name, dict):
                    name = name.items()
                if isinstance(name, tuple):
                    name = [
                     name]
                if isinstance(name, list):
                    for props in name:
                        field_name, prop = props
                        if field_name not in names:
                            model_strategy.fields.append(props)
                            names[field_name] = prop
                        else:
                            raise ValueError("Cannot add field.  '%s' already exists" % name)

                elif name not in names:
                    fields = self.model._restler_property_map().keys()
                    if name in fields or isinstance(getattr(self.model, name, None), property) or callable(getattr(self.model, name, None)) or getattr(getattr(self.model, name, None), '__class__', None) in self.model._restler_types():
                        model_strategy.fields.append(name)
                        names[name] = name
                    else:
                        raise ValueError("Cannot add field.  '%s' is not a valid field for model '%s'" % (name, self.model))
                else:
                    raise ValueError("Cannot add field.  '%s' already exists" % (name,))

        else:
            raise ValueError('Only lists/tuples or fields can be added')
        return model_strategy

    def __remove(self, fields):
        m = ModelStrategy(self.model, output_name=self.name) + self.fields
        names = self.__name_map()
        if isinstance(fields, (tuple, list)):
            for field in fields:
                if isinstance(field, dict):
                    field, _ = field.items()[0]
                if isinstance(field, tuple):
                    field, _ = field
                if field in names:
                    if callable(names[field]):
                        m.fields.remove((field, names[field]))
                    else:
                        m.fields.remove(names[field])
                else:
                    raise ValueError("'%s' cannot be removed. It is not in the current fields list (%s)" % (field, self.fields))

        else:
            raise ValueError('Fields must be a tuple or list.')
        return m

    def to_dict(self):
        if self.name is not None:
            return {self.model: {self.name: self.fields}}
        else:
            return {self.model: self.fields}

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return SerializationStrategy(self) + other
        if isinstance(other, SerializationStrategy):
            return other + self
        if isinstance(other, (list, tuple, basestring)):
            return self.__add(other)
        raise ValueError('Cannot add type %s' % type(other))

    def include(self, *args, **kwargs):
        """ Include fields for serialization

        :param args: one of more field names (strings) to include
        :param kwargs: renamed properties in the format ``new_name="property_name"``
            *or* derived properties in the format ``property_name=callable``
        :return: a new instance of a ModelStrategy
        """
        if len(kwargs):
            return self.__add__(args + (kwargs,))
        return self.__add__(args)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            raise ValueError('Cannot subtract type %s' % type(other))
        else:
            if isinstance(other, SerializationStrategy):
                return other - self
            if isinstance(other, (list, tuple, basestring)):
                return self.__remove(other)
            raise ValueError('Cannot add type %s' % type(other))

    def exclude(self, *args):
        """ Exclude fields for serialization

        :param args: one or more field names (strings) to exclude in the
            format ``"field1", "field2",...``
        :return: a new instance of a ``ModelStrategy``
        """
        return self.__sub__(args)

    def __lshift__(self, other):
        """ Shorthand for overriding fields with new behavior
            i.e. remove the fields and add back in with new mappings"""
        if not isinstance(other, (list, tuple, basestring)):
            raise ValueError('Cannot add type %s' % type(other))
        return self.__remove(other).__add(other)

    def override(self, **kwargs):
        """
        Change a previously exposed property either by renaming it or delegating it to a callable.

        :param kwargs: properties to override either by renaming it with the format
            ``new_name="property_name"`` *or* derived properties in the ``format property_name=callable``
        :return: a new instance of a ModelStrategy
        """
        return self.__lshift__(kwargs.items())

    def __repr__(self):
        return pprint.pformat(self.to_dict())


def encoder_builder(type_, strategy=None, style=None, context={}):
    encoders = {}
    for strat in strategy:
        if hasattr(strat, '_restler_types'):
            encoders.update(strat._restler_types())

    def default_impl(obj):
        if strategy:
            if obj is not None:
                if obj.__class__ in encoders:
                    return encoders[obj.__class__](obj)
        if isinstance(obj, datetime.datetime):
            d = datetime_safe.new_datetime(obj)
            return d.strftime('%s %s' % (DATE_FORMAT, TIME_FORMAT))
        else:
            if isinstance(obj, datetime.date):
                d = datetime_safe.new_date(obj)
                return d.strftime(DATE_FORMAT)
            if isinstance(obj, datetime.time):
                return obj.strftime(TIME_FORMAT)
            if isinstance(obj, decimal.Decimal):
                return str(obj)
            ret = {}
            if hasattr(obj, '_restler_serialization_name') or isinstance(obj, models.TransientModel):
                model = {}
                kind = obj._restler_serialization_name()
                if strategy is None:
                    fields = obj._restler_property_map().keys()
                else:
                    fields = strategy.get(obj.__class__, None)
                    if fields is None:
                        fields = obj._restler_property_map().keys()
                    elif isinstance(fields, dict):
                        if len(fields.keys()) != 1:
                            raise ValueError('fields must an instance dict(<model name>=<field list>)')
                        kind, fields = fields.items()[0]
                        if callable(kind):
                            kind = kind(obj)
                    if type_ == 'json' and bool(style['json']['flatten']):
                        model = ret
                    else:
                        ret[unicode(kind)] = model
                    if not isinstance(fields, (tuple, list)):
                        fields = [
                         fields]
                    target = None
                    for field_name in fields:
                        if isinstance(field_name, tuple):
                            field_name, target = field_name
                        if callable(target):
                            if hasattr(target, 'func_code') and target.func_code.co_argcount == 2:
                                warnings.warn('Callable should be called with the following three arguments: instance, field_name, context', DeprecationWarning)
                                model[field_name] = target(obj, context)
                            elif hasattr(target, 'func_code') and target.func_code.co_argcount == 3:
                                model[field_name] = target(obj, field_name, context)
                            else:
                                warnings.warn('Callable should be called with the following three arguments: instance, field_name, context', DeprecationWarning)
                                model[field_name] = target(obj)
                            if isinstance(model[field_name], SkipField):
                                del model[field_name]
                        else:
                            field_name_type = obj._restler_property_map().get(target or field_name, None)
                            field_callable = obj._restler_types().get(field_name_type, None)
                            if target and not hasattr(obj, target):
                                raise ValueError("'%s' was not found " % target)
                            if field_callable:
                                model[field_name] = field_callable(getattr(obj, target or field_name))
                            else:
                                model[field_name] = getattr(obj, target or field_name)

            return ret

    if type_ == 'json':

        class AEEncoder(json.JSONEncoder):

            def default(self, obj):
                return default_impl(obj)

        return AEEncoder
    if type_ == 'xml':
        return default_impl
    raise ValueError("type is required to be 'xml' or 'json'")


def to_json(thing, strategy=None, context={}):
    """Encode a ``db.Model`` instance or collection to a JSON string.

    :param thing: a collection, iterable, ``db.Query`` or ``db.Model`` instance
    :param strategy: a ``ModelStrategy`` or ``SerializationStrategy``
    :param context: an object that will be passed to every derived property (``callable``)
     that has a second parameter defined (the param is the model instance).
    :return: a JSON encoded string
    """
    if not isinstance(strategy, (ModelStrategy, SerializationStrategy, types.NoneType)):
        raise ValueError('Serialization strategy must be a ModelStrategy, SerializationStrategy or dict')
    if isinstance(strategy, ModelStrategy):
        strategy = SerializationStrategy(strategy)
    if strategy is None:
        strategy = SerializationStrategy()
    mappings = strategy.mappings
    style = strategy.style
    encoder = encoder_builder('json', mappings, style, context)
    return json.dumps(thing, cls=encoder, indent=style['json']['indent'])


def _encode_xml(thing, node, strategy, style, context):
    xml_style = style['xml']
    encoder = encoder_builder('xml', strategy, style, context)
    simple_types = (
     bool, basestring, int, long, float, decimal.Decimal)
    collection_types = (list, dict)
    if isinstance(thing, dict):
        el = xml_style['dict'](node, thing)
        if el is None:
            el = node
        for key, value in thing.items():
            if not isinstance(key, basestring):
                raise ValueError('key is not a valid string')
            e = ET.SubElement(el, key)
            if value is None:
                xml_style['null'](e, None)
            elif not isinstance(value, simple_types):
                if isinstance(value, collection_types):
                    _encode_xml(value, e, strategy, style, context)
                else:
                    _encode_xml(encoder(value), e, strategy, style, context)
            else:
                e.text = unicode(value)

        return
    if isinstance(thing, list):
        el = xml_style['list'](node, thing)
        if el is None:
            el = node
        for value in thing:
            if hasattr(value, '_restler_serialization_name'):
                _encode_xml(encoder(value), el, strategy, style, context)
                continue
            i = xml_style['list_item'](el, value)
            if not isinstance(value, simple_types):
                if isinstance(value, collection_types):
                    _encode_xml(value, i, strategy, style, context)
                else:
                    _encode_xml(encoder(value), i, strategy, style, context)
            else:
                i.text = unicode(value)
            if value is None:
                xml_style['null'](i, None)

        return
    if isinstance(thing, simple_types):
        node.text = unicode(thing)
    elif thing is None:
        xml_style['null'](node, None)
    else:
        _encode_xml(encoder(thing), node, strategy, style, context)
    return


def to_xml(thing, strategy=None, context={}):
    """Encode a ``db.Model`` instance or collection to an XML string.

    :param thing: a collection, iterable, ``db.Query`` or ``db.Model`` instance
    :param strategy: a ``ModelStrategy`` or ``SerializationStrategy``
    :param context: an object that will be passed to every derived property (``callable``)
     that has a second parameter defined (the param is the model instance).
    :return: a XML encoded string
    """
    if not isinstance(strategy, (ModelStrategy, SerializationStrategy, types.NoneType)):
        raise ValueError('Serialization strategy must be a ModelStrategy, SerializationStrategy or dict')
    if isinstance(strategy, ModelStrategy):
        strategy = SerializationStrategy(strategy)
    if strategy is None:
        strategy = SerializationStrategy()
    style = strategy.style
    mappings = strategy.mappings
    root = style['xml']['root'](thing)
    _encode_xml(thing, root, mappings, style, context)
    return ET.tostring(root)