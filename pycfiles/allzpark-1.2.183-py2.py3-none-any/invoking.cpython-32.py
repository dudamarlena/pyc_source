# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/impl/processor/invoking.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jun 30, 2011\n\n@package: ally core\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the invoking handler.\n'
from ally.api.config import GET, INSERT, UPDATE, DELETE
from ally.api.operator.type import TypeModelProperty
from ally.api.type import Input
from ally.core.spec.codes import INPUT_ERROR, INSERT_ERROR, INSERT_SUCCESS, UPDATE_SUCCESS, UPDATE_ERROR, DELETE_SUCCESS, DELETE_ERROR
from ally.core.spec.resources import Invoker
from ally.core.spec.transform.render import Object, List, Value
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed
from ally.exception import DevelError, InputError, Ref
import logging
log = logging.getLogger(__name__)

class Request(Context):
    """
    The request context.
    """
    invoker = requires(Invoker)
    arguments = requires(dict)


class Response(Context):
    """
    The response context.
    """
    code = defines(str)
    isSuccess = defines(bool)
    errorDetails = defines(Object)
    obj = defines(object, doc='\n    @rtype: object\n    The response object.\n    ')


class InvokingHandler(HandlerProcessorProceed):
    """
    Implementation for a processor that makes the actual call to the request method corresponding invoke. The invoking will
    use all the obtained arguments from the previous processors and perform specific actions based on the requested method.
    In GET case it will provide to the request the invoke returned object as to be rendered to the response, in DELETE case
    it will stop the execution chain and send as a response a success code.
    """

    def __init__(self):
        """
        Construct the handler.
        """
        super().__init__()
        self.invokeCallBack = {GET: self.afterGet, 
         INSERT: self.afterInsert, 
         UPDATE: self.afterUpdate, 
         DELETE: self.afterDelete}

    def process(self, request: Request, response: Response, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Invoke the request invoker.
        """
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        if response.isSuccess is False:
            return
        else:
            assert isinstance(request.invoker, Invoker), 'Invalid invoker %s' % request.invoker
            callBack = self.invokeCallBack.get(request.invoker.method)
            assert callBack is not None, "Method cannot be processed for invoker '%s', something is wrong in the setups" % request.invoker.name
            assert isinstance(request.arguments, dict), 'Invalid arguments %s' % request.arguments
            arguments = []
            for inp in request.invoker.inputs:
                assert isinstance(inp, Input), 'Invalid input %s' % inp
                if inp.name in request.arguments:
                    arguments.append(request.arguments[inp.name])
                elif inp.hasDefault:
                    arguments.append(inp.default)
                else:
                    raise DevelError("No value for mandatory input '%s' for invoker '%s'" % (inp.name, request.invoker.name))

            try:
                value = request.invoker.invoke(*arguments)
                if not log.debug("Successful on calling invoker '%s' with values %s", request.invoker, tuple(arguments)):
                    assert True
                callBack(request.invoker, value, response)
            except InputError as e:
                assert isinstance(e, InputError)
                response.code, response.isSuccess = INPUT_ERROR
                response.errorDetails = self.processInputError(e)
                if not log.debug('User input exception: %s', e, exc_info=True):
                    assert True

            return

    def processInputError(self, e):
        """
        Process the input error into an error object.
        
        @return: Object
            The object containing the details of the input error.
        """
        assert isinstance(e, InputError), 'Invalid input error %s' % e
        messages, names, models, properties = ([], [], {}, {})
        for msg in e.message:
            assert isinstance(msg, Ref)
            if not msg.model:
                messages.append(Value('message', msg.message))
            elif not msg.property:
                messagesModel = models.get(msg.model)
                if not messagesModel:
                    messagesModel = models[msg.model] = []
                messagesModel.append(Value('message', msg.message))
                if msg.model not in names:
                    names.append(msg.model)
            else:
                propertiesModel = properties.get(msg.model)
                if not propertiesModel:
                    propertiesModel = properties[msg.model] = []
                propertiesModel.append(Value(msg.property, msg.message))
                if msg.model not in names:
                    names.append(msg.model)
                    continue

        errors = []
        if messages:
            errors.append(List('error', *messages))
        for name in names:
            messagesModel, propertiesModel = models.get(name), properties.get(name)
            props = []
            if messagesModel:
                props.append(List('error', *messagesModel))
            if propertiesModel:
                props.extend(propertiesModel)
            errors.append(Object(name, *props))

        return Object('model', *errors)

    def afterGet(self, invoker, value, response):
        """
        Process the after get action on the value.
        
        @param invoker: Invoker
            The invoker used.
        @param value: object
            The value returned.
        @param response: Response
            The response to set the error if is the case.
        @return: boolean
            False if the invoking has failed, True for success.
        """
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert invoker.output.isValid(value), "Invalid return value '%s' for invoker %s" % (value, invoker)
        response.obj = value

    def afterInsert(self, invoker, value, response):
        """
        Process the after insert action on the value.
        
        @param invoker: Invoker
            The invoker used.
        @param value: object
            The value returned.
        @param response: Response
            The response to set the error if is the case.
        @return: boolean
            False if the invoking has failed, True for success.
        """
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert invoker.output.isValid(value), "Invalid return value '%s' for invoker %s" % (value, invoker)
        if isinstance(invoker.output, TypeModelProperty) and invoker.output.container.propertyId == invoker.output.property:
            if value is not None:
                response.obj = value
        else:
            response.code, response.isSuccess = INSERT_ERROR
            if not log.debug('Cannot insert resource'):
                assert True
                return
            else:
                response.obj = value
            response.code, response.isSuccess = INSERT_SUCCESS
            return

    def afterUpdate(self, invoker, value, response):
        """
        Process the after update action on the value.
        
        @param invoker: Invoker
            The invoker used.
        @param value: object
            The value returned.
        @param response: Response
            The response to set the error if is the case.
        @return: boolean
            False if the invoking has failed, True for success.
        """
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert invoker.output.isValid(value), "Invalid return value '%s' for invoker %s" % (value, invoker)
        if invoker.output.isOf(None):
            response.code, response.isSuccess = UPDATE_SUCCESS
            if not log.debug('Successful updated resource'):
                assert True
        elif invoker.output.isOf(bool):
            pass
        if value == True:
            response.code, response.isSuccess = UPDATE_SUCCESS
            if not log.debug('Successful updated resource'):
                if not True:
                    raise AssertionError
        else:
            response.code, response.isSuccess = UPDATE_ERROR
            if not log.debug('Cannot update resource'):
                assert True
            else:
                response.code, response.isSuccess = UPDATE_SUCCESS
                response.obj = value
            return

    def afterDelete(self, invoker, value, response):
        """
        Process the after delete action on the value.
        
        @param invoker: Invoker
            The invoker used.
        @param value: object
            The value returned.
        @param response: Response
            The response to set the error if is the case.
        @return: boolean
            False if the invoking has failed, True for success.
        """
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        assert isinstance(response, Response), 'Invalid response %s' % response
        assert invoker.output.isValid(value), "Invalid return value '%s' for invoker %s" % (value, invoker)
        if invoker.output.isOf(bool):
            if value == True:
                response.code, response.isSuccess = DELETE_SUCCESS
                if not log.debug('Successfully deleted resource'):
                    if not True:
                        raise AssertionError
        else:
            response.code, response.isSuccess = DELETE_ERROR
            if not log.debug('Cannot deleted resource'):
                assert True
            else:
                response.code, response.isSuccess = DELETE_SUCCESS
                response.obj = value