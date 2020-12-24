# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/robomaker.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 8202 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.robomaker
from troposphere.robomaker import RenderingEngine as _RenderingEngine, RobotSoftwareSuite as _RobotSoftwareSuite, SimulationSoftwareSuite as _SimulationSoftwareSuite, SourceConfig as _SourceConfig, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Fleet(troposphere.robomaker.Fleet, Mixin):

    def __init__(self, title, template=None, validation=True, Name=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         Tags=Tags, **kwargs)
        (super(Fleet, self).__init__)(**processed_kwargs)


class Robot(troposphere.robomaker.Robot, Mixin):

    def __init__(self, title, template=None, validation=True, Architecture=REQUIRED, GreengrassGroupId=REQUIRED, Fleet=NOTHING, Name=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Architecture=Architecture, 
         GreengrassGroupId=GreengrassGroupId, 
         Fleet=Fleet, 
         Name=Name, 
         Tags=Tags, **kwargs)
        (super(Robot, self).__init__)(**processed_kwargs)


class RobotSoftwareSuite(troposphere.robomaker.RobotSoftwareSuite, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Version=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Version=Version, **kwargs)
        (super(RobotSoftwareSuite, self).__init__)(**processed_kwargs)


class SourceConfig(troposphere.robomaker.SourceConfig, Mixin):

    def __init__(self, title=None, Architecture=REQUIRED, S3Bucket=REQUIRED, S3Key=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Architecture=Architecture, 
         S3Bucket=S3Bucket, 
         S3Key=S3Key, **kwargs)
        (super(SourceConfig, self).__init__)(**processed_kwargs)


class RobotApplication(troposphere.robomaker.RobotApplication, Mixin):

    def __init__(self, title, template=None, validation=True, RobotSoftwareSuite=REQUIRED, Sources=REQUIRED, CurrentRevisionId=NOTHING, Name=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RobotSoftwareSuite=RobotSoftwareSuite, 
         Sources=Sources, 
         CurrentRevisionId=CurrentRevisionId, 
         Name=Name, 
         Tags=Tags, **kwargs)
        (super(RobotApplication, self).__init__)(**processed_kwargs)


class RobotApplicationVersion(troposphere.robomaker.RobotApplicationVersion, Mixin):

    def __init__(self, title, template=None, validation=True, Application=REQUIRED, CurrentRevisionId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Application=Application, 
         CurrentRevisionId=CurrentRevisionId, **kwargs)
        (super(RobotApplicationVersion, self).__init__)(**processed_kwargs)


class RenderingEngine(troposphere.robomaker.RenderingEngine, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Version=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Version=Version, **kwargs)
        (super(RenderingEngine, self).__init__)(**processed_kwargs)


class SimulationSoftwareSuite(troposphere.robomaker.SimulationSoftwareSuite, Mixin):

    def __init__(self, title=None, Name=REQUIRED, Version=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Name=Name, 
         Version=Version, **kwargs)
        (super(SimulationSoftwareSuite, self).__init__)(**processed_kwargs)


class SimulationApplication(troposphere.robomaker.SimulationApplication, Mixin):

    def __init__(self, title, template=None, validation=True, RenderingEngine=REQUIRED, RobotSoftwareSuite=REQUIRED, SimulationSoftwareSuite=REQUIRED, Sources=REQUIRED, CurrentRevisionId=NOTHING, Name=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         RenderingEngine=RenderingEngine, 
         RobotSoftwareSuite=RobotSoftwareSuite, 
         SimulationSoftwareSuite=SimulationSoftwareSuite, 
         Sources=Sources, 
         CurrentRevisionId=CurrentRevisionId, 
         Name=Name, 
         Tags=Tags, **kwargs)
        (super(SimulationApplication, self).__init__)(**processed_kwargs)


class SimulationApplicationVersion(troposphere.robomaker.SimulationApplicationVersion, Mixin):

    def __init__(self, title, template=None, validation=True, Application=REQUIRED, CurrentRevisionId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Application=Application, 
         CurrentRevisionId=CurrentRevisionId, **kwargs)
        (super(SimulationApplicationVersion, self).__init__)(**processed_kwargs)