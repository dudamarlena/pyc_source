# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/cloudformation.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 6556 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.cloudformation
from troposphere.cloudformation import InitFileContext as _InitFileContext, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Stack(troposphere.cloudformation.Stack, Mixin):

    def __init__(self, title, template=None, validation=True, TemplateURL=REQUIRED, NotificationARNs=NOTHING, Parameters=NOTHING, Tags=NOTHING, TimeoutInMinutes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         TemplateURL=TemplateURL, 
         NotificationARNs=NotificationARNs, 
         Parameters=Parameters, 
         Tags=Tags, 
         TimeoutInMinutes=TimeoutInMinutes, **kwargs)
        (super(Stack, self).__init__)(**processed_kwargs)


class WaitCondition(troposphere.cloudformation.WaitCondition, Mixin):

    def __init__(self, title, template=None, validation=True, Count=NOTHING, Handle=NOTHING, Timeout=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Count=Count, 
         Handle=Handle, 
         Timeout=Timeout, **kwargs)
        (super(WaitCondition, self).__init__)(**processed_kwargs)


class WaitConditionHandle(troposphere.cloudformation.WaitConditionHandle, Mixin):

    def __init__(self, title, template=None, validation=True, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, **kwargs)
        (super(WaitConditionHandle, self).__init__)(**processed_kwargs)


class InitFile(troposphere.cloudformation.InitFile, Mixin):

    def __init__(self, title=None, content=NOTHING, mode=NOTHING, owner=NOTHING, encoding=NOTHING, group=NOTHING, source=NOTHING, authentication=NOTHING, context=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         content=content, 
         mode=mode, 
         owner=owner, 
         encoding=encoding, 
         group=group, 
         source=source, 
         authentication=authentication, 
         context=context, **kwargs)
        (super(InitFile, self).__init__)(**processed_kwargs)


class InitService(troposphere.cloudformation.InitService, Mixin):

    def __init__(self, title=None, ensureRunning=NOTHING, enabled=NOTHING, files=NOTHING, packages=NOTHING, sources=NOTHING, commands=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ensureRunning=ensureRunning, 
         enabled=enabled, 
         files=files, 
         packages=packages, 
         sources=sources, 
         commands=commands, **kwargs)
        (super(InitService, self).__init__)(**processed_kwargs)


class InitConfig(troposphere.cloudformation.InitConfig, Mixin):

    def __init__(self, title=None, groups=NOTHING, users=NOTHING, sources=NOTHING, packages=NOTHING, files=NOTHING, commands=NOTHING, services=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         groups=groups, 
         users=users, 
         sources=sources, 
         packages=packages, 
         files=files, 
         commands=commands, 
         services=services, **kwargs)
        (super(InitConfig, self).__init__)(**processed_kwargs)


class AuthenticationBlock(troposphere.cloudformation.AuthenticationBlock, Mixin):

    def __init__(self, title=None, accessKeyId=NOTHING, buckets=NOTHING, password=NOTHING, secretKey=NOTHING, type=NOTHING, uris=NOTHING, username=NOTHING, roleName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         accessKeyId=accessKeyId, 
         buckets=buckets, 
         password=password, 
         secretKey=secretKey, 
         type=type, 
         uris=uris, 
         username=username, 
         roleName=roleName, **kwargs)
        (super(AuthenticationBlock, self).__init__)(**processed_kwargs)