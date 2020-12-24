# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/transfer.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 3878 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.transfer
from troposphere.transfer import EndpointDetails as _EndpointDetails, IdentityProviderDetails as _IdentityProviderDetails, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class EndpointDetails(troposphere.transfer.EndpointDetails, Mixin):

    def __init__(self, title=None, VpcEndpointId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         VpcEndpointId=VpcEndpointId, **kwargs)
        (super(EndpointDetails, self).__init__)(**processed_kwargs)


class IdentityProviderDetails(troposphere.transfer.IdentityProviderDetails, Mixin):

    def __init__(self, title=None, InvocationRole=REQUIRED, Url=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         InvocationRole=InvocationRole, 
         Url=Url, **kwargs)
        (super(IdentityProviderDetails, self).__init__)(**processed_kwargs)


class Server(troposphere.transfer.Server, Mixin):

    def __init__(self, title, template=None, validation=True, EndpointDetails=NOTHING, EndpointType=NOTHING, IdentityProviderDetails=NOTHING, IdentityProviderType=NOTHING, LoggingRole=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         EndpointDetails=EndpointDetails, 
         EndpointType=EndpointType, 
         IdentityProviderDetails=IdentityProviderDetails, 
         IdentityProviderType=IdentityProviderType, 
         LoggingRole=LoggingRole, 
         Tags=Tags, **kwargs)
        (super(Server, self).__init__)(**processed_kwargs)


class User(troposphere.transfer.User, Mixin):

    def __init__(self, title, template=None, validation=True, Role=REQUIRED, ServerId=REQUIRED, UserName=REQUIRED, HomeDirectory=NOTHING, Policy=NOTHING, SshPublicKeys=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Role=Role, 
         ServerId=ServerId, 
         UserName=UserName, 
         HomeDirectory=HomeDirectory, 
         Policy=Policy, 
         SshPublicKeys=SshPublicKeys, 
         Tags=Tags, **kwargs)
        (super(User, self).__init__)(**processed_kwargs)