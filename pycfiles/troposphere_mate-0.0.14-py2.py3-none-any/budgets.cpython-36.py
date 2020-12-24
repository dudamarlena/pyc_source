# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/budgets.py
# Compiled at: 2020-02-12 18:15:55
# Size of source mod 2**32: 6711 bytes
"""
This code is auto generated from troposphere_mate.code_generator.__init__.py scripts.
"""
import sys
if sys.version_info.major >= 3:
    if sys.version_info.minor >= 5:
        from typing import Union, List, Any
import troposphere.budgets
from troposphere.budgets import BudgetData as _BudgetData, CostTypes as _CostTypes, Notification as _Notification, NotificationWithSubscribers as _NotificationWithSubscribers, Spend as _Spend, Subscriber as _Subscriber, TimePeriod as _TimePeriod
from troposphere import Template, AWSHelperFn
from troposphere_mate.core.mate import preprocess_init_kwargs, Mixin
from troposphere_mate.core.sentiel import REQUIRED, NOTHING

class CostTypes(troposphere.budgets.CostTypes, Mixin):

    def __init__(self, title=None, IncludeCredit=NOTHING, IncludeDiscount=NOTHING, IncludeOtherSubscription=NOTHING, IncludeRecurring=NOTHING, IncludeRefund=NOTHING, IncludeSubscription=NOTHING, IncludeSupport=NOTHING, IncludeTax=NOTHING, IncludeUpfront=NOTHING, UseAmortized=NOTHING, UseBlended=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         IncludeCredit=IncludeCredit, 
         IncludeDiscount=IncludeDiscount, 
         IncludeOtherSubscription=IncludeOtherSubscription, 
         IncludeRecurring=IncludeRecurring, 
         IncludeRefund=IncludeRefund, 
         IncludeSubscription=IncludeSubscription, 
         IncludeSupport=IncludeSupport, 
         IncludeTax=IncludeTax, 
         IncludeUpfront=IncludeUpfront, 
         UseAmortized=UseAmortized, 
         UseBlended=UseBlended, **kwargs)
        (super(CostTypes, self).__init__)(**processed_kwargs)


class Spend(troposphere.budgets.Spend, Mixin):

    def __init__(self, title=None, Amount=REQUIRED, Unit=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Amount=Amount, 
         Unit=Unit, **kwargs)
        (super(Spend, self).__init__)(**processed_kwargs)


class TimePeriod(troposphere.budgets.TimePeriod, Mixin):

    def __init__(self, title=None, End=NOTHING, Start=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         End=End, 
         Start=Start, **kwargs)
        (super(TimePeriod, self).__init__)(**processed_kwargs)


class BudgetData(troposphere.budgets.BudgetData, Mixin):

    def __init__(self, title=None, BudgetType=REQUIRED, TimeUnit=REQUIRED, BudgetLimit=NOTHING, BudgetName=NOTHING, CostFilters=NOTHING, CostTypes=NOTHING, PlannedBudgetLimits=NOTHING, TimePeriod=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         BudgetType=BudgetType, 
         TimeUnit=TimeUnit, 
         BudgetLimit=BudgetLimit, 
         BudgetName=BudgetName, 
         CostFilters=CostFilters, 
         CostTypes=CostTypes, 
         PlannedBudgetLimits=PlannedBudgetLimits, 
         TimePeriod=TimePeriod, **kwargs)
        (super(BudgetData, self).__init__)(**processed_kwargs)


class Notification(troposphere.budgets.Notification, Mixin):

    def __init__(self, title=None, ComparisonOperator=REQUIRED, NotificationType=REQUIRED, Threshold=REQUIRED, ThresholdType=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         ComparisonOperator=ComparisonOperator, 
         NotificationType=NotificationType, 
         Threshold=Threshold, 
         ThresholdType=ThresholdType, **kwargs)
        (super(Notification, self).__init__)(**processed_kwargs)


class Subscriber(troposphere.budgets.Subscriber, Mixin):

    def __init__(self, title=None, Address=REQUIRED, SubscriptionType=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Address=Address, 
         SubscriptionType=SubscriptionType, **kwargs)
        (super(Subscriber, self).__init__)(**processed_kwargs)


class NotificationWithSubscribers(troposphere.budgets.NotificationWithSubscribers, Mixin):

    def __init__(self, title=None, Notification=REQUIRED, Subscribers=REQUIRED, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         Notification=Notification, 
         Subscribers=Subscribers, **kwargs)
        (super(NotificationWithSubscribers, self).__init__)(**processed_kwargs)


class Budget(troposphere.budgets.Budget, Mixin):

    def __init__(self, title, template=None, validation=True, Budget=REQUIRED, NotificationsWithSubscribers=NOTHING, **kwargs):
        processed_kwargs = preprocess_init_kwargs(title=title, 
         template=template, 
         validation=validation, 
         Budget=Budget, 
         NotificationsWithSubscribers=NotificationsWithSubscribers, **kwargs)
        (super(Budget, self).__init__)(**processed_kwargs)