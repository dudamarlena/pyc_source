# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/ec2/elb/policies.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 3856 bytes
from boto.resultset import ResultSet

class AppCookieStickinessPolicy(object):

    def __init__(self, connection=None):
        self.cookie_name = None
        self.policy_name = None

    def __repr__(self):
        return 'AppCookieStickiness(%s, %s)' % (self.policy_name,
         self.cookie_name)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'CookieName':
            self.cookie_name = value
        elif name == 'PolicyName':
            self.policy_name = value


class LBCookieStickinessPolicy(object):

    def __init__(self, connection=None):
        self.policy_name = None
        self.cookie_expiration_period = None

    def __repr__(self):
        return 'LBCookieStickiness(%s, %s)' % (self.policy_name,
         self.cookie_expiration_period)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'CookieExpirationPeriod':
            self.cookie_expiration_period = value
        elif name == 'PolicyName':
            self.policy_name = value


class OtherPolicy(object):

    def __init__(self, connection=None):
        self.policy_name = None

    def __repr__(self):
        return 'OtherPolicy(%s)' % self.policy_name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        self.policy_name = value


class Policies(object):
    __doc__ = '\n    ELB Policies\n    '

    def __init__(self, connection=None):
        self.connection = connection
        self.app_cookie_stickiness_policies = None
        self.lb_cookie_stickiness_policies = None
        self.other_policies = None

    def __repr__(self):
        app = 'AppCookieStickiness%s' % self.app_cookie_stickiness_policies
        lb = 'LBCookieStickiness%s' % self.lb_cookie_stickiness_policies
        other = 'Other%s' % self.other_policies
        return 'Policies(%s,%s,%s)' % (app, lb, other)

    def startElement(self, name, attrs, connection):
        if name == 'AppCookieStickinessPolicies':
            rs = ResultSet([('member', AppCookieStickinessPolicy)])
            self.app_cookie_stickiness_policies = rs
            return rs
        if name == 'LBCookieStickinessPolicies':
            rs = ResultSet([('member', LBCookieStickinessPolicy)])
            self.lb_cookie_stickiness_policies = rs
            return rs
        if name == 'OtherPolicies':
            rs = ResultSet([('member', OtherPolicy)])
            self.other_policies = rs
            return rs

    def endElement(self, name, value, connection):
        pass