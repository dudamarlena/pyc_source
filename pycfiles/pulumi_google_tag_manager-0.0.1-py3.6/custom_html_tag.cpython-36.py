# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pulumi_google_tag_manager/dynamic_providers/custom_html_tag.py
# Compiled at: 2020-03-24 14:26:01
# Size of source mod 2**32: 1533 bytes
from pulumi import Input, Output
from pulumi.dynamic import Resource
from pulumi_google_tag_manager.dynamic_providers.gtm.custom_html_tag_provider import CustomHtmlTagProvider
from ..service import get_key_file_location
from .tag_provider import TagProvider

class CustomHtmlTagArgs(object):
    __doc__ = '\n    Describes a GTM Custom HTML Tag.  See https://support.google.com/tagmanager/answer/6107167?hl=en#CustomHTML\n    '
    workspace_path: Input[str]
    tag_name: Input[str]
    html: Input[str]
    supportDocumentWrite: Input[bool]

    def __init__(self, workspace_path, tag_name, html, supportDocumentWrite=None):
        self.workspace_path = workspace_path
        self.tag_name = tag_name
        self.html = html
        self.supportDocumentWrite = supportDocumentWrite


class CustomHtmlTag(Resource):
    tag_id: Output[str]
    path: Output[str]

    def __init__(self, name, args, opts=None):
        full_args = {**{'tag_id':None, 
         'path':None, 
         'key_location':get_key_file_location()}, **(vars(args))}
        super().__init__(CustomHtmlTagProvider(), name, full_args, opts)