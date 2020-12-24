# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/cloudfront.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 19505 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.cloudfront
from troposphere.cloudfront import CacheBehavior as _CacheBehavior, CloudFrontOriginAccessIdentityConfig as _CloudFrontOriginAccessIdentityConfig, Cookies as _Cookies, CustomErrorResponse as _CustomErrorResponse, CustomOriginConfig as _CustomOriginConfig, DefaultCacheBehavior as _DefaultCacheBehavior, DistributionConfig as _DistributionConfig, ForwardedValues as _ForwardedValues, GeoRestriction as _GeoRestriction, LambdaFunctionAssociation as _LambdaFunctionAssociation, Logging as _Logging, Origin as _Origin, OriginCustomHeader as _OriginCustomHeader, Restrictions as _Restrictions, S3Origin as _S3Origin, S3OriginConfig as _S3OriginConfig, StreamingDistributionConfig as _StreamingDistributionConfig, Tags as _Tags, TrustedSigners as _TrustedSigners, ViewerCertificate as _ViewerCertificate
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Cookies(troposphere.cloudfront.Cookies, Mixin):

    def __init__(self, title=None, Forward=REQUIRED, WhitelistedNames=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Forward=Forward, 
         WhitelistedNames=WhitelistedNames, **kwargs)
        (super(Cookies, self).__init__)(**processed_kwargs)


class ForwardedValues(troposphere.cloudfront.ForwardedValues, Mixin):

    def __init__(self, title=None, QueryString=REQUIRED, Cookies=NOTHING, Headers=NOTHING, QueryStringCacheKeys=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         QueryString=QueryString, 
         Cookies=Cookies, 
         Headers=Headers, 
         QueryStringCacheKeys=QueryStringCacheKeys, **kwargs)
        (super(ForwardedValues, self).__init__)(**processed_kwargs)


class LambdaFunctionAssociation(troposphere.cloudfront.LambdaFunctionAssociation, Mixin):

    def __init__(self, title=None, EventType=NOTHING, LambdaFunctionARN=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         EventType=EventType, 
         LambdaFunctionARN=LambdaFunctionARN, **kwargs)
        (super(LambdaFunctionAssociation, self).__init__)(**processed_kwargs)


class CacheBehavior(troposphere.cloudfront.CacheBehavior, Mixin):

    def __init__(self, title=None, ForwardedValues=REQUIRED, PathPattern=REQUIRED, TargetOriginId=REQUIRED, ViewerProtocolPolicy=REQUIRED, AllowedMethods=NOTHING, CachedMethods=NOTHING, Compress=NOTHING, DefaultTTL=NOTHING, FieldLevelEncryptionId=NOTHING, LambdaFunctionAssociations=NOTHING, MaxTTL=NOTHING, MinTTL=NOTHING, SmoothStreaming=NOTHING, TrustedSigners=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ForwardedValues=ForwardedValues, 
         PathPattern=PathPattern, 
         TargetOriginId=TargetOriginId, 
         ViewerProtocolPolicy=ViewerProtocolPolicy, 
         AllowedMethods=AllowedMethods, 
         CachedMethods=CachedMethods, 
         Compress=Compress, 
         DefaultTTL=DefaultTTL, 
         FieldLevelEncryptionId=FieldLevelEncryptionId, 
         LambdaFunctionAssociations=LambdaFunctionAssociations, 
         MaxTTL=MaxTTL, 
         MinTTL=MinTTL, 
         SmoothStreaming=SmoothStreaming, 
         TrustedSigners=TrustedSigners, **kwargs)
        (super(CacheBehavior, self).__init__)(**processed_kwargs)


class DefaultCacheBehavior(troposphere.cloudfront.DefaultCacheBehavior, Mixin):

    def __init__(self, title=None, ForwardedValues=REQUIRED, TargetOriginId=REQUIRED, ViewerProtocolPolicy=REQUIRED, AllowedMethods=NOTHING, CachedMethods=NOTHING, Compress=NOTHING, DefaultTTL=NOTHING, FieldLevelEncryptionId=NOTHING, LambdaFunctionAssociations=NOTHING, MaxTTL=NOTHING, MinTTL=NOTHING, SmoothStreaming=NOTHING, TrustedSigners=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ForwardedValues=ForwardedValues, 
         TargetOriginId=TargetOriginId, 
         ViewerProtocolPolicy=ViewerProtocolPolicy, 
         AllowedMethods=AllowedMethods, 
         CachedMethods=CachedMethods, 
         Compress=Compress, 
         DefaultTTL=DefaultTTL, 
         FieldLevelEncryptionId=FieldLevelEncryptionId, 
         LambdaFunctionAssociations=LambdaFunctionAssociations, 
         MaxTTL=MaxTTL, 
         MinTTL=MinTTL, 
         SmoothStreaming=SmoothStreaming, 
         TrustedSigners=TrustedSigners, **kwargs)
        (super(DefaultCacheBehavior, self).__init__)(**processed_kwargs)


