# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/pinpoint.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 38234 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.pinpoint
from troposphere.pinpoint import APNSPushNotificationTemplate as _APNSPushNotificationTemplate, AndroidPushNotificationTemplate as _AndroidPushNotificationTemplate, Behavior as _Behavior, CampaignEmailMessage as _CampaignEmailMessage, CampaignEventFilter as _CampaignEventFilter, CampaignHook as _CampaignHook, CampaignSmsMessage as _CampaignSmsMessage, Coordinates as _Coordinates, DefaultPushNotificationTemplate as _DefaultPushNotificationTemplate, Demographic as _Demographic, EventDimensions as _EventDimensions, GPSPoint as _GPSPoint, Groups as _Groups, Limits as _Limits, Location as _Location, Message as _Message, MessageConfiguration as _MessageConfiguration, QuietTime as _QuietTime, Recency as _Recency, Schedule as _Schedule, SegmentDimensions as _SegmentDimensions, SegmentGroups as _SegmentGroups, SetDimension as _SetDimension, SourceSegments as _SourceSegments, WriteTreatmentResource as _WriteTreatmentResource
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class ADMChannel(troposphere.pinpoint.ADMChannel, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationId=REQUIRED, ClientId=REQUIRED, ClientSecret=REQUIRED, Enabled=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationId=ApplicationId, 
         ClientId=ClientId, 
         ClientSecret=ClientSecret, 
         Enabled=Enabled, **kwargs)
        (super(ADMChannel, self).__init__)(**processed_kwargs)


class APNSChannel(troposphere.pinpoint.APNSChannel, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationId=REQUIRED, BundleId=NOTHING, Certificate=NOTHING, DefaultAuthenticationMethod=NOTHING, Enabled=NOTHING, PrivateKey=NOTHING, TeamId=NOTHING, TokenKey=NOTHING, TokenKeyId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationId=ApplicationId, 
         BundleId=BundleId, 
         Certificate=Certificate, 
         DefaultAuthenticationMethod=DefaultAuthenticationMethod, 
         Enabled=Enabled, 
         PrivateKey=PrivateKey, 
         TeamId=TeamId, 
         TokenKey=TokenKey, 
         TokenKeyId=TokenKeyId, **kwargs)
        (super(APNSChannel, self).__init__)(**processed_kwargs)


class APNSSandboxChannel(troposphere.pinpoint.APNSSandboxChannel, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationId=REQUIRED, BundleId=NOTHING, Certificate=NOTHING, DefaultAuthenticationMethod=NOTHING, Enabled=NOTHING, PrivateKey=NOTHING, TeamId=NOTHING, TokenKey=NOTHING, TokenKeyId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationId=ApplicationId, 
         BundleId=BundleId, 
         Certificate=Certificate, 
         DefaultAuthenticationMethod=DefaultAuthenticationMethod, 
         Enabled=Enabled, 
         PrivateKey=PrivateKey, 
         TeamId=TeamId, 
         TokenKey=TokenKey, 
         TokenKeyId=TokenKeyId, **kwargs)
        (super(APNSSandboxChannel, self).__init__)(**processed_kwargs)


class APNSVoipChannel(troposphere.pinpoint.APNSVoipChannel, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationId=REQUIRED, BundleId=NOTHING, Certificate=NOTHING, DefaultAuthenticationMethod=NOTHING, Enabled=NOTHING, PrivateKey=NOTHING, TeamId=NOTHING, TokenKey=NOTHING, TokenKeyId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationId=ApplicationId, 
         BundleId=BundleId, 
         Certificate=Certificate, 
         DefaultAuthenticationMethod=DefaultAuthenticationMethod, 
         Enabled=Enabled, 
         PrivateKey=PrivateKey, 
         TeamId=TeamId, 
         TokenKey=TokenKey, 
         TokenKeyId=TokenKeyId, **kwargs)
        (super(APNSVoipChannel, self).__init__)(**processed_kwargs)


class APNSVoipSandboxChannel(troposphere.pinpoint.APNSVoipSandboxChannel, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationId=REQUIRED, BundleId=NOTHING, Certificate=NOTHING, DefaultAuthenticationMethod=NOTHING, Enabled=NOTHING, PrivateKey=NOTHING, TeamId=NOTHING, TokenKey=NOTHING, TokenKeyId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationId=ApplicationId, 
         BundleId=BundleId, 
         Certificate=Certificate, 
         DefaultAuthenticationMethod=DefaultAuthenticationMethod, 
         Enabled=Enabled, 
         PrivateKey=PrivateKey, 
         TeamId=TeamId, 
         TokenKey=TokenKey, 
         TokenKeyId=TokenKeyId, **kwargs)
        (super(APNSVoipSandboxChannel, self).__init__)(**processed_kwargs)


