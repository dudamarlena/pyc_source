# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/iotevents.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 13262 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.iotevents
from troposphere.iotevents import Action as _Action, Attribute as _Attribute, ClearTimer as _ClearTimer, DetectorModelDefinition as _DetectorModelDefinition, Event as _Event, Firehose as _Firehose, InputDefinition as _InputDefinition, IotEvents as _IotEvents, IotTopicPublish as _IotTopicPublish, Lambda as _Lambda, OnEnter as _OnEnter, OnExit as _OnExit, OnInput as _OnInput, ResetTimer as _ResetTimer, SetTimer as _SetTimer, SetVariable as _SetVariable, Sns as _Sns, Sqs as _Sqs, State as _State, Tags as _Tags, TransitionEvent as _TransitionEvent
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class ClearTimer(troposphere.iotevents.ClearTimer, Mixin):

    def __init__(self, title=None, TimerName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TimerName=TimerName, **kwargs)
        (super(ClearTimer, self).__init__)(**processed_kwargs)


class Firehose(troposphere.iotevents.Firehose, Mixin):

    def __init__(self, title=None, DeliveryStreamName=NOTHING, Separator=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DeliveryStreamName=DeliveryStreamName, 
         Separator=Separator, **kwargs)
        (super(Firehose, self).__init__)(**processed_kwargs)


class IotEvents(troposphere.iotevents.IotEvents, Mixin):

    def __init__(self, title=None, InputName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         InputName=InputName, **kwargs)
        (super(IotEvents, self).__init__)(**processed_kwargs)


class IotTopicPublish(troposphere.iotevents.IotTopicPublish, Mixin):

    def __init__(self, title=None, MqttTopic=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MqttTopic=MqttTopic, **kwargs)
        (super(IotTopicPublish, self).__init__)(**processed_kwargs)


class Lambda(troposphere.iotevents.Lambda, Mixin):

    def __init__(self, title=None, FunctionArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FunctionArn=FunctionArn, **kwargs)
        (super(Lambda, self).__init__)(**processed_kwargs)


class ResetTimer(troposphere.iotevents.ResetTimer, Mixin):

    def __init__(self, title=None, TimerName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TimerName=TimerName, **kwargs)
        (super(ResetTimer, self).__init__)(**processed_kwargs)


class SetTimer(troposphere.iotevents.SetTimer, Mixin):

    def __init__(self, title=None, Seconds=NOTHING, TimerName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Seconds=Seconds, 
         TimerName=TimerName, **kwargs)
        (super(SetTimer, self).__init__)(**processed_kwargs)


class SetVariable(troposphere.iotevents.SetVariable, Mixin):

    def __init__(self, title=None, Value=NOTHING, VariableName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Value=Value, 
         VariableName=VariableName, **kwargs)
        (super(SetVariable, self).__init__)(**processed_kwargs)


class Sns(troposphere.iotevents.Sns, Mixin):

    def __init__(self, title=None, TargetArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         TargetArn=TargetArn, **kwargs)
        (super(Sns, self).__init__)(**processed_kwargs)


class Sqs(troposphere.iotevents.Sqs, Mixin):

    def __init__(self, title=None, QueueUrl=NOTHING, UseBase64=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         QueueUrl=QueueUrl, 
         UseBase64=UseBase64, **kwargs)
        (super(Sqs, self).__init__)(**processed_kwargs)


class Action(troposphere.iotevents.Action, Mixin):

    def __init__(self, title=None, ClearTimer=NOTHING, Firehose=NOTHING, IotEvents=NOTHING, IotTopicPublish=NOTHING, Lambda=NOTHING, ResetTimer=NOTHING, SetTimer=NOTHING, SetVariable=NOTHING, Sns=NOTHING, Sqs=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ClearTimer=ClearTimer, 
         Firehose=Firehose, 
         IotEvents=IotEvents, 
         IotTopicPublish=IotTopicPublish, 
         Lambda=Lambda, 
         ResetTimer=ResetTimer, 
         SetTimer=SetTimer, 
         SetVariable=SetVariable, 
         Sns=Sns, 
         Sqs=Sqs, **kwargs)
        (super(Action, self).__init__)(**processed_kwargs)


