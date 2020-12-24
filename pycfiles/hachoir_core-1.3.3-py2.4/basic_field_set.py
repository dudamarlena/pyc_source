# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/field/basic_field_set.py
# Compiled at: 2009-09-07 17:44:28
from hachoir_core.field import Field, FieldError
from hachoir_core.stream import InputStream
from hachoir_core.endian import BIG_ENDIAN, LITTLE_ENDIAN
from hachoir_core.event_handler import EventHandler

class ParserError(FieldError):
    """
    Error raised by a field set.

    @see: L{FieldError}
    """
    __module__ = __name__


class MatchError(FieldError):
    """
    Error raised by a field set when the stream content doesn't
    match to file format.

    @see: L{FieldError}
    """
    __module__ = __name__


class BasicFieldSet(Field):
    __module__ = __name__
    _event_handler = None
    is_field_set = True
    endian = None

    def __init__(self, parent, name, stream, description, size):
        if not not parent:
            assert issubclass(parent.__class__, BasicFieldSet)
            assert issubclass(stream.__class__, InputStream)
            if size is None and self.static_size:
                pass
            else:
                raise isinstance(self.static_size, (int, long)) or AssertionError
            size = self.static_size
        self._parent = parent
        self._name = name
        self._size = size
        self._description = description
        self.stream = stream
        self._field_array_count = {}
        if not self.endian:
            assert parent and parent.endian
            self.endian = parent.endian
        if parent:
            self._address = parent.nextFieldAddress()
            self.root = parent.root
            assert id(self.stream) == id(parent.stream)
        else:
            self._address = 0
            self.root = self
            self._global_event_handler = None
        assert self.endian in (BIG_ENDIAN, LITTLE_ENDIAN)
        if self._size is not None and self._size <= 0:
            raise ParserError("Invalid parser '%s' size: %s" % (self.path, self._size))
        return

    def reset(self):
        self._field_array_count = {}

    def createValue(self):
        return

    def connectEvent(self, event_name, handler, local=True):
        assert event_name in ('field-value-changed', 'field-resized', 'field-inserted',
                              'field-replaced', 'set-field-value'), 'Event name %r is invalid' % event_name
        if local:
            if self._event_handler is None:
                self._event_handler = EventHandler()
            self._event_handler.connect(event_name, handler)
        else:
            if self.root._global_event_handler is None:
                self.root._global_event_handler = EventHandler()
            self.root._global_event_handler.connect(event_name, handler)
        return

    def raiseEvent(self, event_name, *args):
        if self._event_handler is not None:
            self._event_handler.raiseEvent(event_name, *args)
        if self.root._global_event_handler is not None:
            self.root._global_event_handler.raiseEvent(event_name, *args)
        return

    def setUniqueFieldName(self, field):
        key = field._name[:-2]
        try:
            self._field_array_count[key] += 1
        except KeyError:
            self._field_array_count[key] = 0

        field._name = key + '[%u]' % self._field_array_count[key]

    def readFirstFields(self, number):
        """
        Read first number fields if they are not read yet.

        Returns number of new added fields.
        """
        number = number - self.current_length
        if 0 < number:
            return self.readMoreFields(number)
        else:
            return 0

    def createFields(self):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()

    def getField(self, key, const=True):
        raise NotImplementedError()

    def nextFieldAddress(self):
        raise NotImplementedError()

    def getFieldIndex(self, field):
        raise NotImplementedError()

    def readMoreFields(self, number):
        raise NotImplementedError()