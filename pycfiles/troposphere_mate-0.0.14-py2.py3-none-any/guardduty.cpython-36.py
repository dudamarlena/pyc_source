# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/guardduty.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 7199 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.guardduty
from troposphere.guardduty import Condition as _Condition, FindingCriteria as _FindingCriteria
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Detector(troposphere.guardduty.Detector, Mixin):

    def __init__(self, title, template=None, validation=True, Enable=REQUIRED, FindingPublishingFrequency=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Enable=Enable, 
         FindingPublishingFrequency=FindingPublishingFrequency, **kwargs)
        (super(Detector, self).__init__)(**processed_kwargs)


class Condition(troposphere.guardduty.Condition, Mixin):

    def __init__(self, title=None, Eq=NOTHING, Gte=NOTHING, Lt=NOTHING, Lte=NOTHING, Neq=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Eq=Eq, 
         Gte=Gte, 
         Lt=Lt, 
         Lte=Lte, 
         Neq=Neq, **kwargs)
        (super(Condition, self).__init__)(**processed_kwargs)


class FindingCriteria(troposphere.guardduty.FindingCriteria, Mixin):

    def __init__(self, title=None, Criterion=NOTHING, ItemType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Criterion=Criterion, 
         ItemType=ItemType, **kwargs)
        (super(FindingCriteria, self).__init__)(**processed_kwargs)


class Filter(troposphere.guardduty.Filter, Mixin):

    def __init__(self, title, template=None, validation=True, Action=REQUIRED, Description=REQUIRED, DetectorId=REQUIRED, FindingCriteria=REQUIRED, Rank=REQUIRED, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Action=Action, 
         Description=Description, 
         DetectorId=DetectorId, 
         FindingCriteria=FindingCriteria, 
         Rank=Rank, 
         Name=Name, **kwargs)
        (super(Filter, self).__init__)(**processed_kwargs)


class IPSet(troposphere.guardduty.IPSet, Mixin):

    def __init__(self, title, template=None, validation=True, Activate=REQUIRED, DetectorId=REQUIRED, Format=REQUIRED, Location=REQUIRED, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Activate=Activate, 
         DetectorId=DetectorId, 
         Format=Format, 
         Location=Location, 
         Name=Name, **kwargs)
        (super(IPSet, self).__init__)(**processed_kwargs)


class Master(troposphere.guardduty.Master, Mixin):

    def __init__(self, title, template=None, validation=True, DetectorId=REQUIRED, MasterId=REQUIRED, InvitationId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DetectorId=DetectorId, 
         MasterId=MasterId, 
         InvitationId=InvitationId, **kwargs)
        (super(Master, self).__init__)(**processed_kwargs)


class Member(troposphere.guardduty.Member, Mixin):

    def __init__(self, title, template=None, validation=True, DetectorId=REQUIRED, Email=REQUIRED, MemberId=REQUIRED, Message=NOTHING, Status=NOTHING, DisableEmailNotification=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DetectorId=DetectorId, 
         Email=Email, 
         MemberId=MemberId, 
         Message=Message, 
         Status=Status, 
         DisableEmailNotification=DisableEmailNotification, **kwargs)
        (super(Member, self).__init__)(**processed_kwargs)


class ThreatIntelSet(troposphere.guardduty.ThreatIntelSet, Mixin):

    def __init__(self, title, template=None, validation=True, Activate=REQUIRED, DetectorId=REQUIRED, Format=REQUIRED, Location=REQUIRED, Name=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Activate=Activate, 
         DetectorId=DetectorId, 
         Format=Format, 
         Location=Location, 
         Name=Name, **kwargs)
        (super(ThreatIntelSet, self).__init__)(**processed_kwargs)