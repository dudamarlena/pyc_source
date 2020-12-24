# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/service_reflection.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 11577 bytes
"""Contains metaclasses used to create protocol service and service stub
classes from ServiceDescriptor objects at runtime.

The GeneratedServiceType and GeneratedServiceStubType metaclasses are used to
inject all useful functionality into the classes output by the protocol
compiler at compile-time.
"""
__author__ = 'petar@google.com (Petar Petrov)'
from google.protobuf.internal import api_implementation
if api_implementation.Type() == 'cpp':
    from google.protobuf.pyext import _message

class GeneratedServiceType(type):
    __doc__ = 'Metaclass for service classes created at runtime from ServiceDescriptors.\n\n  Implementations for all methods described in the Service class are added here\n  by this class. We also create properties to allow getting/setting all fields\n  in the protocol message.\n\n  The protocol compiler currently uses this metaclass to create protocol service\n  classes at runtime. Clients can also manually create their own classes at\n  runtime, as in this example:\n\n  mydescriptor = ServiceDescriptor(.....)\n  class MyProtoService(service.Service):\n    __metaclass__ = GeneratedServiceType\n    DESCRIPTOR = mydescriptor\n  myservice_instance = MyProtoService()\n  ...\n  '
    _DESCRIPTOR_KEY = 'DESCRIPTOR'

    def __init__(cls, name, bases, dictionary):
        """Creates a message service class.

    Args:
      name: Name of the class (ignored, but required by the metaclass
        protocol).
      bases: Base classes of the class being constructed.
      dictionary: The class dictionary of the class being constructed.
        dictionary[_DESCRIPTOR_KEY] must contain a ServiceDescriptor object
        describing this protocol service type.
    """
        if GeneratedServiceType._DESCRIPTOR_KEY not in dictionary:
            return
        descriptor = dictionary[GeneratedServiceType._DESCRIPTOR_KEY]
        if isinstance(descriptor, str):
            descriptor = _message.default_pool.FindServiceByName(descriptor)
            dictionary[GeneratedServiceType._DESCRIPTOR_KEY] = descriptor
        service_builder = _ServiceBuilder(descriptor)
        service_builder.BuildService(cls)
        cls.DESCRIPTOR = descriptor


class GeneratedServiceStubType(GeneratedServiceType):
    __doc__ = 'Metaclass for service stubs created at runtime from ServiceDescriptors.\n\n  This class has similar responsibilities as GeneratedServiceType, except that\n  it creates the service stub classes.\n  '
    _DESCRIPTOR_KEY = 'DESCRIPTOR'

    def __init__(cls, name, bases, dictionary):
        descriptor = dictionary.get(cls._DESCRIPTOR_KEY)
        if isinstance(descriptor, str):
            descriptor = _message.default_pool.FindServiceByName(descriptor)
            dictionary[GeneratedServiceStubType._DESCRIPTOR_KEY] = descriptor
        super(GeneratedServiceStubType, cls).__init__(name, bases, dictionary)
        if GeneratedServiceStubType._DESCRIPTOR_KEY not in dictionary:
            return
        service_stub_builder = _ServiceStubBuilder(descriptor)
        service_stub_builder.BuildServiceStub(cls)


