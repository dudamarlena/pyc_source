# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/codestarnotifications.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 2236 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.codestarnotifications
from troposphere.codestarnotifications import Target as _Target
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Target(troposphere.codestarnotifications.Target, Mixin):

    def __init__(self, title=None, TargetAddress=NOTHING, TargetType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TargetAddress=TargetAddress, 
         TargetType=TargetType, **kwargs)
        (super(Target, self).__init__)(**processed_kwargs)


class NotificationRule(troposphere.codestarnotifications.NotificationRule, Mixin):

    def __init__(self, title, template=None, validation=True, DetailType=REQUIRED, EventTypeIds=REQUIRED, Name=REQUIRED, Resource=REQUIRED, Targets=REQUIRED, Status=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DetailType=DetailType, 
         EventTypeIds=EventTypeIds, 
         Name=Name, 
         Resource=Resource, 
         Targets=Targets, 
         Status=Status, 
         Tags=Tags, **kwargs)
        (super(NotificationRule, self).__init__)(**processed_kwargs)