class S3Origin(troposphere.cloudfront.S3Origin, Mixin):

    def __init__(self, title=None, DomainName=REQUIRED, OriginAccessIdentity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DomainName=DomainName, 
         OriginAccessIdentity=OriginAccessIdentity, **kwargs)
        (super(S3Origin, self).__init__)(**processed_kwargs)


class CustomOriginConfig(troposphere.cloudfront.CustomOriginConfig, Mixin):

    def __init__(self, title=None, OriginProtocolPolicy=REQUIRED, HTTPPort=NOTHING, HTTPSPort=NOTHING, OriginKeepaliveTimeout=NOTHING, OriginReadTimeout=NOTHING, OriginSSLProtocols=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         OriginProtocolPolicy=OriginProtocolPolicy, 
         HTTPPort=HTTPPort, 
         HTTPSPort=HTTPSPort, 
         OriginKeepaliveTimeout=OriginKeepaliveTimeout, 
         OriginReadTimeout=OriginReadTimeout, 
         OriginSSLProtocols=OriginSSLProtocols, **kwargs)
        (super(CustomOriginConfig, self).__init__)(**processed_kwargs)


class OriginCustomHeader(troposphere.cloudfront.OriginCustomHeader, Mixin):

    def __init__(self, title=None, HeaderName=REQUIRED, HeaderValue=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         HeaderName=HeaderName, 
         HeaderValue=HeaderValue, **kwargs)
        (super(OriginCustomHeader, self).__init__)(**processed_kwargs)


class S3OriginConfig(troposphere.cloudfront.S3OriginConfig, Mixin):

    def __init__(self, title=None, OriginAccessIdentity=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         OriginAccessIdentity=OriginAccessIdentity, **kwargs)
        (super(S3OriginConfig, self).__init__)(**processed_kwargs)


class Origin(troposphere.cloudfront.Origin, Mixin):

    def __init__(self, title=None, DomainName=REQUIRED, Id=REQUIRED, CustomOriginConfig=NOTHING, OriginCustomHeaders=NOTHING, OriginPath=NOTHING, S3OriginConfig=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DomainName=DomainName, 
         Id=Id, 
         CustomOriginConfig=CustomOriginConfig, 
         OriginCustomHeaders=OriginCustomHeaders, 
         OriginPath=OriginPath, 
         S3OriginConfig=S3OriginConfig, **kwargs)
        (super(Origin, self).__init__)(**processed_kwargs)


class Logging(troposphere.cloudfront.Logging, Mixin):

    def __init__(self, title=None, Bucket=REQUIRED, IncludeCookies=NOTHING, Prefix=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Bucket=Bucket, 
         IncludeCookies=IncludeCookies, 
         Prefix=Prefix, **kwargs)
        (super(Logging, self).__init__)(**processed_kwargs)


class CustomErrorResponse(troposphere.cloudfront.CustomErrorResponse, Mixin):

    def __init__(self, title=None, ErrorCode=REQUIRED, ErrorCachingMinTTL=NOTHING, ResponseCode=NOTHING, ResponsePagePath=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ErrorCode=ErrorCode, 
         ErrorCachingMinTTL=ErrorCachingMinTTL, 
         ResponseCode=ResponseCode, 
         ResponsePagePath=ResponsePagePath, **kwargs)
        (super(CustomErrorResponse, self).__init__)(**processed_kwargs)


class GeoRestriction(troposphere.cloudfront.GeoRestriction, Mixin):

    def __init__(self, title=None, RestrictionType=REQUIRED, Locations=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         RestrictionType=RestrictionType, 
         Locations=Locations, **kwargs)
        (super(GeoRestriction, self).__init__)(**processed_kwargs)


class Restrictions(troposphere.cloudfront.Restrictions, Mixin):

    def __init__(self, title=None, GeoRestriction=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         GeoRestriction=GeoRestriction, **kwargs)
        (super(Restrictions, self).__init__)(**processed_kwargs)


