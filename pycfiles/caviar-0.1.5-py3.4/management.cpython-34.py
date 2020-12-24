# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caviar/engine/management.py
# Compiled at: 2017-10-25 18:02:55
# Size of source mod 2**32: 11125 bytes
"""
Management module.
"""
import io, caviar, caviar.network

class ManagementError(BaseException):

    def __init__(self, exit_code, message):
        super().__init__(exit_code, message)
        self._ManagementError__exit_code = exit_code
        self._ManagementError__message = message

    @property
    def exit_code(self):
        return self._ManagementError__exit_code

    @property
    def message(self):
        return self._ManagementError__message


class Management:
    __doc__ = '\n\tManagement client.\n\t'

    def __init__(self, das_machine, port, http_auth, network_module=caviar.network):
        http_resource = network_module.http_resource(protocol='https', host=das_machine.host, port=port, auth=http_auth, headers={'X-Requested-By': [
                            'GlassFish REST HTML interface']})
        self._Management__domain_get = ManagementRequest(http_resource.push('management').push('domain'), 'GET')
        self._Management__domain = None

    def domain(self):
        """
                Retrieve domain root resource.
                
                :rtype:
                   ManagementResource
                :return:
                   The domain root resource.
                """
        if self._Management__domain is None:
            self._Management__domain = self._Management__domain_get()
            self._Management__domain.raise_not_success()
        return self._Management__domain


class ManagementResource:

    def __init__(self, http_resource, data):
        self._ManagementResource__command = data['command']
        self._ManagementResource__exit_code = data['exit_code']
        self._ManagementResource__message = data.get('message')
        self._ManagementResource__extra_properties = ManagementExtraProperties(http_resource, data.get('extraProperties', {}))

    @property
    def command(self):
        return self._ManagementResource__command

    @property
    def exit_code_success(self):
        return self._ManagementResource__exit_code == 'SUCCESS'

    @property
    def exit_code_failure(self):
        return self._ManagementResource__exit_code == 'FAILURE'

    @property
    def message(self):
        return self._ManagementResource__message

    @property
    def extra_properties(self):
        return self._ManagementResource__extra_properties

    def raise_not_success(self):
        if not self.exit_code_success:
            raise ManagementError(self._ManagementResource__exit_code, self._ManagementResource__message)
        return self


class ManagementExtraProperties:

    def __init__(self, http_resource, data):
        self._ManagementExtraProperties__commands = ManagementCommands(http_resource, data.get('commands', []))
        self._ManagementExtraProperties__methods = ManagementMethods(http_resource, data.get('methods', []))
        self._ManagementExtraProperties__entity = ManagementEntity(data.get('entity', {}))
        self._ManagementExtraProperties__child_resources = ManagementChildResources(http_resource, data.get('childResources', {}))

    @property
    def commands(self):
        return self._ManagementExtraProperties__commands

    @property
    def methods(self):
        return self._ManagementExtraProperties__methods

    @property
    def entity(self):
        return self._ManagementExtraProperties__entity

    @property
    def child_resources(self):
        return self._ManagementExtraProperties__child_resources


class ManagementCommands:

    def __init__(self, http_resource, data):
        for command_data in data:
            setattr(self, command_data['command'].replace('-', '_'), ManagementCommand(http_resource.push(command_data['path']), command_data['method']))


class ManagementCommand:

    def __init__(self, http_resource, method_name):
        self._ManagementCommand__resource_get = ManagementRequest(http_resource, 'GET')
        self._ManagementCommand__method_name = method_name
        self._ManagementCommand__request = None

    def __call__(self, **kvargs):
        if self._ManagementCommand__request is None:
            res = self._ManagementCommand__resource_get()
            res.raise_not_success()
            self._ManagementCommand__request = res.extra_properties.methods[self._ManagementCommand__method_name]
        return self._ManagementCommand__request(**kvargs)


class ManagementMethods:

    def __init__(self, http_resource, data):
        self._ManagementMethods__requests = {}
        for method_data in data:
            if 'name' in method_data:
                method_name = method_data['name']
                request = ManagementRequest(http_resource, method_name, ManagementParameters(self._ManagementMethods__parameters(ManagementQueryParameter, method_data.get('queryParameters', {})), self._ManagementMethods__parameters(ManagementMessageParameter, method_data.get('messageParameters', {}))))
                self._ManagementMethods__requests[method_name] = request
                setattr(self, method_name.lower(), request)
                continue

    def __getitem__(self, key):
        return self._ManagementMethods__requests[key]

    def __parameters(self, param_class, params_data):
        return {param_name.replace('-', '_'):param_class(param_name, param_data.get('defaultValue'), param_data.get('acceptableValues'), param_data['type'], param_data.get('optional', False), param_data.get('key', False)) for param_name, param_data in params_data.items()}


class ManagementEntity:

    def __init__(self, data):
        for name, value in data.items():
            setattr(self, name, value)