class App(troposphere.pinpoint.App, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         Tags=Tags, **kwargs)
        (super(App, self).__init__)(**processed_kwargs)


class CampaignHook(troposphere.pinpoint.CampaignHook, Mixin):

    def __init__(self, title=None, LambdaFunctionName=NOTHING, Mode=NOTHING, WebUrl=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         LambdaFunctionName=LambdaFunctionName, 
         Mode=Mode, 
         WebUrl=WebUrl, **kwargs)
        (super(CampaignHook, self).__init__)(**processed_kwargs)


class Limits(troposphere.pinpoint.Limits, Mixin):

    def __init__(self, title=None, Daily=NOTHING, MaximumDuration=NOTHING, MessagesPerSecond=NOTHING, Total=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Daily=Daily, 
         MaximumDuration=MaximumDuration, 
         MessagesPerSecond=MessagesPerSecond, 
         Total=Total, **kwargs)
        (super(Limits, self).__init__)(**processed_kwargs)


class QuietTime(troposphere.pinpoint.QuietTime, Mixin):

    def __init__(self, title=None, End=REQUIRED, Start=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         End=End, 
         Start=Start, **kwargs)
        (super(QuietTime, self).__init__)(**processed_kwargs)


class ApplicationSettings(troposphere.pinpoint.ApplicationSettings, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationId=REQUIRED, CampaignHook=NOTHING, CloudWatchMetricsEnabled=NOTHING, Limits=NOTHING, QuietTime=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationId=ApplicationId, 
         CampaignHook=CampaignHook, 
         CloudWatchMetricsEnabled=CloudWatchMetricsEnabled, 
         Limits=Limits, 
         QuietTime=QuietTime, **kwargs)
        (super(ApplicationSettings, self).__init__)(**processed_kwargs)


class BaiduChannel(troposphere.pinpoint.BaiduChannel, Mixin):

    def __init__(self, title, template=None, validation=True, ApiKey=REQUIRED, ApplicationId=REQUIRED, SecretKey=REQUIRED, Enabled=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiKey=ApiKey, 
         ApplicationId=ApplicationId, 
         SecretKey=SecretKey, 
         Enabled=Enabled, **kwargs)
        (super(BaiduChannel, self).__init__)(**processed_kwargs)


class CampaignEmailMessage(troposphere.pinpoint.CampaignEmailMessage, Mixin):

    def __init__(self, title=None, Body=NOTHING, FromAddress=NOTHING, HtmlBody=NOTHING, Title=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Body=Body, 
         FromAddress=FromAddress, 
         HtmlBody=HtmlBody, 
         Title=Title, **kwargs)
        (super(CampaignEmailMessage, self).__init__)(**processed_kwargs)


class CampaignSmsMessage(troposphere.pinpoint.CampaignSmsMessage, Mixin):

    def __init__(self, title=None, Body=NOTHING, MessageType=NOTHING, SenderId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Body=Body, 
         MessageType=MessageType, 
         SenderId=SenderId, **kwargs)
        (super(CampaignSmsMessage, self).__init__)(**processed_kwargs)


class Message(troposphere.pinpoint.Message, Mixin):

    def __init__(self, title=None, Action=NOTHING, Body=NOTHING, ImageIconUrl=NOTHING, ImageSmallIconUrl=NOTHING, ImageUrl=NOTHING, JsonBody=NOTHING, MediaUrl=NOTHING, RawContent=NOTHING, SilentPush=NOTHING, TimeToLive=NOTHING, Title=NOTHING, Url=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Action=Action, 
         Body=Body, 
         ImageIconUrl=ImageIconUrl, 
         ImageSmallIconUrl=ImageSmallIconUrl, 
         ImageUrl=ImageUrl, 
         JsonBody=JsonBody, 
         MediaUrl=MediaUrl, 
         RawContent=RawContent, 
         SilentPush=SilentPush, 
         TimeToLive=TimeToLive, 
         Title=Title, 
         Url=Url, **kwargs)
        (super(Message, self).__init__)(**processed_kwargs)


