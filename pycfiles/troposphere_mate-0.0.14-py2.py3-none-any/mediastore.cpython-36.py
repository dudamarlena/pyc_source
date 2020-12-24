# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/mediastore.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 2425 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.mediastore
from troposphere.mediastore import CorsRule as _CorsRule
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class CorsRule(troposphere.mediastore.CorsRule, Mixin):

    def __init__(self, title=None, AllowedHeaders=NOTHING, AllowedMethods=NOTHING, AllowedOrigins=NOTHING, ExposeHeaders=NOTHING, MaxAgeSeconds=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AllowedHeaders=AllowedHeaders, 
         AllowedMethods=AllowedMethods, 
         AllowedOrigins=AllowedOrigins, 
         ExposeHeaders=ExposeHeaders, 
         MaxAgeSeconds=MaxAgeSeconds, **kwargs)
        (super(CorsRule, self).__init__)(**processed_kwargs)


class Container(troposphere.mediastore.Container, Mixin):

    def __init__(self, title, template=None, validation=True, ContainerName=REQUIRED, AccessLoggingEnabled=NOTHING, CorsPolicy=NOTHING, LifecyclePolicy=NOTHING, Policy=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ContainerName=ContainerName, 
         AccessLoggingEnabled=AccessLoggingEnabled, 
         CorsPolicy=CorsPolicy, 
         LifecyclePolicy=LifecyclePolicy, 
         Policy=Policy, **kwargs)
        (super(Container, self).__init__)(**processed_kwargs)