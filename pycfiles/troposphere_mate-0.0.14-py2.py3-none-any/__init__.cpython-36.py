# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/__init__.py
# Compiled at: 2020-02-13 14:29:41
# Size of source mod 2**32: 1016 bytes
"""
Package Description.
"""
from ._version import __version__
__short_description__ = 'Orchestrate AWS Resource in Pythonic Way.'
__license__ = 'MIT'
__author__ = 'Sanhe Hu'
__author_email__ = 'husanhe@gmail.com'
__github_username__ = 'MacHu-GWU'
try:
    from troposphere import *
    from troposphere import AWSObject as TroposphereAWSObject
    from .associate import associate, LinkerApi
    from .core import metadata as mtdt
    from .core.mate import Template, Parameter, Output, DEFAULT_LABELS_FIELD
    from .core.canned import Canned, MultiEnvBasicConfig, ServerlessConfig, ConfigClass, Constant, Derivable, slugify, camelcase, helper_fn_sub
    from .core.sentiel import Sentinel, REQUIRED, NOTHING
    from .core.stack_deploy import upload_template, package, deploy_stack, link_stack_template, StackManager
    from . import canned
except ImportError as e:
    pass