class ViewerCertificate(troposphere.cloudfront.ViewerCertificate, Mixin):

    def __init__(self, title=None, AcmCertificateArn=NOTHING, CloudFrontDefaultCertificate=NOTHING, IamCertificateId=NOTHING, MinimumProtocolVersion=NOTHING, SslSupportMethod=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         AcmCertificateArn=AcmCertificateArn, 
         CloudFrontDefaultCertificate=CloudFrontDefaultCertificate, 
         IamCertificateId=IamCertificateId, 
         MinimumProtocolVersion=MinimumProtocolVersion, 
         SslSupportMethod=SslSupportMethod, **kwargs)
        (super(ViewerCertificate, self).__init__)(**processed_kwargs)


class DistributionConfig(troposphere.cloudfront.DistributionConfig, Mixin):

    def __init__(self, title=None, DefaultCacheBehavior=REQUIRED, Enabled=REQUIRED, Origins=REQUIRED, Aliases=NOTHING, CacheBehaviors=NOTHING, Comment=NOTHING, CustomErrorResponses=NOTHING, DefaultRootObject=NOTHING, HttpVersion=NOTHING, IPV6Enabled=NOTHING, Logging=NOTHING, PriceClass=NOTHING, Restrictions=NOTHING, ViewerCertificate=NOTHING, WebACLId=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DefaultCacheBehavior=DefaultCacheBehavior, 
         Enabled=Enabled, 
         Origins=Origins, 
         Aliases=Aliases, 
         CacheBehaviors=CacheBehaviors, 
         Comment=Comment, 
         CustomErrorResponses=CustomErrorResponses, 
         DefaultRootObject=DefaultRootObject, 
         HttpVersion=HttpVersion, 
         IPV6Enabled=IPV6Enabled, 
         Logging=Logging, 
         PriceClass=PriceClass, 
         Restrictions=Restrictions, 
         ViewerCertificate=ViewerCertificate, 
         WebACLId=WebACLId, **kwargs)
        (super(DistributionConfig, self).__init__)(**processed_kwargs)


class Distribution(troposphere.cloudfront.Distribution, Mixin):

    def __init__(self, title, template=None, validation=True, DistributionConfig=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DistributionConfig=DistributionConfig, 
         Tags=Tags, **kwargs)
        (super(Distribution, self).__init__)(**processed_kwargs)


class CloudFrontOriginAccessIdentityConfig(troposphere.cloudfront.CloudFrontOriginAccessIdentityConfig, Mixin):

    def __init__(self, title=None, Comment=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Comment=Comment, **kwargs)
        (super(CloudFrontOriginAccessIdentityConfig, self).__init__)(**processed_kwargs)


class CloudFrontOriginAccessIdentity(troposphere.cloudfront.CloudFrontOriginAccessIdentity, Mixin):

    def __init__(self, title, template=None, validation=True, CloudFrontOriginAccessIdentityConfig=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         CloudFrontOriginAccessIdentityConfig=CloudFrontOriginAccessIdentityConfig, **kwargs)
        (super(CloudFrontOriginAccessIdentity, self).__init__)(**processed_kwargs)


class TrustedSigners(troposphere.cloudfront.TrustedSigners, Mixin):

    def __init__(self, title=None, Enabled=REQUIRED, AwsAccountNumbers=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Enabled=Enabled, 
         AwsAccountNumbers=AwsAccountNumbers, **kwargs)
        (super(TrustedSigners, self).__init__)(**processed_kwargs)


class StreamingDistributionConfig(troposphere.cloudfront.StreamingDistributionConfig, Mixin):

    def __init__(self, title=None, Comment=REQUIRED, Enabled=REQUIRED, S3Origin=REQUIRED, TrustedSigners=REQUIRED, Aliases=NOTHING, Logging=NOTHING, PriceClass=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Comment=Comment, 
         Enabled=Enabled, 
         S3Origin=S3Origin, 
         TrustedSigners=TrustedSigners, 
         Aliases=Aliases, 
         Logging=Logging, 
         PriceClass=PriceClass, **kwargs)
        (super(StreamingDistributionConfig, self).__init__)(**processed_kwargs)


class StreamingDistribution(troposphere.cloudfront.StreamingDistribution, Mixin):

    def __init__(self, title, template=None, validation=True, StreamingDistributionConfig=REQUIRED, Tags=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         StreamingDistributionConfig=StreamingDistributionConfig, 
         Tags=Tags, **kwargs)
        (super(StreamingDistribution, self).__init__)(**processed_kwargs)