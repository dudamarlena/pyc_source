# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pulumi_google_tag_manager/dynamic_providers/workspace.py
# Compiled at: 2020-03-24 14:26:01
# Size of source mod 2**32: 802 bytes
from pulumi.dynamic import Resource
from pulumi import Input, Output
from .workspace_provider import WorkspaceProvider
from ..service import get_key_file_location

class WorkspaceArgs(object):
    container_path: Input[str]
    workspace_name: Input[str]

    def __init__(self, container_path, workspace_name):
        self.container_path = container_path
        self.workspace_name = workspace_name


class Workspace(Resource):
    workspace_id: Output[str]
    path: Output[str]

    def __init__(self, name, args, opts=None):
        full_args = {**{'workspace_id':None, 
         'path':None, 
         'key_location':get_key_file_location()}, **(vars(args))}
        super().__init__(WorkspaceProvider(), name, full_args, opts)