# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/datapipeline.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 5213 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.datapipeline
from troposphere.datapipeline import ObjectField as _ObjectField, ParameterObject as _ParameterObject, ParameterObjectAttribute as _ParameterObjectAttribute, ParameterValue as _ParameterValue, PipelineObject as _PipelineObject, PipelineTag as _PipelineTag
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class ParameterObjectAttribute(troposphere.datapipeline.ParameterObjectAttribute, Mixin):

    def __init__(self, title=None, Key=REQUIRED, StringValue=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         StringValue=StringValue, **kwargs)
        (super(ParameterObjectAttribute, self).__init__)(**processed_kwargs)


class ParameterObject(troposphere.datapipeline.ParameterObject, Mixin):

    def __init__(self, title=None, Attributes=REQUIRED, Id=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Attributes=Attributes, 
         Id=Id, **kwargs)
        (super(ParameterObject, self).__init__)(**processed_kwargs)


class ParameterValue(troposphere.datapipeline.ParameterValue, Mixin):

    def __init__(self, title=None, Id=REQUIRED, StringValue=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Id=Id, 
         StringValue=StringValue, **kwargs)
        (super(ParameterValue, self).__init__)(**processed_kwargs)


class ObjectField(troposphere.datapipeline.ObjectField, Mixin):

    def __init__(self, title=None, Key=REQUIRED, RefValue=NOTHING, StringValue=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         RefValue=RefValue, 
         StringValue=StringValue, **kwargs)
        (super(ObjectField, self).__init__)(**processed_kwargs)


class PipelineObject(troposphere.datapipeline.PipelineObject, Mixin):

    def __init__(self, title=None, Fields=REQUIRED, Id=REQUIRED, Name=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Fields=Fields, 
         Id=Id, 
         Name=Name, **kwargs)
        (super(PipelineObject, self).__init__)(**processed_kwargs)


class PipelineTag(troposphere.datapipeline.PipelineTag, Mixin):

    def __init__(self, title=None, Key=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Key=Key, 
         Value=Value, **kwargs)
        (super(PipelineTag, self).__init__)(**processed_kwargs)


class Pipeline(troposphere.datapipeline.Pipeline, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, PipelineObjects=REQUIRED, Activate=NOTHING, Description=NOTHING, ParameterObjects=NOTHING, ParameterValues=NOTHING, PipelineTags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         PipelineObjects=PipelineObjects, 
         Activate=Activate, 
         Description=Description, 
         ParameterObjects=ParameterObjects, 
         ParameterValues=ParameterValues, 
         PipelineTags=PipelineTags, **kwargs)
        (super(Pipeline, self).__init__)(**processed_kwargs)