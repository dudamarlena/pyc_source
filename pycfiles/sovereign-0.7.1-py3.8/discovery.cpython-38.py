# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sovereign/discovery.py
# Compiled at: 2020-04-16 21:27:51
# Size of source mod 2**32: 6673 bytes
"""
Discovery
---------

Functions used to render and return discovery responses to Envoy proxies.

The templates are configurable. `todo See ref:Configuration#Templates`
"""
import sys, zlib, yaml
from yaml.parser import ParserError
from functools import lru_cache
from enum import Enum
from jinja2 import meta
from starlette.exceptions import HTTPException
from sovereign import XDS_TEMPLATES, config
from sovereign.logs import LOG
from sovereign.statistics import stats
from sovereign.context import template_context
from sovereign.sources import match_node, extract_node_key, source_metadata
from sovereign.config_loader import jinja_env
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


    @lru_cache(config.context_cache_size)
    def make_context(node_value, disable_decryption, using_python_templates: bool, jinja_source: str, discovery_type: str, resource_names: str, source_version: str='-'):
        """
    Creates context variables to be passed into either a jinja template,
    or as kwargs to a python template.
    """
        matches = match_node(node_value=node_value,
          discovery_type=discovery_type)
        context = {**template_context}
        for scope, instances in matches.scopes.items():
            if scope == 'default':
                context['instances'] = instances
            else:
                context[scope] = instances
        else:
            if disable_decryption:
                context['crypto'] = disabled_suite
            template_ast = using_python_templates or jinja_env.parse(jinja_source)
            used_variables = meta.find_undeclared_variables(template_ast)
            for key in list(context):
                if key in used_variables:
                    pass
                else:
                    context.pop(key, None)
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
          using_python_templates=(template.is_python_source),
          jinja_source=(template.source),
          disable_decryption=(request.node.metadata.get('hide_private_keys')),
          resource_names=(','.join(request.resources)),
          source_version=(source_metadata.updated.isoformat()),
          discovery_type=xds_type)
        config_version = version_hash(context, template.checksum, request.node.common, request.resources)
        if config_version == request.version_info:
            return {'version_info': config_version}
        kwargs = dict(discovery_request=request, 
         host_header=host, 
         resource_names=request.resources, **context)
        if template.is_python_source:
            envoy_configuration = {'resources':list((template.code.call)(**kwargs)),  'version_info':config_version}
        else:
            rendered = await (template.content.render_async)(**kwargs)
            try:
                envoy_configuration = yaml.safe_load(rendered)
                envoy_configuration['version_info'] = config_version
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
                return remove_unwanted_resources(envoy_configuration, request.resources)


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