# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pulumi_google_tag_manager/dynamic_providers/container.py
# Compiled at: 2020-03-24 14:26:01
# Size of source mod 2**32: 913 bytes
from pulumi.dynamic import Resource
from pulumi import Input, Output
from .container_provider import ContainerProvider
from ..service import get_key_file_location

class ContainerArgs(object):
    account_id: Input[str]
    container_name: Input[str]

    def __init__(self, account_id, container_name):
        self.account_id = account_id
        self.container_name = container_name


class Container(Resource):
    container_id: Output[str]
    path: Output[str]
    gtm_tag: Output[str]
    gtm_tag_noscript: Output[str]

    def __init__(self, name, args, opts=None):
        full_args = {**{'container_id':None, 
         'path':None, 
         'key_location':get_key_file_location(), 
         'gtm_tag_noscript':None, 
         'gtm_tag':None}, **(vars(args))}
        super().__init__(ContainerProvider(), name, full_args, opts)