# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /codebuild/output/src613133936/src/github.com/awslabs/aws-service-catalog-puppet/servicecatalog_puppet/config.py
# Compiled at: 2020-05-13 08:59:18
# Size of source mod 2**32: 3676 bytes
import functools, pkg_resources, yaml
from betterboto import client as betterboto_client
from jinja2 import Environment, FileSystemLoader
from servicecatalog_puppet import asset_helpers
from servicecatalog_puppet import constants
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

@functools.lru_cache(maxsize=32)
def get_config(default_region=None):
    logger.info('getting config,  default_region: {}'.format(default_region))
    with betterboto_client.ClientContextManager('ssm',
      region_name=(default_region if default_region else get_home_region())) as (ssm):
        response = ssm.get_parameter(Name=(constants.CONFIG_PARAM_NAME))
        return yaml.safe_load(response.get('Parameter').get('Value'))


@functools.lru_cache(maxsize=32)
def get_regions(default_region=None):
    logger.info('getting regions,  default_region: {}'.format(default_region))
    return get_config(default_region).get('regions')


@functools.lru_cache(maxsize=32)
def get_should_use_sns(default_region=None):
    logger.info('getting should_use_sns,  default_region: {}'.format(default_region))
    return get_config(default_region).get('should_collect_cloudformation_events', True)


@functools.lru_cache(maxsize=32)
def get_should_use_eventbridge(default_region=None):
    logger.info('getting should_use_eventbridge,  default_region: {}'.format(default_region))
    return get_config(default_region).get('should_forward_events_to_eventbridge', False)


@functools.lru_cache(maxsize=32)
def get_should_forward_failures_to_opscenter(default_region=None):
    logger.info('getting should_forward_failures_to_opscenter,  default_region: {}'.format(default_region))
    return get_config(default_region).get('should_forward_failures_to_opscenter', False)


@functools.lru_cache(maxsize=32)
def get_should_use_product_plans(default_region=None):
    logger.info('getting should_use_product_plans,  default_region: {}'.format(default_region))
    return get_config(default_region).get('should_use_product_plans', True)


@functools.lru_cache()
def get_home_region():
    with betterboto_client.ClientContextManager('ssm') as (ssm):
        response = ssm.get_parameter(Name=(constants.HOME_REGION_PARAM_NAME))
        return response.get('Parameter').get('Value')


@functools.lru_cache(maxsize=32)
def get_org_iam_role_arn():
    with betterboto_client.ClientContextManager('ssm', region_name=(get_home_region())) as (ssm):
        try:
            response = ssm.get_parameter(Name=(constants.CONFIG_PARAM_NAME_ORG_IAM_ROLE_ARN))
            return response.get('Parameter').get('Value')
        except ssm.exceptions.ParameterNotFound:
            logger.info('No org role set')
            return


template_dir = asset_helpers.resolve_from_site_packages('templates')
env = Environment(loader=(FileSystemLoader(template_dir)),
  extensions=[
 'jinja2.ext.do'])

@functools.lru_cache(maxsize=32)
def get_puppet_account_id():
    with betterboto_client.ClientContextManager('sts') as (sts):
        return sts.get_caller_identity().get('Account')


def get_ssm_config_for_parameter(account_ssm_param, required_parameter_name):
    if account_ssm_param.get('region') is not None:
        return {'name':account_ssm_param.get('name'),  'region':account_ssm_param.get('region'), 
         'parameter_name':required_parameter_name}
    return {'name':account_ssm_param.get('name'), 
     'parameter_name':required_parameter_name}


def get_puppet_version():
    return pkg_resources.require('aws-service-catalog-puppet')[0].version