class MessageConfiguration(troposphere.pinpoint.MessageConfiguration, Mixin):

    def __init__(self, title=None, ADMMessage=NOTHING, APNSMessage=NOTHING, BaiduMessage=NOTHING, DefaultMessage=NOTHING, EmailMessage=NOTHING, GCMMessage=NOTHING, SMSMessage=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ADMMessage=ADMMessage, 
         APNSMessage=APNSMessage, 
         BaiduMessage=BaiduMessage, 
         DefaultMessage=DefaultMessage, 
         EmailMessage=EmailMessage, 
         GCMMessage=GCMMessage, 
         SMSMessage=SMSMessage, **kwargs)
        (super(MessageConfiguration, self).__init__)(**processed_kwargs)


class SetDimension(troposphere.pinpoint.SetDimension, Mixin):

    def __init__(self, title=None, DimensionType=NOTHING, Values=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DimensionType=DimensionType, 
         Values=Values, **kwargs)
        (super(SetDimension, self).__init__)(**processed_kwargs)


class EventDimensions(troposphere.pinpoint.EventDimensions, Mixin):

    def __init__(self, title=None, Attributes=NOTHING, EventType=NOTHING, Metrics=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Attributes=Attributes, 
         EventType=EventType, 
         Metrics=Metrics, **kwargs)
        (super(EventDimensions, self).__init__)(**processed_kwargs)


class CampaignEventFilter(troposphere.pinpoint.CampaignEventFilter, Mixin):

    def __init__(self, title=None, Dimensions=NOTHING, FilterType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Dimensions=Dimensions, 
         FilterType=FilterType, **kwargs)
        (super(CampaignEventFilter, self).__init__)(**processed_kwargs)


class Schedule(troposphere.pinpoint.Schedule, Mixin):

    def __init__(self, title=None, EndTime=NOTHING, EventFilter=NOTHING, Frequency=NOTHING, IsLocalTime=NOTHING, QuietTime=NOTHING, StartTime=NOTHING, TimeZone=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EndTime=EndTime, 
         EventFilter=EventFilter, 
         Frequency=Frequency, 
         IsLocalTime=IsLocalTime, 
         QuietTime=QuietTime, 
         StartTime=StartTime, 
         TimeZone=TimeZone, **kwargs)
        (super(Schedule, self).__init__)(**processed_kwargs)


class WriteTreatmentResource(troposphere.pinpoint.WriteTreatmentResource, Mixin):

    def __init__(self, title=None, MessageConfiguration=NOTHING, Schedule=NOTHING, SizePercent=NOTHING, TreatmentDescription=NOTHING, TreatmentName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         MessageConfiguration=MessageConfiguration, 
         Schedule=Schedule, 
         SizePercent=SizePercent, 
         TreatmentDescription=TreatmentDescription, 
         TreatmentName=TreatmentName, **kwargs)
        (super(WriteTreatmentResource, self).__init__)(**processed_kwargs)


class Campaign(troposphere.pinpoint.Campaign, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationId=REQUIRED, MessageConfiguration=REQUIRED, Name=REQUIRED, Schedule=REQUIRED, SegmentId=REQUIRED, AdditionalTreatments=NOTHING, CampaignHook=NOTHING, Description=NOTHING, HoldoutPercent=NOTHING, IsPaused=NOTHING, Limits=NOTHING, SegmentVersion=NOTHING, Tags=NOTHING, TreatmentDescription=NOTHING, TreatmentName=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationId=ApplicationId, 
         MessageConfiguration=MessageConfiguration, 
         Name=Name, 
         Schedule=Schedule, 
         SegmentId=SegmentId, 
         AdditionalTreatments=AdditionalTreatments, 
         CampaignHook=CampaignHook, 
         Description=Description, 
         HoldoutPercent=HoldoutPercent, 
         IsPaused=IsPaused, 
         Limits=Limits, 
         SegmentVersion=SegmentVersion, 
         Tags=Tags, 
         TreatmentDescription=TreatmentDescription, 
         TreatmentName=TreatmentName, **kwargs)
        (super(Campaign, self).__init__)(**processed_kwargs)


