# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/service/object.py
# Compiled at: 2020-01-29 15:49:52
from ..debugging import bacpypes_debugging, ModuleLogger
from ..capability import Capability
from ..basetypes import ErrorType, PropertyIdentifier
from ..primitivedata import Atomic, Null, Unsigned
from ..constructeddata import Any, Array, ArrayOf, List
from ..apdu import SimpleAckPDU, ReadPropertyACK, ReadPropertyMultipleACK, ReadAccessResult, ReadAccessResultElement, ReadAccessResultElementChoice
from ..errors import ExecutionError
from ..object import PropertyError
_debug = 0
_log = ModuleLogger(globals())
ArrayOfPropertyIdentifier = ArrayOf(PropertyIdentifier)

@bacpypes_debugging
class ReadWritePropertyServices(Capability):

    def __init__(self):
        if _debug:
            ReadWritePropertyServices._debug('__init__')
        Capability.__init__(self)

    def do_ReadPropertyRequest(self, apdu):
        """Return the value of some property of one of our objects."""
        if _debug:
            ReadWritePropertyServices._debug('do_ReadPropertyRequest %r', apdu)
        objId = apdu.objectIdentifier
        if objId == ('device', 4194303) and self.localDevice is not None:
            if _debug:
                ReadWritePropertyServices._debug('    - wildcard device identifier')
            objId = self.localDevice.objectIdentifier
        obj = self.get_object_id(objId)
        if _debug:
            ReadWritePropertyServices._debug('    - object: %r', obj)
        if not obj:
            raise ExecutionError(errorClass='object', errorCode='unknownObject')
        try:
            datatype = obj.get_datatype(apdu.propertyIdentifier)
            if _debug:
                ReadWritePropertyServices._debug('    - datatype: %r', datatype)
            value = obj.ReadProperty(apdu.propertyIdentifier, apdu.propertyArrayIndex)
            if _debug:
                ReadWritePropertyServices._debug('    - value: %r', value)
            if value is None:
                raise PropertyError(apdu.propertyIdentifier)
            if issubclass(datatype, Atomic):
                value = datatype(value)
            elif issubclass(datatype, Array) and apdu.propertyArrayIndex is not None:
                if apdu.propertyArrayIndex == 0:
                    value = Unsigned(value)
                elif issubclass(datatype.subtype, Atomic):
                    value = datatype.subtype(value)
                elif not isinstance(value, datatype.subtype):
                    raise TypeError(('invalid result datatype, expecting {0} and got {1}').format(datatype.subtype.__name__, type(value).__name__))
            elif issubclass(datatype, List):
                value = datatype(value)
            elif not isinstance(value, datatype):
                raise TypeError(('invalid result datatype, expecting {0} and got {1}').format(datatype.__name__, type(value).__name__))
            if _debug:
                ReadWritePropertyServices._debug('    - encodeable value: %r', value)
            resp = ReadPropertyACK(context=apdu)
            resp.objectIdentifier = objId
            resp.propertyIdentifier = apdu.propertyIdentifier
            resp.propertyArrayIndex = apdu.propertyArrayIndex
            resp.propertyValue = Any()
            resp.propertyValue.cast_in(value)
            if _debug:
                ReadWritePropertyServices._debug('    - resp: %r', resp)
        except PropertyError:
            raise ExecutionError(errorClass='property', errorCode='unknownProperty')

        self.response(resp)
        return

    def do_WritePropertyRequest(self, apdu):
        """Change the value of some property of one of our objects."""
        if _debug:
            ReadWritePropertyServices._debug('do_WritePropertyRequest %r', apdu)
        obj = self.get_object_id(apdu.objectIdentifier)
        if _debug:
            ReadWritePropertyServices._debug('    - object: %r', obj)
        if not obj:
            raise ExecutionError(errorClass='object', errorCode='unknownObject')
        try:
            if obj.ReadProperty(apdu.propertyIdentifier, apdu.propertyArrayIndex) is None:
                raise PropertyError(apdu.propertyIdentifier)
            if apdu.propertyValue.is_application_class_null():
                datatype = Null
            else:
                datatype = obj.get_datatype(apdu.propertyIdentifier)
            if _debug:
                ReadWritePropertyServices._debug('    - datatype: %r', datatype)
            if issubclass(datatype, Array) and apdu.propertyArrayIndex is not None:
                if apdu.propertyArrayIndex == 0:
                    value = apdu.propertyValue.cast_out(Unsigned)
                else:
                    value = apdu.propertyValue.cast_out(datatype.subtype)
            else:
                value = apdu.propertyValue.cast_out(datatype)
            if _debug:
                ReadWritePropertyServices._debug('    - value: %r', value)
            value = obj.WriteProperty(apdu.propertyIdentifier, value, apdu.propertyArrayIndex, apdu.priority)
            resp = SimpleAckPDU(context=apdu)
            if _debug:
                ReadWritePropertyServices._debug('    - resp: %r', resp)
        except PropertyError:
            raise ExecutionError(errorClass='property', errorCode='unknownProperty')

        self.response(resp)
        return


