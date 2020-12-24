# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/providers/cfn_base_api_provider.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 2374 bytes
"""Class that parses the CloudFormation Api Template"""
import logging
from samcli.commands.local.lib.swagger.parser import SwaggerParser
from samcli.commands.local.lib.swagger.reader import SwaggerReader
LOG = logging.getLogger(__name__)

class CfnBaseApiProvider:
    RESOURCE_TYPE = 'Type'

    def extract_resources(self, resources, collector, cwd=None):
        """
        Extract the Route Object from a given resource and adds it to the RouteCollector.

        Parameters
        ----------
        resources: dict
            The dictionary containing the different resources within the template

        collector: samcli.commands.local.lib.route_collector.RouteCollector
            Instance of the API collector that where we will save the API information

        cwd : str
            Optional working directory with respect to which we will resolve relative path to Swagger file

        Return
        -------
        Returns a list of routes
        """
        raise NotImplementedError('not implemented')

    def extract_swagger_route(self, logical_id, body, uri, binary_media, collector, cwd=None):
        """
        Parse the Swagger documents and adds it to the ApiCollector.

        Parameters
        ----------
        logical_id : str
            Logical ID of the resource

        body : dict
            The body of the RestApi

        uri : str or dict
            The url to location of the RestApi

        binary_media: list
            The link to the binary media

        collector: samcli.commands.local.lib.route_collector.RouteCollector
            Instance of the Route collector that where we will save the route information

        cwd : str
            Optional working directory with respect to which we will resolve relative path to Swagger file
        """
        reader = SwaggerReader(definition_body=body, definition_uri=uri, working_dir=cwd)
        swagger = reader.read()
        parser = SwaggerParser(swagger)
        routes = parser.get_routes()
        LOG.debug("Found '%s' APIs in resource '%s'", len(routes), logical_id)
        collector.add_routes(logical_id, routes)
        collector.add_binary_media_types(logical_id, parser.get_binary_media_types())
        collector.add_binary_media_types(logical_id, binary_media)