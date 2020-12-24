# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/mediaconvert.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 4199 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.mediaconvert
from troposphere.mediaconvert import AccelerationSettings as _AccelerationSettings
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class AccelerationSettings(troposphere.mediaconvert.AccelerationSettings, Mixin):

    def __init__(self, title=None, Mode=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Mode=Mode, **kwargs)
        (super(AccelerationSettings, self).__init__)(**processed_kwargs)


class JobTemplate(troposphere.mediaconvert.JobTemplate, Mixin):

    def __init__(self, title, template=None, validation=True, SettingsJson=REQUIRED, AccelerationSettings=NOTHING, Category=NOTHING, Description=NOTHING, Name=NOTHING, Priority=NOTHING, Queue=NOTHING, StatusUpdateInterval=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SettingsJson=SettingsJson, 
         AccelerationSettings=AccelerationSettings, 
         Category=Category, 
         Description=Description, 
         Name=Name, 
         Priority=Priority, 
         Queue=Queue, 
         StatusUpdateInterval=StatusUpdateInterval, 
         Tags=Tags, **kwargs)
        (super(JobTemplate, self).__init__)(**processed_kwargs)


class Preset(troposphere.mediaconvert.Preset, Mixin):

    def __init__(self, title, template=None, validation=True, SettingsJson=REQUIRED, Category=NOTHING, Description=NOTHING, Name=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         SettingsJson=SettingsJson, 
         Category=Category, 
         Description=Description, 
         Name=Name, 
         Tags=Tags, **kwargs)
        (super(Preset, self).__init__)(**processed_kwargs)


class Queue(troposphere.mediaconvert.Queue, Mixin):

    def __init__(self, title, template=None, validation=True, Description=NOTHING, Name=NOTHING, PricingPlan=NOTHING, Status=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Description=Description, 
         Name=Name, 
         PricingPlan=PricingPlan, 
         Status=Status, 
         Tags=Tags, **kwargs)
        (super(Queue, self).__init__)(**processed_kwargs)