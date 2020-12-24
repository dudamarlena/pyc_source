# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quart_openapi/__init__.py
# Compiled at: 2020-04-13 15:04:18
# Size of source mod 2**32: 1024 bytes
"""quart-openapi

Quart-OpenAPI is an extension for Quart_ that adds support for generating a openapi.json file using openapi 3.0.
If you are familiar with Quart_, this just wraps around it to add a openapi.json route similar to Flask-RESTX_
generating a swagger.json route and adds a Resource base class for building RESTful APIs.

Documentation can be found on https://factset.github.io/quart-openapi/
"""
from .resource import Resource
from .pint import Pint, OpenApiView, PintBlueprint
from .swagger import Swagger
from .__about__ import __short_version__, __description__, __release__
Resource.__module__ = __name__
Pint.__module__ = __name__
PintBlueprint.__module__ = __name__
Swagger.__module__ = __name__
__all__ = [
 '__short_version__',
 '__description__',
 '__release__',
 'Pint',
 'PintBlueprint',
 'Resource',
 'Swagger',
 'OpenApiView']