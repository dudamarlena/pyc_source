# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pulumi_google_tag_manager/dynamic_providers/tag.py
# Compiled at: 2020-03-24 14:26:01
# Size of source mod 2**32: 795 bytes
from pulumi.dynamic import Resource
from pulumi import Input, Output
from .tag_provider import TagProvider
from ..service import get_key_file_location

class TagArgs(object):
    workspace_path: Input[str]
    tag_name: Input[str]
    tracking_id: Input[str]

    def __init__(self, workspace_path, tag_name, tracking_id):
        self.workspace_path = workspace_path
        self.tag_name = tag_name
        self.tracking_id = tracking_id


class Tag(Resource):
    tag_id: Output[str]
    path: Output[str]

    def __init__(self, name, args, opts=None):
        full_args = {**{'tag_id':None, 
         'path':None, 
         'key_location':get_key_file_location()}, **(vars(args))}
        super().__init__(TagProvider(), name, full_args, opts)