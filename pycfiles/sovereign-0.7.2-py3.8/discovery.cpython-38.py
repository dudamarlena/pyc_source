# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/discovery.py
# Compiled at: 2020-04-29 02:35:50
# Size of source mod 2**32: 6001 bytes
"""
Discovery
---------

Functions used to render and return discovery responses to Envoy proxies.

The templates are configurable. `todo See ref:Configuration#Templates`
"""
import sys, zlib, yaml
from yaml.parser import ParserError
from enum import Enum
from starlette.exceptions import HTTPException
from sovereign import XDS_TEMPLATES, config
from sovereign.logs import LOG
from sovereign.statistics import stats
from sovereign.context import template_context
from sovereign.sources import match_node, extract_node_key
from sovereign.schemas import XdsTemplate, DiscoveryRequest
from sovereign.utils.crypto import disabled_suite
try:
    default_templates = XDS_TEMPLATES['default']
except KeyError:
    raise KeyError('Your configuration should contain default templates. For more details, see https://vsyrakis.bitbucket.io/sovereign/docs/html/guides/tutorial.html#create-templates ')
else:
    discovery_types = (_type for _type in sorted(XDS_TEMPLATES['__any__'].keys()))
    DiscoveryTypes = Enum('DiscoveryTypes', {t:t for t in discovery_types})

    @stats.timed('discovery.version_hash_ms')
    def version_hash(*args) -> str:
        """
    Creates a 'version hash' to be used in envoy Discovery Responses.
    """
        data = repr(args).encode()
        version_info = zlib.adler32(data)
        return str(version_info)


    def make_context(node_value: str, template: XdsTemplate):
        """
    Creates context variables to be passed into either a jinja template,
    or as kwargs to a python template.
    """
        matches = match_node(node_value=node_value)
        context = {**template_context}
        for scope, instances in matches.scopes.items():
            if scope == 'default':
                context['instances'] = instances
            else:
                context[scope] = instances
        else:
            for variable in template.is_python_source or list(context):
                if variable in template.jinja_variables:
                    pass
                else:
                    context.pop(variable, None)
                stats.set('discovery.context.bytes', sys.getsizeof(context))
                return context


    async def response(request: DiscoveryRequest, xds_type: DiscoveryTypes, host: str='none'):
        """
    A Discovery **Request** typically looks something like:

    .. code-block:: json

        {
            "version_info": "0",
            "node": {
                "cluster": "T1",
                "build_version": "<revision hash>/<version>/Clean/RELEASE",
                "metadata": {
                    "auth": "..."
                }
            }
        }

    When we receive this, we give the client the latest configuration via a
    Discovery **Response** that looks something like this:

    .. code-block:: json

        {
            "version_info": "abcdef1234567890",
            "resources": []
        }

    The version_info is derived from :func:`sovereign.discovery.version_hash`

    :param request: An envoy Discovery Request
    :param xds_type: what type of XDS template to use when rendering
    :param host: the host header that was received from the envoy client
    :return: An envoy Discovery Response
    """
        template = XDS_TEMPLATES.get(request.envoy_version, default_templates)[xds_type]
        context = make_context(node_value=(extract_node_key(request.node)),
          template=template)
        if request.node.metadata.get('hide_private_keys'):
            context['crypto'] = disabled_suite
        else:
            config_version = '0'
            if config.cache_strategy == 'context':
                config_version = version_hash(context, template.checksum, request.node.common, request.resources)
                if config_version == request.version_info:
                    return {'version_info': config_version}
            kwargs = dict(discovery_request=request, 
             host_header=host, 
             resource_names=request.resources, **context)
            if template.is_python_source:
                content = {'resources': list((template.code.call)(**kwargs))}
            else:
                content = await (template.content.render_async)(**kwargs)
        if config.cache_strategy == 'content':
            config_version = version_hash(content)
            if config_version == request.version_info:
                return {'version_info': config_version}
        if not template.is_python_source:
            content = deserialize_config(content)
        content['version_info'] = config_version
        return remove_unwanted_resources(content, request.resources)


    def deserialize_config(content):
        try:
            envoy_configuration = yaml.safe_load(content)
        except ParserError as e:
            try:
                LOG.msg(error=(repr(e)),
                  context=(e.context),
                  context_mark=(e.context_mark),
                  note=(e.note),
                  problem=(e.problem),
                  problem_mark=(e.problem_mark))
                raise HTTPException(status_code=500,
                  detail='Failed to load configuration, there may be a syntax error in the configured templates.')
            finally:
                e = None
                del e

        else:
            return envoy_configuration


    def remove_unwanted_resources(conf, requested):
        """
    If Envoy specifically requested a resource, this removes everything
    that does not match the name of the resource.
    If Envoy did not specifically request anything, every resource is retained.
    """
        ret = dict()
        ret['version_info'] = conf['version_info']
        ret['resources'] = [resource for resource in conf.get('resources', []) if resource_name(resource) in requested]
        return ret


    def resource_name(resource):
        return resource.get('name') or resource['cluster_name']