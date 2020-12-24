# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/model/adapter/protorpc.py
# Compiled at: 2014-10-03 07:13:34
__doc__ = '\n\n  protorpc model extensions\n  ~~~~~~~~~~~~~~~~~~~~~~~~~\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
import datetime
from .abstract import KeyMixin
from .abstract import ModelMixin
from canteen.util import struct as datastructures
try:
    protorpc = __import__('protorpc', tuple(), tuple(), [], 0)
except ImportError as e:
    _PROTORPC, _root_message_class = False, object
else:
    _p = __import__('protorpc', [], [], ['messages', 'message_types'], 0)
    pmessages = getattr(_p, 'messages')
    pmessage_types = getattr(_p, 'message_types')
    _model_impl = {}
    _field_kwarg = 'field'
    _PROTORPC, _root_message_class = True, pmessages.Message
    _field_basetype_map = {int: pmessages.IntegerField, 
       long: pmessages.IntegerField, 
       bool: pmessages.BooleanField, 
       float: pmessages.FloatField, 
       str: pmessages.StringField, 
       unicode: pmessages.StringField, 
       basestring: pmessages.StringField, 
       datetime.time: pmessages.StringField, 
       datetime.date: pmessages.StringField, 
       datetime.datetime: pmessages.StringField}
    _builtin_basetypes = frozenset(_field_basetype_map.keys())
    _field_explicit_map = {pmessages.EnumField.__name__: pmessages.EnumField, 
       pmessages.BytesField.__name__: pmessages.BytesField, 
       pmessages.FloatField.__name__: pmessages.FloatField, 
       pmessages.StringField.__name__: pmessages.StringField, 
       pmessages.IntegerField.__name__: pmessages.IntegerField, 
       pmessages.BooleanField.__name__: pmessages.BooleanField}
    _builtin_fields = frozenset(_field_explicit_map.keys())

    def build_message(_model):
        """ Recursively builds a new `Message` class dynamically from a canteen
        :py:class:`model.Model`. Properties are converted to their
        :py:mod:`protorpc` equivalents and factoried into a full
        :py:class:`messages.Message` class.

        :param _model: Model class to convert to a
          :py:class:`protorpc.messages.Message` class.

        :raises TypeError: In the case of an unidentified or unknown
          property basetype.
        :raises ValueError: In the case of a missing implementation field
          or serialization error.

        :returns: Constructed (but not instantiated)
          :py:class:`protorpc.messages.Message` class. """
        from canteen import rpc
        from canteen import model
        _field_i, _model_message = 1, {'__module__': _model.__module__}
        lookup, property_map = _model.__lookup__, {}
        _model_message['key'] = pmessages.MessageField(rpc.Key, _field_i)
        for name in lookup:
            _pargs, _pkwargs = [], {}
            prop = property_map[name] = _model.__dict__[name]
            if prop.default != prop.sentinel:
                _pkwargs['default'] = prop.default
            _pkwargs['required'], _pkwargs['repeated'] = prop.required, prop.repeated
            if _field_kwarg in prop.options:
                explicit = prop.options.get(_field_kwarg, datastructures.EMPTY)
                if explicit is False or explicit is None:
                    continue
                if not isinstance(explicit, (basestring, tuple)):
                    context = (
                     name, _model.kind(), type(explicit))
                    raise TypeError('Invalid type found for explicit message field implementation binding - property "%s" of model "%s" cannot bind to field of type "%s". A basestring field name or tuple of (name, *args, <**kwargs>) was expected.' % context)
                elif isinstance(explicit, tuple):
                    if len(explicit) == 2:
                        explicit, _pargs = explicit
                        _pkwargs = {}
                    elif len(explicit) == 3:
                        explicit, _pargs, _pkwargs = explicit
                if explicit in _builtin_fields:
                    if len(_pargs) > 0:
                        if not isinstance(_pargs, list):
                            _pargs = [ i for i in _pargs ]
                        _field_i += 1
                        _pargs.append(_field_i)
                        _pargs = tuple(_pargs)
                    else:
                        _field_i += 1
                        _pargs = (_field_i,)
                    _model_message[name] = _field_explicit_map[explicit](*_pargs, **_pkwargs)
                    continue
                else:
                    raise ValueError('No such message implementation field: "%s".' % name)
            if prop.basetype == dict:
                _field_i += 1
                _model_message[name] = rpc.VariantField(_field_i)
                continue
            elif isinstance(prop.basetype, type(type)) and issubclass(prop.basetype, model.AbstractModel):
                if prop.basetype is model.Model:
                    _field_i += 1
                    _model_message[name] = rpc.VariantField(_field_i)
                    continue
                _field_i += 1
                _pargs.append(prop.basetype.to_message_model())
                _pargs.append(_field_i)
                _model_message[name] = pmessages.MessageField(*_pargs, **_pkwargs)
                continue
            elif isinstance(prop.basetype, tuple) and prop.basetype in ((int, str), (str, int)):
                _field_i += 1
                _pargs.append(_field_i)
                _model_message[name] = rpc.StringOrIntegerField(*_pargs, **_pkwargs)
                continue
            elif issubclass(prop.basetype, model.AbstractKey):
                _field_i += 1
                _pargs.append(rpc.Key)
                _pargs.append(_field_i)
                _model_message[name] = pmessages.MessageField(*_pargs)
                continue
            elif issubclass(prop.basetype, datastructures.BidirectionalEnum):
                _field_i += 1
                _enum = pmessages.Enum.__metaclass__.__new__(*(
                 pmessages.Enum.__metaclass__,
                 prop.basetype.__name__,
                 (
                  pmessages.Enum,), {k:v for k, v in prop.basetype}))
                _pargs.append(_enum)
                _pargs.append(_field_i)
                if prop.default not in (
                 model.Property.sentinel, None):
                    _pkwargs['default'] = prop.basetype.reverse_resolve(prop.default)
                _model_message[name] = pmessages.EnumField(*_pargs, **_pkwargs)
                continue
            elif prop.basetype in _builtin_basetypes:
                _field_i += 1
                _pargs.append(_field_i)
                if 'default' in _pkwargs and prop.basetype in (
                 datetime.datetime, datetime.date):
                    del _pkwargs['default']
                _model_message[name] = _field_basetype_map[prop.basetype](*_pargs, **_pkwargs)
                continue
            elif hasattr(prop.basetype, '__message__'):
                _field_i += 1
                _pargs.append(_field_i)
                _model_message[name] = prop.basetype.__message__(*_pargs, **_pkwargs)
                continue
            else:
                context = (
                 name, _model.kind(), prop.basetype)
                raise ValueError('Could not resolve proper serialization for property "%s" of model "%s" (found basetype "%s").' % context)

        return type(_model.kind(), (pmessages.Message,), _model_message)


    class ProtoRPCKey(KeyMixin):
        """ Adapt `Key` classes to ProtoRPC messages. """

        def to_message(self, flat=False, encoded=False):
            """ Convert a `Key` instance to a ProtoRPC `Message` instance.

          :returns: Constructed :py:class:`protorpc.Key` message object. """
            from canteen import rpc
            args = {'id': self.id, 
               'kind': self.kind, 
               'encoded': self.urlsafe()}
            if self.parent:
                if encoded:
                    return rpc.Key(**args)
                args['parent'] = self.parent.to_message(not flat, flat)
            return rpc.Key(**args)

        @classmethod
        def to_message_model(cls):
            """ Return a schema for a `Key` instance in ProtoRPC `Message` form.

          :returns: Vanilla :py:class:`protorpc.Key` class. """
            from canteen import rpc
            return rpc.Key

        @classmethod
        def from_message(cls, key_message):
            """  """
            parent = cls.from_message(key_message.parent) if key_message.parent else None
            return cls(key_message.kind, key_message.id, parent=parent)


    class ProtoRPCModel(ModelMixin):
        """ Adapt Model classes to ProtoRPC messages. """

        def to_message(self, *args, **kwargs):
            """ Convert a `Model` instance to a ProtoRPC `Message` class.

          :param args: Positional arguments to pass to
            :py:meth:`Model.to_dict`.

          :param kwargs: Keyword arguments to pass to
            :py:meth:`Model.to_dict`.

          :returns: Constructed and initialized :py:class:`protorpc.Message`
            object. """
            from canteen import rpc
            from canteen import model
            values = {}
            for prop, value in self.to_dict(convert_keys=False, *args, **kwargs).items():
                if isinstance(value, (model.Key, model.VertexKey, model.EdgeKey)):
                    values[prop] = rpc.Key(id=value.id, kind=value.kind, encoded=value.urlsafe())
                    continue
                if isinstance(value, (datetime.date, datetime.time, datetime.datetime)):
                    values[prop] = value.isoformat()
                    continue
                values[prop] = value

            if self.key:
                return self.__class__.to_message_model()(key=self.key.to_message(), **values)

            def _check_value(item):
                """ Checks for invalid ProtoRPC values. """
                key, value = item
                if isinstance(value, list) and len(value) == 0:
                    return False
                return True

            filtered = filter(_check_value, values.iteritems())
            return self.__class__.to_message_model()(**dict(filtered))

        @classmethod
        def to_message_model(cls):
            """ Convert a `Model` class to a ProtoRPC `Message` class. Delegates
          to :py:func:`build_message`, see docs there for exceptions raised
          (:py:exc:`TypeError` and :py:exc:`ValueError`).

          :returns: Constructed (but not initialized) dynamically-build
            :py:class:`message.Message` class corresponding to
            the current model (``cls``). """
            global _model_impl
            if (
             cls, cls.__lookup__) not in _model_impl:
                _model_impl[(cls, cls.__lookup__)] = build_message(cls)
            return _model_impl[(cls, cls.__lookup__)]

        @classmethod
        def from_message(cls, message):
            """ DOCSTRING """
            key = cls.__keyclass__.from_message(message.key) if hasattr(message, 'key') and message.key is not None else None
            model = cls(key=key) if key else cls()
            for field, value in ((k.name, message.get_assigned_value(k.name)) for k in message.all_fields()):
                if field is not 'key':
                    model[field] = value

            return model