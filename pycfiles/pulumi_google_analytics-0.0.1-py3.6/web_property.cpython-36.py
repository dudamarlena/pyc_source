# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pulumi_google_analytics/dynamic_providers/web_property.py
# Compiled at: 2020-03-24 13:31:47
# Size of source mod 2**32: 1018 bytes
from pulumi.dynamic import Resource
from pulumi import Input, Output
from .web_property_provider import WebPropertyProvider
from ..service import get_key_file_location

class WebPropertyArgs(object):
    __doc__ = '\n    Describes a GA web property.\n    '
    account_id: Input[str]
    site_name: Input[str]
    site_url: Input[str]

    def __init__(self, account_id, site_name, site_url):
        self.account_id = account_id
        self.site_name = site_name
        self.site_url = site_url


class WebProperty(Resource):
    tracking_id: Output[str]

    def __init__(self, name, args, opts=None):
        full_args = {**{'tracking_id':None, 
         'key_location':get_key_file_location()}, **(vars(args))}
        super().__init__(WebPropertyProvider(), name, full_args, opts)