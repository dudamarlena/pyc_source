# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cirdan/decorators.py
# Compiled at: 2015-07-07 15:46:54
# Size of source mod 2**32: 2272 bytes
from __future__ import absolute_import
import json
from cirdan.registry import registry, Parameter, ReturnStatus

def title(value):

    def inner(wrapped):
        item = registry.get(wrapped)
        item.title = value
        return wrapped

    return inner


def description(value):

    def inner(wrapped):
        item = registry.get(wrapped)
        item.description = value
        return wrapped

    return inner


def secret(wrapped):
    item = registry.get(wrapped)
    item.secret = True
    return wrapped


def param(name, description, required=False):

    def inner(wrapped):
        route = registry.get(wrapped)
        route.parameters.append(Parameter(name, description, required))
        return wrapped

    return inner


def returns_status(status_code, description):

    def inner(wrapped):
        route = registry.get(wrapped)
        route.return_statuses.append(ReturnStatus(status_code, description))
        return wrapped

    return inner


def content_type(value):

    def inner(wrapped):
        route = registry.get(wrapped)
        route.content_type = value
        return wrapped

    return inner


def requires_permission(value):

    def inner(wrapped):
        route = registry.get(wrapped)
        route.requires_permission = value
        return wrapped

    return inner


def example(request=None, response=None):

    def inner(wrapped):
        route = registry.get(wrapped)
        if request is not None:
            route.example_request = request if isinstance(request, str) else json.dumps(request, indent=4)
        if response is not None:
            route.example_response = response if isinstance(response, str) else json.dumps(response, indent=4)
        return wrapped

    return inner