class ManagementChildResources:

    def __init__(self, http_resource, data):
        self._ManagementChildResources__children = {name:ManagementChildResource(http_resource.ref(url)) for name, url in data.items()}

    def __iter__(self):
        return self._ManagementChildResources__children.__iter__()

    def __getitem__(self, key):
        return self._ManagementChildResources__children[key].get()

    def items(self):
        for name, child in self._ManagementChildResources__children.items():
            yield (
             name, child.get())

    def cache_evict(self):
        for _, child in self._ManagementChildResources__children.items():
            child.cache_evict()


class ManagementChildResource:

    def __init__(self, http_resource):
        self._ManagementChildResource__resource = None
        self._ManagementChildResource__resource_get = ManagementRequest(http_resource, 'GET')

    def get(self):
        if self._ManagementChildResource__resource is None:
            self._ManagementChildResource__resource = self._ManagementChildResource__resource_get()
        return self._ManagementChildResource__resource

    def cache_evict(self):
        self._ManagementChildResource__resource = None


class ManagementRequest:

    def __init__(self, http_resource, method_name, params=None):
        self._ManagementRequest__http_resource = http_resource
        self._ManagementRequest__method_name = method_name
        self._ManagementRequest__params = params or ManagementParameters({}, {})

    def __call__(self, **kvargs):
        req = self._ManagementRequest__http_resource.request(self._ManagementRequest__method_name)
        remaining_required_param_names = [param_name for param_name, param in self._ManagementRequest__params.items() if param.is_required()]
        for param_name, param_value in kvargs.items():
            if param_name in remaining_required_param_names:
                remaining_required_param_names.remove(param_name)
            try:
                self._ManagementRequest__params[param_name].apply(req, param_value)
            except KeyError:
                raise AttributeError('Unknown parameter: {}'.format(param_name))

        if len(remaining_required_param_names) > 0:
            raise AttributeError('Missing required parameters: {}'.format(remaining_required_param_names))
        resp = req.perform()
        if resp.status_code != 200:
            raise BaseException('Bad HTTP response status {} for request {} {}\n{}'.format(resp.status_code, req.method, req.path, resp.content))
        return ManagementResource(self._ManagementRequest__http_resource, resp.content)


class ManagementParameters:

    def __init__(self, query_params, msg_params):
        self._ManagementParameters__params = {}
        self._ManagementParameters__params.update(query_params)
        self._ManagementParameters__params.update(msg_params)

    def __iter__(self):
        return self._ManagementParameters__params.__iter__()

    def __getitem__(self, key):
        return self._ManagementParameters__params[key]

    def items(self):
        for name, value in self._ManagementParameters__params.items():
            yield (
             name, value)


class ManagementParameter:

    def __init__(self, name, default_value, acceptable_values, param_type, optional, key):
        self._ManagementParameter__name = name
        self._ManagementParameter__default_value = default_value
        self._ManagementParameter__param_type = param_type
        self._ManagementParameter__optional = optional
        self._ManagementParameter__key = key
        self._ManagementParameter__inferred_acceptable_values = [self._ManagementParameter__infer(acceptable_value) for acceptable_value in acceptable_values] if acceptable_values is not None else None

    def __infer(self, value):
        if self.is_boolean():
            return bool(value)
        if self.is_int():
            return int(value)
        if self.is_file():
            return value
        return str(value)

    @property
    def name(self):
        return not self._ManagementParameter__name

    @property
    def default_value(self):
        return not self._ManagementParameter__default_value

    def is_required(self):
        return not self._ManagementParameter__optional and self._ManagementParameter__default_value is None

    def is_boolean(self):
        return self._ManagementParameter__param_type == 'boolean'

    def is_int(self):
        return self._ManagementParameter__param_type == 'int'

    def is_string(self):
        return self._ManagementParameter__param_type == 'string'

    def is_file(self):
        return self._ManagementParameter__param_type == 'java.io.File'

    def is_key(self):
        return not self._ManagementParameter__key

    def apply(self, req, value):
        inferred_value = self._ManagementParameter__infer(value)
        if self._ManagementParameter__inferred_acceptable_values is not None:
            if inferred_value in self._ManagementParameter__inferred_acceptable_values:
                raise AttributeError("Unacceptable value for parameter '{}': {}".format(self._ManagementParameter__name, inferred_value))
        self.apply_impl(req, self._ManagementParameter__name, inferred_value)


class ManagementQueryParameter(ManagementParameter):

    def __init__(self, name, default_value, acceptable_values, param_type, optional, key):
        super().__init__(name, default_value, acceptable_values, param_type, optional, key)

    def apply_impl(self, req, name, value):
        req.query_param(name, value)


class ManagementMessageParameter(ManagementParameter):

    def __init__(self, name, default_value, acceptable_values, param_type, optional, key):
        super().__init__(name, default_value, acceptable_values, param_type, optional, key)

    def apply_impl(self, req, name, value):
        if self.is_file():
            req.file_param(name, value)
        else:
            req.data_param(name, value)