@bacpypes_debugging
def read_property_to_any(obj, propertyIdentifier, propertyArrayIndex=None):
    """Read the specified property of the object, with the optional array index,
    and cast the result into an Any object."""
    if _debug:
        read_property_to_any._debug('read_property_to_any %s %r %r', obj, propertyIdentifier, propertyArrayIndex)
    datatype = obj.get_datatype(propertyIdentifier)
    if _debug:
        read_property_to_any._debug('    - datatype: %r', datatype)
    if datatype is None:
        raise ExecutionError(errorClass='property', errorCode='datatypeNotSupported')
    value = obj.ReadProperty(propertyIdentifier, propertyArrayIndex)
    if _debug:
        read_property_to_any._debug('    - value: %r', value)
    if value is None:
        raise ExecutionError(errorClass='property', errorCode='unknownProperty')
    if issubclass(datatype, Atomic):
        value = datatype(value)
    elif issubclass(datatype, Array) and propertyArrayIndex is not None:
        if propertyArrayIndex == 0:
            value = Unsigned(value)
        elif issubclass(datatype.subtype, Atomic):
            value = datatype.subtype(value)
        elif not isinstance(value, datatype.subtype):
            raise TypeError('invalid result datatype, expecting %s and got %s' % (
             datatype.subtype.__name__, type(value).__name__))
    elif not isinstance(value, datatype):
        raise TypeError('invalid result datatype, expecting %s and got %s' % (
         datatype.__name__, type(value).__name__))
    if _debug:
        read_property_to_any._debug('    - encodeable value: %r', value)
    result = Any()
    result.cast_in(value)
    if _debug:
        read_property_to_any._debug('    - result: %r', result)
    return result


@bacpypes_debugging
def read_property_to_result_element(obj, propertyIdentifier, propertyArrayIndex=None):
    """Read the specified property of the object, with the optional array index,
    and cast the result into an Any object."""
    if _debug:
        read_property_to_result_element._debug('read_property_to_result_element %s %r %r', obj, propertyIdentifier, propertyArrayIndex)
    read_result = ReadAccessResultElementChoice()
    try:
        if not obj:
            raise ExecutionError(errorClass='object', errorCode='unknownObject')
        read_result.propertyValue = read_property_to_any(obj, propertyIdentifier, propertyArrayIndex)
        if _debug:
            read_property_to_result_element._debug('    - success')
    except PropertyError as error:
        if _debug:
            read_property_to_result_element._debug('    - error: %r', error)
        read_result.propertyAccessError = ErrorType(errorClass='property', errorCode='unknownProperty')
    except ExecutionError as error:
        if _debug:
            read_property_to_result_element._debug('    - error: %r', error)
        read_result.propertyAccessError = ErrorType(errorClass=error.errorClass, errorCode=error.errorCode)

    read_access_result_element = ReadAccessResultElement(propertyIdentifier=propertyIdentifier, propertyArrayIndex=propertyArrayIndex, readResult=read_result)
    if _debug:
        read_property_to_result_element._debug('    - read_access_result_element: %r', read_access_result_element)
    return read_access_result_element


