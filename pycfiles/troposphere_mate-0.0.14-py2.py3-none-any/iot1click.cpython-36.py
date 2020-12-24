# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/iot1click.py
# Compiled at: 2020-02-12 18:15:54
# Size of source mod 2**32: 3448 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.iot1click
from troposphere.iot1click import PlacementTemplate as _PlacementTemplate
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Device(troposphere.iot1click.Device, Mixin):

    def __init__(self, title, template=None, validation=True, DeviceId=REQUIRED, Enabled=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DeviceId=DeviceId, 
         Enabled=Enabled, **kwargs)
        (super(Device, self).__init__)(**processed_kwargs)


class Placement(troposphere.iot1click.Placement, Mixin):

    def __init__(self, title, template=None, validation=True, ProjectName=REQUIRED, AssociatedDevices=NOTHING, Attributes=NOTHING, PlacementName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ProjectName=ProjectName, 
         AssociatedDevices=AssociatedDevices, 
         Attributes=Attributes, 
         PlacementName=PlacementName, **kwargs)
        (super(Placement, self).__init__)(**processed_kwargs)


class PlacementTemplate(troposphere.iot1click.PlacementTemplate, Mixin):

    def __init__(self, title=None, DefaultAttributes=NOTHING, DeviceTemplates=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DefaultAttributes=DefaultAttributes, 
         DeviceTemplates=DeviceTemplates, **kwargs)
        (super(PlacementTemplate, self).__init__)(**processed_kwargs)


class Project(troposphere.iot1click.Project, Mixin):

    def __init__(self, title, template=None, validation=True, PlacementTemplate=REQUIRED, Description=NOTHING, ProjectName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         PlacementTemplate=PlacementTemplate, 
         Description=Description, 
         ProjectName=ProjectName, **kwargs)
        (super(Project, self).__init__)(**processed_kwargs)