class EmailChannel(troposphere.pinpoint.EmailChannel, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationId=REQUIRED, FromAddress=REQUIRED, Identity=REQUIRED, ConfigurationSet=NOTHING, Enabled=NOTHING, RoleArn=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationId=ApplicationId, 
         FromAddress=FromAddress, 
         Identity=Identity, 
         ConfigurationSet=ConfigurationSet, 
         Enabled=Enabled, 
         RoleArn=RoleArn, **kwargs)
        (super(EmailChannel, self).__init__)(**processed_kwargs)


class EmailTemplate(troposphere.pinpoint.EmailTemplate, Mixin):

    def __init__(self, title, template=None, validation=True, Subject=REQUIRED, TemplateName=REQUIRED, HtmlPart=NOTHING, Tags=NOTHING, TextPart=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Subject=Subject, 
         TemplateName=TemplateName, 
         HtmlPart=HtmlPart, 
         Tags=Tags, 
         TextPart=TextPart, **kwargs)
        (super(EmailTemplate, self).__init__)(**processed_kwargs)


class EventStream(troposphere.pinpoint.EventStream, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationId=REQUIRED, DestinationStreamArn=REQUIRED, RoleArn=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationId=ApplicationId, 
         DestinationStreamArn=DestinationStreamArn, 
         RoleArn=RoleArn, **kwargs)
        (super(EventStream, self).__init__)(**processed_kwargs)


class GCMChannel(troposphere.pinpoint.GCMChannel, Mixin):

    def __init__(self, title, template=None, validation=True, ApiKey=REQUIRED, ApplicationId=REQUIRED, Enabled=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApiKey=ApiKey, 
         ApplicationId=ApplicationId, 
         Enabled=Enabled, **kwargs)
        (super(GCMChannel, self).__init__)(**processed_kwargs)


class APNSPushNotificationTemplate(troposphere.pinpoint.APNSPushNotificationTemplate, Mixin):

    def __init__(self, title=None, Action=NOTHING, Body=NOTHING, MediaUrl=NOTHING, Sound=NOTHING, Title=NOTHING, Url=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Action=Action, 
         Body=Body, 
         MediaUrl=MediaUrl, 
         Sound=Sound, 
         Title=Title, 
         Url=Url, **kwargs)
        (super(APNSPushNotificationTemplate, self).__init__)(**processed_kwargs)


class AndroidPushNotificationTemplate(troposphere.pinpoint.AndroidPushNotificationTemplate, Mixin):

    def __init__(self, title=None, Action=NOTHING, Body=NOTHING, ImageIconUrl=NOTHING, ImageUrl=NOTHING, SmallImageIconUrl=NOTHING, Sound=NOTHING, Title=NOTHING, Url=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Action=Action, 
         Body=Body, 
         ImageIconUrl=ImageIconUrl, 
         ImageUrl=ImageUrl, 
         SmallImageIconUrl=SmallImageIconUrl, 
         Sound=Sound, 
         Title=Title, 
         Url=Url, **kwargs)
        (super(AndroidPushNotificationTemplate, self).__init__)(**processed_kwargs)


class DefaultPushNotificationTemplate(troposphere.pinpoint.DefaultPushNotificationTemplate, Mixin):

    def __init__(self, title=None, Action=NOTHING, Body=NOTHING, Sound=NOTHING, Title=NOTHING, Url=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Action=Action, 
         Body=Body, 
         Sound=Sound, 
         Title=Title, 
         Url=Url, **kwargs)
        (super(DefaultPushNotificationTemplate, self).__init__)(**processed_kwargs)


class PushTemplate(troposphere.pinpoint.PushTemplate, Mixin):

    def __init__(self, title, template=None, validation=True, TemplateName=REQUIRED, ADM=NOTHING, APNS=NOTHING, Baidu=NOTHING, Default=NOTHING, GCM=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         TemplateName=TemplateName, 
         ADM=ADM, 
         APNS=APNS, 
         Baidu=Baidu, 
         Default=Default, 
         GCM=GCM, 
         Tags=Tags, **kwargs)
        (super(PushTemplate, self).__init__)(**processed_kwargs)


class SMSChannel(troposphere.pinpoint.SMSChannel, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationId=REQUIRED, Enabled=NOTHING, SenderId=NOTHING, ShortCode=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationId=ApplicationId, 
         Enabled=Enabled, 
         SenderId=SenderId, 
         ShortCode=ShortCode, **kwargs)
        (super(SMSChannel, self).__init__)(**processed_kwargs)