class _ServiceBuilder(object):
    __doc__ = 'This class constructs a protocol service class using a service descriptor.\n\n  Given a service descriptor, this class constructs a class that represents\n  the specified service descriptor. One service builder instance constructs\n  exactly one service class. That means all instances of that class share the\n  same builder.\n  '

    def __init__(self, service_descriptor):
        """Initializes an instance of the service class builder.

    Args:
      service_descriptor: ServiceDescriptor to use when constructing the
        service class.
    """
        self.descriptor = service_descriptor

    def BuildService(self, cls):
        """Constructs the service class.

    Args:
      cls: The class that will be constructed.
    """

        def _WrapCallMethod(srvc, method_descriptor, rpc_controller, request, callback):
            return self._CallMethod(srvc, method_descriptor, rpc_controller, request, callback)

        self.cls = cls
        cls.CallMethod = _WrapCallMethod
        cls.GetDescriptor = staticmethod(lambda : self.descriptor)
        cls.GetDescriptor.__doc__ = 'Returns the service descriptor.'
        cls.GetRequestClass = self._GetRequestClass
        cls.GetResponseClass = self._GetResponseClass
        for method in self.descriptor.methods:
            setattr(cls, method.name, self._GenerateNonImplementedMethod(method))

    def _CallMethod(self, srvc, method_descriptor, rpc_controller, request, callback):
        """Calls the method described by a given method descriptor.

    Args:
      srvc: Instance of the service for which this method is called.
      method_descriptor: Descriptor that represent the method to call.
      rpc_controller: RPC controller to use for this method's execution.
      request: Request protocol message.
      callback: A callback to invoke after the method has completed.
    """
        if method_descriptor.containing_service != self.descriptor:
            raise RuntimeError('CallMethod() given method descriptor for wrong service type.')
        method = getattr(srvc, method_descriptor.name)
        return method(rpc_controller, request, callback)

    def _GetRequestClass(self, method_descriptor):
        """Returns the class of the request protocol message.

    Args:
      method_descriptor: Descriptor of the method for which to return the
        request protocol message class.

    Returns:
      A class that represents the input protocol message of the specified
      method.
    """
        if method_descriptor.containing_service != self.descriptor:
            raise RuntimeError('GetRequestClass() given method descriptor for wrong service type.')
        return method_descriptor.input_type._concrete_class

    def _GetResponseClass(self, method_descriptor):
        """Returns the class of the response protocol message.

    Args:
      method_descriptor: Descriptor of the method for which to return the
        response protocol message class.

    Returns:
      A class that represents the output protocol message of the specified
      method.
    """
        if method_descriptor.containing_service != self.descriptor:
            raise RuntimeError('GetResponseClass() given method descriptor for wrong service type.')
        return method_descriptor.output_type._concrete_class

    def _GenerateNonImplementedMethod(self, method):
        """Generates and returns a method that can be set for a service methods.

    Args:
      method: Descriptor of the service method for which a method is to be
        generated.

    Returns:
      A method that can be added to the service class.
    """
        return lambda inst, rpc_controller, request, callback: self._NonImplementedMethod(method.name, rpc_controller, callback)

    def _NonImplementedMethod(self, method_name, rpc_controller, callback):
        """The body of all methods in the generated service class.

    Args:
      method_name: Name of the method being executed.
      rpc_controller: RPC controller used to execute this method.
      callback: A callback which will be invoked when the method finishes.
    """
        rpc_controller.SetFailed('Method %s not implemented.' % method_name)
        callback(None)


class _ServiceStubBuilder(object):
    __doc__ = 'Constructs a protocol service stub class using a service descriptor.\n\n  Given a service descriptor, this class constructs a suitable stub class.\n  A stub is just a type-safe wrapper around an RpcChannel which emulates a\n  local implementation of the service.\n\n  One service stub builder instance constructs exactly one class. It means all\n  instances of that class share the same service stub builder.\n  '

    def __init__(self, service_descriptor):
        """Initializes an instance of the service stub class builder.

    Args:
      service_descriptor: ServiceDescriptor to use when constructing the
        stub class.
    """
        self.descriptor = service_descriptor

    def BuildServiceStub(self, cls):
        """Constructs the stub class.

    Args:
      cls: The class that will be constructed.
    """

        def _ServiceStubInit(stub, rpc_channel):
            stub.rpc_channel = rpc_channel

        self.cls = cls
        cls.__init__ = _ServiceStubInit
        for method in self.descriptor.methods:
            setattr(cls, method.name, self._GenerateStubMethod(method))

    def _GenerateStubMethod--- This code section failed: ---

 L. 282         0  LOAD_CONST               (None,)
                2  LOAD_CLOSURE             'method'
                4  LOAD_CLOSURE             'self'
                6  BUILD_TUPLE_2         2 
                8  LOAD_LAMBDA              '<code_object <lambda>>'
               10  LOAD_STR                 '_ServiceStubBuilder._GenerateStubMethod.<locals>.<lambda>'
               12  MAKE_FUNCTION_9          'default, closure'
               14  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def _StubMethod(self, stub, method_descriptor, rpc_controller, request, callback):
        """The body of all service methods in the generated stub class.

    Args:
      stub: Stub instance.
      method_descriptor: Descriptor of the invoked method.
      rpc_controller: Rpc controller to execute the method.
      request: Request protocol message.
      callback: A callback to execute when the method finishes.
    Returns:
      Response message (in case of blocking call).
    """
        return stub.rpc_channel.CallMethod(method_descriptor, rpc_controller, request, method_descriptor.output_type._concrete_class, callback)