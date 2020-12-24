# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/kinesis.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 2738 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.kinesis
from troposphere.kinesis import StreamEncryption as _StreamEncryption, Tags as _Tags
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class StreamEncryption(troposphere.kinesis.StreamEncryption, Mixin):

    def __init__(self, title=None, EncryptionType=REQUIRED, KeyId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EncryptionType=EncryptionType, 
         KeyId=KeyId, **kwargs)
        (super(StreamEncryption, self).__init__)(**processed_kwargs)


class Stream(troposphere.kinesis.Stream, Mixin):

    def __init__(self, title, template=None, validation=True, Name=NOTHING, RetentionPeriodHours=NOTHING, ShardCount=NOTHING, StreamEncryption=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         RetentionPeriodHours=RetentionPeriodHours, 
         ShardCount=ShardCount, 
         StreamEncryption=StreamEncryption, 
         Tags=Tags, **kwargs)
        (super(Stream, self).__init__)(**processed_kwargs)


class StreamConsumer(troposphere.kinesis.StreamConsumer, Mixin):

    def __init__(self, title, template=None, validation=True, ConsumerName=REQUIRED, StreamARN=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ConsumerName=ConsumerName, 
         StreamARN=StreamARN, **kwargs)
        (super(StreamConsumer, self).__init__)(**processed_kwargs)