class Recency(troposphere.pinpoint.Recency, Mixin):

    def __init__(self, title=None, Duration=REQUIRED, RecencyType=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Duration=Duration, 
         RecencyType=RecencyType, **kwargs)
        (super(Recency, self).__init__)(**processed_kwargs)


class Behavior(troposphere.pinpoint.Behavior, Mixin):

    def __init__(self, title=None, Recency=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Recency=Recency, **kwargs)
        (super(Behavior, self).__init__)(**processed_kwargs)


class Demographic(troposphere.pinpoint.Demographic, Mixin):

    def __init__(self, title=None, AppVersion=NOTHING, Channel=NOTHING, DeviceType=NOTHING, Make=NOTHING, Model=NOTHING, Platform=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AppVersion=AppVersion, 
         Channel=Channel, 
         DeviceType=DeviceType, 
         Make=Make, 
         Model=Model, 
         Platform=Platform, **kwargs)
        (super(Demographic, self).__init__)(**processed_kwargs)


class Coordinates(troposphere.pinpoint.Coordinates, Mixin):

    def __init__(self, title=None, Latitude=REQUIRED, Longitude=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Latitude=Latitude, 
         Longitude=Longitude, **kwargs)
        (super(Coordinates, self).__init__)(**processed_kwargs)


class GPSPoint(troposphere.pinpoint.GPSPoint, Mixin):

    def __init__(self, title=None, Coordinates=REQUIRED, RangeInKilometers=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Coordinates=Coordinates, 
         RangeInKilometers=RangeInKilometers, **kwargs)
        (super(GPSPoint, self).__init__)(**processed_kwargs)


class Location(troposphere.pinpoint.Location, Mixin):

    def __init__(self, title=None, Country=NOTHING, GPSPoint=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Country=Country, 
         GPSPoint=GPSPoint, **kwargs)
        (super(Location, self).__init__)(**processed_kwargs)


class SegmentDimensions(troposphere.pinpoint.SegmentDimensions, Mixin):

    def __init__(self, title=None, Attributes=NOTHING, Behavior=NOTHING, Demographic=NOTHING, Location=NOTHING, Metrics=NOTHING, UserAttributes=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Attributes=Attributes, 
         Behavior=Behavior, 
         Demographic=Demographic, 
         Location=Location, 
         Metrics=Metrics, 
         UserAttributes=UserAttributes, **kwargs)
        (super(SegmentDimensions, self).__init__)(**processed_kwargs)


class SourceSegments(troposphere.pinpoint.SourceSegments, Mixin):

    def __init__(self, title=None, Id=REQUIRED, Version=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Id=Id, 
         Version=Version, **kwargs)
        (super(SourceSegments, self).__init__)(**processed_kwargs)


class Groups(troposphere.pinpoint.Groups, Mixin):

    def __init__(self, title=None, Dimensions=NOTHING, SourceSegments=NOTHING, SourceType=NOTHING, Type=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Dimensions=Dimensions, 
         SourceSegments=SourceSegments, 
         SourceType=SourceType, 
         Type=Type, **kwargs)
        (super(Groups, self).__init__)(**processed_kwargs)


class SegmentGroups(troposphere.pinpoint.SegmentGroups, Mixin):

    def __init__(self, title=None, Groups=NOTHING, Include=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Groups=Groups, 
         Include=Include, **kwargs)
        (super(SegmentGroups, self).__init__)(**processed_kwargs)


class Segment(troposphere.pinpoint.Segment, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationId=REQUIRED, Name=REQUIRED, Dimensions=NOTHING, SegmentGroups=NOTHING, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationId=ApplicationId, 
         Name=Name, 
         Dimensions=Dimensions, 
         SegmentGroups=SegmentGroups, 
         Tags=Tags, **kwargs)
        (super(Segment, self).__init__)(**processed_kwargs)


class SmsTemplate(troposphere.pinpoint.SmsTemplate, Mixin):

    def __init__(self, title, template=None, validation=True, Body=REQUIRED, TemplateName=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Body=Body, 
         TemplateName=TemplateName, 
         Tags=Tags, **kwargs)
        (super(SmsTemplate, self).__init__)(**processed_kwargs)


class VoiceChannel(troposphere.pinpoint.VoiceChannel, Mixin):

    def __init__(self, title, template=None, validation=True, ApplicationId=REQUIRED, Enabled=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         ApplicationId=ApplicationId, 
         Enabled=Enabled, **kwargs)
        (super(VoiceChannel, self).__init__)(**processed_kwargs)