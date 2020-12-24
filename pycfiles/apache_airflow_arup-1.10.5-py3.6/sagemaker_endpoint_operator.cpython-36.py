# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sagemaker_endpoint_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6188 bytes
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.contrib.operators.sagemaker_base_operator import SageMakerBaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

class SageMakerEndpointOperator(SageMakerBaseOperator):
    __doc__ = "\n    Create a SageMaker endpoint.\n\n    This operator returns The ARN of the endpoint created in Amazon SageMaker\n\n    :param config:\n        The configuration necessary to create an endpoint.\n\n        If you need to create a SageMaker endpoint based on an existed\n        SageMaker model and an existed SageMaker endpoint config::\n\n            config = endpoint_configuration;\n\n        If you need to create all of SageMaker model, SageMaker endpoint-config and SageMaker endpoint::\n\n            config = {\n                'Model': model_configuration,\n                'EndpointConfig': endpoint_config_configuration,\n                'Endpoint': endpoint_configuration\n            }\n\n        For details of the configuration parameter of model_configuration see\n        :py:meth:`SageMaker.Client.create_model`\n\n        For details of the configuration parameter of endpoint_config_configuration see\n        :py:meth:`SageMaker.Client.create_endpoint_config`\n\n        For details of the configuration parameter of endpoint_configuration see\n        :py:meth:`SageMaker.Client.create_endpoint`\n\n    :type config: dict\n    :param aws_conn_id: The AWS connection ID to use.\n    :type aws_conn_id: str\n    :param wait_for_completion: Whether the operator should wait until the endpoint creation finishes.\n    :type wait_for_completion: bool\n    :param check_interval: If wait is set to True, this is the time interval, in seconds, that this operation\n        waits before polling the status of the endpoint creation.\n    :type check_interval: int\n    :param max_ingestion_time: If wait is set to True, this operation fails if the endpoint creation doesn't\n        finish within max_ingestion_time seconds. If you set this parameter to None it never times out.\n    :type max_ingestion_time: int\n    :param operation: Whether to create an endpoint or update an endpoint. Must be either 'create or 'update'.\n    :type operation: str\n    "

    @apply_defaults
    def __init__(self, config, wait_for_completion=True, check_interval=30, max_ingestion_time=None, operation='create', *args, **kwargs):
        (super(SageMakerEndpointOperator, self).__init__)(args, config=config, **kwargs)
        self.config = config
        self.wait_for_completion = wait_for_completion
        self.check_interval = check_interval
        self.max_ingestion_time = max_ingestion_time
        self.operation = operation.lower()
        if self.operation not in ('create', 'update'):
            raise ValueError('Invalid value! Argument operation has to be one of "create" and "update"')
        self.create_integer_fields()

    def create_integer_fields(self):
        if 'EndpointConfig' in self.config:
            self.integer_fields = [['EndpointConfig', 'ProductionVariants', 'InitialInstanceCount']]

    def expand_role(self):
        if 'Model' not in self.config:
            return
        hook = AwsHook(self.aws_conn_id)
        config = self.config['Model']
        if 'ExecutionRoleArn' in config:
            config['ExecutionRoleArn'] = hook.expand_role(config['ExecutionRoleArn'])

    def execute(self, context):
        self.preprocess_config()
        model_info = self.config.get('Model')
        endpoint_config_info = self.config.get('EndpointConfig')
        endpoint_info = self.config.get('Endpoint', self.config)
        if model_info:
            self.log.info('Creating SageMaker model %s.', model_info['ModelName'])
            self.hook.create_model(model_info)
        else:
            if endpoint_config_info:
                self.log.info('Creating endpoint config %s.', endpoint_config_info['EndpointConfigName'])
                self.hook.create_endpoint_config(endpoint_config_info)
            else:
                if self.operation == 'create':
                    sagemaker_operation = self.hook.create_endpoint
                    log_str = 'Creating'
                else:
                    if self.operation == 'update':
                        sagemaker_operation = self.hook.update_endpoint
                        log_str = 'Updating'
                    else:
                        raise ValueError('Invalid value! Argument operation has to be one of "create" and "update"')
            self.log.info('%s SageMaker endpoint %s.', log_str, endpoint_info['EndpointName'])
            response = sagemaker_operation(endpoint_info,
              wait_for_completion=(self.wait_for_completion),
              check_interval=(self.check_interval),
              max_ingestion_time=(self.max_ingestion_time))
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise AirflowException('Sagemaker endpoint creation failed: %s' % response)
            else:
                return {'EndpointConfig':self.hook.describe_endpoint_config(endpoint_info['EndpointConfigName']),  'Endpoint':self.hook.describe_endpoint(endpoint_info['EndpointName'])}