@bacpypes_debugging
class ReadWritePropertyMultipleServices(Capability):

    def __init__(self):
        if _debug:
            ReadWritePropertyMultipleServices._debug('__init__')
        Capability.__init__(self)

    def do_ReadPropertyMultipleRequest(self, apdu):
        """Respond to a ReadPropertyMultiple Request."""
        if _debug:
            ReadWritePropertyMultipleServices._debug('do_ReadPropertyMultipleRequest %r', apdu)
        resp = None
        read_access_result_list = []
        for read_access_spec in apdu.listOfReadAccessSpecs:
            objectIdentifier = read_access_spec.objectIdentifier
            if _debug:
                ReadWritePropertyMultipleServices._debug('    - objectIdentifier: %r', objectIdentifier)
            if objectIdentifier == ('device', 4194303) and self.localDevice is not None:
                if _debug:
                    ReadWritePropertyMultipleServices._debug('    - wildcard device identifier')
                objectIdentifier = self.localDevice.objectIdentifier
            obj = self.get_object_id(objectIdentifier)
            if _debug:
                ReadWritePropertyMultipleServices._debug('    - object: %r', obj)
            read_access_result_element_list = []
            for prop_reference in read_access_spec.listOfPropertyReferences:
                propertyIdentifier = prop_reference.propertyIdentifier
                if _debug:
                    ReadWritePropertyMultipleServices._debug('    - propertyIdentifier: %r', propertyIdentifier)
                propertyArrayIndex = prop_reference.propertyArrayIndex
                if _debug:
                    ReadWritePropertyMultipleServices._debug('    - propertyArrayIndex: %r', propertyArrayIndex)
                if propertyIdentifier in ('all', 'required', 'optional'):
                    if not obj:
                        read_result = ReadAccessResultElementChoice()
                        read_result.propertyAccessError = ErrorType(errorClass='object', errorCode='unknownObject')
                        read_access_result_element = ReadAccessResultElement(propertyIdentifier=propertyIdentifier, propertyArrayIndex=propertyArrayIndex, readResult=read_result)
                        read_access_result_element_list.append(read_access_result_element)
                    else:
                        for propId, prop in obj._properties.items():
                            if _debug:
                                ReadWritePropertyMultipleServices._debug('    - checking: %r %r', propId, prop.optional)
                            if propId == 'propertyList':
                                if _debug:
                                    ReadWritePropertyMultipleServices._debug('    - ignore propertyList')
                                continue
                            if propertyIdentifier == 'all':
                                pass
                            elif propertyIdentifier == 'required' and prop.optional:
                                if _debug:
                                    ReadWritePropertyMultipleServices._debug('    - not a required property')
                                continue
                            elif propertyIdentifier == 'optional' and not prop.optional:
                                if _debug:
                                    ReadWritePropertyMultipleServices._debug('    - not an optional property')
                                continue
                            read_access_result_element = read_property_to_result_element(obj, propId, propertyArrayIndex)
                            if read_access_result_element.readResult.propertyAccessError and read_access_result_element.readResult.propertyAccessError.errorCode == 'unknownProperty':
                                continue
                            read_access_result_element_list.append(read_access_result_element)

                else:
                    read_access_result_element = read_property_to_result_element(obj, propertyIdentifier, propertyArrayIndex)
                    read_access_result_element_list.append(read_access_result_element)

            read_access_result = ReadAccessResult(objectIdentifier=objectIdentifier, listOfResults=read_access_result_element_list)
            if _debug:
                ReadWritePropertyMultipleServices._debug('    - read_access_result: %r', read_access_result)
            read_access_result_list.append(read_access_result)

        if not resp:
            resp = ReadPropertyMultipleACK(context=apdu)
            resp.listOfReadAccessResults = read_access_result_list
            if _debug:
                ReadWritePropertyMultipleServices._debug('    - resp: %r', resp)
        self.response(resp)
        return