class Event(troposphere.iotevents.Event, Mixin):

    def __init__(self, title=None, Actions=NOTHING, Condition=NOTHING, EventName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Actions=Actions, 
         Condition=Condition, 
         EventName=EventName, **kwargs)
        (super(Event, self).__init__)(**processed_kwargs)


class OnEnter(troposphere.iotevents.OnEnter, Mixin):

    def __init__(self, title=None, Events=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Events=Events, **kwargs)
        (super(OnEnter, self).__init__)(**processed_kwargs)


class OnExit(troposphere.iotevents.OnExit, Mixin):

    def __init__(self, title=None, Events=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Events=Events, **kwargs)
        (super(OnExit, self).__init__)(**processed_kwargs)


class TransitionEvent(troposphere.iotevents.TransitionEvent, Mixin):

    def __init__(self, title=None, Actions=NOTHING, Condition=NOTHING, EventName=NOTHING, NextState=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Actions=Actions, 
         Condition=Condition, 
         EventName=EventName, 
         NextState=NextState, **kwargs)
        (super(TransitionEvent, self).__init__)(**processed_kwargs)


class OnInput(troposphere.iotevents.OnInput, Mixin):

    def __init__(self, title=None, Events=NOTHING, TransitionEvents=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Events=Events, 
         TransitionEvents=TransitionEvents, **kwargs)
        (super(OnInput, self).__init__)(**processed_kwargs)


class State(troposphere.iotevents.State, Mixin):

    def __init__(self, title=None, OnEnter=NOTHING, OnExit=NOTHING, OnInput=NOTHING, StateName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         OnEnter=OnEnter, 
         OnExit=OnExit, 
         OnInput=OnInput, 
         StateName=StateName, **kwargs)
        (super(State, self).__init__)(**processed_kwargs)


class DetectorModelDefinition(troposphere.iotevents.DetectorModelDefinition, Mixin):

    def __init__(self, title=None, InitialStateName=NOTHING, States=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         InitialStateName=InitialStateName, 
         States=States, **kwargs)
        (super(DetectorModelDefinition, self).__init__)(**processed_kwargs)


class DetectorModel(troposphere.iotevents.DetectorModel, Mixin):

    def __init__(self, title, template=None, validation=True, DetectorModelDefinition=NOTHING, DetectorModelDescription=NOTHING, DetectorModelName=NOTHING, Key=NOTHING, RoleArn=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DetectorModelDefinition=DetectorModelDefinition, 
         DetectorModelDescription=DetectorModelDescription, 
         DetectorModelName=DetectorModelName, 
         Key=Key, 
         RoleArn=RoleArn, 
         Tags=Tags, **kwargs)
        (super(DetectorModel, self).__init__)(**processed_kwargs)


class Attribute(troposphere.iotevents.Attribute, Mixin):

    def __init__(self, title=None, JsonPath=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         JsonPath=JsonPath, **kwargs)
        (super(Attribute, self).__init__)(**processed_kwargs)


class InputDefinition(troposphere.iotevents.InputDefinition, Mixin):

    def __init__(self, title=None, Attributes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Attributes=Attributes, **kwargs)
        (super(InputDefinition, self).__init__)(**processed_kwargs)


class Input(troposphere.iotevents.Input, Mixin):

    def __init__(self, title, template=None, validation=True, InputDefinition=NOTHING, InputDescription=NOTHING, InputName=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         InputDefinition=InputDefinition, 
         InputDescription=InputDescription, 
         InputName=InputName, 
         Tags=Tags, **kwargs)
        (super(Input, self).__init__)(**processed_kwargs)