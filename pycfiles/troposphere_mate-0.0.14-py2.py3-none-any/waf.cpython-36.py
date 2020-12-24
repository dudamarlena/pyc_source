# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/waf.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 11060 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.waf
from troposphere.waf import Action as _Action, ByteMatchTuples as _ByteMatchTuples, FieldToMatch as _FieldToMatch, IPSetDescriptors as _IPSetDescriptors, Predicates as _Predicates, Rules as _Rules, SizeConstraint as _SizeConstraint, SqlInjectionMatchTuples as _SqlInjectionMatchTuples, XssMatchTuple as _XssMatchTuple
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class Action(troposphere.waf.Action, Mixin):

    def __init__(self, title=None, Type=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, **kwargs)
        (super(Action, self).__init__)(**processed_kwargs)


class FieldToMatch(troposphere.waf.FieldToMatch, Mixin):

    def __init__(self, title=None, Type=REQUIRED, Data=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Data=Data, **kwargs)
        (super(FieldToMatch, self).__init__)(**processed_kwargs)


class ByteMatchTuples(troposphere.waf.ByteMatchTuples, Mixin):

    def __init__(self, title=None, FieldToMatch=REQUIRED, PositionalConstraint=REQUIRED, TextTransformation=REQUIRED, TargetString=NOTHING, TargetStringBase64=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FieldToMatch=FieldToMatch, 
         PositionalConstraint=PositionalConstraint, 
         TextTransformation=TextTransformation, 
         TargetString=TargetString, 
         TargetStringBase64=TargetStringBase64, **kwargs)
        (super(ByteMatchTuples, self).__init__)(**processed_kwargs)


class IPSetDescriptors(troposphere.waf.IPSetDescriptors, Mixin):

    def __init__(self, title=None, Type=REQUIRED, Value=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Type=Type, 
         Value=Value, **kwargs)
        (super(IPSetDescriptors, self).__init__)(**processed_kwargs)


class Predicates(troposphere.waf.Predicates, Mixin):

    def __init__(self, title=None, DataId=REQUIRED, Negated=REQUIRED, Type=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         DataId=DataId, 
         Negated=Negated, 
         Type=Type, **kwargs)
        (super(Predicates, self).__init__)(**processed_kwargs)


class Rules(troposphere.waf.Rules, Mixin):

    def __init__(self, title=None, Action=REQUIRED, Priority=REQUIRED, RuleId=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Action=Action, 
         Priority=Priority, 
         RuleId=RuleId, **kwargs)
        (super(Rules, self).__init__)(**processed_kwargs)


class SqlInjectionMatchTuples(troposphere.waf.SqlInjectionMatchTuples, Mixin):

    def __init__(self, title=None, FieldToMatch=REQUIRED, TextTransformation=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FieldToMatch=FieldToMatch, 
         TextTransformation=TextTransformation, **kwargs)
        (super(SqlInjectionMatchTuples, self).__init__)(**processed_kwargs)


class ByteMatchSet(troposphere.waf.ByteMatchSet, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, ByteMatchTuples=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         ByteMatchTuples=ByteMatchTuples, **kwargs)
        (super(ByteMatchSet, self).__init__)(**processed_kwargs)


class IPSet(troposphere.waf.IPSet, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, IPSetDescriptors=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         IPSetDescriptors=IPSetDescriptors, **kwargs)
        (super(IPSet, self).__init__)(**processed_kwargs)


class Rule(troposphere.waf.Rule, Mixin):

    def __init__(self, title, template=None, validation=True, MetricName=REQUIRED, Name=REQUIRED, Predicates=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         MetricName=MetricName, 
         Name=Name, 
         Predicates=Predicates, **kwargs)
        (super(Rule, self).__init__)(**processed_kwargs)


class SqlInjectionMatchSet(troposphere.waf.SqlInjectionMatchSet, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, SqlInjectionMatchTuples=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         SqlInjectionMatchTuples=SqlInjectionMatchTuples, **kwargs)
        (super(SqlInjectionMatchSet, self).__init__)(**processed_kwargs)


class WebACL(troposphere.waf.WebACL, Mixin):

    def __init__(self, title, template=None, validation=True, DefaultAction=REQUIRED, MetricName=REQUIRED, Name=REQUIRED, Rules=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         DefaultAction=DefaultAction, 
         MetricName=MetricName, 
         Name=Name, 
         Rules=Rules, **kwargs)
        (super(WebACL, self).__init__)(**processed_kwargs)


class SizeConstraint(troposphere.waf.SizeConstraint, Mixin):

    def __init__(self, title=None, ComparisonOperator=REQUIRED, FieldToMatch=REQUIRED, Size=REQUIRED, TextTransformation=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ComparisonOperator=ComparisonOperator, 
         FieldToMatch=FieldToMatch, 
         Size=Size, 
         TextTransformation=TextTransformation, **kwargs)
        (super(SizeConstraint, self).__init__)(**processed_kwargs)


class SizeConstraintSet(troposphere.waf.SizeConstraintSet, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, SizeConstraints=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         SizeConstraints=SizeConstraints, **kwargs)
        (super(SizeConstraintSet, self).__init__)(**processed_kwargs)


class XssMatchTuple(troposphere.waf.XssMatchTuple, Mixin):

    def __init__(self, title=None, FieldToMatch=REQUIRED, TextTransformation=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         FieldToMatch=FieldToMatch, 
         TextTransformation=TextTransformation, **kwargs)
        (super(XssMatchTuple, self).__init__)(**processed_kwargs)


class XssMatchSet(troposphere.waf.XssMatchSet, Mixin):

    def __init__(self, title, template=None, validation=True, Name=REQUIRED, XssMatchTuples=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Name=Name, 
         XssMatchTuples=XssMatchTuples, **kwargs)
        (super(XssMatchSet, self).__init__)(**processed_kwargs)